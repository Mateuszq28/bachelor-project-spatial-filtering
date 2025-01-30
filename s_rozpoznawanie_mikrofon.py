import speech_recognition as sr
import os
import RPi.GPIO as GPIO
from s_slownik_komend import Dictionary
from s_wykonaj_komende import Control


class MicrophoneRec:
    def __init__(self):
        self.dic = Dictionary()
        self.r = sr.Recognizer()
        #self.r.energy_threshold = 100
        self.command = ''

        # numerowanie pinów BCM
        GPIO.setmode(GPIO.BCM)
        # nie zawsze używamy GPIO.cleanup(), więc będzie krzyczeć
        GPIO.setwarnings(False)
        # pin sygnalizujący nasłuchiwanie komend
        GPIO.setup(23, GPIO.OUT)
        # pin sygnalizujący budowanie wektora kierunku
        GPIO.setup(24, GPIO.OUT)
        GPIO.output(24, 0)


    # drukuje na ekran aktualną ścieżkę
    def printPath(self):
        try:
            with open('zmienne/z_sciezka.txt', 'r') as f:
                systemPath = f.read()
        except:
            systemPath = self.dic.main[0] + '>'
        print(systemPath)


    # wysyła komendę do interpretacji (stara metoda)
    def command_interpret(self):
        os.system('python3 {} {}'.format('zmienne/s_wykonaj_komende.py', self.command))
        #execfile('s_wykonaj_komende.py')


    # Nagrywa komendę, zamienia na tekst i podaje do interpretacji
    def listen(self, source):
        #self.r.adjust_for_ambient_noise(source)
        print('<System>Słucham...')
        self.printPath()
        GPIO.output(23, 1)
        data = self.r.listen(source)

        """
        #Powstałby plik z nagranym tylko jednym kanałem
        wave = data.get_wav_data()
        with open("wynik_sluchania.wav", 'w') as f:
            f.write(wave)
        """
        
        GPIO.output(23, 0)
        print('<system>Przetwarzam...')
        try:
            #command = self.r.recognize_google(data, language='en-EN').strip()
            self.command = self.r.recognize_google(data, language='pl-PL').strip()
            print('<Rozpoznany tekst>', self.command)
        except:
            print('<system>Nie rozpoznano tekstu')
            self.command = ''

        c = Control()
        newCom = c.start(list(self.command.split()))
        self.command = newCom
        return newCom


    def loop(self):
        with sr.Microphone(device_index=0) as source:
            while self.command not in self.dic.exit:
                self.listen(source)
        GPIO.cleanup()
        print('<system>papa :)', '\n<system wyłączony>')
        os.system('echo stop > z_efekt.txt')


    def once(self):
        with sr.Microphone(device_index=0) as source:
            self.listen(source)


if __name__ == "__main__":
    mic = MicrophoneRec()
    mic.loop()