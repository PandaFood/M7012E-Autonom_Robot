#Requires the modules SpeechRecognition and pyaudio
import speech_recognition as sr
import sys
sys.path.insert(1, "..")
from camera.camera import Camera
from widefind.widefindScript import WidefindTracker

def recognizeSpeech(recognizer, microphone):
    #Check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("'recognizer' must be 'Recognizer' instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("'microphone' must be 'Microphone' instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    response = {
        "success": True, #Boolean for success true/false
        "error": None, #None if no errors, otherwise returns error message from speech recognition API
        "transcription": None #None if speech recognition failed, otherwise returns a transcription of input speech
    }

    try:
        print("Analysing voice sample...")
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        response["error"] = "Unable to recognize speech"

    return response

def recordAudio(recognizer, microphone):
    print("\nListening for input, say something!")

    audio = recognizeSpeech(recognizer, microphone)

    success = audio["success"]
    error = audio["error"]
    transcription = audio["transcription"]

    print("Success: " + str(success))
    print("Error: " + str(error))
    print("Transcription: " + str(transcription))

    handleTranscription(transcription)

    #Start listening for additional commands
    recordAudio(recognizer, microphone)

#Handle transcriptions here
def handleTranscription(transcription):
    if(not transcription):
        return
    
    if("help" in transcription):
        print("Helping")
        sensor.help()

    if ("follow" in transcription):
        print("Follow command recognized!")
        print("Following")
        sensor.follow()

    if ("stop" in transcription):
        print("Stop command recognized!")
        sensor.stop()

    #Two examples of easily recognizing transcript commands

    #This will trigger if the transcription contains the letters "example" in order, anywhere in the string
    #This is useful as if your speech is interpreted as "examples" it will trigger "example"
    #Might lead to unintended commands as some words can contain other words
    if ("example" in transcription):
        print("example command recognized! (partial match)")
        #Call function

    #This will only trigger if the transcription is exactly "example"
    #Might lead to problems if a string contains more words than just the command word(s) and if "example" is interpreted as "examples"
    if (transcription == "example"):
        print("example command recognized! (exact match)")
        #Call function
    


if __name__ == "__main__":
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    c = Camera()
    sensor = WidefindTracker()
    sensor.start()

    recordAudio(recognizer, microphone)
