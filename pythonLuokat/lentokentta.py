import random
class Lentokentta():
    def __init__(self, ident):
        self.ident = ident
        self.sotilaat = 0
        self.valloitettu = False

        sql = "SELECT name, latitude_deg, longitude_deg FROM airport WHERE ident = '" + self.ident + "'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()
        for rivi in tulos:
            self.nimi = rivi[0]
            self.koordinaatit = str(rivi[1]) + ", " + str(rivi[2])

    def luoSotilaat(self):
        noppa = random.randint(1, 3)
        maara = 0
        if noppa == 1:
            maara = 500
        elif noppa == 2:
            maara = 750
        elif noppa == 3:
            maara = 1000
        self.sotilaat = maara
        return

    def getLentokentanSotilaat(self):
        return self.sotilaat

    def setLentokentanSotilaat(self, maara):
        self.sotilaat = maara
        return

    def getLentokentanNimi(self):
        return self.nimi

    def getLentokentanKoordinaatit(self):
        return self.koordinaatit

    def onkoValloitettu(self):
        return self.valloitettu

    def Valloita(self):
        self.valloitettu = True

    def getIdent(self):
        return self.ident