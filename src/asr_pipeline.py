import onnx_asr
from llama_cpp import Llama
from datetime import datetime,timedelta
from contextlib import redirect_stderr
import os
import json
import re

def convert_times_to_24h(text: str) -> str:
    """
    Converts 12-hour times in free-form ASR text to 24-hour format.
    Special rule: 12 PM -> 23:59
    Correctly removes trailing dots from a.m./p.m.
    """

    time_pattern = re.compile(
        r'\b(?P<hour>\d{1,2})'                 # hour
        r'(?:[:\.](?P<minute>\d{2}))?'         # optional minutes
        r'\s*(?P<period>a|p)'                  # a / p
        r'(?:\.?\s*m\.?)+'                     # m, m., .m., m..
        , flags=re.IGNORECASE
    )

    def replacer(match):
        hour = int(match.group('hour'))
        minute = int(match.group('minute') or 0)
        period = match.group('period').lower()

        # Special rule
        if hour == 12 and period == 'p':
            return '23:59'

        if period == 'p' and hour != 12:
            hour += 12
        if period == 'a' and hour == 12:
            hour = 0

        return f"{hour:02d}:{minute:02d}"

    return time_pattern.sub(replacer, text)




#@profile
def get_transcription(audio_filename="data/sample_1/sample_1.wav"):

    model = onnx_asr.load_model("nemo-parakeet-tdt-0.6b-v3", "models/parakeet-v3") # uses about 2.2GB of memory
    transcription=model.recognize(audio_filename) # uses about 300-600MB of extra memory for inferencing
    return transcription

def generate_task(transcript):

    # Path to your GGUF file
    MODEL_PATH = "models/gemma-3-4b.gguf"
    prompt_template = """
### Instruction:
Extract task information from the following user transcript to create a Todo object.

You MUST calculate exact calendar dates and times using the provided context.

Extraction and precedence rules:
1. Explicitly mentioned information ALWAYS overrides defaults.
2. name: If not stated, summarize the main action of the transcript.
3. tag: Categorize based on context (e.g., Work, Education, Productivity, Entertainment, Chore, Home). Default to "None".
4. status: If not mentioned, default to "Not Started".

Datetime rules:
1. If a weekday (e.g., Monday, Saturday) is mentioned, interpret it as the NEXT occurrence of that weekday after the context date.
2. If a time or time range is mentioned, include it in start_date and end_date.
3. If the end time is earlier than the start time, assume the task ends on the following day.
4. If 12 P.M. or 24:00 is specified as the time, convert it to 00:00 of the next day.
5. Defaults apply ONLY if not explicitly mentioned:
   - start_date: Today at 00:00
   - end_date: Today at 23:59

Context (current datetime): {context}

Output ONLY a valid JSON object.
Do NOT include explanations, comments, or extra text.

### Input Transcript:
"{USER_TRANSCRIPT}"

### Output:
"""

    today=datetime.today()
    today_as_string=today.strftime("%d/%m/%Y %H:%M")
    context=f"Today is '{today_as_string}' ({today.strftime("%A")}).\nUpcoming Days:\n"

    for i in range(7):
        day= today + timedelta(days=i)
        day_as_string=day.strftime('%d/%m/%Y')
        context+=f"{day.strftime('%A')}: {day_as_string}\n"
        

    tomorrow= today + timedelta(days=1)
    tomorrow_start_as_string=tomorrow.replace(hour=0, minute=00).strftime("%d/%m/%Y %H:%M")
    tomorrow_end_as_string=tomorrow.replace(hour=23, minute=59).strftime("%d/%m/%Y %H:%M")




    prompt=prompt_template.format(context=context,USER_TRANSCRIPT=transcript, tomorrow_date_start=tomorrow_start_as_string, tomorrow_date_end=tomorrow_end_as_string)
    print(prompt)


    #Load the model
    with open(os.devnull, "w") as devnull:
        with redirect_stderr(devnull):
            model = Llama(model_path=MODEL_PATH, n_ctx=2048, verbose=False)

    # Generate output
    output = model(prompt,max_tokens=300, stop=["}"], echo=False)
    json_output=output["choices"][0]["text"]+"}"
    json_output= json.loads(json_output[json_output.rfind('{'): ])


    return json_output

def process_transcription(transcription):
    print(transcription)
    transcription=convert_times_to_24h(transcription)
    return transcription

def run_speech_to_task_pipeline(audio_file):
    original_transcription=get_transcription(audio_file)
    processed_transcription=process_transcription(original_transcription)
    task=generate_task(processed_transcription)
    return task

if __name__=="__main__":
    print(generate_task(process_transcription(get_transcription())))
