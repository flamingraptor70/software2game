import random
class Lentokentta():
    def __init__(self, ident, yhteys):
        self.ident = ident
        self.yhteys = yhteys
        self.sotilaat = 0
        self.valloitettu = False

        sql = "SELECT name, latitude_deg, longitude_deg, iso_country FROM airport WHERE ident = '" + self.ident + "'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()
        for rivi in tulos:
            self.nimi = rivi[0]
            self.lat = rivi[1]
            self.lon = rivi[2]
            self.maa = rivi[3]

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


        sql = "INSERT INTO Troops(Airport_ID, Count, Visited) VALUES('" + self.ident + "', '" + str(maara) + "', 0)"
        kursori = self.yhteys.cursor()
        kursori.execute(sql)

        return

    def getLentokentanSotilaat(self):
        return self.sotilaat

    def setLentokentanSotilaat(self, maara):
        self.sotilaat = maara


        sql = "UPDATE Troops SET Count = '" + str(maara) + "' WHERE Airport_ID = '" + self.ident + "'"
        kursori = self.yhteys.cursor()
        kursori.execute(sql)

        return

    def getLentokentanNimi(self):
        return self.nimi

    def getLentokentanLat(self):
        return self.lat

    def getLentokentanLon(self):
        return self.lon

    def onkoValloitettu(self):
        return self.valloitettu

    def Valloita(self):
        self.valloitettu = True

        '''sql = "UPDATE Troops SET Visited = '0' WHERE Airport_ID = '" + self.ident + "'"'''
        kursori = self.yhteys.cursor()
        '''kursori.execute(sql)'''


    def getIdent(self):
        return self.ident

    def getLentokentanMaa(self):
        return self.maa
