from s_filtracja_przestrzenna import SpaceFiltration
from s_slownik_komend import Dictionary
from s_rozpoznaj_z_pliku import FileRecognizer
import RPi.GPIO as GPIO
import os


class Manager:
    def __init__(self):
        self.mode = None
        self.command = ''
        self.dic = Dictionary()
        self.fr = FileRecognizer('audio_wyniki/noFilter.wav')
        self.tunnel = [0, 0]
        self.spacefilt = SpaceFiltration()

        # numerowanie pinów BCM
        GPIO.setmode(GPIO.BCM)
        # nie zawsze używamy GPIO.cleanup(), więc będzie krzyczeć
        GPIO.setwarnings(False)
        # pin sygnalizujący nasłuchiwanie komend
        GPIO.setup(23, GPIO.OUT)
        # pin sygnalizujący budowanie wektora kierunku
        GPIO.setup(24, GPIO.OUT)


    # sprawdź czy włączyć filtrację
    def checkCalibration(self):
        try:    
            with open('zmienne/z_kalibracja.txt', 'r') as f:
                text = f.read().strip()
        except:
            text = self.dic.reset[0]

        if text in self.dic.reset:
            self.tunnel = [0, 0]
            self.mode = None
        else:
            self.mode = 'time'
            self.tunnel = [int(elem) for elem in text.split()]


    def start(self):
        while self.command not in self.dic.exit:
            self.checkCalibration()
            GPIO.output(23, 1)
            GPIO.output(24, 1)
            angle, elevation, filename = self.spacefilt.recAndFilter(self.mode, self.tunnel[0], self.tunnel[1])
            GPIO.output(23, 0)
            GPIO.output(24, 0)
            self.command = self.fr.start(filename, angle, elevation)
        GPIO.cleanup()
        os.system('echo stop > zmienne/z_efekt.txt')
        print('<system>papa :)', '\n<system wyłączony>')


if __name__ == "__main__":
    man = Manager()
    man.start()