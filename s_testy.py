from s_rozpoznaj_z_pliku_windows import FileRecognizer
from s_slownik_komend import Dictionary

nagrania = 1

if nagrania == 0:
    komendy = ['menu_R.wav','radar_R.wav','światło_R.wav','powrót_R.wav','kalibracja_R.wav','efekty_R.wav','oczko_R.wav','wyjście_R.wav','ścieżka_R.wav','włącz_R.wav','wyłącz_R.wav','wszystkie_R.wav','jeden_R.wav','dwa_R.wav','trzy_R.wav','cztery_R.wav','pięć_R.wav','reset_R.wav','tunel_R.wav','migotanie_R.wav','kolejka_R.wav','nic_R.wav','policja_R.wav','stop_R.wav','start_R.wav','kropelka_R.wav','ignoruj_R.wav']
    przedrostek = 'komendy_od_razu_'
elif nagrania == 1:
    komendy = ['menu_R_','radar_R_','światło_R_','powrót_R_','kalibracja_R_','efekty_R_','oczko_R_','wyjście_R_','ścieżka_R_','włącz_R_','wyłącz_R_','wszystkie_R_','jeden_R_','dwa_R_','trzy_R_','cztery_R_','pięć_R_','reset_R_','tunel_R_','migotanie_R_','kolejka_R_','nic_R_','policja_R_','stop_R_','start_R_','kropelka_R_','ignoruj_R_']
    przedrostek = 'komenda_cisza'

if nagrania == 0:

    # badanie na co przetworzono tekst
    fr = FileRecognizer('byleco')
    wyniki = ''
    lista_rozpoznanych = []
    for k in komendy:
        wyraz = fr.start(k)
        wyniki += wyraz +'\n'
        lista_rozpoznanych.append(wyraz)


    with open(przedrostek+'wyniki_rozpoznane_wyrazy.txt', 'w') as f:
        f.write(wyniki)


    # badanie czy słowo mieści się w słowniku
    slownik = Dictionary()
    czy_w_slowniku = ''
    for i in range(0, len(komendy)):
            if lista_rozpoznanych[i] in slownik.tabOfAllCommands[i]:
                czyOK = 'TAK'
            else:
                czyOK = 'NIE'
            czy_w_slowniku += czyOK + '\n'

    with open(przedrostek+'wyniki_czy_w_slowniku.txt', 'w') as f:
        f.write(czy_w_slowniku)

else:
    for filtrationFlag in ['noFilter', 'filteredTime', 'filteredTime1', 'filteredFreq']:

        # badanie na co przetworzono tekst
        fr = FileRecognizer('byleco')
        wyniki = ''
        lista_rozpoznanych = []
        for k in komendy:
            wyraz = fr.start(k+filtrationFlag+'.wav')
            wyniki += wyraz +'\n'
            lista_rozpoznanych.append(wyraz)


        with open('wyniki_rozpoznane_wyrazy_'+przedrostek+'_'+filtrationFlag+'.txt', 'w') as f:
            f.write(wyniki)


        # badanie czy słowo mieści się w słowniku
        slownik = Dictionary()
        czy_w_slowniku = ''
        for i in range(0, len(komendy)):
                if lista_rozpoznanych[i] in slownik.tabOfAllCommands[i]:
                    czyOK = 'TAK'
                else:
                    czyOK = 'NIE'
                czy_w_slowniku += czyOK + '\n'

        with open('wyniki_czy_w_slowniku_'+przedrostek+'_'+filtrationFlag+'.txt', 'w') as f:
            f.write(czy_w_slowniku)