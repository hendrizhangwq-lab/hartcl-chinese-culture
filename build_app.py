import os
import json
import re

base_dir = '/Users/hendrizhang/Desktop/HartCL'
subdirs = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and re.match(r'^\d{2}_', d)])

lessons = []

for d in subdirs:
    p = os.path.join(base_dir, d)
    files = os.listdir(p)
    
    audio_file = [f for f in files if f.endswith('.m4a')][0] if any(f.endswith('.m4a') for f in files) else None
    transcript_file = [f for f in files if f.endswith('.md')][0] if any(f.endswith('.md') for f in files) else None
    cover_file = 'cover.jpg' if 'cover.jpg' in files else None
    quote_cards = sorted([f for f in files if f.startswith('quote_card_') and f.endswith('.jpg')])
    
    title = d.split('_', 1)[1] if '_' in d else d
    index_num = d.split('_', 1)[0]
    
    transcript_text = ""
    if transcript_file:
        with open(os.path.join(p, transcript_file), 'r', encoding='utf-8') as f:
            transcript_text = f.read()
            
    # Clean header out of transcript for reading view
    clean_body = re.sub(r'^#\s+.*\n+', '', transcript_text)
    clean_body = re.sub(r'^- \*\*.*\n+', '', clean_body, flags=re.MULTILINE)
    clean_body = re.sub(r'^---\n+', '', clean_body, flags=re.MULTILINE)
    clean_body = re.sub(r'^##\s+📜.*\n+', '', clean_body, flags=re.MULTILINE)
    clean_body = clean_body.strip()
    
    lessons.append({
        'id': index_num,
        'folder': d,
        'title': title,
        'audioRelPath': f'./{d}/{audio_file}' if audio_file else '',
        'coverRelPath': f'./{d}/{cover_file}' if cover_file else '',
        'quoteCards': [f'./{d}/{q}' for q in quote_cards],
        'transcript': clean_body
    })

print(f"Loaded {len(lessons)} lessons for web app.")

lessons_json = json.dumps(lessons, ensure_ascii=False)

