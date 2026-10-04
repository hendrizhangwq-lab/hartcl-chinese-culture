document.addEventListener('DOMContentLoaded', () => {
  let lessons = [];
  let currentLessonIndex = 0;
  let currentLanguage = 'summary'; // 'summary', 'zh', 'en'
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

  const guideBanner = document.getElementById('guideBanner');
  const dismissGuideBtn = document.getElementById('dismissGuideBtn');
  const helpBtn = document.getElementById('helpBtn');

  // Interactive Chat Bubble Tour with Spotlight Cutout
  const tourSteps = [
    {
      icon: 'ri-sparkling-line',
      target: () => document.querySelector('button[data-lang="summary"]'),
      title: '第一步：30 秒双语导读',
      descZh: '首选入口！先看 Summary 选项卡，30 秒快速掌握本讲的中英双语核心要点与精髓概念。',
      descEn: 'Start here! Scan key concepts and executive takeaways in Chinese & English.'
    },
    {
      icon: 'ri-play-circle-line',
      target: () => document.getElementById('playPauseBtn'),
      title: '第二步：收听讲义原音',
      descZh: '点击这里播放或暂停音频，右侧可自由调节 1.0x / 1.25x / 1.5x 倍速。',
      descEn: 'Tap here to Play/Pause audio. Adjust playback speed on the right.'
    },
    {
      icon: 'ri-file-text-line',
      target: () => document.querySelector('.language-toggle-group'),
      title: '第三步：跟读逐字文稿',
      descZh: '切换至「中文」或「English」，边听音频边同步跟读逐字完整文稿。',
      descEn: 'Switch tabs here to read along with full speech transcripts.'
    },
    {
      icon: 'ri-menu-line',
      target: () => (window.innerWidth <= 900 ? document.getElementById('mobileMenuBtn') : document.querySelector('#lessonList .lesson-item:first-child') || document.getElementById('lessonList')),
      title: '第四步：自由选修 24 讲',
      descZh: '点击左上角 ☰ 菜单(手机端) 或左侧边栏，自由浏览并选择 24 讲精选课程。',
      descEn: 'Tap top-left ☰ or sidebar to browse and pick any of the 24 modules.'
    }
  ];

  let currentTourStep = 0;
  const tourModal = document.getElementById('tourModal');
  const tourCard = document.getElementById('tourCard');
  const tourSpotlight = document.getElementById('tourSpotlight');
  const tourBubbleArrow = document.getElementById('tourBubbleArrow');
  const tourCloseBtn = document.getElementById('tourCloseBtn');
  const tourBackdrop = document.getElementById('tourBackdrop');
  const tourPrevBtn = document.getElementById('tourPrevBtn');
  const tourNextBtn = document.getElementById('tourNextBtn');
  const tourStepBadge = document.getElementById('tourStepBadge');
  const tourIconWrap = document.getElementById('tourIconWrap');
  const tourTitle = document.getElementById('tourTitle');
  const tourDescZh = document.getElementById('tourDescZh');
  const tourDescEn = document.getElementById('tourDescEn');
  const tourDots = document.querySelectorAll('.tour-dots .dot');

  function positionSpotlightAndBubble(targetEl) {
    if (!tourCard || !tourModal || !tourModal.classList.contains('active')) return;

    if (!targetEl) {
      if (tourSpotlight) tourSpotlight.style.display = 'none';
      tourCard.className = 'tour-card arrow-none';
      tourCard.style.top = '50%';
      tourCard.style.left = '50%';
      tourCard.style.transform = 'translate(-50%, -50%)';
      if (tourBubbleArrow) tourBubbleArrow.style.display = 'none';
      return;
    }

    tourCard.style.transform = 'none';
    const rect = targetEl.getBoundingClientRect();

    // 1. Position Spotlight around Target Element
    if (tourSpotlight) {
      tourSpotlight.style.display = 'block';
      const pad = 6;
      tourSpotlight.style.top = `${Math.max(2, rect.top - pad)}px`;
      tourSpotlight.style.left = `${Math.max(2, rect.left - pad)}px`;
      tourSpotlight.style.width = `${rect.width + pad * 2}px`;
      tourSpotlight.style.height = `${rect.height + pad * 2}px`;
    }

    // 2. Position Chat Bubble & Arrow
    const bubbleWidth = Math.min(320, window.innerWidth - 24);
    tourCard.style.width = `${bubbleWidth}px`;
    const bubbleHeight = tourCard.offsetHeight || 210;
    const arrowOffset = 14;

    let top, left, placement;
    const spaceBelow = window.innerHeight - rect.bottom;
    const spaceAbove = rect.top;

    if (spaceBelow >= bubbleHeight + arrowOffset + 10 || spaceBelow >= spaceAbove) {
      placement = 'arrow-top';
      top = rect.bottom + arrowOffset;
    } else {
      placement = 'arrow-bottom';
      top = rect.top - bubbleHeight - arrowOffset;
    }

    // Clamp top inside screen
    top = Math.max(12, Math.min(top, window.innerHeight - bubbleHeight - 12));

    // Align horizontally with target element center
    const targetCenterX = rect.left + rect.width / 2;
    left = targetCenterX - bubbleWidth / 2;
    left = Math.max(12, Math.min(left, window.innerWidth - bubbleWidth - 12));

    tourCard.className = `tour-card ${placement}`;
    tourCard.style.top = `${top}px`;
    tourCard.style.left = `${left}px`;

    if (tourBubbleArrow) {
      tourBubbleArrow.style.display = 'block';
      const arrowLeft = Math.max(18, Math.min(targetCenterX - left - 7, bubbleWidth - 28));
      tourBubbleArrow.style.left = `${arrowLeft}px`;
    }
  }

  function getTargetForStep(step) {
    if (!step) return null;
    return typeof step.target === 'function' ? step.target() : document.querySelector(step.target);
  }

  function showTourStep(index) {
    if (index < 0 || index >= tourSteps.length) return;
    currentTourStep = index;
    const step = tourSteps[index];

    tourStepBadge.textContent = `Step ${index + 1} of ${tourSteps.length}`;
    tourIconWrap.innerHTML = `<i class="${step.icon}"></i>`;
    tourTitle.textContent = step.title;
    tourDescZh.textContent = step.descZh;
    tourDescEn.textContent = step.descEn;

    tourDots.forEach((d, i) => d.classList.toggle('active', i === index));

    tourPrevBtn.style.visibility = index === 0 ? 'hidden' : 'visible';
    if (index === tourSteps.length - 1) {
      tourNextBtn.textContent = '完成 / Got It';
    } else {
      tourNextBtn.textContent = '下一步 / Next';
    }

    // On mobile, ensure sidebar drawer is closed
    if (sidebarEl && window.innerWidth <= 900) {
      sidebarEl.classList.remove('open');
    }

    const targetEl = getTargetForStep(step);
    if (targetEl) {
      targetEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
      positionSpotlightAndBubble(targetEl);
      setTimeout(() => positionSpotlightAndBubble(targetEl), 120);
      setTimeout(() => positionSpotlightAndBubble(targetEl), 300);
      setTimeout(() => positionSpotlightAndBubble(targetEl), 500);
    } else {
      positionSpotlightAndBubble(null);
    }
  }

  function updateActiveTourPosition() {
    if (tourModal && tourModal.classList.contains('active')) {
      const step = tourSteps[currentTourStep];
      const targetEl = getTargetForStep(step);
      positionSpotlightAndBubble(targetEl);
    }
  }

  window.addEventListener('resize', updateActiveTourPosition);
  window.addEventListener('scroll', updateActiveTourPosition, true);

  function startTour() {
    if (!tourModal) return;
    tourModal.classList.add('active');
    showTourStep(0);
  }

  function closeTour() {
    if (!tourModal) return;
    tourModal.classList.remove('active');
    if (tourSpotlight) tourSpotlight.style.display = 'none';
    sessionStorage.setItem('tourSeen', 'true');
  }

  if (tourNextBtn) {
    tourNextBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (currentTourStep === tourSteps.length - 1) {
        closeTour();
      } else {
        showTourStep(currentTourStep + 1);
      }
    });
  }

  if (tourPrevBtn) {
    tourPrevBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      showTourStep(currentTourStep - 1);
    });
  }

  if (tourCloseBtn) tourCloseBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    closeTour();
  });

  if (tourBackdrop) tourBackdrop.addEventListener('click', closeTour);

  // Auto start tour once per session for first-time visitors
  if (!sessionStorage.getItem('tourSeen')) {
    setTimeout(() => {
      startTour();
    }, 500);
  }

  if (helpBtn) {
    helpBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      startTour();
    });
  }

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
  fetch('lessons_data.json?v=3')
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
  function selectLesson(index, autoplay = false) {
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
    if (autoplay) {
      playAudio();
    } else {
      pauseAudio();
    }

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

    if (currentLanguage === 'summary') {
      const sum = lesson.summary || {};
      const gistZh = sum.gistZh || '暂无摘要';
      const gistEn = sum.gistEn || 'No summary available.';
      const highlights = sum.highlights || [];

      let highlightsHtml = '';
      highlights.forEach((h, idx) => {
        highlightsHtml += `
          <div class="summary-card-point">
            <div class="point-badge">${idx + 1}</div>
            <div class="point-text">
              <div class="point-zh">${h.zh}</div>
              <div class="point-en">${h.en}</div>
            </div>
          </div>
        `;
      });

      transcriptContentEl.innerHTML = `
        <div class="summary-wrapper">
          <div class="summary-block">
            <div class="summary-section-title">
              <i class="ri-compass-3-line"></i>
              <span>核心要点 / Executive Summary</span>
            </div>
            <div class="summary-gist-box">
              <p class="summary-gist-zh">${gistZh}</p>
              <p class="summary-gist-en">${gistEn}</p>
            </div>
          </div>

          <div class="summary-block">
            <div class="summary-section-title">
              <i class="ri-lightbulb-line"></i>
              <span>关键概念与亮点 / Key Concepts & Highlights</span>
            </div>
            <div class="summary-highlights-list">
              ${highlightsHtml}
            </div>
          </div>

          <div class="summary-tip">
            <i class="ri-information-line"></i>
            <span>提示：您可以在顶部或下方播放音频，或切换至「中文」/「English」选项卡阅读完整语音文稿。</span>
          </div>
        </div>
      `;
    } else if (currentLanguage === 'zh') {
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
