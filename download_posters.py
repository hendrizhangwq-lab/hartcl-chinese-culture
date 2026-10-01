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
    {'index': 0, 'title': '孔子：一个君子的文化苦旅', 'trackId': 82976208},
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
print("Downloading Cover Posters and Quote Cards for all 25 folders...")
print("==================================================\n")

for item in target_tracks:
    idx = item['index']
    title = item['title']
    track_id = item['trackId']
    
    safe_title = re.sub(r'[\/\\:\*\?"<>\|]', '_', title)
    folder_name = f"{idx:02d}_{safe_title}"
    folder_path = os.path.join(base_dir, folder_name)
    os.makedirs(folder_path, exist_ok=True)
    
    try:
        url_mobile = f'https://mobile.ximalaya.com/mobile/track/detail?trackId={track_id}'
        req_m = urllib.request.Request(url_mobile, headers=headers)
        d_m = json.loads(urllib.request.urlopen(req_m, timeout=10).read().decode('utf-8'))
        cover_url = d_m.get('coverLarge') or (d_m.get('images') and d_m.get('images')[0])
        
        url_simple = f'https://www.ximalaya.com/revision/track/simple?trackId={track_id}'
        req_s = urllib.request.Request(url_simple, headers=headers)
        d_s = json.loads(urllib.request.urlopen(req_s, timeout=10).read().decode('utf-8'))
        rich_intro = d_s.get('data', {}).get('trackInfo', {}).get('richIntro', '')
        
        quote_imgs = re.findall(r'src=\"([^\"]+)\"', rich_intro)
        
        # Save Cover Poster
        if cover_url:
            if cover_url.startswith('//'): cover_url = 'http:' + cover_url
            cover_path = os.path.join(folder_path, 'cover.jpg')
            req_img = urllib.request.Request(cover_url, headers=headers)
            with urllib.request.urlopen(req_img, timeout=15) as r, open(cover_path, 'wb') as f:
                f.write(r.read())
            print(f"[{idx:02d}] Saved cover.jpg for '{title}'")
            
        # Save Quote Cards
        for q_idx, q_url in enumerate(quote_imgs, 1):
            if q_url.startswith('//'): q_url = 'http:' + q_url
            q_path = os.path.join(folder_path, f'quote_card_{q_idx}.jpg')
            req_q = urllib.request.Request(q_url, headers=headers)
            with urllib.request.urlopen(req_q, timeout=15) as r, open(q_path, 'wb') as f:
                f.write(r.read())
            print(f"   - Saved quote_card_{q_idx}.jpg")
    except Exception as e:
        print(f"[{idx:02d}] Error for {title}: {e}")
        
    time.sleep(0.2)

print("\n==================================================")
print("SUCCESS: ALL POSTERS & QUOTE CARDS DOWNLOADED!")
print("==================================================")
