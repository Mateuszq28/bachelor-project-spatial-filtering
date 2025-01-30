import pyaudio
import wave
import sys
import numpy as np

# aby pokazywać logi z błędami
import logging
log = logging.getLogger(__name__)


#klasa ułatwiająca zapis/odczyt plików tekstowych
class TextFiles:
    def __init__(self):
        pass

    def writeAll(self, data, file_name):
        with open(file_name, 'w') as f:
            f.write(data)

    def readAll(self, file_name):
        with open(file_name, 'r') as f:
            data = f.read()
        return data

    def filterStringToint(self, text):
        array = text.split(',')
        new = []
        for a in array:
            new.append(float(a))
        return new
        

# Klasa służąca do nagrywania sygnałów z czujnika
class Recorder:
    def  __init__(self,
                 chunk = 1024,
                 sample_format = pyaudio.paInt32,
                 channels = 6,
                 fs = 44100,
                 seconds = 3,
                 filename = "audio_wyniki/nagranie6k.wav"):
        self.chunk = chunk  # nagrywaj w chunkach po 1024 próbki
        self.sample_format = sample_format # 16 bits na próbkę
        self.channels = channels
        self.fs = fs  # nagrywaj w 44100 próbkach na sekundę
        self.seconds = seconds
        self.filename = filename


    # Nagrywanie wzorowane na kodzie ze strony:
    # https://realpython.com/playing-and-recording-sound-python/
    # Znacznie przerobione, aby umożliwić seperację 6 kanałów
    def rec(self):
        print('<System>Nagrywanie')

        # stwórz interface do PortAudio
        p = pyaudio.PyAudio() 
        stream = p.open(format=self.sample_format,
                        channels=self.channels,
                        rate=self.fs,
                        frames_per_buffer=self.chunk,
                        input=True,
                        input_device_index=0)

        frames = []  # utwórz tablicę do przechowywania ramek
        frames4chx = [] # tablica dla 6 kanałów przechowywanych w osobnych rzędach
        for c in range(0, self.channels):
            frames4chx.append([])

        # Ile bitów na próbkę
        if self.sample_format == pyaudio.paInt32:
            bytesPerSam = 4
        elif self.sample_format == pyaudio.paInt16:
            bytesPerSam = 2
        else:
            bytesPerSam = 4

        # Zbieranie danych
        # 4 bajty kanału 1, 4 bajty kanału 2, 4 bajty kanału 3 ...
        for i in range(0, int(self.fs / self.chunk * self.seconds)):
            data = stream.read(self.chunk)
            #print(sys.getsizeof(data))
            frames.append(data)
            for j in range(0, int(len(data)/(self.channels*bytesPerSam))):
                for c in range(0, self.channels):
                    index = (j*self.channels+c)*bytesPerSam
                    frames4chx[c].append(data[(index):(index+bytesPerSam)])

        # Zatrzymaj i zamknij strumień
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        p.terminate()

        print('<System>Koniec nagrywania')
        return frames, frames4chx


    def floatToInt(self, array):
        #print(type(array[0]))
        #print(type(array[0][0]))
        listType = [list, MatlabMatrix, np.ndarray]
        floatType = [float, np.float64]
        if type(array) in listType:
            if type(array[0]) in floatType:
                new = []
                for i in range(0, len(array)):
                    new.append(int(array[i]*(2**31)))
                return new
            elif type(array[0]) in listType:
                if type(array[0][0]) in floatType:
                    new = []
                    for c in range(0, len(array)):
                        new.append([])
                        for i in range(0, len(array[0])):
                            new[c].append(int(array[c][i]*(2**31)))
                    return new
                else:
                    return None 
            else:
                return None
        elif type(array) in floatType:
            return int(array*(2**32))
        else:
            return None


    def intToFloat(self, array):
        #print(type(array[0]))
        #print(type(array[0][0]))
        listType = [list, MatlabMatrix]
        if type(array) in listType:
            if type(array[0]) == int:
                new = []
                for i in range(0, len(array)):
                    new.append(array[i]/(2**31))
                return new
            elif type(array[0]) in listType:
                if type(array[0][0]) == int:
                    new = []
                    for c in range(0, len(array)):
                        new.append([])
                        for i in range(0, len(array[0])):
                            new[c].append(array[c][i]/(2**31))
                    return new
                else:
                    return None
            else:
                return None
        elif type(array) == int:
            return array/(2**32)
        else:
            return None


    def writeBytesToWave(self, frames, filename=None, channels=None, sample_format=None, fs=None):
        if filename == None:
            filename=self.filename
        if channels == None:
            channels=self.channels
        if sample_format == None:
            sample_format=self.sample_format
        if fs == None:
            fs=self.fs
        # stwórz interface do PortAudio
        p = pyaudio.PyAudio() 
        # Zapisz dane jako plik WAV
        wf = wave.open(filename, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(sample_format))
        wf.setframerate(fs)
        wf.writeframes(b''.join(frames))
        wf.close()


    def toInt(self, frames, frames4chx):
        # zamień bloki 16 bitów (2 bajty) na int
        amp4chx = []
        for c in range(0, self.channels):
            amp4chx.append([])
            for i in frames4chx[c]:
                amp4chx[c].append(int.from_bytes(i, byteorder='little', signed=True))
        return amp4chx


    def recAndWriteToInt(self):
        frames, frames4chx = self.recAndWrite()
        return self.toInt(frames, frames4chx)

    
    def recAndWriteToFloat(self):
        return self.intToFloat(self.recAndWriteToInt())


    def recToInt(self):
        frames, frames4chx = self.rec()
        return self.toInt(frames, frames4chx)


    def recToFloat(self):
        return self.intToFloat(self.recToInt())


    def recAndWrite(self):
        frames, frames4chx = self.rec()
        self.writeBytesToWave(frames=frames)
        for c in range(0, self.channels):
            channel_name = 'audio_wyniki/nagranie' + str(c+1) + 'ch.wav'
            self.writeBytesToWave(frames=frames4chx[c], filename=channel_name, channels=1)
        return frames, frames4chx


    # byte - ile bajtów na próbkę (dla Int32 będzie to 4)
    def waveToInt(self, filename, channels, byte):
        with open(filename, 'r+b') as f:
            array = f.read()
        new = []
        for c in range(0, channels):
                new.append([])
        for i in range(0, len(array), byte*channels):
            for c in range(0, channels):
                new[c].append(int.from_bytes(array[i+byte*c:i+byte*c+byte], byteorder='little', signed=True))
        return new


    # byte - ile bajtów na próbkę (dla Int32 będzie to 4)
    def waveToFloat(self, filename, channels, byte):
        return self.intToFloat(self.waveToInt(filename, channels, byte))


    def intToWave(self, array, filename = "intWave", channels = 1):
        new = []
        for i in range(0, len(array[0])):
            for c in range(0, channels):
                temp = int(array[c][i])
                new.append(temp.to_bytes(length=4, byteorder='little', signed=True))
        self.writeBytesToWave(frames=new, filename=filename, channels=channels)


    def floatToWave(self, array, filename = "floatWave", channels = 1):
        new = self.floatToInt(array)
        self.intToWave(new, filename, channels)


