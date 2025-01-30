import sys
import os
import RPi.GPIO as GPIO
from time import sleep
from s_slownik_komend import Dictionary
# do czytania tekstu przez syntezator
import pyttsx3 as tts


# Steruje radarem pokazującym kierunek dotarcia komendy na 8 diodach
class Radar:
        
    def __init__(self, angle=0):
        # słownik komend
        self.dic = Dictionary()
        self.angle = angle
        # numerowanie pinów BCM
        GPIO.setmode(GPIO.BCM)
        # nie zawsze używamy GPIO.cleanup(), więc będzie krzyczeć
        GPIO.setwarnings(False)
        # piny zasilania demultipleksera jako wyjście
        GPIO.setup(26, GPIO.OUT)              
        GPIO.setup(5, GPIO.OUT)
        # piny sterowania demultipleksera jako wyjście
        GPIO.setup(6, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        GPIO.setup(19, GPIO.OUT)
        # sprawdź statu radaru
        try:
            with open('zmienne/z_radar_switch.txt', 'r') as f:
                self.switch = f.read().strip()
        except:
            self.switch = self.dic.off[0]
            

    # wysyła napięcia na piny
    def radar_led(self, C, B, A):
        GPIO.output(6, C)
        GPIO.output(13, B)
        GPIO.output(19, A)
    

    # Ustala jakie diody zapalić w zależności od azymutu
    # wsyła zadanie zmiany stanu odpowiednim kodem binarnym
    def radar_update(self):
        angle = self.angle
        if self.switch in self.dic.on:
            if 0 <= angle < 23 or angle >= 338:
                self.radar_led(1, 1, 1)
            elif 23 <= angle < 68:
                self.radar_led(1, 1, 0)
            elif 68 <= angle < 113:
                self.radar_led(1, 0, 1)
            elif 113 <= angle < 158:
                self.radar_led(1, 0, 0)
            elif 158 <= angle < 203:
                self.radar_led(0, 1, 1)
            elif 203 <= angle < 248:
                self.radar_led(0, 1, 0)
            elif 248 <= angle < 293:
                self.radar_led(0, 0, 1)
            else:
                self.radar_led(0, 0, 0)
    
    
# klada zarządzająca przetwarzaniem komend
class Control:
    def __init__(self, angle=0, elevation=0):
        self.angle = angle
        self.elevation = elevation
        # słownik komend
        self.dic = Dictionary()
        # wczytaj ścieżkę programu
        try:
            with open('zmienne/z_sciezka.txt', 'r') as f:
                self.systemPath = f.read().strip()
        except:
            self.systemPath = self.dic.main[0] + '>'

        # numerowanie pinów BCM
        GPIO.setmode(GPIO.BCM)
        # nie zawsze używamy GPIO.cleanup(), więc będzie krzyczeć
        GPIO.setwarnings(False)
        # piny kolorowych led jako wyjście
        GPIO.setup(22, GPIO.OUT)
        GPIO.setup(27, GPIO.OUT)
        GPIO.setup(17, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(4, GPIO.OUT)

        # interfejs radaru
        self.radar = Radar(angle)

        # aktualny (poprzedni) stan na diodach LED
        self.led1 = 0
        self.led2 = 0
        self.led3 = 0
        self.led4 = 0
        self.led5 = 0
        with open('zmienne/z_stan_led.txt', 'r') as f:
            try:
                states = f.read()
                state_list = states.split()
                self.led1 = int(state_list[0])
                self.led2 = int(state_list[1])
                self.led3 = int(state_list[2])
                self.led4 = int(state_list[3])
                self.led5 = int(state_list[4])
            except:
                pass

        # # do czytania tekstu przez syntezator
        self.engine = tts.init()
        self.engine.setProperty('rate', 150)
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', 'polish')
        

    # zaczyna przetwarzać komendy tekstowe
    def start(self, command):
        raport = self.command_interpret(command)
        self.radar.radar_update()
        
        with open('zmienne/z_sciezka.txt', 'w') as f:
            f.write(self.systemPath)

        return raport


    # wysyła napięcia na piny 5 diod led oraz zapisuje ich stan do pliku
    def update_led(self):
        with open('zmienne/z_stan_led.txt', 'w') as f:
            f.write('{} {} {} {} {}'.format(self.led1, self.led2, self.led3, self.led4, self.led5))
        GPIO.output(22, self.led1)
        GPIO.output(27, self.led2)
        GPIO.output(17, self.led3)
        GPIO.output(18, self.led4)
        GPIO.output(4, self.led5)


    # wywołuje się gdy nie rozpoznano komendy
    def command_failed(self):
        print('<system>Nieprawidłowa komenda')


    # zmienia stan na diodzie num (1-5) na przeciwny
    # num='all' zmienia stan na wszystkich diodach
    def switch_led(self, num):
        if num in self.dic.one:
            self.led1 = (self.led1+1) % 2
        elif num in self.dic.two:
            self.led2 = (self.led2 + 1) % 2
        elif num in self.dic.three:
            self.led3 = (self.led3 + 1) % 2
        elif num in self.dic.four:
            self.led4 = (self.led4 + 1) % 2
        elif num in self.dic.five:
            self.led5 = (self.led5 + 1) % 2
        elif num in self.dic.all:
            self.led1 = (self.led1+1) % 2
            self.led2 = (self.led2 + 1) % 2
            self.led3 = (self.led3 + 1) % 2
            self.led4 = (self.led4 + 1) % 2
            self.led5 = (self.led5 + 1) % 2
        self.update_led()


    # kończy pracę systemu
    def exit_led(self):
        self.systemPath = self.dic.main[0] + '>'
        self.radar.switch = self.dic.off[0]
        GPIO.cleanup()
        return self.dic.exit[0]
        

    # mruga 5 diodami
    def blink(self):
        GPIO.output(22, 0)
        GPIO.output(27, 0)
        GPIO.output(17, 0)
        GPIO.output(18, 0)
        GPIO.output(4, 0)
        sleep(1)
        GPIO.output(22, 1)
        GPIO.output(27, 1)
        GPIO.output(17, 1)
        GPIO.output(18, 1)
        GPIO.output(4, 1)
        sleep(1)
        self.update_led()
    

    # skomplikowana metoda, ale chodzi o to, że wykonuje LISTĘ komend po kolei
    # standardowo zwraca ''
    # jeśli zamyka się system zwraca dic.exit[0] (np. 'exit')
    def command_interpret(self, command):
        #com_array = command.split()
        com_array = command
        dic = self.dic
        for craw in com_array:
            c = craw.lower()
            if c in dic.main:
                self.systemPath = dic.main[0] + '>'
            elif c in dic.back:
                if self.systemPath[0:-1] not in dic.main:
                    while self.systemPath[-1] != '/':
                        self.systemPath = self.systemPath[0:-1]
                    self.systemPath = self.systemPath[0:-1] + '>'
            elif c in dic.radar:
                if self.systemPath[0:-1] in dic.main:
                    self.systemPath = dic.main[0] + '/' + dic.radar[0] + '>'
                else:
                    self.command_failed()
            elif c in dic.led:
                if self.systemPath[0:-1] in dic.main:
                    self.systemPath = dic.main[0] + '/' + dic.led[0] + '>'
                else:
                    self.command_failed()
            elif c in dic.calibration:
                if self.systemPath[0:-1] in dic.main:
                    self.systemPath = dic.main[0] + '/' + dic.calibration[0] + '>'
                else:
                    self.command_failed()
            elif c in dic.on:
                if self.systemPath == dic.main[0] + '/' + dic.radar[0] + '>':
                    #pin zasilania demultipleksera
                    GPIO.output(26, 1)
                    #pin włącznik demultipleksera
                    GPIO.output(5, 1)
                    print('<system>Radar turned on')
                    self.radar.switch = dic.on[0]
                    with open('zmienne/z_radar_switch.txt', 'w') as f:
                        f.write(self.radar.switch)
                else:
                    self.command_failed()
            elif c in dic.off:
                if self.systemPath == dic.main[0] + '/' + dic.radar[0] + '>':
                    #pin zasilania demultipleksera
                    GPIO.output(26, 0)
                    #pin włącznik demultipleksera
                    GPIO.output(5, 0)
                    print('<system>Radar turned off')
                    self.radar.switch = dic.off[0]
                    with open('zmienne/z_radar_switch.txt', 'w') as f:
                        f.write(self.radar.switch)
                else:
                    self.command_failed()
            elif c in dic.reset:
                if self.systemPath == dic.main[0] + '/' + dic.calibration[0] + '>':
                    calibration = 'reset'
                    with open ('zmienne/z_kalibracja.txt', 'w') as f:
                        f.write(calibration)
                    print('<system>Filtracja wyłączona (RESET)')
                else:
                    self.command_failed()
            elif c in dic.tunnel:
                if self.systemPath == dic.main[0] + '/' + dic.calibration[0] + '>':
                    calibration = '{} {}'.format(self.angle, self.elevation)
                    with open ('zmienne/z_kalibracja.txt', 'w') as f:
                        f.write(calibration)
                    print('<system>Filtracja włączona (TUNNEL)')
                else:
                    self.command_failed()
            elif c in (dic.one + dic.two + dic.three + dic.four + dic.five):
                if self.systemPath == dic.main[0] + '/' + dic.led[0] + '>':
                    self.switch_led(c)
                else:
                    self.command_failed()
            elif c in dic.all:
                if self.systemPath == dic.main[0] + '/' + dic.led[0] + '>':
                    self.switch_led(c)
                else:
                    self.command_failed()
            elif c in dic.exit:
                return self.exit_led()
            elif c in dic.blink:
                self.blink()
            elif c in dic.path:
                print(self.systemPath)
                self.mow(self.systemPath)
            elif c in dic.effects:
                if self.systemPath == dic.main[0] + '/' + dic.led[0] + '>':
                    self.systemPath = dic.main[0] + '/' + dic.led[0] + '/' + dic.effects[0] + '>'
                else:
                    self.command_failed()
            elif c in (dic.gleam + dic.queue + dic.droplet + dic.police + dic.null + dic.stop):
                if self.systemPath == dic.main[0] + '/' + dic.led[0] + '/' + dic.effects[0] + '>':
                    #with open ('zmienne/z_efekt.txt', 'w') as f:
                    #    f.write(c)
                    if c not in dic.stop:
                        os.system('echo ' + c + ' > z_efekt.txt')
                else:
                    self.command_failed()
            elif c in dic.ignore:
                pass
            elif c in dic.start:
                if self.systemPath == dic.main[0] + '/' + dic.led[0] + '/' + dic.effects[0] + '>':
                    pass
                    #os.system('python3 s_efekty.py')
                else:
                    self.command_failed()
            else:
                self.command_failed()

        return ''


    def mow(self, text):
        self.engine.say("Dzień Dzień dobry ścieżka to "+text)
        self.engine.runAndWait()
        self.engine.stop()


if __name__ == "__main__":
    # dzięki temu możemy podawać dowolną liczbę argumnetów wywołując skrypt pisemnie z konsoli
    print('DO SKRYPTU {} DOSTAŁO SIĘ {}'.format(sys.argv[0], sys.argv[1:]))
    command = sys.argv[1:]
    c = Control()
    c.start(command)