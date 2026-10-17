import os
import json
import re

lesson_dir = "lessons/03-02_如何应对小人？冷落、搁置并最终拯救他们"

with open(os.path.join(lesson_dir, "transcript.md"), "r", encoding="utf-8") as f:
    zh_lines = [l.strip() for l in f if l.strip() and not l.startswith("#") and not l.startswith("-") and not l.startswith("---")]

with open(os.path.join(lesson_dir, "english_transcript.md"), "r", encoding="utf-8") as f:
    en_lines = [l.strip() for l in f if l.strip() and not l.startswith("#") and not l.startswith("-") and not l.startswith("---")]

assert len(zh_lines) == len(en_lines) == 20, f"Mismatch: {len(zh_lines)} ZH vs {len(en_lines)} EN"

# 20 calibrated time blocks based on Whisper ground truth
block_times = [
  (31.0, 77.0, False),     # 1: P1
  (80.0, 80.0, True),      # 2: Heading 1
  (80.0, 135.0, False),    # 3: P2
  (135.0, 162.0, False),   # 4: P3
  (162.0, 245.0, False),   # 5: P4
  (245.0, 265.0, False),   # 6: P5
  (265.0, 330.0, False),   # 7: P6
  (330.0, 368.0, False),   # 8: P7
  (368.0, 368.0, True),    # 9: Heading 2
  (368.0, 417.0, False),   # 10: P8
  (417.0, 478.0, False),   # 11: P9
  (478.0, 545.0, False),   # 12: P10
  (545.0, 580.0, False),   # 13: P11
  (580.0, 580.0, True),    # 14: Heading 3
  (580.0, 620.0, False),   # 15: P12
  (620.0, 686.0, False),   # 16: P13
  (686.0, 737.0, False),   # 17: P14
  (737.0, 794.0, False),   # 18: P15
  (794.0, 843.0, False),   # 19: P16
  (843.0, 911.0, False)    # 20: P17
]

def split_zh(text):
    parts = re.split(r"([。！？])", text)
    sents = []
    for i in range(0, len(parts)-1, 2):
        s = parts[i].strip() + parts[i+1].strip()
        if s: sents.append(s)
    if len(parts) % 2 == 1 and parts[-1].strip():
        sents.append(parts[-1].strip())
    return sents

def split_en(text):
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [p.strip() for p in parts if p.strip()]

aligned = []
timed = []

for idx in range(20):
    start, end, is_heading = block_times[idx]
    zh_text = zh_lines[idx]
    en_text = en_lines[idx]
    
    aligned_item = {
        "id": idx + 1,
        "isHeading": is_heading,
        "start": start,
        "end": end,
        "zh": zh_text,
        "en": en_text
    }
    aligned.append(aligned_item)
    
    if is_heading:
        timed_item = {
            "id": idx + 1,
            "isHeading": True,
            "start": start,
            "end": end,
            "zh": zh_text,
            "en": en_text,
            "zhSentences": [{"text": zh_text, "start": start, "end": end}],
            "enSentences": [{"text": en_text, "start": start, "end": end}]
        }
    else:
        zh_sents = split_zh(zh_text)
        en_sents = split_en(en_text)
        
        duration = end - start
        
        total_zh_len = sum(len(s) for s in zh_sents)
        zh_timed = []
        cur_t = start
        for i, s in enumerate(zh_sents):
            s_dur = (len(s) / total_zh_len) * duration
            s_end = round(cur_t + s_dur, 1) if i < len(zh_sents) - 1 else end
            zh_timed.append({"text": s, "start": round(cur_t, 1), "end": s_end})
            cur_t = s_end
            
        total_en_len = sum(len(s) for s in en_sents)
        en_timed = []
        cur_t = start
        for i, s in enumerate(en_sents):
            s_dur = (len(s) / total_en_len) * duration
            s_end = round(cur_t + s_dur, 1) if i < len(en_sents) - 1 else end
            en_timed.append({"text": s, "start": round(cur_t, 1), "end": s_end})
            cur_t = s_end
            
        timed_item = {
            "id": idx + 1,
            "isHeading": False,
            "start": start,
            "end": end,
            "zh": zh_text,
            "en": en_text,
            "zhSentences": zh_timed,
            "enSentences": en_timed
        }
    timed.append(timed_item)

out_aligned = os.path.join(lesson_dir, "aligned_paragraphs.json")
out_timed = os.path.join(lesson_dir, "timed_transcript.json")

with open(out_aligned, "w", encoding="utf-8") as f:
    json.dump(aligned, f, ensure_ascii=False, indent=2)

with open(out_timed, "w", encoding="utf-8") as f:
    json.dump(timed, f, ensure_ascii=False, indent=2)

print(f"Successfully calibrated 03-02 alignment ({len(aligned)} blocks)!")
