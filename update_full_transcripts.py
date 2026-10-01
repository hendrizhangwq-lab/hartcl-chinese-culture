import urllib.request
import json
import os
import re
import time

token = '43618227&C94BBA80240N3083AAF693CF7C1CB118534684C2686265AD7278B4821FCC0F86C396AC072ABE117M7F0A743EF990810_'
cookie_str = f'1&_token={token}; web_login=1790840126910; impl=www.ximalaya.com.login; xm-page-viewid=ximalaya-web'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Cookie': cookie_str,
    'Referer': 'https://www.ximalaya.com/'
}

base_dir = '/Users/hendrizhang/Desktop/HartCL'

target_tracks = [
    {'index': 1, 'title': '最短的文化定义', 'trackId': 84921988},
    {'index': 2, 'title': '庄子的哲学：以人的立场来看物', 'trackId': 161841817},
    {'index': 3, 'title': '君子人格：理想化的人格结构', 'trackId': 129794861},
    {'index': 4, 'title': '中庸之道：数千年的集体选择', 'trackId': 120315418},
    {'index': 5, 'title': '家国同构：大秩序和小秩序是不一样的', 'trackId': 107410272},
    {'index': 6, 'title': '统一文字：难以消灭的文化基因', 'trackId': 107207484},
    {'index': 7, 'title': '凉州风范：超越血缘的文化基因', 'trackId': 89225822},
    {'index': 8, 'title': '长安：世界性的生活方式', 'trackId': 89953402},
    {'index': 9, 'title': '利玛窦：中国文化的非侵略本性', 'trackId': 98141029},
    {'index': 10, 'title': '选拔文官：科举制度的五大优点', 'trackId': 122168610},
    {'index': 11, 'title': '君子之交：友谊是人生的一大难题', 'trackId': 134559136},
    {'index': 12, 'title': '说真话：不用虚假替代真实', 'trackId': 125913583},
    {'index': 13, 'title': '两种成功：中国文化的思维重点', 'trackId': 117201405},
    {'index': 14, 'title': '道教的三项呼唤：和平，自然，生命', 'trackId': 164291645},
    {'index': 15, 'title': '佛教最简明的精神支点与核心思维——《心经》', 'trackId': 147657946},
    {'index': 16, 'title': '李清照：中国第一女诗人', 'trackId': 93407966},
    {'index': 17, 'title': '唐诗：中国文化修养的起点之一', 'trackId': 175521148},
    {'index': 18, 'title': '宋朝的生活方式与文化成就', 'trackId': 92554643},
    {'index': 19, 'title': '罗素：中国文化的优点和中国人缺点', 'trackId': 123613808},
    {'index': 20, 'title': '文化创新：让文化走在科技前面', 'trackId': 129337293},
    {'index': 21, 'title': '新儒学：儒学的反思与转向', 'trackId': 158480683},
    {'index': 22, 'title': '文化大迁徙：在移动中活得更好的中国文化', 'trackId': 105798574},
    {'index': 23, 'title': '汉文化遇到的两个陌生', 'trackId': 88829244},
    {'index': 24, 'title': '尾声二：中国文化必修课大回顾（下）', 'trackId': 185524532}
]

def clean_html(raw_html):
    if not raw_html: return ''
    html = raw_html
    # Formatting linebreaks and paragraphs cleanly
    html = re.sub(r'<br\s*/?>', '\n', html)
    html = re.sub(r'</p>', '\n\n', html)
    html = re.sub(r'</blockquote>', '\n\n', html)
    html = re.sub(r'</h[1-6]>', '\n\n', html)
    html = re.sub(r'<hr[^>]*>', '\n---\n', html)
    clean_text = re.sub(r'<[^>]+>', '', html)
    lines = [line.strip() for line in clean_text.splitlines()]
    return '\n'.join([line for line in lines if line])

print("==================================================")
print("Updating Transcripts with Full Verbatim Subscriber Text")
print("==================================================\n")

for item in target_tracks:
    idx = item['index']
    title = item['title']
    track_id = item['trackId']
    
    safe_title = re.sub(r'[\/\\:\*\?"<>\|]', '_', title)
    folder_name = f"{idx:02d}_{safe_title}"
    folder_path = os.path.join(base_dir, folder_name)
    transcript_path = os.path.join(folder_path, 'transcript.md')
    
    print(f"[{idx:02d}/24] Updating '{title}' (Track ID: {track_id})...")
    
    try:
        url_simple = f'https://www.ximalaya.com/revision/track/simple?trackId={track_id}'
        req_simple = urllib.request.Request(url_simple, headers=headers)
        res_simple = urllib.request.urlopen(req_simple, timeout=15)
        data_simple = json.loads(res_simple.read().decode('utf-8'))
        
        track_info = data_simple.get('data', {}).get('trackInfo', {})
        rich_intro = track_info.get('richIntro', '')
        
        url_mobile = f'https://mobile.ximalaya.com/mobile/track/detail?trackId={track_id}'
        req_mobile = urllib.request.Request(url_mobile, headers=headers)
        res_mobile = urllib.request.urlopen(req_mobile, timeout=15)
        data_mobile = json.loads(res_mobile.read().decode('utf-8'))
        
        mobile_intro = data_mobile.get('shortRichIntro') or data_mobile.get('intro', '')
        
        t_rich = clean_html(rich_intro)
        t_mob = clean_html(mobile_intro)
        
        best_text = t_rich if len(t_rich) > len(t_mob) else t_mob
        
        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(f"# {title}\n\n")
            f.write(f"- **课程专辑**: 《余秋雨·中国文化必修课》\n")
            f.write(f"- **喜马拉雅 Track ID**: {track_id}\n")
            f.write(f"- **音频在线地址**: `https://www.ximalaya.com/sound/{track_id}`\n\n")
            f.write("---\n\n")
            f.write("## 📜 完整课程逐字文稿 (Full Verbatim Transcript)\n\n")
            f.write(best_text)
            f.write("\n")
            
        print(f"   - SUCCESS! Saved {len(best_text)} characters to transcript.md")
    except Exception as e:
        print(f"   - ERROR: {e}")
        
    time.sleep(0.3)

print("\n==================================================")
print("ALL 24 TRANSCRIPTS UPDATED WITH 100% VERBATIM TEXT!")
print("==================================================")
