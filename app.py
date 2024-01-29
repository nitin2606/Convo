from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import os
import speech_recognition as sr
import question
import imageio
import threading
import time
import firebase_admin
from firebase_admin import credentials, db, initialize_app
import mic_control
import serial_comm
import update_vid
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


time.sleep(1.5)

app = Flask(__name__)
socketio = SocketIO(app)

current_directory = os.path.dirname(os.path.realpath(__file__))

json_path = os.path.join(current_directory, 'auth.json')

cred = credentials.Certificate(json_path)
firebase_admin.initialize_app(cred, {'databaseURL': 'https://authentication-app-59d78-default-rtdb.firebaseio.com/'})

data_ref = db.reference('/intents_and_questions')
vid_ref = db.reference('/video_urls')
#ref = db.reference('/')
data = data_ref.get()

video_urls_cloud = vid_ref.get()

update_vid.sync_video(video_urls=video_urls_cloud)

video_urls_local = question.video_urls

print("Local Video Url: ", video_urls_local)

micPermission = True

class SharedData:

    def __init__(self):

        self.micPermission = micPermission
      


'''def get_intent(text):
    lowercase_text = text.lower()
    matching_intent = [intent for intent, questions in intents_and_question.items() if any(q in lowercase_text for q in questions)]
    return matching_intent[0] if matching_intent else 'no_answer'
'''


'''def get_intent_firebase(text):

    lowercase_text = text.lower()
    matching_intent = [intent for intent, questions in data.items() if any(q in lowercase_text for q in questions)]
    return matching_intent[0] if matching_intent else 'no_answer'
'''


def get_intent_firebase(text):
  lowercase_text = text.lower()
  matching_intent = []
  # Find the closest matching question for each intent
  for intent, questions in data.items():
    closest_q, score = process.extractOne(lowercase_text, questions, scorer=fuzz.ratio)
    #print(score)
    if score > 70:  # Set a threshold for confidence
      print(matching_intent)
      matching_intent.append(intent)

  # Return the first matching intent or "no_answer" if no match is found
  return matching_intent[0] if matching_intent else "no_answer"



def get_video_response(intent):
    return video_urls_local.get(intent)
    


def calc_video_length(url):
    try:
        reader = imageio.get_reader(url)
        duration = reader.get_meta_data()['duration']
        reader.close()
        return duration
    
    except Exception as e:
        return 0
    

def recognize_and_emit():

    count = 0
    while True:

        if (serial_comm.sensorData() == 0):
            
            count = count+1
            
            print(f"Inside If statement, sensor value:{serial_comm.sensorData()}")

            if count==1:

                socketio.emit('text_received', {'text': "active", 'intent': 'greet', 'video_url': "static/greet.mp4"})
                
                mic_control.mute_microphone()
                print("Recognized Text:", 'active')

                time.sleep(calc_video_length("static/greet.mp4"))
                mic_control.unmute_microphone()
            

            elif count>1:

            
                try:

                    print("Inside try statement")

                    recognizer = sr.Recognizer()

                    with sr.Microphone() as source:
                    
                        
                        print("Listening ....")
                        audio_data = recognizer.record(source, duration = 3.5)
                        #audio_data = recognizer.listen(source, timeout=None)
                        print("Recognizing your text .........")
                        text = recognizer.recognize_google(audio_data)

                        print("Recognised Text: ",text)
                        #intent = get_intent(text.strip())
                        intent = get_intent_firebase(text.strip())
                        video_url = get_video_response(intent)

                        length = calc_video_length(video_url)

                        
                        socketio.emit('text_received', {'text': text, 'intent': intent, 'video_url': video_url})
                        print("Recognized Text:", text)

                        
                        print("Going to sleep...")
                        #source = None
                        mic_control.mute_microphone()
                        time.sleep(length)
                        
                        mic_control.unmute_microphone()

                        print("Getting out from listening function...")
                        

                            
                except sr.UnknownValueError:
                    
                    print("Speech Recognition could not understand audio")
                    

                except sr.RequestError as e:
                
                    print(f"Could not request {e}")
                
        

        elif serial_comm.sensorData()==1:

            count = 0
            
            print(f"Inside Passive statement")
            
        
       



@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('start_listening')
def start_listening(data):
    
    
    recognition_thread = threading.Thread(target=recognize_and_emit)
    recognition_thread.start()

   
    #recognition_thread.join()  # Wait for the recognition thread to finish

   

if __name__ == '__main__':
    socketio.run(app, debug=False)
