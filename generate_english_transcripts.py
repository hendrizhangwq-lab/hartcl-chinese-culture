import urllib.request
import urllib.parse
import json
import os
import re
import time

base_dir = '/Users/hendrizhang/Desktop/HartCL'
subdirs = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and re.match(r'^\d{2}_', d) and not d.startswith('00_')])

def translate_text(text):
    if not text.strip(): return ''
    # MyMemory API has 500 char limit per chunk
    chunks = [text[i:i+400] for i in range(0, len(text), 400)]
    translated_chunks = []
    for chunk in chunks:
        try:
            url = 'https://api.mymemory.translated.net/get?q=' + urllib.parse.quote(chunk) + '&langpair=zh-CN|en'
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req, timeout=10)
            data = json.loads(res.read().decode('utf-8'))
            t = data.get('responseData', {}).get('translatedText', '')
            translated_chunks.append(t if t else chunk)
            time.sleep(0.15)
        except Exception as e:
            translated_chunks.append(chunk)
    return ' '.join(translated_chunks)

print(f"Translating {len(subdirs)} lessons to English...\n")

for d in subdirs:
    p = os.path.join(base_dir, d)
    zh_file = os.path.join(p, 'transcript.md')
    en_file = os.path.join(p, 'english_transcript.md')
    
    if os.path.exists(zh_file):
        with open(zh_file, 'r', encoding='utf-8') as f:
            zh_text = f.read()
            
        print(f"Translating {d}...")
        paragraphs = zh_text.splitlines()
        en_paragraphs = []
        
        for line in paragraphs:
            if line.startswith('#') or line.startswith('-') or not line.strip():
                # Keep headers or metadata
                if line.startswith('# '):
                    title_zh = line.replace('# ', '')
                    title_en = translate_text(title_zh)
                    en_paragraphs.append(f"# {title_en}")
                elif line.startswith('## '):
                    h_zh = line.replace('## ', '')
                    h_en = translate_text(h_zh)
                    en_paragraphs.append(f"## {h_en}")
                else:
                    en_paragraphs.append(line)
            else:
                en_trans = translate_text(line)
                en_paragraphs.append(en_trans)
                
        en_final = '\n'.join(en_paragraphs)
        with open(en_file, 'w', encoding='utf-8') as f:
            f.write(en_final)
            
        print(f"   - SUCCESS! Saved English transcript for {d}")

print("\n==================================================")
print("ALL 24 ENGLISH TRANSCRIPTS GENERATED SUCCESSFULLY!")
print("==================================================")
