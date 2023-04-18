class Pelaaja():
    def __init__(self, raha, polttoaine, sotilaat):
        self.raha = raha
        self.polttoaine = polttoaine
        self.sotilaat = sotilaat

    def GetRaha(self):
        return self.raha

    def GetPolttoAine(self):
        return self.polttoaine

    def GetSotilaat(self):
        return self.sotilaat

    def SetRaha(self, raha):
        self.raha = raha

    def SetPolttoAine(self, polttoAine):
        self.polttoaine = polttoAine

    def SetSotilaat(self, sotilaat):
        self.sotilaat = sotilaat