import os
import json
import whisper

print("Loading Whisper model (base)...")
model = whisper.load_model("base")

lessons_to_process = [
    {
        "index": "02-01",
        "dir": "./lessons/02-01_逍遥游：中国艺术的最高理想"
    },
    {
        "index": "02-02",
        "dir": "./lessons/02-02_《逍遥游》今译：中国文学和中国艺术的总体概括"
    }
]

for item in lessons_to_process:
    audio_path = os.path.join(item["dir"], "audio.m4a")
    print(f"\n--- Transcribing {item['index']} audio at {audio_path} ---")
    result = model.transcribe(audio_path, language="zh")
    
    segments_data = []
    for i, seg in enumerate(result["segments"]):
        segments_data.append({
            "id": i,
            "start": round(seg["start"], 2),
            "end": round(seg["end"], 2),
            "text": seg["text"].strip()
        })
    
    out_path = os.path.join(item["dir"], "whisper_segments.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(segments_data, f, ensure_ascii=False, indent=2)
    print(f"Saved {len(segments_data)} segments to {out_path}")

print("\nTranscription complete!")
