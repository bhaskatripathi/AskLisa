# AskLisa
Ask Lisa is an AI powered chatbot experiment that provides users with animated video responses to their questions using OpenAI. Ask anything, from general knowledge, advice, to fun facts and play the video responses.

# Demo:
https://bhaskartripathi-text2videolisa.hf.space
[![Output image](Asklisa.png)](https://bhaskartripathi-text2videolisa.hf.space)

## Web Component
```
<script
	type="module"
	src="https://gradio.s3-us-west-2.amazonaws.com/3.28.0/gradio.js"
></script>
<gradio-app src="https://bhaskartripathi-text2videolisa.hf.space"></gradio-app>
```
## Run with Docker
```
docker run -it -p 7860:7860 --platform=linux/amd64 \
	registry.hf.space/bhaskartripathi-text2videolisa:latest python app.py
  ```
## Note
Please Star this project if you like it.

# TODO
1. Lip Synching using Wav2Lip
2. Real time Voice Cloning support of own individual voice
3. Create a Next.js based app
4. Autoplay video after taking input.
