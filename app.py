import gradio as gr
import openai
import requests
from gtts import gTTS
from moviepy.editor import *
from io import BytesIO
from tempfile import NamedTemporaryFile
from base64 import b64encode
from pydub import AudioSegment

input_gif_path = "https://i.imgur.com/ork8hoP.gif"
#Lucy https://i.imgur.com/RLMkj1P.gif
#Lisa "https://i.imgur.com/ork8hoP.gif"

def get_text_response(prompt,openAI_key):
  openai.api_key = openAI_key
  completions = openai.Completion.create(engine="text-davinci-003",prompt=prompt,max_tokens=600,n=1,stop=None,temperature=0.5,)
  message = completions.choices[0].text.strip()
  return message

def text_to_speech(text, output_file):
    tts = gTTS(text=text, lang='en', tld='co.uk')
    tts.save(output_file)

def chat_and_animate(output_file, user_prompt,openAI_key):
    # Get audio response from OpenAI API
    text_response = get_text_response(user_prompt,openAI_key)
    text_to_speech(text_response, "response.mp3")

    # Get audio duration in milliseconds
    audio = AudioSegment.from_file("response.mp3")
    audio_duration = len(audio)

    # Download the input GIF
    response = requests.get(input_gif_path)

    # Save the input GIF to a temporary file
    with NamedTemporaryFile(delete=False, suffix=".gif") as temp_gif:
        temp_gif.write(response.content)

        # Load the input GIF
        gif_clip = VideoFileClip(temp_gif.name)

    # Calculate the number of loops required to match the audio duration
    num_loops = audio_duration / (gif_clip.duration * 1000)

    # Duplicate the animated GIF to match the audio duration
    final_gif = gif_clip.loop(n=int(num_loops))

    # Set the audio to the animated GIF
    final_video = final_gif.set_audio(AudioFileClip("response.mp3"))

    # Save the final video
    final_video.write_videofile(output_file, codec="libx264", audio_codec="aac")

    # Clean up the temporary GIF file
    os.unlink(temp_gif.name)

# Set up the input and output components for the Gradio app
user_prompt = gr.inputs.Textbox(label="Ask me anything", default="Welcome")
output_video = gr.outputs.Video()

def chatbot(user_prompt,openAI_key):
    if user_prompt.strip() == '':
        return '[ERROR]: Blank input not allowed.'
    if openAI_key.strip() == '':
      return '[ERROR]: Please enter your Open AI Key. Get your key here : https://platform.openai.com/account/api-keys'
    if user_prompt.lower() == "welcome":
        output_file = "preloaded.mp4"
    else:
        output_file = "output.mp4"
        chat_and_animate(output_file, user_prompt,openAI_key)
    return output_file

with gr.Blocks() as demo:
    gr.Markdown(f'<center><h1>Ask Lisa !</h1></center>')
    gr.Markdown(f'<center><p>Ask Lisa is an AI powered chatbot experiment that provides users with animated video responses to their questions. Ask anything, from general knowledge, advice, to fun facts and play the video responses.</p></center>')
    gr.Markdown(f'<center><p>Powered by <a href="https://www.bhaskartripathi.com">www.bhaskartripathi.com</a></p></center>')
    gr.Markdown(f'<span><img src="https://i.imgur.com/ork8hoP.gif" width="100" height="100"></span>')
    with gr.Row():

        with gr.Group():
            gr.Markdown(f'<p style="text-align:center">Get your Open AI API key <a href="https://platform.openai.com/account/api-keys">here</a></p>')
            openAI_key=gr.Textbox(label='Enter your OpenAI API key here')
            question = gr.Textbox(label='Ask me anything, and I will give you an animated response! Enteryour question here')
            btn = gr.Button(value='Talk')

            btn.style(full_width=True)
        with gr.Group():
            output_video = gr.outputs.Video()
        btn.click(chatbot, inputs=[question,openAI_key], outputs=[output_video])
#openai.api_key = os.getenv('Your_Key_Here') 

demo.launch()
