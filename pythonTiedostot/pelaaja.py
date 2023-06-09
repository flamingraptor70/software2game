class Pelaaja():
    def __init__(self, pNimi, raha, polttoaine, sotilaat, score, yhteys, sijainti=""):
        self.pNimi = pNimi
        self.raha = raha
        self.polttoaine = polttoaine
        self.sotilaat = sotilaat
        self.score = score
        self.sijainti = sijainti
        self.yhteys = yhteys
        print(self.yhteys)

        sql = "INSERT INTO Game(Fuel, Money, Troops, User_name, Score) VALUES('" + str(self.polttoaine) + "', '" + str(self.raha) + "', '" + str(self.sotilaat) + "', '" + self.pNimi + "', '" + str(self.score) + "')"
        kursori = self.yhteys.cursor()
        kursori.execute(sql)

        sql2 = "SELECT MAX(Game_ID) FROM Game WHERE User_name = '" + pNimi + "'"
        kursori.execute(sql2)
        tulos = kursori.fetchall()

        if kursori.rowcount > 0:
            for rivi in tulos:
                self.peliID = rivi[0]

    def GetRaha(self):
        return self.raha

    def GetPolttoAine(self):
        return round(self.polttoaine, 2)

    def GetSotilaat(self):
        return self.sotilaat

    def GetScore(self):
        return self.score

    def GetSijainti(self):
        return self.sijainti

    def GetNimi(self):
        return self.pNimi

    def SetRaha(self, raha):
        self.raha = raha

        sql = "UPDATE Game SET Money = '" + str(raha) + "' WHERE Game_ID = '" + str(self.peliID) + "'"
        kursori = self.yhteys.cursor()
        kursori.execute(sql)


    def SetPolttoAine(self, polttoAine):
        self.polttoaine = polttoAine

        sql = "UPDATE Game SET Fuel = '" + str(polttoAine) + "' WHERE Game_ID = '" + str(self.peliID) + "'"
        kursori = self.yhteys.cursor()
        kursori.execute(sql)


    def SetSotilaat(self, sotilaat):
        self.sotilaat = sotilaat

        sql = "UPDATE Game SET Troops = '" + str(sotilaat) + "' WHERE Game_ID = '" + str(self.peliID) + "'"
        kursori = self.yhteys.cursor()
        kursori.execute(sql)


    def SetScore(self, score):
        self.score += score

        sql = "UPDATE Game SET Score = '" + str(self.score) + "' WHERE Game_ID = '" + str(self.peliID) + "'"
        kursori = self.yhteys.cursor()
        kursori.execute(sql)


    def SetSijainti(self, sijainti):
        self.sijainti = sijainti
