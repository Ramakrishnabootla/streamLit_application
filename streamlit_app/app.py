import streamlit as st
from datetime import datetime

st.set_page_config(page_title="HeritageVerse", layout="centered")
st.title("HeritageVerse: Share Your Cultural Stories")

st.write("""
Welcome to HeritageVerse! Share your stories, proverbs, or memories in any language. We'll detect the language, generate audio, and create a beautiful story card for you.
""")

with st.form("story_form"):
    name = st.text_input("Your Name (optional)")
    story = st.text_area("Your Story or Proverb", height=150)
    submitted = st.form_submit_button("Submit")

if submitted and story.strip():
    st.info("Processing your submission...")
    # Language detection
    from langdetect import detect, DetectorFactory
    DetectorFactory.seed = 0
    try:
        detected_lang = detect(story)
        st.success(f"Detected Language: {detected_lang}")
    except Exception as e:
        st.error(f"Language detection failed: {e}")
        detected_lang = None
    # TTS generation
    import os
    import pyttsx3
    import uuid
    audio_dir = os.path.join("data", "audio")
    os.makedirs(audio_dir, exist_ok=True)
    audio_filename = f"audio_{uuid.uuid4().hex}.mp3"
    audio_path = os.path.join(audio_dir, audio_filename)
    try:
        engine = pyttsx3.init()
        engine.save_to_file(story, audio_path)
        engine.runAndWait()
        st.audio(audio_path, format="audio/mp3")
        with open(audio_path, "rb") as f:
            st.download_button("Download Audio", f, file_name=audio_filename)
        st.success("Audio generated!")
    except Exception as e:
        st.error(f"TTS generation failed: {e}")
    # Image card generation
    from PIL import Image, ImageDraw, ImageFont
    card_dir = os.path.join("data", "cards")
    os.makedirs(card_dir, exist_ok=True)
    card_filename = f"card_{uuid.uuid4().hex}.png"
    card_path = os.path.join(card_dir, card_filename)
    try:
        # Create a blank image
        img = Image.new('RGB', (800, 400), color=(245, 235, 220))
        draw = ImageDraw.Draw(img)
        # Try to use a truetype font, fallback to default
        try:
            font = ImageFont.truetype("arial.ttf", 28)
        except:
            font = ImageFont.load_default()
        # Word wrap the story text
        import textwrap
        margin, offset = 40, 40
        for line in textwrap.wrap(story, width=40):
            bbox = font.getbbox(line)
            line_height = bbox[3] - bbox[1]
            draw.text((margin, offset), line, font=font, fill=(60, 40, 20))
            offset += line_height + 8
        # Add name if provided
        if name.strip():
            draw.text((margin, 350), f"- {name.strip()}", font=font, fill=(100, 80, 60))
        img.save(card_path)
        with open(card_path, "rb") as f:
            st.download_button("Download Story Card", f, file_name=card_filename)
        st.image(card_path, caption="Your Story Card", use_column_width=True)
        st.success("Story card generated!")
    except Exception as e:
        st.error(f"Story card generation failed: {e}")
    # Data storage
    import json
    data = {
        "name": name.strip(),
        "story": story.strip(),
        "language": detected_lang,
        "timestamp": datetime.now().isoformat(),
        "audio_path": audio_path,
        "card_path": card_path
    }
    json_path = "stories.json"
    # Read existing data
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                stories = json.load(f)
            except Exception:
                stories = []
    else:
        stories = []
    stories.append(data)
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(stories, f, ensure_ascii=False, indent=2)
    st.success("Submission saved locally!")
    # Placeholder: Data storage
    st.info("Feature implementation coming up") 