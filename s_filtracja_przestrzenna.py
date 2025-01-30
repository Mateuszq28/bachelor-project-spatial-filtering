from s_tools import TextFiles
from s_tools import Recorder
from s_tools import MatlabMatrix as mm
import numpy as np
import math


# klasa odpowiadająca za korekcję fazy i amplitudy sygnałów
class CorrectionFilters:
    def __init__(self):
        ts = TextFiles()
        # IMPORTUJ FILTRY KOREKCYJNE
            # do korekcji fazy
        self.c_xp = ts.filterStringToint(ts.readAll('filtry_korekcyjne/corr_filter_X_p_mls.txt'))
        self.c_xu = ts.filterStringToint(ts.readAll('filtry_korekcyjne/corr_filter_X_u_mls.txt'))
        self.c_yp = ts.filterStringToint(ts.readAll('filtry_korekcyjne/corr_filter_Y_p_mls.txt'))
        self.c_yu = ts.filterStringToint(ts.readAll('filtry_korekcyjne/corr_filter_Y_u_mls.txt'))
        self.c_zp = ts.filterStringToint(ts.readAll('filtry_korekcyjne/corr_filter_Z_p_mls.txt'))
        self.c_zu = ts.filterStringToint(ts.readAll('filtry_korekcyjne/corr_filter_Z_u_mls.txt'))
            # do korekcji amplitudy
        self.c_p1 = ts.filterStringToint(ts.readAll('filtry_korekcyjne/corr_filter_p1_f_100_10k_mls.txt'))
        self.c_p2 = ts.filterStringToint(ts.readAll('filtry_korekcyjne/corr_filter_p2_f_100_10k_mls.txt'))
        self.c_p3 = ts.filterStringToint(ts.readAll('filtry_korekcyjne/corr_filter_p3_f_100_10k_mls.txt'))
        self.c_p4 = ts.filterStringToint(ts.readAll('filtry_korekcyjne/corr_filter_p4_f_100_10k_mls.txt'))
        self.c_p5 = ts.filterStringToint(ts.readAll('filtry_korekcyjne/corr_filter_p5_f_100_10k_mls.txt'))
        self.c_p6 = ts.filterStringToint(ts.readAll('filtry_korekcyjne/corr_filter_p6_f_100_10k_mls.txt'))


    # pobiera tablicę 6 kanałów i zwraca je po korekcji amplitudy
    def correctAmplitude(self, signal):
        #SPLOTY Z FILTRAMI AMPLITUDY
        smic0x = np.convolve(signal[0], self.c_p1)
        smic1x = np.convolve(signal[1], self.c_p2)

        smic0y = np.convolve(signal[2], self.c_p3)
        smic1y = np.convolve(signal[3], self.c_p4)

        smic0z = np.convolve(signal[4], self.c_p5)
        smic1z = np.convolve(signal[5], self.c_p6)

        return smic0x, smic1x, smic0y, smic1y, smic0z, smic1z


    # pobiera tablicę 6 kanałów i zwraca je po korekcji fazy
    def correctPhase(self, signal):
        # KOREKCJA FAZY
            # najpierw zamiana z typu MatlabMatrix na list
        c_apx = np.convolve(signal[0], self.c_xp)
        c_aux = np.convolve(signal[1], self.c_xu)

        c_apy = np.convolve(signal[2], self.c_yp)
        c_auy = np.convolve(signal[3], self.c_yu)

        c_apz = np.convolve(signal[4], self.c_zp)
        c_auz = np.convolve(signal[5], self.c_zu)

        return c_apx, c_aux, c_apy, c_auy, c_apz, c_auz


class Test:
    def __init__(self, switch='off'):
        self.switch = switch

    def writeListToFile(self, array, filename):
        if self.switch == 'on':
            new = [str(i) for i in array]
            with open(filename, 'w') as f:
                f.write('\n'.join(new))


# Klasa odpowiedzialna za filtrację przestrzenną
# dodatkowo:
# -zarządza nagrywaniem sygnałów (s_tools.py)
# -zarządza korekcją
class SpaceFiltration:
    def __init__(self):
        pass


