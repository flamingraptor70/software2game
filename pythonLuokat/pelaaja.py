class Pelaaja():
    def __init__(self, raha, polttoaine, sotilaat, score, sijainti):
        self.raha = raha
        self.polttoaine = polttoaine
        self.sotilaat = sotilaat
        self.score = score
        self.sijainti = sijainti

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

    def SetPolttoAine(self, polttoAine):
        self.polttoaine = polttoAine

    def SetSotilaat(self, sotilaat):
        self.sotilaat = sotilaat

    def SetScore(self, score):
        self.score = score

    def SetSijainti(self, sijainti):
        self.sijainti = sijainti