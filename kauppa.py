
class Kauppa():
    def __init__(self, pelaaja):
        self.pl = pelaaja
    def Kauppa(self):
        while True:
            print(f"Rahamäärä: {self.pl.GetRaha()} €. Polttoainemäärä: {self.pl.GetPolttoAine()} km. Sotilasmäärä: {self.pl.GetSotilaat()}\n")
            valinta = input("Valitse toiminto kirjoittamalla toimintoa vastaava luku:\n"
                            "1) Osta polttoainetta\n2) Osta sotilaita\n3) Poistu kaupasta\nValinta: ")

            if valinta == "1":
                maara = float(input("Kuinka monta km haluat ostaa polttoainetta: "))
                self.OstaPolttoAinetta(maara)
            elif valinta == "2":
                maara = float(input("Kuinka monta sotilasta haluat ostaa: "))
                self.OstaSotilaita(maara)
            elif valinta == "3":
                break
            else:
                print("Epäkelpo luku. Yritä uudestaan.")

    def Maksu(self, hinta, maara, tyyppi):
        polttoAine = float(self.pl.GetPolttoAine())
        raha = float(self.pl.GetRaha())
        omatSotilaat = float(self.pl.GetSotilaat())
        if tyyppi == "polttoaine":
            valinta = input(f"Olet ostamassa polttoainetta {maara} km verran. Se tulee maksamaan {hinta} €.\n"
                            f"Syötä '1' hyväksyäksesi ostoksen tai syötä '2' kumotaksesi ostoksen: ")
            if valinta == "1":
                if raha - hinta >= 0:
                    raha -= hinta
                    polttoAine += maara
                    self.pl.SetRaha(raha)
                    self.pl.SetPolttoAine(polttoAine)
                    return print("Kiitos ostoksestasi")
                else:
                    return print("Rahasi eivät riitä ostokseen.")
            elif valinta == "2":
                return print("Ostoksesi on peruutettu.")
        elif tyyppi == "sotilas":
            valinta = input(f"Olet ostamassa sotilaita {maara} verran. Se tulee maksamaan {hinta} €.\n"
                            f"Syötä '1' hyväksyäksesi ostoksen tai syötä '2' kumotaksesi ostoksen: ")
            if valinta == "1":
                if raha - hinta >= 0:
                    raha -= hinta
                    omatSotilaat += maara
                    self.pl.SetRaha(raha)
                    self.pl.SetSotilaat(omatSotilaat)
                    return print("Kiitos ostoksestasi")
                else:
                    return print("Rahasi eivät riitä ostokseen.")
            elif valinta == "2":
                return print("Ostoksesi on peruutettu.")

    def OstaPolttoAinetta(self, maara):
        # 2km = 1€
        self.Maksu(maara / 2, maara, "polttoaine")

    def OstaSotilaita(self, maara):
        # 1s = 2€
        self.Maksu(maara * 2, maara, "sotilas")