# Kanały pobierane z czujnika za pomocą MiniDSP USBStreamer Kit
# I2S0
# kana?y 
# 1 -> Mic X2 azymut 180
# 2 -> Mic X1 azymut 0
# 
# I2S1
# 3 -> Mic Y2 azymut 270
# 4 -> Mic Y1 azymut 90
# 
# I2S2
# 5 -> Mic Z1 elewacja 90
# 6 -> Mic Z2 elewacja -90


    # Zapisuje sygnały do pliku stereo
        # 1 KANAŁ = apa = średnia z 6 kanałów (CIŚNIENIE AKUSTYCZNE)
        # 2 KANAŁ = sygnał różnicowy dla każdej z osi (PRĘDKOŚCI CZĄSTECZEK)
    def writeTestStereo(self, apx, aux, apy, auy, apz, auz, filename = "_"):
        recorder = Recorder()
        new = []
        new.append(apx)
        new.append(aux)
        recorder.floatToWave(new, filename + "x.wav", 2)
        new[0] = apy
        new[1] = auy
        recorder.floatToWave(new, filename + "y.wav", 2)
        new[0] = apz
        new[1] = auz
        recorder.floatToWave(new, filename + "z.wav", 2)


    # Zapisuje sygnały do pliku 6 kanałowego
        # 1 KANAŁ = apa = średnia z 6 kanałów (CIŚNIENIE AKUSTYCZNE)
        # pozostałe kanały - prędkości cząsteczek - sygnały różnicowe
    def writeTestALL(self, apx, aux, auy, auz, filename = "audio_wyniki/apk_ALL.wav"):
        recorder = Recorder()
        new = []
        new.append(apx)
        new.append(aux)
        new.append(auy)
        new.append(auz)
        recorder.floatToWave(new, filename, 4)


    # Zamienia współrzędne kartezjańskie na sferyczne
    def cartesianToSpherical(self, x, y, z):
        xy = (x*x + y*y)**0.5
        radius = (x*x + y*y + z*z)**0.5

        if x > 0:
            angle = math.atan(y/x)*180/math.pi
        elif y > 0:
            angle = 180 + math.atan(y/x)*180/math.pi
        else:
            angle = -180 + math.atan(y/x)*180/math.pi
        
        elevation = math.atan(z/xy)*180/math.pi
        
        # zamiana zakres azymutu na <0;360)
        if angle < 0:
            angle = 360 + angle

        return angle, elevation, radius


    # Oblicza średnią z tablicy
    def mean(self, tab):
        return sum(tab)/len(tab)


    # Uśrednia obliczone kąty
    # Średnia dynamiczna - liczona średnia dla przedziału mean/2 próbek wstecz i mean/2-1 do przodu
    def dynamicAverage(self, ix_f, iy_f, iz_f, angle_f, elevation_f, radius_f, mean=None):
        length = len(ix_f)
        half_frame = int(mean/2)
        # pojemniki do obliczeń
        ix = []
        iy = []
        iz = []
        ang = []
        elev = []
        rad = []
        # wypełnienie początku list - wartości brzegowe
        for i in range(0, half_frame):
            ix.append(ix_f[i])
            iy.append(iy_f[i])
            iz.append(iz_f[i])
            ang.append(angle_f[i])
            elev.append(elevation_f[i])
            rad.append(radius_f[i])
        # obliczanie średniej ruchomej dla wartości w środku tablicy
        for i in range(half_frame, length-half_frame):
            ix.append(self.mean(ix_f[i-half_frame:i+half_frame]))
            iy.append(self.mean(iy_f[i-half_frame:i+half_frame]))
            iz.append(self.mean(iz_f[i-half_frame:i+half_frame]))
            a, e, r = self.cartesianToSpherical(ix[i], iy[i], iz[i])
            ang.append(a)
            elev.append(e)
            rad.append(r)
        # wypełnienie końca listy - wartości brzegowe
        for i in range(length-half_frame, length):
            ix.append(ix_f[i])
            iy.append(iy_f[i])
            iz.append(iz_f[i])
            ang.append(angle_f[i])
            elev.append(elevation_f[i])
            rad.append(radius_f[i])
        return ix, iy, iz, ang, elev, rad


    # Oblicza kierunek podanego sygnału rozbitego na apa, aux, auy, auz
    # p - ciśnienie akustyczne, u - prędkości cząsteczek w danej osi
    # Obliczenia uśredniane dla całej ramki o długości frame_size
    # dla framesize=1 obliczenia dla każdej próbki z osobna
    # mean daje możliwośc dodatkowego wyrównania wyników pomiędzy ramkami
    # Wielkość okna uśredniania sterowana parametrem mean
    # dla mean=None uśrednianie wyłączone
    def directionTime(self, apa, aux, auy, auz, frame_size, mean=20):
        n_samples = len(apa)
        
        # pojemniki kątów dla całego sygnału
        ix = []
        iy = []
        iz = []
        angle = []
        elevation = []
        radius = []

        # pojemniki dla pojedynczych ramek
        ix_f = []
        iy_f = []
        iz_f = []
        angle_f = []
        elevation_f = []
        radius_f = []

        # wypełnienie pojemników dla ramek
        frame_n_counter = 0
        frame_counter = 0
        ix_f.append(0)
        iy_f.append(0)
        iz_f.append(0)
        for n in range(0, n_samples):
            
            ix_f[frame_counter] += apa[n] * aux[n]
            iy_f[frame_counter] += apa[n] * auy[n]
            iz_f[frame_counter] += apa[n] * auz[n]

            frame_n_counter += 1
            if frame_n_counter >= frame_size:
                angl, elev, ra = self.cartesianToSpherical(ix_f[frame_counter], iy_f[frame_counter], iz_f[frame_counter])
                angle_f.append(angl)
                elevation_f.append(elev)
                radius_f.append(ra)
                if n < n_samples-1:
                    frame_n_counter = 0
                    frame_counter += 1
                    ix_f.append(0)
                    iy_f.append(0)
                    iz_f.append(0)

            if n == n_samples-1:
                angl, elev, ra = self.cartesianToSpherical(ix_f[frame_counter], iy_f[frame_counter], iz_f[frame_counter])
                angle_f.append(angl)
                elevation_f.append(elev)
                radius_f.append(ra)

        # obliczanie średniej dynamicznej - 'mean' próbek w tył i 'mean-1' w przód - wygładza wykres obliczonego kąta od czasu
        if mean != None:
            ix_f, iy_f, iz_f, angle_f, elevation_f, radius_f = self.dynamicAverage(ix_f, iy_f, iz_f, angle_f, elevation_f, radius_f, mean) 

        # wypełnienie pojemników dla każdej próbki
        frame_counter = 0
        for n in range(0, n_samples):
            ix.append(ix_f[frame_counter])
            iy.append(iy_f[frame_counter])
            iz.append(iz_f[frame_counter])
            angle.append(angle_f[frame_counter])
            elevation.append(elevation_f[frame_counter])
            radius.append(radius_f[frame_counter])
            if n % frame_size == frame_size-1:
                frame_counter += 1

        # Jeśli testy są aktywowane (w klasie Test), poniższe linijki zapiszą obliczone tablice do plików
        # dzięki temu można np wykreślić wykresy, dokonać analizy
        test = Test()
        test.writeListToFile(ix, 'audio_wyniki/frame' + str(frame_size) + '_mean' + str(mean) + '_ix.txt')
        test.writeListToFile(iy, 'audio_wyniki/frame' + str(frame_size) + '_mean' + str(mean) + '_iy.txt')
        test.writeListToFile(iz, 'audio_wyniki/frame' + str(frame_size) + '_mean' + str(mean) + '_iz.txt')
        test.writeListToFile(angle, 'audio_wyniki/frame' + str(frame_size) + '_mean' + str(mean) + '_angle.txt')
        test.writeListToFile(elevation, 'audio_wyniki/frame' + str(frame_size) + '_mean' + str(mean) + '_elevation.txt')
        test.writeListToFile(radius, 'audio_wyniki/frame' + str(frame_size) + '_mean' + str(mean) + '_radius.txt')
        return ix, iy, iz, angle, elevation, radius

 
    # Sprawdza czy kąt (angle) i elewacja (elevation) mieszczą się w zakresie bez filtracji (filt_ang, filtr_elev)
    # margin - margines
    def isInRange(self, angle, elevation, filt_ang, filt_elev, margin):
        # warunek kątu
        if filt_ang - margin < 0:
            if not (angle > filt_ang - margin + 360 or angle < filt_ang + margin):
                return False

        if filt_ang + margin > 360:
            if not (angle > filt_ang - margin or angle < filt_ang + margin - 360):
                return False

        if filt_ang - margin > 0 and filt_ang + margin < 360:
            if not (angle > filt_ang - margin and angle < filt_ang + margin):
                return False

        # warunek elewacji
        if elevation < filt_elev - margin or elevation > filt_elev + margin:
            return False
        
        return True


    # Filtruje sygnał w dziedzinie czasu
    # apa - uśrednione ciśnienie z 6 kanałów
    # aux, auy, auz - prędkości cząsteczek dla każdej z osi
    # frame_size - wielkość ramki filtracji
    # filt_ang - azymut, który NIE ma ulec filtracji
    # filt_elev - kąt elewacji, który NIE ma ulec filtracji
    # margin - margines tolerancji
    # mean - średnia dynamiczna, None - brak, int - szerokość okna uśredniania
    def spatialFiltrationTime(self, apa, aux, auy, auz, frame_size=1024, filt_ang=0, filt_elev=0, margin=30, mean=None):
        n_samples = len(apa)
        ix, iy, iz, angle, elevation, radius = self.directionTime(apa, aux, auy, auz, frame_size, mean)
        new = []
        for i in range(0, n_samples):
            if not self.isInRange(angle[i], elevation[i], filt_ang, filt_elev, margin):
                new.append(np.float64(0))
            else:
                new.append(apa[i])
        return new

    
    # Filtruje sygnał w dziedzinie częstotliwości
    # apa - uśrednione ciśnienie z 6 kanałów
    # aux, auy, auz - prędkości cząsteczek dla każdej z osi
    # fft_size - wielkość ramki filtracji (i tym samym okna FFT)
    # filt_ang - azymut, który NIE ma ulec filtracji
    # filt_elev - kąt elewacji, który NIE ma ulec filtracji
    # margin - margines tolerancji
    # windowStart - czy sygnał ma być mnożony przez okno Hanna przed FFT (True/False) - ZALECANE FALSE
    # windowEnd - czy sygnał ma być mnożony przez odrwócone okno Hanna po FFT (True/False) - ZALECANE FALSE
    def spatialFiltrationFreq(self, apa, aux, auy, auz, fft_size=2048, filt_ang=0, filt_elev=0, margin=30, windowStart=False, windowEnd=False):
        n_frames = int(len(apa)/fft_size)
        filtered = []
        for i in range(0, n_frames):
            # numer pierwszej próbki w oknie
            first_n = i*fft_size
            
            if windowStart == True:
                # okno Hanna
                window = np.array(np.hanning(fft_size))
            else:
                window = 1

            # obliczanie zespolonego fft
            fft_frame_x = np.fft.fft(window * np.array(aux[first_n:first_n+fft_size]))
            fft_frame_y = np.fft.fft(window * np.array(auy[first_n:first_n+fft_size]))
            fft_frame_z = np.fft.fft(window * np.array(auz[first_n:first_n+fft_size]))
            fft_frame_p = np.fft.fft(window * np.array(apa[first_n:first_n+fft_size]))

            # bufor do zapisu przefiltrowanych próbek
            frameBUF = fft_frame_p

            for j in range(0, fft_size):
                # oblicz natężenie
                ix = np.real(fft_frame_p[j] * np.conjugate(fft_frame_x[j]))
                iy = np.real(fft_frame_p[j] * np.conjugate(fft_frame_y[j]))
                iz = np.real(fft_frame_p[j] * np.conjugate(fft_frame_z[j]))
                # oblicz kierunek
                angle, elevation, radius = self.cartesianToSpherical(ix, iy, iz)
                # zeruj prążki poza tunelem
                if not self.isInRange(angle, elevation, filt_ang, filt_elev, margin):
                    frameBUF[j] = 0

            # Modyfikacja okna, aby uniknąć dzielenia przez 0
            if windowEnd == True:
                window = np.array(np.hanning(fft_size))
                window[0] = window[1]
                window[-1] = window[-2]
                filtered += list(np.real(np.fft.ifft(frameBUF)) / window)
            else:
                filtered += list(np.real(np.fft.ifft(frameBUF)))
                #filtered = list(np.array(filtered) / (2**2))
        return filtered


    # WERCJA ZAPISUJĄCA DO PLIKÓW WSZYSTKIE PRZEKSZTAŁCENIA PO KOLEI (KONTROLNIE)
    # 1. Nagrywa sygnał
    # 2. Dokonuje korekcji fazy i amplitudy
    # 3. Dokonuje filtracji
    def recAndFilterWriteAll(self):
        recorder = Recorder(seconds = 4)
        corector = CorrectionFilters()

        # lista listy intów - 6 kanałów (index 0-5)
        #TEST
        amp4chx = recorder.recAndWriteToFloat()

        #TEST
        recorder.floatToWave(array=amp4chx, filename="audio_wyniki/bk_6k.wav", channels=6)
        recorder.floatToWave(array=amp4chx, filename="audio_wyniki/bk_6k1ch.wav", channels=1)

        # korekcja amplitudy
        smic0x, smic1x, smic0y, smic1y, smic0z, smic1z = corector.correctAmplitude(amp4chx)
        # Zamiana na tp MatlabMatrix - umożliwienie operacji macierzowych z matlaba - mm()
        # Średnia amplituda po pierwszej korekcji
        apa = (mm(smic1x) + mm(smic0x) + mm(smic1y) + mm(smic0y) + mm(smic1z) + mm(smic0z))/6

        # OBLICZANIE SYGNAŁÓW RÓŻNICOWYCH
            # prędkość cząsteczek w danej osi - aux, auy, auz
            # ciśnienie akustyczne uśrednione dla wszystkich - apa, apx, apy, apz
        # oś x
        apx = apa
        aux = (mm(smic1x) - mm(smic0x))
        # oś y
        apy = apa
        auy = (mm(smic1y) - mm(smic0y))
        # oś z
        apz = apa
        auz = (mm(smic1z) - mm(smic0z))
  
        #TEST
        # ZAPIS SYGNAŁÓW PO 1 KOREKCJI (AMPLITUDY) DO PLIKÓW STEREOFONICZNYCH (2 KANAŁY)
        self.writeTestStereo(apx, aux, apy, auy, apz, auz, "audio_wyniki/ak_")

        # korekcja fazy
        c_apx, c_aux, c_apy, c_auy, c_apz, c_auz = corector.correctPhase([apx.unwrap(), aux.unwrap(), apy.unwrap(), auy.unwrap(), apz.unwrap(), auz.unwrap()])
        c_apa = c_apx

        #TEST
        # ZAPIS PLIKOW PO KOREKCJI FAZY I AMPLITUDY
        self.writeTestStereo(c_apx, c_aux, c_apy, c_auy, c_apz, c_auz, "audio_wyniki/apk_")

        #TEST
        # Zapis sygnału zbiorowego
        self.writeTestALL(c_apa, c_aux, c_auy, c_auz)

        filteredTime1 = self.spatialFiltrationTime(c_apa, c_aux, c_auy, c_auz, frame_size=1, filt_ang=90, filt_elev=0, margin=30, mean=None)
        # TEST
        recorder.floatToWave(array=[filteredTime1], filename="audio_wyniki/filteredTime1.wav", channels=1)

        filteredTime2 = self.spatialFiltrationTime(c_apa, c_aux, c_auy, c_auz, frame_size=1024, filt_ang=90, filt_elev=0, margin=30, mean=None)
        # TEST
        recorder.floatToWave(array=[filteredTime2], filename="audio_wyniki/filteredTime1024.wav", channels=1)

        filteredTime3 = self.spatialFiltrationTime(c_apa, c_aux, c_auy, c_auz, frame_size=1, filt_ang=90, filt_elev=0, margin=30, mean=20)
        # TEST
        recorder.floatToWave(array=[filteredTime3], filename="audio_wyniki/filteredTime1mean20.wav", channels=1)

        filteredTime4 = self.spatialFiltrationTime(c_apa, c_aux, c_auy, c_auz, frame_size=1024, filt_ang=90, filt_elev=0, margin=30, mean=20)
        # TEST
        recorder.floatToWave(array=[filteredTime4], filename="audio_wyniki/filteredTime1024mean20.wav", channels=1)

        filteredFreq = self.spatialFiltrationFreq(c_apa, c_aux, c_auy, c_auz, fft_size=2048, filt_ang=90, filt_elev=0, margin=30, windowStart=False, windowEnd=False)
        # TEST
        recorder.floatToWave(array=[filteredFreq], filename="audio_wyniki/filteredFreq.wav", channels=1)

        # OBliczony kąt z całego sygnału
        ix, iy, iz, a, e, r = self.directionTime(c_apa, c_aux, c_auy, c_auz, frame_size=len(c_apa), mean=None)
        test = Test()
        test.writeListToFile([ix[0], iy[0], iz[0], a[0], e[0], r[0]], 'audio_wyniki/allSig.txt')
       

    # WERCJA ZAPISUJĄCA DO PLIKU TYLKO OSTATECZNY WYNIK FILTRACJI
    # 1. Nagrywa sygnał
    # 2. Dokonuje korekcji fazy i amplitudy
    # 3. Dokonuje filtracji (mode: None - brak filtracji, 'time' - filtracja w dziedzinie czasu, 'freq' - filtracja w dziedzinie częstotliwości)
    # angle_tun, elevation_tun - kąty azymut i elewacji, które nie mają zostą wyfiltrowane (tunelujemy dźwięk z tego kierunku)
    def recAndFilter(self, mode=None, angle_tun=0, elevation_tun=0, filename_prefix=''):
        recorder = Recorder(seconds = 4)
        corector = CorrectionFilters()

        # lista listy intów - 6 kanałów (index 0-5)
        amp4chx = recorder.recToFloat()
        # korekcja amplitudy
        smic0x, smic1x, smic0y, smic1y, smic0z, smic1z = corector.correctAmplitude(amp4chx)
        # Zamiana na tp MatlabMatrix - umożliwienie operacji macierzowych z matlaba - mm()
        # Średnia amplituda po pierwszej korekcji
        apa = (np.array(smic1x) + np.array(smic0x) + np.array(smic1y) + np.array(smic0y) + np.array(smic1z) + np.array(smic0z))/6

        # OBLICZANIE SYGNAŁÓW RÓŻNICOWYCH
            # prędkość cząsteczek w danej osi - aux, auy, auz
            # ciśnienie akustyczne uśrednione dla wszystkich - apa, apx, apy, apz
        # oś x
        apx = apa
        aux = (np.array(smic1x) - np.array(smic0x))
        # oś y
        apy = apa
        auy = (np.array(smic1y) - np.array(smic0y))
        # oś z
        apz = apa
        auz = (np.array(smic1z) - np.array(smic0z))

        # korekcja fazy
        c_apx, c_aux, c_apy, c_auy, c_apz, c_auz = corector.correctPhase([apx, aux, apy, auy, apz, auz])
        c_apa = c_apx

        filename = None

        if mode == "time" or mode == 'all':
            filename = "audio_wyniki/"+filename_prefix+"filteredTime.wav"
            filteredTime = self.spatialFiltrationTime(c_apa, c_aux, c_auy, c_auz, frame_size=1024, filt_ang=angle_tun, filt_elev=elevation_tun, margin=30, mean=20)
            recorder.floatToWave([filteredTime], filename, 1)

        if mode == "time1" or mode == 'all':
            filename = "audio_wyniki/"+filename_prefix+"filteredTime1.wav"
            filteredTime = self.spatialFiltrationTime(c_apa, c_aux, c_auy, c_auz, frame_size=1, filt_ang=angle_tun, filt_elev=elevation_tun, margin=30, mean=20)
            recorder.floatToWave([filteredTime], filename, 1)

        if mode == "freq" or mode == 'all':
            filename = "audio_wyniki/"+filename_prefix+"filteredFreq.wav"
            filteredFreq = self.spatialFiltrationFreq(c_apa, c_aux, c_auy, c_auz, fft_size=2048, filt_ang=angle_tun, filt_elev=elevation_tun, margin=30, windowStart=False, windowEnd=False)
            recorder.floatToWave([filteredFreq], filename, 1)

        if mode == None or mode == 'all':
            filename = "audio_wyniki/"+filename_prefix+"noFilter.wav"
            recorder.floatToWave(array=amp4chx, filename=filename, channels=1)

        ix, iy, iz, a, e, r = self.directionTime(c_apa, c_aux, c_auy, c_auz, frame_size=len(c_apa), mean=None)
        return a[0], e[0], filename


    # WERCJA ZAPISUJĄCA DO PLIKU TYLKO OSTATECZNY WYNIK FILTRACJI (oraz nie nagrywa, tylko pobiera z pliku)
    # 1. Pobiera nagranie z pliku
    # 2. Dokonuje korekcji fazy i amplitudy
    # 3. Dokonuje filtracji (mode: None - brak filtracji, 'time' - filtracja w dziedzinie czasu, 'freq' - filtracja w dziedzinie częstotliwości)
    # angle_tun, elevation_tun - kąty azymut i elewacji, które nie mają zostą wyfiltrowane (tunelujemy dźwięk z tego kierunku)
    def getAndFilter(self, mode=None, angle_tun=0, elevation_tun=0, filename_prefix='', filename_open="audio_wyniki/output_pyaudio_meth2.wav"):
        recorder = Recorder(seconds = 4)
        corector = CorrectionFilters()

        # lista listy intów - 6 kanałów (index 0-5)
        amp4chx = recorder.waveToFloat(filename=filename_open, channels=6, byte=4)
    
        # korekcja amplitudy
        smic0x, smic1x, smic0y, smic1y, smic0z, smic1z = corector.correctAmplitude(amp4chx)
        # Zamiana na tp MatlabMatrix - umożliwienie operacji macierzowych z matlaba - mm()
        # Średnia amplituda po pierwszej korekcji
        apa = (np.array(smic1x) + np.array(smic0x) + np.array(smic1y) + np.array(smic0y) + np.array(smic1z) + np.array(smic0z))/6

        # OBLICZANIE SYGNAŁÓW RÓŻNICOWYCH
            # prędkość cząsteczek w danej osi - aux, auy, auz
            # ciśnienie akustyczne uśrednione dla wszystkich - apa, apx, apy, apz
        # oś x
        apx = apa
        aux = (np.array(smic1x) - np.array(smic0x))
        # oś y
        apy = apa
        auy = (np.array(smic1y) - np.array(smic0y))
        # oś z
        apz = apa
        auz = (np.array(smic1z) - np.array(smic0z))

        # korekcja fazy
        c_apx, c_aux, c_apy, c_auy, c_apz, c_auz = corector.correctPhase([apx, aux, apy, auy, apz, auz])
        c_apa = c_apx

        filename = None

        if mode == "time" or mode == 'all':
            filename = "audio_wyniki/"+filename_prefix+"filteredTime.wav"
            filteredTime = self.spatialFiltrationTime(c_apa, c_aux, c_auy, c_auz, frame_size=1024, filt_ang=angle_tun, filt_elev=elevation_tun, margin=30, mean=20)
            recorder.floatToWave([filteredTime], filename, 1)

        if mode == "time1" or mode == 'all':
            filename = "audio_wyniki/"+filename_prefix+"filteredTime1.wav"
            filteredTime = self.spatialFiltrationTime(c_apa, c_aux, c_auy, c_auz, frame_size=1, filt_ang=angle_tun, filt_elev=elevation_tun, margin=30, mean=20)
            recorder.floatToWave([filteredTime], filename, 1)

        if mode == "freq" or mode == 'all':
            filename = "audio_wyniki/"+filename_prefix+"filteredFreq.wav"
            filteredFreq = self.spatialFiltrationFreq(c_apa, c_aux, c_auy, c_auz, fft_size=2048, filt_ang=angle_tun, filt_elev=elevation_tun, margin=30, windowStart=False, windowEnd=False)
            recorder.floatToWave([filteredFreq], filename, 1)

        if mode == None or mode == 'all':
            filename = "audio_wyniki/"+filename_prefix+"noFilter.wav"
            recorder.floatToWave(array=amp4chx, filename=filename, channels=1)

        ix, iy, iz, a, e, r = self.directionTime(c_apa, c_aux, c_auy, c_auz, frame_size=len(c_apa), mean=None)
        return a[0], e[0], filename

        
if __name__ == "__main__":
    sf = SpaceFiltration()
    sf.recAndFilterWriteAll()
    #sf.recAndFilter('time')