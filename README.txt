link do wszystkich plików
https://drive.google.com/drive/folders/120bOeQQk_mx4c1x2odwf8kup_4cmfb9b?usp=sharing

tekst pracy dyplomowej
https://drive.google.com/file/d/1SQ49Gcx5X9bx8CGLrQUuGYgomDhRvBOA/view?usp=sharing

aby uruchomić system otworzyć ten folder w terminalu (polecenie cd),
a następnie wywołać dowolny skrypt poleceniem python3

SKRYPTY DO STEROWANIA UKŁADEM
o	s_efekty.py – Silnik efektów świetlnych, należy go uruchomić w osobnym oknie terminala.
o	s_zarzadzanie.py – Eksperymentalny skrypt uruchomiający sterowanie głosowe z aktywnymi wszystkimi blokami funkcyjnymi. Niestety przy nagrywaniu 6 kanałowego dźwięku tą metodą na Raspberry Pi występuje przepełnienie. Na komputerze pomocniczym o specyfikacji podanej w załączniku 103 przepełnienie nie występuje, dlatego działanie funkcji wymagających lokalizacji przestrzennej źródła zbadano w sposób modularny.
o	s_rozpoznawanie_mikrofon.py – Skrypt uruchomiający sterowanie głosowe z pominięciem bloku filtracji przestrzennej. Metoda ta pozawala na wykorzystanie dowolnego innego mikrofonu na miejscu wektorowego czujnika akustycznego. Jej dużym plusem jest automatyczne wykrywanie tego, czy aktualnie nagrywana jest komenda, czy cisza. Pozwala to na uniknięcie sytuacji, w której nasłuchiwanie komendy przerywane jest w połowie słowa, jak ma to miejsce, gdy czas nagrywania jest wartością stałą.
o	s_rozpoznaj_z_pliku.py – Skrypt wczytuje pojedynczy plik wave podawany jako argument, np. „python3 s_rozpoznaj_z_pliku.py plik.wav”. Z pliku dźwiękowego rozpoznawana jest mowa, a następnie komenda jest interpretowana i wykonywana.
o	s_wykonaj_komende.py – Skrypt interpretujący i wykonywujący komendy podawane jako argumenty rozdzielone spacją; „python3 s_wykonaj_komende.py [komenda1] [komenda2] …”.


SKRYPTY UŻYWANE POŚREDNIO (PRZEZ INNE)
o	s_filtracja_przestrzenna.py – Skrypt wykorzystywany do korekcji sygnałów odebranych z wektorowego czujnika akustycznego oraz filtracji przestrzennej. Wywołany bezpośrednio przez użytkownika z poziomy konsoli nagra dźwięk i przefiltruje go kilkoma sposobami, zapisując przy tym każdy krok algorytmu do plików.
o	s_slownik_komend.py – Skrypt zawierający definicje słowników dla każdej komendy.
o	s_tools.py – Skrypt zawierający klasy pomocnicze, między innymi do nagrywania dźwięku wielokanałowego.


SKRYPTY TESTOWE
o	s_przygotuj_probki.py – Skrypt służący do nagrania odczytywanych komend testowych oraz przygotowania przefiltrowanych przestrzennie plików dźwiękowych
o	s_testy.py – Skrypt sprawdzający skuteczność rozpoznawania mowy z utworzonych skryptem s_przygotuj_probki.py plików dźwiękowych.
o	s_rozpoznaj_z_pliku_windows.py – Skrypt do rozpoznawania mowy z pliku dźwiękowego („python3 s_rozpoznaj_z_pliku.py plik.wav”). Tekst nie jest dalej przetwarzany.
o	sprawdz_mikrofon.py – Skrypt ułatwiający ustalenie indeksu mikrofonu. W aplikacji używany jest mikrofon o indeksie 0.



ZALECANE URUCHAMIANIE:
(w osobnych oknach terminala)
s_efekty.py
s_rozpoznawanie_mikrofon.py

s_ - najważniejsze skrypty
z_ - plik tekstowy przechowywujący używane zmienne
