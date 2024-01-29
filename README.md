
CONVO Application

CONVO is an application that takes audio input, processes it, and generates a video output. It utilizes Flask, Flask-SocketIO, ImageIO, SpeechRecognition, and PyAudio libraries in Python.

Installation
Prerequisites
Before you begin, ensure you have Python and pip installed on your machine.

Install Required Libraries


pip install Flask

pip install imageio[ffmpeg]

pip install Flask-SocketIO

pip install SpeechRecognition

pip install imageio

pip install PyAudio

pip install pyserial

pip install firebase-admin



Note: If pyauido installation gives error on ubuntu then follow these steps:

1. First write this command in terminal

sudo apt-get install portaudio19-dev

2. then

pip install PyAudio


Note: If imageio installation gives error on ubuntu then follow these steps:

1. First write this command in terminal

sudo apt-get install libjpeg-dev

2. then

pip install imageio


If sensor integration throws error on ubuntu 22, type following commands:

sudo apt update

sudo apt remove brltty


And check for serial port:

ls /dev/ttyUSB*

This will install the necessary dependencies for the CONVO application.


Updated fuzzywuzzy need to install python library 
- pip install fuzzywuzzy 

Getting Started
Follow these steps to get the CONVO application up and running:

Once cloned the repo, just navigate to repo and give command:

python3 app.py


