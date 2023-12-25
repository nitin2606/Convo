from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO

import os
import speech_recognition as sr
import question
import imageio
import threading
import time

app = Flask(__name__)
socketio = SocketIO(app)

current_directory = os.path.dirname(os.path.realpath(__file__))

intents_and_question = question.intents_and_question
video_urls = question.video_urls

micPermission = True

class SharedData:

    def __init__(self):

        self.micPermission = micPermission
        #self.pause_event = threading.Event()
        #self.listening_state = True


def get_intent(text):
    lowercase_text = text.lower()
    matching_intent = [intent for intent, questions in intents_and_question.items() if any(q in lowercase_text for q in questions)]
    return matching_intent[0] if matching_intent else 'no_answer'


def get_video_response(intent):
    return video_urls.get(intent)


def calc_video_length(url):
    try:
        reader = imageio.get_reader(url)
        duration = reader.get_meta_data()['duration']
        reader.close()
        return duration
    except Exception as e:
        return "error"
    

def recognize_and_emit(shared_data):

    recognizer = sr.Recognizer()

    if shared_data.micPermission is True:
        with sr.Microphone() as source:
            while True:
                try:
                    
                    #shared_data.pause_event.wait()
                    print("Listening ....")
                    audio_data = recognizer.record(source, duration = 3.5)
                    #audio_data = recognizer.listen(source, timeout=5)
                    print("Recognizing your text .........")
                    text = recognizer.recognize_google(audio_data)

                
                    intent = get_intent(text.strip())
                    video_url = get_video_response(intent)

                    length = calc_video_length(video_url)

                    #shared_data.length = length

                    

                    socketio.emit('text_received', {'text': text, 'intent': intent, 'video_url': video_url})
                    print("Recognized Text:", text)

                    shared_data.micPermission = False
                    print("Going to sleep...")
                    source = None
                    time.sleep(length)
                    shared_data.micPermission = True
                    recognize_and_emit(shared_data)

                   
                    
                except sr.UnknownValueError:
                    print("Speech Recognition could not understand audio")
                except sr.RequestError as e:
                    print(f"Could not request {e}")


def play_video(video_url):
    # Add code to play the video
    pass



@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('start_listening')
def start_listening(data):
    
    shared_data = SharedData()
    recognition_thread = threading.Thread(target=recognize_and_emit, args=(shared_data,))
    recognition_thread.start()

   
    #recognition_thread.join()  # Wait for the recognition thread to finish

   

if __name__ == '__main__':
    socketio.run(app)