template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>余秋雨·中国文化必修课 - Mr. Cliffort Hart 课程学习平台</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Serif+SC:wght@400;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/pinyin-pro@3.18.3/dist/index.js"></script>
    <style>
        :root {
            --bg-body: #0f172a;
            --bg-sidebar: #1e293b;
            --bg-card: #1e293b;
            --bg-card-hover: #334155;
            --accent-color: #f59e0b;
            --accent-hover: #d97706;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --border-color: #334155;
            --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
            --font-serif: 'Noto Serif SC', 'STKaiti', 'KaiTi', serif;
            --reader-font-size: 18px;
        }

        .light-mode {
            --bg-body: #f8fafc;
            --bg-sidebar: #ffffff;
            --bg-card: #ffffff;
            --bg-card-hover: #f1f5f9;
            --accent-color: #d97706;
            --accent-hover: #b45309;
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --text-muted: #94a3b8;
            --border-color: #e2e8f0;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: var(--font-sans);
            background-color: var(--bg-body);
            color: var(--text-primary);
            height: 100vh;
            display: flex;
            overflow: hidden;
        }

        .sidebar {
            width: 380px;
            background-color: var(--bg-sidebar);
            border-right: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            flex-shrink: 0;
            transition: all 0.3s ease;
        }

        .sidebar-header {
            padding: 24px 20px 16px 20px;
            border-bottom: 1px solid var(--border-color);
        }

        .sidebar-title {
            font-size: 20px;
            font-weight: 700;
            color: var(--accent-color);
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 6px;
        }

        .sidebar-subtitle {
            font-size: 13px;
            color: var(--text-secondary);
        }

        .search-box {
            margin-top: 14px;
            position: relative;
        }

        .search-input {
            width: 100%;
            padding: 10px 14px 10px 36px;
            background-color: var(--bg-body);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            color: var(--text-primary);
            font-size: 14px;
            outline: none;
            transition: border-color 0.2s;
        }

        .search-input:focus {
            border-color: var(--accent-color);
        }

        .search-icon {
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 14px;
        }

        .lesson-list {
            flex: 1;
            overflow-y: auto;
            padding: 12px 10px;
        }

        .lesson-item {
            padding: 14px 16px;
            border-radius: 10px;
            margin-bottom: 6px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 14px;
            border: 1px solid transparent;
        }

        .lesson-item:hover {
            background-color: var(--bg-card-hover);
        }

        .lesson-item.active {
            background-color: rgba(245, 158, 11, 0.12);
            border-color: var(--accent-color);
        }

        .lesson-badge {
            width: 36px;
            height: 36px;
            border-radius: 8px;
            background-color: var(--bg-body);
            color: var(--accent-color);
            font-weight: 700;
            font-size: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
            border: 1px solid var(--border-color);
        }

        .lesson-item.active .lesson-badge {
            background-color: var(--accent-color);
            color: #ffffff;
            border-color: var(--accent-color);
        }

        .lesson-info {
            flex: 1;
            min-width: 0;
        }

        .lesson-item-title {
            font-size: 15px;
            font-weight: 600;
            color: var(--text-primary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .lesson-item-sub {
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 4px;
        }

        .main-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            background-color: var(--bg-body);
        }

        .toolbar {
            height: 64px;
            border-bottom: 1px solid var(--border-color);
            padding: 0 28px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            background-color: var(--bg-sidebar);
            flex-shrink: 0;
        }

        .current-lesson-title {
            font-size: 18px;
            font-weight: 700;
            color: var(--text-primary);
        }

        .toolbar-actions {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .btn {
            padding: 8px 14px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            background-color: var(--bg-body);
            color: var(--text-primary);
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }

        .btn:hover {
            border-color: var(--accent-color);
            color: var(--accent-color);
        }

        .btn.active {
            background-color: var(--accent-color);
            color: #ffffff;
            border-color: var(--accent-color);
        }

        .content-body {
            flex: 1;
            overflow-y: auto;
            padding: 32px 48px 160px 48px;
            max-width: 1000px;
            margin: 0 auto;
            width: 100%;
        }

        .player-bar {
            position: fixed;
            bottom: 0;
            right: 0;
            left: 380px;
            height: 90px;
            background-color: rgba(30, 41, 59, 0.95);
            backdrop-filter: blur(12px);
            border-top: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            padding: 0 32px;
            gap: 24px;
            z-index: 100;
        }

        .player-cover {
            width: 56px;
            height: 56px;
            border-radius: 8px;
            object-fit: cover;
            border: 1px solid var(--border-color);
        }

        .player-info {
            width: 200px;
            flex-shrink: 0;
        }

        .player-title {
            font-size: 14px;
            font-weight: 600;
            color: var(--text-primary);
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .player-artist {
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 2px;
        }

        .player-controls-center {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 8px;
        }

        .playback-buttons {
            display: flex;
            align-items: center;
            gap: 16px;
        }

        .play-btn {
            width: 44px;
            height: 44px;
            border-radius: 50%;
            background-color: var(--accent-color);
            color: #ffffff;
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            cursor: pointer;
            transition: transform 0.2s;
        }

        .play-btn:hover {
            transform: scale(1.08);
            background-color: var(--accent-hover);
        }

        .skip-btn {
            background: none;
            border: none;
            color: var(--text-secondary);
            font-size: 16px;
            cursor: pointer;
            transition: color 0.2s;
        }

        .skip-btn:hover {
            color: var(--text-primary);
        }

        .progress-wrapper {
            width: 100%;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .time-text {
            font-size: 12px;
            color: var(--text-secondary);
            width: 40px;
        }

        .progress-bar {
            flex: 1;
            height: 6px;
            background-color: var(--bg-body);
            border-radius: 3px;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }

        .progress-fill {
            height: 100%;
            background-color: var(--accent-color);
            width: 0%;
            border-radius: 3px;
        }

        .speed-selector {
            background-color: var(--bg-body);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 13px;
            cursor: pointer;
        }

        .poster-gallery {
            display: flex;
            gap: 16px;
            margin-bottom: 32px;
            overflow-x: auto;
            padding-bottom: 8px;
        }

        .poster-img {
            height: 260px;
            border-radius: 12px;
            border: 1px solid var(--border-color);
            object-fit: cover;
            transition: transform 0.3s;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }

        .poster-img:hover {
            transform: scale(1.02);
        }

        .reader-content {
            font-family: var(--font-serif);
            font-size: var(--reader-font-size);
            line-height: 2.1;
            color: var(--text-primary);
        }

        .reader-content p {
            margin-bottom: 24px;
            text-indent: 2em;
        }

        .reader-content h2 {
            font-family: var(--font-sans);
            font-size: 24px;
            margin: 36px 0 18px 0;
            color: var(--accent-color);
            border-left: 4px solid var(--accent-color);
            padding-left: 12px;
        }

        .reader-content blockquote {
            background-color: var(--bg-card);
            border-left: 4px solid var(--accent-color);
            padding: 16px 20px;
            border-radius: 0 8px 8px 0;
            margin: 24px 0;
            font-style: italic;
            color: var(--text-secondary);
        }

        ruby {
            ruby-position: over;
        }

        rt {
            font-family: var(--font-sans);
            font-size: 0.6em;
            color: var(--accent-color);
            font-weight: 500;
        }

        @media (max-width: 900px) {
            .sidebar { width: 280px; }
            .player-bar { left: 280px; padding: 0 16px; }
            .content-body { padding: 24px 20px 14px 20px; }
        }
    </style>
</head>
<body>

    <div class="sidebar">
        <div class="sidebar-header">
            <div class="sidebar-title">
                <span>🏮</span> 中国文化必修课
            </div>
            <div class="sidebar-subtitle">主讲：余秋雨先生 | Clifford Hart 专用</div>
            <div class="search-box">
                <span class="search-icon">🔍</span>
                <input type="text" id="searchInput" class="search-input" placeholder="搜索课程主题或关键词..." oninput="filterLessons()">
            </div>
        </div>
        <div class="lesson-list" id="lessonList"></div>
    </div>

    <div class="main-container">
        <div class="toolbar">
            <div class="current-lesson-title" id="currentTitle">加载中...</div>
            <div class="toolbar-actions">
                <button class="btn" id="pinyinBtn" onclick="togglePinyin()">🔤 拼音标注</button>
                <button class="btn" onclick="changeFontSize(1)">A+</button>
                <button class="btn" onclick="changeFontSize(-1)">A-</button>
                <button class="btn" onclick="toggleDarkMode()">🌓 视角模式</button>
            </div>
        </div>

        <div class="content-body">
            <div class="poster-gallery" id="posterGallery"></div>
            <div class="reader-content" id="readerContent"></div>
        </div>
    </div>

    <div class="player-bar">
        <img id="playerCover" class="player-cover" src="" alt="Cover">
        <div class="player-info">
            <div class="player-title" id="playerTitle">-</div>
            <div class="player-artist">余秋雨 · 中国文化必修课</div>
        </div>

        <div class="player-controls-center">
            <div class="playback-buttons">
                <button class="skip-btn" onclick="skipAudio(-10)">↺ 10s</button>
                <button class="play-btn" id="playBtn" onclick="togglePlay()">▶</button>
                <button class="skip-btn" onclick="skipAudio(10)">↻ 10s</button>
            </div>
            <div class="progress-wrapper">
                <span class="time-text" id="currentTime">00:00</span>
                <div class="progress-bar" onclick="seekAudio(event)" id="progressBar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <span class="time-text" id="durationTime">00:00</span>
            </div>
        </div>

        <div>
            <select class="speed-selector" id="speedSelect" onchange="changeSpeed()">
                <option value="0.75">0.75x 慢速</option>
                <option value="1.0" selected>1.0x 标准</option>
                <option value="1.25">1.25x 快速</option>
                <option value="1.5">1.5x 倍速</option>
            </select>
        </div>
    </div>

    <audio id="audioPlayer"></audio>

    <script>
        const lessons = __LESSONS_JSON__;
        let currentLessonIndex = 0;
        let isPlaying = false;
        let isPinyinActive = false;
        let fontSize = 18;

        const audioPlayer = document.getElementById('audioPlayer');
        const playBtn = document.getElementById('playBtn');
        const progressFill = document.getElementById('progressFill');
        const currentTimeEl = document.getElementById('currentTime');
        const durationTimeEl = document.getElementById('durationTime');

        function initApp() {
            renderLessonList(lessons);
            loadLesson(0);
            
            audioPlayer.addEventListener('timeupdate', updateProgress);
            audioPlayer.addEventListener('ended', () => {
                isPlaying = false;
                playBtn.textContent = '▶';
            });
        }

        function renderLessonList(list) {
            const listEl = document.getElementById('lessonList');
            listEl.innerHTML = '';
            list.forEach((lesson, index) => {
                const item = document.createElement('div');
                item.className = `lesson-item ${index === currentLessonIndex ? 'active' : ''}`;
                item.onclick = () => loadLesson(index);
                item.innerHTML = `
                    <div class="lesson-badge">${lesson.id}</div>
                    <div class="lesson-info">
                        <div class="lesson-item-title">${lesson.title}</div>
                        <div class="lesson-item-sub">余秋雨先生讲授</div>
                    </div>
                `;
                listEl.appendChild(item);
            });
        }

        function loadLesson(index) {
            currentLessonIndex = index;
            const lesson = lessons[index];

            document.getElementById('currentTitle').textContent = `${lesson.id}. ${lesson.title}`;
            document.getElementById('playerTitle').textContent = lesson.title;
            if (lesson.coverRelPath) {
                document.getElementById('playerCover').src = lesson.coverRelPath;
            }

            const galleryEl = document.getElementById('posterGallery');
            galleryEl.innerHTML = '';
            if (lesson.coverRelPath) {
                galleryEl.innerHTML += `<img class="poster-img" src="${lesson.coverRelPath}" alt="Cover">`;
            }
            lesson.quoteCards.forEach(card => {
                galleryEl.innerHTML += `<img class="poster-img" src="${card}" alt="Quote Card">`;
            });

            renderTranscript(lesson.transcript);

            audioPlayer.src = lesson.audioRelPath;
            isPlaying = false;
            playBtn.textContent = '▶';

            renderLessonList(lessons);
        }

        function renderTranscript(text) {
            const readerEl = document.getElementById('readerContent');
            const paragraphs = text.split('\\n').filter(p => p.trim() !== '');
            let html = '';

            paragraphs.forEach(p => {
                if (p.startsWith('## ')) {
                    html += `<h2>${p.replace('## ', '')}</h2>`;
                } else if (p.startsWith('> ')) {
                    html += `<blockquote>${p.replace('> ', '')}</blockquote>`;
                } else {
                    html += `<p>${p}</p>`;
                }
            });

            readerEl.innerHTML = html;

            if (isPinyinActive) {
                applyPinyin();
            }
        }

        function togglePinyin() {
            isPinyinActive = !isPinyinActive;
            const btn = document.getElementById('pinyinBtn');
            if (isPinyinActive) {
                btn.classList.add('active');
                applyPinyin();
            } else {
                btn.classList.remove('active');
                renderTranscript(lessons[currentLessonIndex].transcript);
            }
        }

        function applyPinyin() {
            if (window.pinyinPro) {
                const readerEl = document.getElementById('readerContent');
                const ps = readerEl.querySelectorAll('p');
                ps.forEach(p => {
                    const text = p.innerText;
                    const py = pinyinPro.html(text);
                    p.innerHTML = py;
                });
            }
        }

        function togglePlay() {
            if (!audioPlayer.src) return;
            if (isPlaying) {
                audioPlayer.pause();
                playBtn.textContent = '▶';
            } else {
                audioPlayer.play();
                playBtn.textContent = '⏸';
            }
            isPlaying = !isPlaying;
        }

        function skipAudio(seconds) {
            audioPlayer.currentTime = Math.max(0, Math.min(audioPlayer.duration, audioPlayer.currentTime + seconds));
        }

        function updateProgress() {
            if (isNaN(audioPlayer.duration)) return;
            const pct = (audioPlayer.currentTime / audioPlayer.duration) * 100;
            progressFill.style.width = pct + '%';

            currentTimeEl.textContent = formatTime(audioPlayer.currentTime);
            durationTimeEl.textContent = formatTime(audioPlayer.duration);
        }

        function seekAudio(e) {
            const bar = document.getElementById('progressBar');
            const rect = bar.getBoundingClientRect();
            const clickX = e.clientX - rect.left;
            const pct = clickX / rect.width;
            audioPlayer.currentTime = pct * audioPlayer.duration;
        }

        function changeSpeed() {
            const spd = parseFloat(document.getElementById('speedSelect').value);
            audioPlayer.playbackRate = spd;
        }

        function changeFontSize(delta) {
            fontSize = Math.max(14, Math.min(28, fontSize + delta));
            document.documentElement.style.setProperty('--reader-font-size', fontSize + 'px');
        }

        function toggleDarkMode() {
            document.body.classList.toggle('light-mode');
        }

        function filterLessons() {
            const q = document.getElementById('searchInput').value.toLowerCase();
            const filtered = lessons.filter(l => l.title.toLowerCase().includes(q) || l.transcript.toLowerCase().includes(q));
            renderLessonList(filtered);
        }

        function formatTime(s) {
            const mins = Math.floor(s / 60);
            const secs = Math.floor(s % 60);
            return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
        }

        window.onload = initApp;
    </script>
</body>
</html>
"""

final_html = template.replace('__LESSONS_JSON__', lessons_json)

with open(os.path.join(base_dir, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(final_html)

print(f"SUCCESS! Interactive Web Application generated at: {os.path.join(base_dir, 'index.html')}")
