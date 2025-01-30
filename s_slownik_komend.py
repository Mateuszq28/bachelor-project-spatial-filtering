# klada definiująca możliwe do użycia komendy głosowe
class Dictionary:
    def __init__(self):
        self.main = ['', 'main', 'menu', 'melu']
        self.radar = ['', 'radar']
        self.led = ['', 'led', 'światło', 'żarówka']
        self.back = ['', 'back', 'powrót']
        self.calibration = ['', 'calibration', 'nawigacja', 'kalibracja', 'lokalizacja']
        self.effects = ['', 'effects', 'efekty']
        self.blink = ['', 'blink', 'mrugnij', 'oczko', 'poczta']
        self.exit = ['', 'exit', 'wyjście', 'wyślij', 'wyjdzie', 'wyślę']
        self.path = ['', 'path', 'ścieżka', 'śnieżka']
        self.on = ['', 'on', 'włącz', 'wysoki']
        self.off = ['', 'off', 'wyłącz', 'niski']
        self.all = ['', 'all', 'wszystkie']
        self.one = ['', 'one', '1', 'jeden', 'pierwsza', '1:00', 'raz']
        self.two = ['', 'two', '2', 'dwa', 'druga', '2:00']
        self.three = ['', 'three', '3', 'trzy', 'trzecia', '3:00']
        self.four = ['', 'four', '4', 'cztery', 'czwarta', '4:00']
        self.five = ['', 'five', '5', 'pięć', 'piąta', '5:00']
        self.reset = ['', 'reset', 'restart', 'zeruj', 'wyczyść', '0', 'zero', 'zera']
        self.tunnel = ['', 'tunnel', 'tunel', 'tuner']
        self.gleam = ['', 'gleam', 'migotanie', 'błyszczeć', 'notowanie', 'migotanie', 'pytanie', 'gotowanie', 'kochanie', 'gadanie']
        self.queue = ['', 'queue', 'kolejka']
        self.null = ['', 'null', 'nic']
        self.police = ['', 'police', 'policja', 'kogut', 'cena', 'syrena']
        self.stop = ['', 'stop', 'zatrzymaj']
        self.start = ['', 'start', 'rozpocznij', 'zacznij']
        self.droplet = ['', 'droplet', 'kropelka', 'komedia', 'kropla']
        self.ignore = ['', 'ignore', 'ignoruj', 'igor']
        # set default language
        self.setPolish()
        # Array of all commands
        self.tabOfAllCommands = []
        self.tabOfAllCommands.append(self.main)
        self.tabOfAllCommands.append(self.radar)
        self.tabOfAllCommands.append(self.led)
        self.tabOfAllCommands.append(self.back)
        self.tabOfAllCommands.append(self.calibration)
        self.tabOfAllCommands.append(self.effects)
        self.tabOfAllCommands.append(self.blink)
        self.tabOfAllCommands.append(self.exit)
        self.tabOfAllCommands.append(self.path)
        self.tabOfAllCommands.append(self.on)
        self.tabOfAllCommands.append(self.off)
        self.tabOfAllCommands.append(self.all)
        self.tabOfAllCommands.append(self.one)
        self.tabOfAllCommands.append(self.two)
        self.tabOfAllCommands.append(self.three)
        self.tabOfAllCommands.append(self.four)
        self.tabOfAllCommands.append(self.five)
        self.tabOfAllCommands.append(self.reset)
        self.tabOfAllCommands.append(self.tunnel)
        self.tabOfAllCommands.append(self.gleam)
        self.tabOfAllCommands.append(self.queue)
        self.tabOfAllCommands.append(self.null)
        self.tabOfAllCommands.append(self.police)
        self.tabOfAllCommands.append(self.stop)
        self.tabOfAllCommands.append(self.start)
        self.tabOfAllCommands.append(self.droplet)
        self.tabOfAllCommands.append(self.ignore)

    
    def setPolish(self):
        self.main[0] = 'menu'
        self.radar[0] = 'radar'
        self.led[0] = 'światło'
        self.back[0] = 'powrót'
        self.calibration[0] = 'kalibracja'
        self.effects[0] = 'efekty'
        self.blink[0] = 'oczko'
        self.exit[0] = 'wyjście'
        self.path[0] = 'ścieżka'
        self.on[0] = 'włącz'
        self.off[0] = 'wyłącz'
        self.all[0] = 'wszystkie'
        self.one[0] = 'jeden'
        self.two[0] = 'dwa'
        self.three[0] = 'trzy'
        self.four[0] = 'cztery'
        self.five[0] = 'pięć'
        self.reset[0] = 'reset'
        self.tunnel[0] = 'tunel'
        self.gleam[0] = 'migotanie'
        self.queue[0] = 'kolejka'
        self.null[0] = 'nic'
        self.police[0] = 'policja'
        self.stop[0] = 'stop'
        self.start[0] = 'start'
        self.droplet[0] = 'kropelka'
        self.ignore[0] = 'ignoruj'
        
        
    def setEnglish(self):
        self.main[0] = 'main'
        self.radar[0] = 'radar'
        self.led[0] = 'led'
        self.back[0] = 'back'
        self.calibration[0] = 'calibration'
        self.effects[0] = 'effects'
        self.blink[0] = 'blink'
        self.exit[0] = 'exit'
        self.path[0] = 'path'
        self.on[0] = 'on'
        self.off[0] = 'off'
        self.all[0] = 'all'
        self.one[0] = 'one'
        self.two[0] = 'two'
        self.three[0] = 'three'
        self.four[0] = 'four'
        self.five[0] = 'five'
        self.reset[0] = 'reset'
        self.tunnel[0] = 'tunnel'
        self.gleam[0] = 'gleam'
        self.queue[0] = 'queue'
        self.null[0] = 'null'
        self.police[0] = 'police'
        self.stop[0] = 'stop'
        self.start[0] = 'start'
        self.droplet[0] = 'droplet'
        self.ignore[0] = 'ignore'
