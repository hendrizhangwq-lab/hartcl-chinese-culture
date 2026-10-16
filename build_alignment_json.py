import os
import json
import re

def clean_str(s):
    return re.sub(r'[^\u4e00-\u9fff]', '', s)

def build_lesson_alignment(lesson_dir):
    whisper_file = os.path.join(lesson_dir, "whisper_segments.json")
    zh_file = os.path.join(lesson_dir, "transcript.md")
    en_file = os.path.join(lesson_dir, "english_transcript.md")
    
    with open(whisper_file, "r", encoding="utf-8") as f:
        whisper_segments = json.load(f)
        
    with open(zh_file, "r", encoding="utf-8") as f:
        zh_lines = [l.strip() for l in f.readlines() if l.strip()]
        
    with open(en_file, "r", encoding="utf-8") as f:
        en_lines = [l.strip() for l in f.readlines() if l.strip()]

    # Filter out title/track/hr lines
    # We keep headers (e.g., '无待、无己') or regular paragraphs
    items = []
    
    # Pre-build continuous whisper text
    whisper_chars = [] # list of (char, seg_index, seg_time)
    for seg_idx, seg in enumerate(whisper_segments):
        # Ignore intro audio before ~28s if seg text contains '秋语' or intro text
        cleaned_seg = clean_str(seg["text"])
        for ch in cleaned_seg:
            whisper_chars.append((ch, seg_idx, seg["start"], seg["end"]))
            
    # Function to find start & end times for a target Chinese text
    current_char_offset = 0
    # Skip intro segment in whisper if seg starts < 28s
    while current_char_offset < len(whisper_chars) and whisper_chars[current_char_offset][2] < 28.0:
        current_char_offset += 1

    aligned_paras = []
    timed_paras = []
    item_id = 1

    for line_idx in range(len(zh_lines)):
        zh_line = zh_lines[line_idx]
        en_line = en_lines[line_idx] if line_idx < len(en_lines) else ""

        if zh_line.startswith("# ") or zh_line.startswith("- **") or zh_line.startswith("---") or zh_line.startswith("URL:"):
            continue

        # Check if heading (subheading)
        is_heading = False
        clean_zh_heading = zh_line.replace("&nbsp;", "").strip()
        if clean_zh_heading in [
            "无待、无己", "道家的人格理想", "诸子散文的基础记忆和扩大记忆", "今译的重要性", "《逍遥游》今译", "无所依靠",
            "君子的反面群体：小人", "研究小人是为了更好地研究君子"
        ]:
            is_heading = True

        clean_p_zh = clean_str(zh_line)
        if not clean_p_zh and not is_heading:
            continue

        if is_heading:
            # Heading gets timestamp of current offset
            start_t = whisper_chars[current_char_offset][2] if current_char_offset < len(whisper_chars) else 0.0
            aligned_paras.append({
                "id": item_id,
                "isHeading": True,
                "start": round(start_t, 2),
                "end": round(start_t, 2),
                "zh": clean_zh_heading,
                "en": en_line
            })
            timed_paras.append({
                "id": item_id,
                "isHeading": True,
                "start": round(start_t, 2),
                "end": round(start_t, 2),
                "zh": clean_zh_heading,
                "en": en_line
            })
            item_id += 1
            continue

        # Find best start and end match in whisper_chars
        p_len = len(clean_p_zh)
        start_idx = current_char_offset
        end_idx = min(len(whisper_chars) - 1, current_char_offset + p_len)

        # Match prefix characters
        target_prefix = clean_p_zh[:10]
        for search_i in range(current_char_offset, min(len(whisper_chars) - 10, current_char_offset + 150)):
            window = ''.join([ch for ch, _, _, _ in whisper_chars[search_i:search_i+10]])
            if target_prefix and target_prefix[:5] in window:
                start_idx = search_i
                break

        # Match suffix characters
        target_suffix = clean_p_zh[-10:]
        search_start = max(start_idx, start_idx + p_len - 50)
        search_end = min(len(whisper_chars) - 10, start_idx + p_len + 150)
        end_idx = min(len(whisper_chars) - 1, start_idx + p_len)
        for search_i in range(search_start, search_end):
            window = ''.join([ch for ch, _, _, _ in whisper_chars[search_i:search_i+10]])
            if target_suffix and target_suffix[-5:] in window:
                end_idx = search_i + 10
                break

        start_time = whisper_chars[start_idx][2] if start_idx < len(whisper_chars) else 0.0
        end_time = whisper_chars[min(end_idx, len(whisper_chars)-1)][3] if end_idx < len(whisper_chars) else start_time + 5.0
        
        if end_time <= start_time:
            end_time = start_time + max(2.0, p_len * 0.15)

        current_char_offset = max(current_char_offset, end_idx)

        aligned_paras.append({
            "id": item_id,
            "isHeading": False,
            "start": round(start_time, 2),
            "end": round(end_time, 2),
            "zh": zh_line,
            "en": en_line
        })

        # Sentence-level alignment
        # Split Chinese into sentences
        zh_sents = [s for s in re.split(r'([。！？])', zh_line) if s]
        f_zh_sents = []
        for i in range(0, len(zh_sents), 2):
            s_text = zh_sents[i]
            if i + 1 < len(zh_sents):
                s_text += zh_sents[i+1]
            if s_text.strip():
                f_zh_sents.append(s_text.strip())
        if not f_zh_sents:
            f_zh_sents = [zh_line]

        # Split English into sentences
        en_sents = [s.strip() for s in re.split(r'(?<=[.!?])\s+', en_line) if s.strip()]
        if not en_sents:
            en_sents = [en_line]

        # Interpolate sentence timestamps across [start_time, end_time]
        total_dur = max(0.5, end_time - start_time)
        zh_sent_objs = []
        total_zh_chars = sum(len(clean_str(s)) for s in f_zh_sents) or 1
        curr_t = start_time
        for s in f_zh_sents:
            ratio = len(clean_str(s)) / total_zh_chars
            st_dur = total_dur * ratio
            next_t = min(end_time, curr_t + st_dur)
            zh_sent_objs.append({
                "text": s,
                "start": round(curr_t, 2),
                "end": round(next_t, 2)
            })
            curr_t = next_t

        en_sent_objs = []
        total_en_words = sum(len(s.split()) for s in en_sents) or 1
        curr_t = start_time
        for s in en_sents:
            ratio = len(s.split()) / total_en_words
            st_dur = total_dur * ratio
            next_t = min(end_time, curr_t + st_dur)
            en_sent_objs.append({
                "text": s,
                "start": round(curr_t, 2),
                "end": round(next_t, 2)
            })
            curr_t = next_t

        timed_paras.append({
            "id": item_id,
            "isHeading": False,
            "start": round(start_time, 2),
            "end": round(end_time, 2),
            "zh": zh_line,
            "en": en_line,
            "zhSentences": zh_sent_objs,
            "enSentences": en_sent_objs
        })

        item_id += 1

    out_aligned = os.path.join(lesson_dir, "aligned_paragraphs.json")
    out_timed = os.path.join(lesson_dir, "timed_transcript.json")

    with open(out_aligned, "w", encoding="utf-8") as f:
        json.dump(aligned_paras, f, ensure_ascii=False, indent=2)

    with open(out_timed, "w", encoding="utf-8") as f:
        json.dump(timed_paras, f, ensure_ascii=False, indent=2)

    print(f"Generated {len(aligned_paras)} aligned items for {os.path.basename(lesson_dir)}")
    print(f"First item: start={aligned_paras[0]['start']}, end={aligned_paras[0]['end']}")
    print(f"Last item: start={aligned_paras[-1]['start']}, end={aligned_paras[-1]['end']}")

build_lesson_alignment("./lessons/02-01_逍遥游：中国艺术的最高理想")
build_lesson_alignment("./lessons/02-02_《逍遥游》今译：中国文学和中国艺术的总体概括")
build_lesson_alignment("./lessons/03-01_君子的反面：研究小人是为了更好地认识君子")

