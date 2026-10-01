import os
import re

base_dir = '/Users/hendrizhang/Desktop/HartCL'
subdirs = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and re.match(r'^\d{2}_', d)])

def clean_transcript_header(text):
    if not text: return ''
    lines = text.splitlines()
    
    # Preserve metadata lines starting with '#' or '-' if present at top
    header_meta = []
    content_lines = []
    
    for l in lines:
        if l.startswith('# ') or l.startswith('- **') or l.startswith('---'):
            header_meta.append(l)
        else:
            content_lines.append(l)
            
    # Find index of '今日文稿' or '课程金句'
    start_idx = 0
    for i, line in enumerate(content_lines):
        clean_line = re.sub(r'&nbsp;|\s+', '', line).strip()
        if '今日文稿' in clean_line:
            start_idx = i + 1
            break
        elif '课程金句' in clean_line and start_idx == 0:
            start_idx = i + 1

    remaining_lines = content_lines[start_idx:]
    
    final_body = []
    skipping_headers = True
    for line in remaining_lines:
        clean_l = re.sub(r'&nbsp;|\s+', '', line).strip()
        if not clean_l:
            continue
        if skipping_headers:
            if '点击保存图片' in clean_l or '课程金句' in clean_l or '今日文稿' in clean_l or '本周优质评论' in clean_l or '一周优秀学员' in clean_l or '微信' in clean_l or '签名书' in clean_l:
                continue
            if re.match(r'^第\d+集', clean_l):
                continue
            skipping_headers = False
        final_body.append(line)
        
    full_output = header_meta + ['\n## 📜 课程文稿\n'] + final_body
    return '\n'.join(full_output)

def clean_english_header(text):
    if not text: return ''
    lines = text.splitlines()
    
    header_meta = []
    content_lines = []
    
    for l in lines:
        if l.startswith('# ') or l.startswith('- **') or l.startswith('---'):
            header_meta.append(l)
        else:
            content_lines.append(l)
            
    final_body = []
    skipping_headers = True
    for line in content_lines:
        clean_l = line.strip()
        if not clean_l:
            continue
        if skipping_headers:
            if 'Course Quote' in clean_l or 'Today Transcript' in clean_l or 'Save picture' in clean_l or 'Episode' in clean_l or 'Comment' in clean_l or 'WeChat' in clean_l:
                continue
            skipping_headers = False
        final_body.append(line)
        
    full_output = header_meta + ['\n## 📜 Transcript\n'] + final_body
    return '\n'.join(final_output)

print("Cleaning transcript headers for all 24 lessons...\n")

for d in subdirs:
    p = os.path.join(base_dir, d)
    zh_file = os.path.join(p, 'transcript.md')
    en_file = os.path.join(p, 'english_transcript.md')
    
    if os.path.exists(zh_file):
        with open(zh_file, 'r', encoding='utf-8') as f:
            zh_text = f.read()
        clean_zh = clean_transcript_header(zh_text)
        with open(zh_file, 'w', encoding='utf-8') as f:
            f.write(clean_zh)
        print(f"[{d}] Cleaned transcript.md")
        
    if os.path.exists(en_file):
        with open(en_file, 'r', encoding='utf-8') as f:
            en_text = f.read()
        clean_en = clean_english_header(en_text)
        with open(en_file, 'w', encoding='utf-8') as f:
            f.write(clean_en)
        print(f"[{d}] Cleaned english_transcript.md")

print("\nAll transcript headers cleaned!")
