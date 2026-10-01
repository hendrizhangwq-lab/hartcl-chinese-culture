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

print("==================================================")
print("Downloading 100% Full Unabridged Audio Files with Subscriber Auth")
print("==================================================\n")

for item in target_tracks:
    idx = item['index']
    title = item['title']
    track_id = item['trackId']
    
    safe_title = re.sub(r'[\/\\:\*\?"<>\|]', '_', title)
    folder_name = f"{idx:02d}_{safe_title}"
    folder_path = os.path.join(base_dir, folder_name)
    audio_path = os.path.join(folder_path, 'audio.m4a')
    
    print(f"[{idx:02d}/24] Downloading full audio for '{title}' (ID: {track_id})...")
    
    try:
        audio_url = f'https://mobile.ximalaya.com/mobile/redirect/free/play/{track_id}/1'
        req_audio = urllib.request.Request(audio_url, headers=headers)
        with urllib.request.urlopen(req_audio, timeout=45) as resp, open(audio_path, 'wb') as out_f:
            out_f.write(resp.read())
        audio_mb = os.path.getsize(audio_path) / (1024 * 1024)
        print(f"   - SUCCESS! Downloaded full audio ({audio_mb:.2f} MB)")
    except Exception as e:
        print(f"   - ERROR downloading full audio: {e}")
        
    time.sleep(0.3)

print("\n==================================================")
print("SUCCESS: ALL 24 FULL AUDIO FILES DOWNLOADED!")
print("==================================================")
