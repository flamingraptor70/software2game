class Pelaaja():
    def __init__(self, pNimi, raha, polttoaine, sotilaat, score, yhteys, sijainti=""):
        self.pNimi = pNimi
        self.raha = raha
        self.polttoaine = polttoaine
        self.sotilaat = sotilaat
        self.score = score
        self.sijainti = sijainti
        self.yhteys = yhteys

        sql = "INSERT INTO Game(Fuel, Money, Troops, User_name, Score) VALUES('" + self.polttoaine + "', '" + self.raha + "', '" + self.sotilaat + "', '" + self.pNimi + "', '" + self.score + "')"
        kursori = self.yhteys.cursor()
        kursori.execute(sql)

    def GetRaha(self):
        return self.raha

    def GetPolttoAine(self):
        return self.polttoaine

    def GetSotilaat(self):
        return self.sotilaat

    def GetScore(self):
        return self.score

    def GetSijainti(self):
        return self.sijainti

    def SetRaha(self, raha):
        self.raha = raha
        '''
        sql = "UPDATE Game SET Money = '" + str(raha) + "' WHERE Game_ID = '" + str(
        PeliID) + "'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        '''

    def SetPolttoAine(self, polttoAine):
        self.polttoaine = polttoAine
        '''
        sql = "UPDATE Game SET Fuel = '" + str(polttoAine) + "' WHERE Game_ID = '" + str(
        PeliID) + "'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        '''

    def SetSotilaat(self, sotilaat):
        self.sotilaat = sotilaat
        '''
        sql = "UPDATE Game SET Troops = '" + str(sotilaat) + "' WHERE Game_ID = '" + str(
        PeliID) + "'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        '''

    def SetScore(self, score):
        self.score += score
        '''
        uusiScore = float(GetScore()) + 100
        sql = "UPDATE Game SET Score = '" + str(uusiScore) + "' WHERE Game_ID = '" + str(PeliID) + "'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        '''

    def SetSijainti(self, sijainti):
        self.sijainti = sijainti
