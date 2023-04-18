class Pelaaja():
    def __init__(self, raha, polttoaine, sotilaat, score):
        self.raha = raha
        self.polttoaine = polttoaine
        self.sotilaat = sotilaat
        self.score = score

    def GetRaha(self):
        return self.raha

    def GetPolttoAine(self):
        return self.polttoaine

    def GetSotilaat(self):
        return self.sotilaat

    def GetScore(self):
        return self.score

    def SetRaha(self, raha):
        self.raha = raha

    def SetPolttoAine(self, polttoAine):
        self.polttoaine = polttoAine

    def SetSotilaat(self, sotilaat):
        self.sotilaat = sotilaat

    def SetScore(self, score):
        self.score = score