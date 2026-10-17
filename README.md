# HartCL - 中国文化必修课 (Chinese Culture Essential Course) Platform

An interactive, high-performance web-based learning platform for the course **《余秋雨·中国文化必修课》** (*Chinese Culture Required Course* by Yu Qiuyu), titled *"中国文化视角下的全球观察"* (Global Observations from the Perspective of Chinese Culture).

---

## 📖 Overview

HartCL provides a modern web interface for reading, listening to, and studying 24 core lessons on Chinese cultural philosophy, history, and literature. It features synchronized audio playback with live sentence highlighting, bilingual transcripts (Chinese & English), and deep lesson summaries with structured vocabulary glossaries.

---

## 🌐 GitHub Repository & Hosting Details

- **GitHub Account / Owner**: `hendrizhangwq-lab`
- **Account Email**: `hendrizhangwq@gmail.com`
- **Repository**: [`hendrizhangwq-lab/hartcl-chinese-culture`](https://github.com/hendrizhangwq-lab/hartcl-chinese-culture.git)
- **Git Branch**: `main`
- **GitHub Pages URL**: [https://hendrizhangwq-lab.github.io/hartcl-chinese-culture/](https://hendrizhangwq-lab.github.io/hartcl-chinese-culture/)


---

## ✨ Key Features

1. **Synchronized Audio & Live Highlight**:
   - Audio playback synchronizes in real time with transcript text using Whisper-aligned timestamps (`timed_transcript.json`).
   - Clicking any sentence jumps audio playback directly to that timestamp.
2. **Three Interactive View Modes**:
   - **Deep Summary (深度精读)**: Core takeaway (`gist`), 4 key highlights (bilingual), and a structured vocabulary & cultural glossary (with Pinyin, Chinese definitions, and English explanations, curated flexibly according to text difficulty rather than a rigid quota).
   - **Chinese Transcript (中文原文)**: Clean full text in Chinese.
   - **English Translation (英文对照)**: Line-by-line English translation.
3. **Audio Control Panel**:
   - Variable playback speeds (0.8x, 1.0x, 1.25x, 1.5x, 2.0x).
   - Skip back 10s / forward 10s, progress bar seeking, volume controls.
   - Auto-scroll lock & manual scroll sync.
4. **Search & Navigation**:
   - Real-time search filter across lesson titles and transcript contents.
   - Dark mode & Light mode theme toggle.

---

## 📁 Directory Structure

```
HartCL/
├── index.html                    # Main Web Application entry point
├── app.js                        # Core Application logic, state management, audio sync, UI rendering
├── styles.css                    # Responsive layout, dark/light themes, custom typography
├── lessons_data.json             # Compiled master dataset for all 24 lessons
├── build_deep_summaries.py       # Main Python script to generate & update summaries/glossaries in lessons_data.json
├── build_app.py                  # Build tool to package lesson folders into single HTML/JSON apps
├── build_custom_app.py           # Alternative build script for custom web variations
├── download_full_audios.py       # Utility: Download/manage full audio files
├── download_posters.py           # Utility: Fetch cover images and quote card posters
├── generate_english_transcripts.py # Utility: Batch generate English translation markdowns
├── clean_headers.py              # Utility: Clean markdown header metadata
├── update_full_transcripts.py    # Utility: Update raw transcript files
└── 01_ shortest... to 24_.../    # 24 Lesson Directories (e.g., 01_最短的文化定义)
    ├── audio.m4a                 # Original lecture audio
    ├── transcript.md             # Full Chinese transcript
    ├── english_transcript.md     # Full English transcript
    ├── timed_transcript.json     # Word/sentence-level timestamps for player sync
    ├── aligned_paragraphs.json   # Paragraph-aligned timing structure
    ├── whisper_segments.json     # Ground truth speech segmentation data from Whisper
    ├── cover.jpg                 # Lesson cover image
    └── quote_card.jpg            # Cultural quote poster card
```

---

## 📊 Data Schema (`lessons_data.json`)

The compiled `lessons_data.json` contains an array of 24 lesson objects structured as follows:

```json
[
  {
    "index": "01",
    "title": "最短的文化定义",
    "trackId": 1,
    "folderName": "01_最短的文化定义",
    "audioPath": "./01_最短的文化定义/audio.m4a",
    "quoteCardPath": "./01_最短的文化定义/quote_card.jpg",
    "transcriptZh": "...(full Chinese text)...",
    "transcriptEn": "...(full English translation)...",
    "duration": 0,
    "summary": {
      "gistZh": "核心观点（中文）",
      "gistEn": "Core Takeaway (English)",
      "highlights": [
        { "zh": "要点中文", "en": "Key takeaway English" }
      ],
      "vocabulary": [
        {
          "word": "安身立命",
          "pinyin": "ān shēn lì mìng",
          "en": "To Establish Oneself & Find Spiritual Anchoring",
          "explanationZh": "详细中文解释...",
          "explanationEn": "Detailed English explanation..."
        }
      ]
    },
    "timedTranscript": [
      {
        "id": "p0_s0",
        "start": 0.0,
        "end": 4.5,
        "zh": "各位朋友，大家好。",
        "en": "Hello everyone, my friends."
      }
    ]
  }
]
```

---

## 🛠️ How to Run & Build

### 1. Run the Web Application locally
Start a simple local HTTP server from the project directory:

```bash
# Using Python 3
python3 -m http.server 8000
```
Then open `http://localhost:8000` in your web browser.

### 2. Rebuilding or Updating Lesson Data
To re-compile deep summaries, bilingual highlights, and vocabulary glossaries into `lessons_data.json`:

```bash
python3 build_deep_summaries.py
```

---

### 📖 Vocabulary & Cultural Glossary Guideline
- **Content-Driven, Flexible Entry Count**: Difficult vocabulary and cultural glossary terms are **not strictly limited to or required to reach 18 entries**. Entries should be selected or excluded organically based on the actual lexical, philosophical, and cultural difficulty of the lesson's text.

---

## 📌 Project Status & Roadmap

- **Completed**:
  - Full structural setup and asset organization for all units.
  - Deep summaries and structured vocabulary glossaries for core units (including Unit 1, 2, 02-01, 02-02, 03, 03-01, 10).
  - Ground-truth Whisper speech timing synchronization tuned for Units 01, 02, 02-01, 02-02, 03, and 03-01.
  - Fully functional responsive Web UI with dark/light mode and search.
- **Ongoing & Future Work**:
  - Extend deep summaries & text-difficulty-calibrated vocabulary glossaries to remaining units.
  - Fine-tune speech-to-text timing alignment (`timed_transcript.json`) across remaining units.
