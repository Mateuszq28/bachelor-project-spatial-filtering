import RPi.GPIO as GPIO
from time import sleep
import os
from s_slownik_komend import Dictionary


# Klasa z efektami świetlnymi na 5 kolorowych diodach led
class Effects:
    def __init__(self):
        self.dic = Dictionary()
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

        self.effect = self.dic.null[0]

        self.led = [0, 0, 0, 0, 0]


    # zmienia stan zmiennej ze stanem diody
    # nr - numer diody <1, 5>
    # sw - jeśli 2 to zmienia obecny stan na przeciwny,
    #      w przeciwnym wypadku ustawiony jest stan sw
    def switch_led(self, nr, sw=2):
        if 1 <= nr <= 5:
            if sw != 2:
                self.led[nr-1] = sw
            else:
                self.led[nr-1] = (self.led[nr-1] + 1) % 2


    # wysyła zmianę napięć na diody (na podstawie stanu zapisanego w obiekcie)
    def led_update(self):
        GPIO.output(22, self.led[0])
        GPIO.output(27, self.led[1])
        GPIO.output(17, self.led[2])
        GPIO.output(18, self.led[3])
        GPIO.output(4, self.led[4])


    # pętla wykonująca efekty świetlne
    # rodzaj efektu pobiera z pliku (jeśli istnieje)
    def loop(self):
        while self.effect not in self.dic.stop:
            
            if os.path.isfile('z_efekt.txt'):
                with open('z_efekt.txt', 'r') as f:
                    self.effect = f.read().strip()
                os.remove('z_efekt.txt')
                
            effect = self.effect
            switch_led = self.switch_led
            led_update = self.led_update
            dic = self.dic

            if effect in dic.gleam:
                switch_led(1, 1)
                switch_led(2, 0)
                switch_led(3, 1)
                switch_led(4, 0)
                switch_led(5, 1)
                led_update()
                sleep(0.5)
                switch_led(1, 0)
                switch_led(2, 1)
                switch_led(3, 0)
                switch_led(4, 1)
                switch_led(5, 0)
                led_update()
                sleep(0.5)
                
            if effect in dic.queue:
                for i in range(1,8):
                    for j in range(1,6):
                        switch_led(j, 0)
                    switch_led(i-2, 1)
                    switch_led(i-1, 1)
                    switch_led(i, 1)
                    led_update()
                    sleep(0.25)
                    
            if effect in dic.police:
                switch_led(1, 0)
                switch_led(2, 0)
                switch_led(3, 1)
                switch_led(4, 0)
                switch_led(5, 0)
                led_update()
                sleep(0.05)
                switch_led(3, 0)
                led_update()
                sleep(0.05)
                switch_led(3, 1)
                led_update()
                sleep(0.1)
                switch_led(3, 0)
                switch_led(4, 1)
                led_update()
                sleep(0.05)
                switch_led(4, 0)
                led_update()
                sleep(0.05)
                switch_led(4, 1)
                led_update()
                sleep(0.1)
                    
            if effect in dic.droplet:
                time = 0.5
                switch_led(1, 0)
                switch_led(2, 0)
                switch_led(3, 0)
                switch_led(4, 0)
                switch_led(5, 0)
                led_update()
                sleep(2*time)
                switch_led(1, 0)
                switch_led(2, 0)
                switch_led(3, 1)
                switch_led(4, 0)
                switch_led(5, 0)
                led_update()
                sleep(time)
                switch_led(1, 0)
                switch_led(2, 1)
                switch_led(3, 1)
                switch_led(4, 1)
                switch_led(5, 0)
                led_update()
                sleep(time)
                switch_led(1, 1)
                switch_led(2, 1)
                switch_led(3, 1)
                switch_led(4, 1)
                switch_led(5, 1)
                led_update()
                sleep(time)
                switch_led(1, 1)
                switch_led(2, 1)
                switch_led(3, 0)
                switch_led(4, 1)
                switch_led(5, 1)
                led_update()
                sleep(time)
                switch_led(1, 1)
                switch_led(2, 0)
                switch_led(3, 0)
                switch_led(4, 0)
                switch_led(5, 1)
                led_update()
                sleep(time)


if __name__ == "__main__":
    ef = Effects()
    ef.loop()