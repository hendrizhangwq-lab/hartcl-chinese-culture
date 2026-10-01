document.addEventListener('DOMContentLoaded', () => {
  let lessons = [];
  let currentLessonIndex = 0;
  let currentLanguage = 'zh'; // 'zh', 'en', 'bilingual'
  let playbackSpeeds = [0.8, 1.0, 1.25, 1.5, 2.0];
  let currentSpeedIndex = 1; // Default 1.0x

  // DOM Elements
  const lessonListEl = document.getElementById('lessonList');
  const searchInputEl = document.getElementById('searchInput');
  
  const audioElement = document.getElementById('audioElement');
  const playPauseBtn = document.getElementById('playPauseBtn');
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const rewindBtn = document.getElementById('rewindBtn');
  const forwardBtn = document.getElementById('forwardBtn');
  const progressBar = document.getElementById('progressBar');
  const currentTimeEl = document.getElementById('currentTime');
  const durationTimeEl = document.getElementById('durationTime');
  const speedBtn = document.getElementById('speedBtn');
  const volumeBar = document.getElementById('volumeBar');
  const volumeIcon = document.getElementById('volumeIcon');

  const currentTrackNumEl = document.getElementById('currentTrackNum');
  const currentTrackTitleEl = document.getElementById('currentTrackTitle');

  const quoteCardImg = document.getElementById('quoteCardImage');
  const posterPlaceholder = document.getElementById('posterPlaceholder');
  const posterContainer = document.getElementById('posterContainer');

  const transcriptContentEl = document.getElementById('transcriptContent');
  const transcriptLoadingEl = document.getElementById('transcriptLoading');
  const langBtns = document.querySelectorAll('.lang-btn');

  const themeToggleBtn = document.getElementById('themeToggle');
  const imageModal = document.getElementById('imageModal');
  const modalImage = document.getElementById('modalImage');
  const modalCloseBtn = document.getElementById('modalCloseBtn');
  const modalBackdrop = document.getElementById('modalBackdrop');

  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const sidebarOverlay = document.getElementById('sidebarOverlay');
  const sidebarEl = document.querySelector('.sidebar');

  // Mobile Drawer Toggle
  if (mobileMenuBtn && sidebarEl && sidebarOverlay) {
    mobileMenuBtn.addEventListener('click', () => {
      sidebarEl.classList.toggle('open');
      sidebarOverlay.classList.toggle('active');
    });

    sidebarOverlay.addEventListener('click', () => {
      sidebarEl.classList.remove('open');
      sidebarOverlay.classList.remove('active');
    });
  }

  // Fetch Lessons Data
  fetch('lessons_data.json')
    .then(res => res.json())
    .then(data => {
      lessons = data;
      renderLessonList(lessons);
      if (lessons.length > 0) {
        selectLesson(0);
      }
    })
    .catch(err => {
      console.error('Failed to load lessons_data.json:', err);
      transcriptLoadingEl.innerHTML = `<p style="color:var(--accent-red)">无法加载课程数据，请确保 process_all_lessons.py 已执行。</p>`;
    });

  // Render Lesson List
  function renderLessonList(items) {
    lessonListEl.innerHTML = '';
    if (items.length === 0) {
      lessonListEl.innerHTML = '<div style="padding:16px; color:var(--text-muted); font-size:13px;">未找到匹配课程</div>';
      return;
    }

    items.forEach((lesson) => {
      const originalIdx = lessons.findIndex(l => l.trackId === lesson.trackId);
      const itemEl = document.createElement('div');
      itemEl.className = `lesson-item ${originalIdx === currentLessonIndex ? 'active' : ''}`;
      itemEl.dataset.index = originalIdx;

      const formatMin = lesson.duration ? `${Math.floor(lesson.duration / 60)} min` : '';

      itemEl.innerHTML = `
        <div class="lesson-num">${String(lesson.index).padStart(2, '0')}</div>
        <div class="lesson-info">
          <div class="lesson-title" title="${lesson.title}">${lesson.title}</div>
          <div class="lesson-duration">
            <i class="ri-time-line"></i> ${formatMin || '精选音频'}
          </div>
        </div>
      `;

      itemEl.addEventListener('click', () => {
        selectLesson(originalIdx);
      });

      lessonListEl.appendChild(itemEl);
    });
  }

  // Select Lesson
  function selectLesson(index) {
    if (index < 0 || index >= lessons.length) return;
    currentLessonIndex = index;
    const lesson = lessons[index];

    // Update active class in sidebar
    document.querySelectorAll('.lesson-item').forEach(el => {
      el.classList.toggle('active', parseInt(el.dataset.index) === index);
    });

    // Close mobile drawer if open
    if (sidebarEl && sidebarEl.classList.contains('open')) {
      sidebarEl.classList.remove('open');
      if (sidebarOverlay) sidebarOverlay.classList.remove('active');
    }

    // Update Track Info
    currentTrackNumEl.textContent = String(lesson.index).padStart(2, '0');
    currentTrackTitleEl.textContent = lesson.title;

    // Load Audio
    audioElement.src = lesson.audioPath;
    audioElement.playbackRate = playbackSpeeds[currentSpeedIndex];
    audioElement.load();
    playAudio();

    // Load Quote Card Poster Image
    if (lesson.quoteCardPath) {
      quoteCardImg.src = lesson.quoteCardPath;
      quoteCardImg.classList.remove('hidden');
      posterPlaceholder.style.display = 'none';
    } else {
      quoteCardImg.classList.add('hidden');
      posterPlaceholder.style.display = 'flex';
    }

    // Render Transcript
    renderTranscript(lesson);
  }

  // Render Transcript Text according to language selection
  function renderTranscript(lesson) {
    transcriptLoadingEl.style.display = 'none';
    transcriptContentEl.innerHTML = '';

    const zhText = lesson.transcriptZh || '';
    const enText = lesson.transcriptEn || '';

    if (currentLanguage === 'zh') {
      const paras = zhText.split('\n').filter(p => p.trim() !== '');
      paras.forEach(p => {
        const pEl = document.createElement('p');
        pEl.textContent = p;
        transcriptContentEl.appendChild(pEl);
      });
    } else if (currentLanguage === 'en') {
      const paras = enText.split('\n').filter(p => p.trim() !== '');
      paras.forEach(p => {
        const pEl = document.createElement('p');
        pEl.textContent = p;
        transcriptContentEl.appendChild(pEl);
      });
    } else if (currentLanguage === 'bilingual') {
      const zhParas = zhText.split('\n');
      const enParas = enText.split('\n');
      const maxLen = Math.max(zhParas.length, enParas.length);

      for (let i = 0; i < maxLen; i++) {
        const zhP = zhParas[i] || '';
        const enP = enParas[i] || '';
        if (!zhP.trim() && !enP.trim()) continue;

        const pairEl = document.createElement('div');
        pairEl.className = 'bilingual-pair';
        pairEl.innerHTML = `
          <div class="bilingual-zh">${zhP}</div>
          <div class="bilingual-en">${enP}</div>
        `;
        transcriptContentEl.appendChild(pairEl);
      }
    }
  }

  // Audio Player Controls
  function playAudio() {
    audioElement.play().then(() => {
      playPauseBtn.innerHTML = '<i class="ri-pause-fill"></i>';
    }).catch(err => {
      console.log('Autoplay prevented or error:', err);
      playPauseBtn.innerHTML = '<i class="ri-play-fill"></i>';
    });
  }

  function pauseAudio() {
    audioElement.pause();
    playPauseBtn.innerHTML = '<i class="ri-play-fill"></i>';
  }

  playPauseBtn.addEventListener('click', () => {
    if (audioElement.paused) {
      playAudio();
    } else {
      pauseAudio();
    }
  });

  prevBtn.addEventListener('click', () => {
    if (currentLessonIndex > 0) selectLesson(currentLessonIndex - 1);
  });

  nextBtn.addEventListener('click', () => {
    if (currentLessonIndex < lessons.length - 1) selectLesson(currentLessonIndex + 1);
  });

  rewindBtn.addEventListener('click', () => {
    audioElement.currentTime = Math.max(0, audioElement.currentTime - 10);
  });

  forwardBtn.addEventListener('click', () => {
    audioElement.currentTime = Math.min(audioElement.duration || 0, audioElement.currentTime + 10);
  });

  // Time & Progress Updates
  audioElement.addEventListener('timeupdate', () => {
    const current = audioElement.currentTime || 0;
    const duration = audioElement.duration || 0;
    
    if (duration > 0) {
      progressBar.value = (current / duration) * 100;
    }
    currentTimeEl.textContent = formatTime(current);
    durationTimeEl.textContent = formatTime(duration);
  });

  audioElement.addEventListener('ended', () => {
    if (currentLessonIndex < lessons.length - 1) {
      selectLesson(currentLessonIndex + 1);
    } else {
      pauseAudio();
    }
  });

  progressBar.addEventListener('input', () => {
    const duration = audioElement.duration || 0;
    audioElement.currentTime = (progressBar.value / 100) * duration;
  });

  // Speed Toggle
  speedBtn.addEventListener('click', () => {
    currentSpeedIndex = (currentSpeedIndex + 1) % playbackSpeeds.length;
    const speed = playbackSpeeds[currentSpeedIndex];
    audioElement.playbackRate = speed;
    speedBtn.textContent = `${speed.toFixed(1)}x`;
  });

  // Volume Control
  volumeBar.addEventListener('input', () => {
    audioElement.volume = volumeBar.value;
    if (volumeBar.value == 0) {
      volumeIcon.className = 'ri-volume-mute-line';
    } else {
      volumeIcon.className = 'ri-volume-up-line';
    }
  });

  // Format Time Helper
  function formatTime(seconds) {
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
  }

  // Language Buttons
  langBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      langBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentLanguage = btn.dataset.lang;
      if (lessons[currentLessonIndex]) {
        renderTranscript(lessons[currentLessonIndex]);
      }
    });
  });

  // Search Input
  searchInputEl.addEventListener('input', (e) => {
    const query = e.target.value.trim().toLowerCase();
    if (!query) {
      renderLessonList(lessons);
      return;
    }

    const filtered = lessons.filter(l => 
      l.title.toLowerCase().includes(query) ||
      l.transcriptZh.toLowerCase().includes(query) ||
      l.transcriptEn.toLowerCase().includes(query)
    );
    renderLessonList(filtered);
  });

  // Theme Toggle
  themeToggleBtn.addEventListener('click', () => {
    document.body.classList.toggle('dark-theme');
    document.body.classList.toggle('light-theme');
  });

  // Modal Lightbox for Poster
  posterContainer.addEventListener('click', () => {
    if (quoteCardImg.src && !quoteCardImg.classList.contains('hidden')) {
      modalImage.src = quoteCardImg.src;
      imageModal.classList.add('active');
    }
  });

  modalCloseBtn.addEventListener('click', closeModal);
  modalBackdrop.addEventListener('click', closeModal);

  function closeModal() {
    imageModal.classList.remove('active');
  }
});
