import speech_recognition as sr
#from scipy.io import wavfile
import sys


class FileRecognizer:
    def __init__(self, filename):
        self.filename = filename
        self.r = sr.Recognizer()
        #self.r.energy_threshold = 100
    

    # Odczytuje plik i podaje komendę do interpretacji
    def start(self, filename=None, angle=0, elevation=0):
        if filename != None:
            self.filename = filename
        # odsłuchaj dane z pliku
        with sr.WavFile(self.filename) as source:
            audio = self.r.record(source)
        try:
            #command = self.r.recognize_google(data, language='en-EN').strip()
            command = self.r.recognize_google(audio, language='pl-PL').strip()
            print('<Rozpoznany tekst>', command)
        except:
            print('<system>Nie rozpoznano tekstu')
            command = ''
        return command.lower()


if __name__ == "__main__":

    if len(sys.argv) == 1:
        filename = 'audio_wyniki/probka1.wav'
    else:
        filename = sys.argv[1]

    fr = FileRecognizer(filename)
    fr.start()
