# Image to Speech — GenAI App by Adithyaa S Kumar

A generative AI pipeline that takes an uploaded image and produces a narrated audio story. Built with HuggingFace Transformers, Groq LLM, and Streamlit.

---

## How It Works

The app runs a three-stage pipeline:

1. **Image → Caption** — [Salesforce BLIP](https://huggingface.co/Salesforce/blip-image-captioning-base) generates a text description of the uploaded image locally using HuggingFace Transformers.
2. **Caption → Story** — [Groq](https://groq.com/) runs `llama-3.3-70b-versatile` to write a short story (max 50 words) based on the caption.
3. **Story → Audio** — `pyttsx3` converts the story to a narrated WAV audio file, fully offline.

![System Design](img/system-design.drawio.png)

---

 

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| Image Captioning | Salesforce BLIP (`blip-image-captioning-base`) |
| Story Generation | Groq API — LLaMA 3.3 70B |
| Text-to-Speech | pyttsx3 (offline) |
| Environment | python-dotenv |

---
 

 

 
