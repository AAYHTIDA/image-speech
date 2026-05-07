import os
import time
from typing import Any

import streamlit as st
from dotenv import find_dotenv, load_dotenv
from transformers import pipeline

from utils.custom import css_code

load_dotenv(find_dotenv())
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def progress_bar(amount_of_time: int) -> Any:
    """
    A very simple progress bar the increases over time,
    then disappears when it reached completion
    :param amount_of_time: time taken
    :return: None
    """
    progress_text = "Please wait, Generative models hard at work"
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(amount_of_time):
        time.sleep(0.04)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()


def generate_text_from_image(url: str) -> str:
    """
    A function that uses the blip model to generate text from an image.
    :param url: image location
    :return: text: generated text from the image
    """
    from PIL import Image
    from transformers import BlipProcessor, BlipForConditionalGeneration

    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    image = Image.open(url).convert("RGB")
    inputs = processor(image, return_tensors="pt")
    output = model.generate(**inputs)
    generated_text: str = processor.decode(output[0], skip_special_tokens=True)

    print(f"IMAGE INPUT: {url}")
    print(f"GENERATED TEXT OUTPUT: {generated_text}")
    return generated_text


def generate_story_from_text(scenario: str) -> str:
    """
    Uses Groq LLM to generate a short story from a scenario.
    :param scenario: generated text from the image
    :return: generated story
    """
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a talented storyteller."},
            {"role": "user", "content": f"Write a short story in maximum 50 words based on this scene: {scenario}"}
        ],
        temperature=0.9,
        max_tokens=120
    )
    generated_story: str = response.choices[0].message.content.strip()
    print(f"TEXT INPUT: {scenario}")
    print(f"GENERATED STORY OUTPUT: {generated_story}")
    return generated_story


def generate_speech_from_text(message: str) -> None:
    """
    Uses pyttsx3 (offline TTS) to convert story text to a WAV audio file.
    :param message: short story text
    """
    import pyttsx3
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.save_to_file(message, "generated_audio.wav")
    engine.runAndWait()



def main() -> None:
    """
    Main function
    :return: None
    """
    st.set_page_config(page_title= "IMAGE TO STORY CONVERTER", page_icon= "🖼️")

    st.markdown(css_code, unsafe_allow_html=True)

    with st.sidebar:
        st.write("Image-to-Story Converter")

    st.header("Image-to-Story Converter")
    uploaded_file: Any = st.file_uploader("Please choose a file to upload", type="jpg")

    if uploaded_file is not None:
        print(uploaded_file)
        bytes_data: Any = uploaded_file.getvalue()
        with open(uploaded_file.name, "wb") as file:
            file.write(bytes_data)
        st.image(uploaded_file, caption="Uploaded Image",
                 use_container_width=True)
        progress_bar(100)
        with st.spinner("Analyzing image..."):
            scenario: str = generate_text_from_image(uploaded_file.name)
        with st.spinner("Generating story..."):
            story: str = generate_story_from_text(scenario)
        with st.spinner("Generating audio..."):
            generate_speech_from_text(story)

        with st.expander("Generated Image scenario"):
            st.write(scenario)
        with st.expander("Generated short story"):
            st.write(story)

        st.audio("generated_audio.wav")


if __name__ == "__main__":
    main()