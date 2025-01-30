from s_filtracja_przestrzenna import SpaceFiltration

sf = SpaceFiltration()
prefixes = ['menu_R_','radar_R_','światło_R_','powrót_R_','kalibracja_R_','efekty_R_','oczko_R_','wyjście_R_','ścieżka_R_','włącz_R_','wyłącz_R_','wszystkie_R_','jeden_R_','dwa_R_','trzy_R_','cztery_R_','pięć_R_','reset_R_','tunel_R_','migotanie_R_','kolejka_R_','nic_R_','policja_R_','stop_R_','start_R_','kropelka_R_','ignoruj_R_']


for p in prefixes:
    print(p)
    sf.recAndFilter(mode='all', angle_tun=90, elevation_tun=-20, filename_prefix=p)