import os
import json
import re

def clean_text(text):
    # Remove punctuation, spaces, etc.
    return re.sub(r'[^\w\u4e00-\u9fff]', '', text)

def align_lesson(lesson_dir):
    whisper_file = os.path.join(lesson_dir, "whisper_segments.json")
    zh_file = os.path.join(lesson_dir, "transcript.md")
    en_file = os.path.join(lesson_dir, "english_transcript.md")
    
    with open(whisper_file, "r", encoding="utf-8") as f:
        whisper_segments = json.load(f)
        
    with open(zh_file, "r", encoding="utf-8") as f:
        zh_lines = [l.strip() for l in f.readlines() if l.strip()]
        
    with open(en_file, "r", encoding="utf-8") as f:
        en_lines = [l.strip() for l in f.readlines() if l.strip()]
        
    print(f"--- Aligning {os.path.basename(lesson_dir)} ---")
    print(f"Whisper segments: {len(whisper_segments)}, ZH lines: {len(zh_lines)}, EN lines: {len(en_lines)}")

align_lesson("./lessons/02-01_逍遥游：中国艺术的最高理想")
align_lesson("./lessons/02-02_《逍遥游》今译：中国文学和中国艺术的总体概括")
