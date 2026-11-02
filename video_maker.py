import os
import json
from gtts import gTTS
from moviepy.video.VideoClip import ColorClip
from moviepy.audio.io.AudioFileClip import AudioFileClip

IDEAS_FILE = "video_ideas.json"

def load_ideas():
    if os.path.exists(IDEAS_FILE):
        with open(IDEAS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_idea(title, script):
    ideas = load_ideas()
    new_idea = {"id": len(ideas) + 1, "title": title, "script": script}
    ideas.append(new_idea)
    with open(IDEAS_FILE, "w", encoding="utf-8") as f:
        json.dump(ideas, f, ensure_ascii=False, indent=4)
    print(f"[+] Saved Idea #{new_idea['id']} successfully!")

def generate_faceless_video(idea_id):
    ideas = load_ideas()
    target = next((i for i in ideas if i["id"] == idea_id), None)
    
    if not target:
        print("[-] Idea not found!")
        return

    print(f"\n==========================================")
    print(f"🎬 Processing Video #{target['id']}: {target['title']}")
    print(f"==========================================")
    
    # 1. توليد التعليق الصوتي
    print(f"[1/4] Generating AI Voiceover...")
    audio_filename = f"audio_{target['id']}.mp3"
    tts = gTTS(text=target['script'], lang='ar', slow=False)
    tts.save(audio_filename)
    print(f"    └── ✅ Audio ready: {audio_filename}")

    # 2. تجهيز الخلفية السينمائية
    print(f"[2/4] Preparing cinematic background...")

    # 3. دمج الصوت والصورة وإنتاج الفيديو النهائي
    print(f"[3/4] Rendering video & transitions...")
    video_filename = f"output_video_{target['id']}.mp4"
    
    try:
        audio_clip = AudioFileClip(audio_filename)
        duration = audio_clip.duration
        
        # إنشاء خلفية سينمائية مقاس تيك توك 1080x1920 مع الصوت مباشرة
        bg_clip = ColorClip(size=(1080, 1920), color=[20, 20, 20], duration=duration)
        
        # ربط الصوت بالخلفية بالطريقة المتوافقة مع الإصدار الحديث
        final_video = bg_clip.with_audio(audio_clip)
        
        # تصدير الفيديو النهائي
        print(f"[4/4] Exporting final MP4 video...")
        final_video.write_videofile(video_filename, fps=24, codec='libx264', audio_codec='aac')
        
        print(f"\n🎉 SUCCESS! Video exported as: {video_filename}")
        print(f"✅ Ready to upload to TikTok & YouTube Shorts!\n")
        
    except Exception as e:
        # محاولة أخيرة بديلة في حال اختلاف اسم الدالة في الإصدار
        try:
            bg_clip = ColorClip(size=(1080, 1920), color=[20, 20, 20], duration=duration)
            final_video = bg_clip.set_audio(audio_clip)
            final_video.write_videofile(video_filename, fps=24, codec='libx264', audio_codec='aac')
            print(f"\n🎉 SUCCESS! Video exported as: {video_filename}")
        except Exception as e2:
            print(f"[-] Error during video rendering: {e2}")

if __name__ == "__main__":
    print("🤖 Faceless Video Engine Initialized.")
    
    script_text = "الذكاء الاصطناعي يغير العالم، والذين يسيطرون على الأدوات اليوم هم قادة المستقبل."
    save_idea("AI Future", script_text)
    
    all_ideas = load_ideas()
    if all_ideas:
        generate_faceless_video(all_ideas[-1]["id"])