# klada wzorowana na numpy.array
# przesilone operatory + - / *
# mnożenia i dzielenia tablicowe, a nie macierzowe !!!
# działa, ale psuje czytelność kodu dlatego
# użyto tylko w metodzie getAndFilterWriteAll
# aby zademonstrować działanie
class MatlabMatrix:
    def __init__(self, intArray):
        self.matrix = intArray


    def __len__(self):
        return len(self.matrix)


    def __getitem__(self, key):
        return self.matrix[key]


    def __setitem__(self, key, value):
        self.matrix[key] = value


    def __add__(self, other):
        if len(self.matrix) == len(other):
            new = []
            for i in range(0, len(other)):
                new.append(self[i] + other[i])
            return MatlabMatrix(new)
        else:
            log.warning("Tablice mają różne długości")
            return None


    def __truediv__(self, other):
        if type(other) == int:
            new = []
            for i in self.matrix:
                new.append(i / other)
            return MatlabMatrix(new)


    def __mul__(self, other):
        if type(other) == int:
            new = []
            for i in self.matrix:
                new.append(i * other)
            return MatlabMatrix(new)


    def __sub__(self, other):
        if len(self.matrix) == len(other):
            new = []
            for i in range(0, len(other)):
                new.append(self[i] - other[i])
            return MatlabMatrix(new)
        else:
            log.warning("Tablice mają różne długości")
            return None

    
    def unwrap(self):
        return self.matrix