import gradio as gr
from TTS.api import TTS
import torch

if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = "cpu"  # mps doesn't work yet
else:
    device = "cpu"

torch.set_default_device(device)
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v1")
tts.to(device)

def predict(prompt, language, audio_file_pth, agree):
    if agree == True:
        tts.tts_to_file(
            text=prompt,
            file_path="output.wav",
            speaker_wav=audio_file_pth,
            language=language,
        )

        return (
            gr.make_waveform(
                audio="output.wav",
            ),
            "output.wav",
        )
    else:
        gr.Warning("Please accept the Terms & Condition!")


title = "Coqui🐸 XTTS"

description = """
<a href="https://huggingface.co/coqui/XTTS-v1">XTTS</a> is a Voice generation model that lets you clone voices into different languages by using just a quick 3-second audio clip. 
<br/>
Built on Tortoise, XTTS has important model changes that make cross-language voice cloning and multi-lingual speech generation super easy. 
<br/>
This is the same model that powers Coqui Studio, and Coqui API, however we apply a few tricks to make it faster and support streaming inference.
<br/>
<br/>
<p>For faster inference without waiting in the queue, you should duplicate this space and upgrade to GPU via the settings.
<br/>
<a href="https://huggingface.co/spaces/coqui/xtts?duplicate=true">
<img style="margin-top: 0em; margin-bottom: 0em" src="https://bit.ly/3gLdBN6" alt="Duplicate Space"></a>
</p>
"""

article = """
<div style='margin:20px auto;'>
<p>By using this demo you agree to the terms of the Coqui Public Model License at https://coqui.ai/cpml</p>
</div>
"""

examples = [
    [
        "Once when I was six years old I saw a magnificent picture.",
        "en",
        "examples/female.wav",
        True,
    ],
    [
        "Lorsque j'avais six ans j'ai vu, une fois, une magnifique image.",
        "fr",
        "examples/male.wav",
        True,
    ],
    [
        "Un tempo lontano, quando avevo sei anni, vidi un magnifico disegno.",
        "it",
        "examples/female.wav",
        True,
    ],
]

gr.Interface(
    fn=predict,
    inputs=[
        gr.Textbox(
            label="Text Prompt",
            info="One or two sentences at a time is better",
            value="It took me quite a long time to develop a voice, and now that I have it I'm not going to be silent.",
        ),
        gr.Dropdown(
            label="Language",
            info="Select an output language for the synthesised speech",
            choices=[
                "en",
                "es",
                "fr",
                "de",
                "it",
                "pt",
                "pl",
                "tr",
                "ru",
                "nl",
                "cz",
                "ar",
                "zh-cn",
            ],
            max_choices=1,
            value="en",
        ),
        gr.Audio(
            label="Reference Audio",
            info="Click on the ✎ button to upload your own target speaker audio",
            type="filepath",
            value="examples/female.wav",
        ),
        gr.Checkbox(
            label="Agree",
            value=False,
            info="I agree to the terms of the Coqui Public Model License at https://coqui.ai/cpml",
        ),
    ],
    outputs=[
        gr.Video(label="Waveform Visual"),
        gr.Audio(label="Synthesised Audio"),
    ],
    title=title,
    description=description,
    article=article,
    examples=examples,
).queue().launch(debug=True)
