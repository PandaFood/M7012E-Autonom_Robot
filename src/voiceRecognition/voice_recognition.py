#Requires the modules SpeechRecognition and pyaudio
import speech_recognition as sr

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
    if (transcription == "camera follow me"):
        print("Command 'camera follow me' recognized!")
        #Do something

if __name__ == "__main__":
    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    recordAudio(recognizer, microphone)
