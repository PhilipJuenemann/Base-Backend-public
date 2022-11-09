from moviepy.editor import *
from google.oauth2 import service_account
from google.cloud import speech_v1 as speech
from google.cloud import storage
from dotenv import load_dotenv, find_dotenv

# loading credentials

#upload to gcloud
def upload_to_gcloud(mp3_location,bucket="the_base_user_inputs"):
    client = storage.Client(credentials=credentials)
    bucket = client.get_bucket('the_base_user_inputs')
    blob = bucket.blob(file)
    blob.upload_from_filename(file)

#delete from gcloud
def delete_from_gcloud(mp3_location,bucket="the_base_user_inputs"):
    client = storage.Client(credentials=credentials)
    bucket = client.get_bucket('the_base_user_inputs')
    blob = bucket.blob(mp3_location)
    blob.delete()

#function to get mp3_from_mp4
def get_mp3_from_mp4(content):
    videoclip = VideoFileClip(content)
    audioclip = videoclip.audio
    mp3_location = audioclip.write_audiofile('mp3_output')
    audioclip.close()
    videoclip.close()
    return mp3_location

#function to convert mp3_to_text
def convert_mp3_to_text(mp3_location):
    upload_to_gcloud(mp3_location)
    media_uri = f"gs://the_base_user_inputs/{mp3_location}"
    long_audi_wav = speech.RecognitionAudio(uri=media_uri)
    speech_client = speech.SpeechClient(credentials=credentials)

    config_wav_enhanced = speech.RecognitionConfig(
    sample_rate_hertz=48000,
    enable_automatic_punctuation=True,
    language_code='en-US',
    use_enhanced=True,
    model='video'
    )

    operation = speech_client.long_running_recognize(
    config=config_wav_enhanced,
    audio=long_audi_wav
    )
    response = operation.result(timeout=90)

    delete_from_gcloud(mp3_location)

    all_parts =[]
    for result in response.results:
        all_parts.append(result.alternatives[0].transcript)
    final_output=''.join(all_parts)
    return final_output

#function to convert mp4_to_text
def convert_mp4_to_text(content):
    convert = get_mp3_from_mp4(content)
    text = convert_mp3_to_text(convert)
    return text
