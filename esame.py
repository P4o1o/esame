class CSVTimeSeriesFile:

    def __init__(self, name):
        # controllo se 'name' è di tipo 'string'
        if type("odskm") == type(name):
            # assegno a name il nome del file
            self.name = name
        else:
            raise ExamException('il percorso/nome del file fornito non è di tipo string: name = "{}"'.format(name))

    def get_data(self):
        # controllo se il file esiste e lo apro
        try:
            file = open(self.name, "r")
        except Exception as e:
            raise ExamException('file "{}" non trovato'.format(self.name))
        # inizializzo la lista che sarà restituita dal metodo
        result = []
        # per ogni riga nel file
        for line in file:
            try:
                # divido la righa del csv dove trovo ',' e salvo gli elementi in una lista
                elements = line.split(",")
                lista = [int(elements[0]), float(elements[1])]
            except Exception as e:
                # se ci sono campi vuoti o con meno di 2 colonne o righe non in formato csv ignoro la riga
                continue
            # aggiungo la lista [ora, misurazione] alla lista risultato
            result.append(lista)
        # chiudo il file
        file.close()
        return result


def compute_daily_max_difference(time_series):
    # inizializzo la lista che sarà restituita dal metodo
    result = []
    # inizializzo epoch del giorno precedente a quello considerato
    previous_epoch = 0
    # inizializzo la lista di temperature per ogni giorno
    temperatures = []
    # inizializzo la lista di temperature per il singolo giorno
    temperatures_series = []
    for i in range(len(time_series)):
        # trovo il giorno a cui appartiene l'epoche del giorno 'i'
        day_start_epoch = time_series[i][0] - (time_series[i][0] % 86400)
        # se si tratta del giorno successivo all'epoche precedentemente considerato
        if day_start_epoch > previous_epoch:
            # elimino un altrimenti lista vuota iniziale
            if previous_epoch != 0:
                # aggiungo una copia della lista del giorno precedente alla lista totale
                temperatures.append(temperatures_series.copy())
            # pulisco la lista giornaliera
            temperatures_series.clear()
            # si considera il giorno successivo
            previous_epoch = day_start_epoch
        elif day_start_epoch < previous_epoch:
            raise ExamException('timestamp "{}" fuori ordine'.format(i))
        # aggiungo la misurazione alla lista giornaliera
        temperatures_series.append(time_series[i][1])
        # aggiungo l'ultima giornata
        if i == (len(time_series) - 1):
            temperatures.append(temperatures_series.copy())
    for days in temperatures:
        # cerco massimo e minimo di ogni singolo giorno
        minimo = 1000
        massimo = -1000
        for temps in days:
            if temps > massimo:
                massimo = temps
            if temps < minimo:
                minimo = temps
        # se si ha una sola misurazione valore nullo
        if len(days) == 1:
            result.append(None)
        # altrimenti aggiungo l'escursione termica alla lista
        else:
            result.append(massimo - minimo)
    return result


class ExamException(Exception):
    pass
