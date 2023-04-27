from lentokentta import Lentokentta
from kauppa import Kauppa
from pelaaja import Pelaaja
from yhteys import yhteys
import random
from geopy.distance import geodesic

class Peli():
    def __init__(self):
        pass

    def LuoPeli(self, pNimi, polttoAine, omatSotilaat, raha, score):
        self.lentokentat = []
        self.havinnyt = False
        self.pelaaja = Pelaaja(pNimi, raha, polttoAine, omatSotilaat, score, yhteys)
        '''self.kauppa = Kauppa(self.pelaaja)'''

    def ArvoPaikat(self):
        sql = "SELECT iso_country FROM airport WHERE continent = 'EU' GROUP BY iso_country ORDER BY RAND() LIMIT 10"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()

        if kursori.rowcount > 0:
            for rivi in tulos:
                sql2 = "SELECT ident FROM airport WHERE iso_country = '" + rivi[0] + "' and continent = 'EU' ORDER BY RAND() LIMIT 1"
                kursori.execute(sql2)
                tulos2 = kursori.fetchall()
                if kursori.rowcount > 0:
                    for rivi2 in tulos2:
                        lKentta = Lentokentta(rivi2[0], yhteys)
                        self.lentokentat.append(lKentta)
        return

    def getPaikat(self):
        paikat = []
        for i in range(len(self.lentokentat)):
            lkentta = {
                "icao": self.lentokentat[i].getIdent(),
                "maa": self.lentokentat[i].getLentokentanMaa(),
                "nimi": self.lentokentat[i].getLentokentanNimi(),
                "sotilaat": self.lentokentat[i].getLentokentanSotilaat(),
                "valloitettu": self.lentokentat[i].onkoValloitettu(),
                "lat": self.lentokentat[i].getLentokentanLat(),
                "lon": self.lentokentat[i].getLentokentanLon(),
                "etaisyys": self.getEtaisyys(self.lentokentat[i].getIdent())
            }
            paikat.append(lkentta)
        return paikat

    def getPaikka(self, icao):
        lkentta = {
            "icao": self.oikeaLentokentta(icao).getIdent(),
            "maa": self.oikeaLentokentta(icao).getLentokentanMaa(),
            "nimi": self.oikeaLentokentta(icao).getLentokentanNimi(),
            "sotilaat": self.oikeaLentokentta(icao).getLentokentanSotilaat(),
            "valloitettu": self.oikeaLentokentta(icao).onkoValloitettu(),
            "lat": self.oikeaLentokentta(icao).getLentokentanLat(),
            "lon": self.oikeaLentokentta(icao).getLentokentanLon(),
            "etaisyys": self.getEtaisyys(icao)
        }
        return lkentta

    def oikeaLentokentta(self, ident):
        for i in range(len(self.lentokentat)):
            if self.lentokentat[i].getIdent() == ident:
                print(self.lentokentat[i].getIdent())
                return self.lentokentat[i]

    def Taistelu(self, ident):
        omat = float(self.pelaaja.GetSotilaat())
        lKentta = self.oikeaLentokentta(ident)
        viholliset = float(lKentta.getlentokentanSotilaat())
        if omat > 0:
            while True:
                print("Taistelu meneilllään. Omat sotilaat: " + str(omat) + ", vihollisen sotilaat: " + str(viholliset))
                omaHyokkays = random.randint(int(0.01 * omat), int(0.1 * omat))
                vihollisenHyokkays = random.randint(int(0.01 * viholliset), int(0.1 * viholliset))

                if omaHyokkays < 1:
                    omaHyokkays = 1

                if vihollisenHyokkays < 1:
                    vihollisenHyokkays = 1

                # print("Omien hyökkäys: " + str(omaHyokkays) + ", vihollisen hyökkäys: " + str(vihollisenHyokkays))
                omat -= vihollisenHyokkays
                viholliset -= omaHyokkays

                if omat <= 0:
                    omat = 0
                    print("Hävisit taistelun.")
                    if viholliset <= 0:
                        viholliset = 0
                    self.pelaaja.SetSotilaat(omat)
                    lKentta.setLentokentanSotilaat(viholliset)
                    '''SetSotilaat(omat)
                    SetLentokentanSotilaat(ident, viholliset)'''
                    return False
                if viholliset <= 0:
                    viholliset = 0
                    '''SetLentokentanSotilaat(ident, viholliset)'''
                    lKentta.setLentokentanSotilaat(viholliset)
                    if omat > 0:
                        print("Voitit taistelun.")
                        '''SetSotilaat(omat)'''
                        self.pelaaja.SetSotilaat(omat)
                        return True
        else:
            print("Tarvitset sotilaita vallataksesi lentoaseman.")
            return False

    def ValitseAloitus(self, sijainti):
        asemat = "Valitse aloitusasema kirjoittamalla lentokentän icao-koodi:\n"
        for i in range(len(self.lentokentat)):
            valiVaihe = self.lentokentat[i]
            asemat += "Icao-koodi: " + valiVaihe.getIdent() + ", nimi: " + valiVaihe.getLentokentanNimi() + ", maa: " + valiVaihe.getLentokentanMaa() + "\n"
            '''
            Tallenna tietokantaan muutokset
            '''
        print(asemat)
        '''sijainti = input("Aloitusasema: ")'''
        self.pelaaja.SetSijainti(sijainti)
        self.oikeaLentokentta(sijainti).Valloita()

        '''Valloita(nykySijainti)'''
        return

    '''def Matkat(self):
        matkat = "Valitse matka kirjoittamalla lentokentän icao-koodi:\n"
        tyhja = True
        polttoAine = float(self.pelaaja.GetPolttoAine())
        for i in range(len(self.lentokentat)):
            valiVaihe = self.lentokentat[i]
            etaisyys = geodesic(self.oikeaLentokentta(self.pelaaja.GetSijainti()).getLentokentanKoordinaatit(), valiVaihe.getLentokentanKoordinaatit()).km
            etaisyys = geodesic(Haekoordinaatit(nykySijainti), Haekoordinaatit(valiVaihe[0])).km
            if valiVaihe != self.pelaaja.GetSijainti():
                if etaisyys <= float(polttoAine) and valiVaihe.onkoValloitettu() == False:
                    tyhja = False
                    matkat += "Icao-koodi: " + valiVaihe.getIdent() + ", nimi: " + valiVaihe.getLentokentanNimi() + ", maa: " + valiVaihe.getLentokentanMaa() \
                                + ", matka: " + str(etaisyys) + ", sotilaat: " + str(valiVaihe.getLentokentanSotilaat()) + "\n"
        if tyhja == True:
            return print("Et voi matkustaa mihinkään.")
        else:
            print(matkat)
            kohde = input("Matkustuskohde: ")
            self.Matkusta(kohde)
            return
        return'''

    def getLentokentanKoordinaatit(self, icao):
        print("Lentokentän koordinaatit: " + str(self.oikeaLentokentta(icao).getLentokentanLat()) + ", " + str(self.oikeaLentokentta(icao).getLentokentanLon()))
        etaisyys = str(self.oikeaLentokentta(icao).getLentokentanLat()) + ", " + str(self.oikeaLentokentta(icao).getLentokentanLon())
        return etaisyys
    def getEtaisyys(self, kohde):
        if self.pelaaja.GetSijainti() != "":
            etaisyys = geodesic(self.getLentokentanKoordinaatit(self.pelaaja.GetSijainti()), self.getLentokentanKoordinaatit(kohde)).km
            etaisyys = round(etaisyys, 2)
            return etaisyys
        else:
            return 0

    def Matkusta(self, kohde):
        polttoAine = float(self.pelaaja.GetPolttoAine())
        etaisyys = self.getEtaisyys(kohde)
        '''if self.Taistelu(kohde):'''
        polttoAine -= etaisyys
        self.pelaaja.SetSijainti(kohde)
        self.pelaaja.SetPolttoAine(polttoAine)
        self.oikeaLentokentta(kohde).Valloita()
        '''self.MatemaattinenOngelma()'''

    def MatemaattinenOngelma(self):
        sql = "SELECT Questions_text, Answer FROM Questions ORDER BY RAND() LIMIT 1"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()
        if kursori.rowcount > 0:
            for rivi in tulos:
                print("Vastaa seuraavaan kysymykseen oikein suorittaaksesi kidnappauksen: " + rivi[0])
                vastaus = input("Vastaus: ")
                if float(vastaus) == float(rivi[1]):
                    print("Vastaus oikein. Sait kidnappauksesta 1000 €")
                    raha = float(self.pelaaja.GetRaha()) + float(1000)
                    self.pelaaja.SetRaha(raha)
                else:
                    print("Vastaus väärin.")
        return

    def HavinnytTarkistus(self, lista):
        global nykySijainti
        polttoAine = self.pelaaja.GetPolttoAine()
        raha = self.pelaaja.GetRaha()
        lahin = ""
        for i in range(len(self.lentokentat)):
            valiVaihe = self.lentokentat[i]
            if valiVaihe.getIdent() != nykySijainti and valiVaihe.onkoValloitettu() != True:
                if lahin == "":
                    lahin = valiVaihe.getIdent()
                elif geodesic(self.oikeaLentokentta(self.pelaaja.GetSijainti()), self.oikeaLentokentta(lahin).getLentokentanKoordinaatit()) > \
                        geodesic(self.oikeaLentokentta(self.pelaaja.GetSijainti()), self.oikeaLentokentta(valiVaihe).getLentokentanKoordinaatit()).km:
                    lahin = valiVaihe
        etaisyys = geodesic(self.oikeaLentokentta(self.pelaaja.GetSijainti()), self.oikeaLentokentta(lahin).getLentokentanKoordinaatit()).km
        maxPolttoAine = float(polttoAine) + (float(raha) * 2)

        if float(raha) < 2 and int(self.pelaaja.GetSotilaat()) == 0:
            self.havinnyt = True
            return print("Hävisit pelin")
        elif etaisyys > maxPolttoAine:
            self.havinnyt = True
            return print("Hävisit pelin")
        return

    def VoittoTarkistus(self):
        voitto = True
        for i in range(len(self.lentokentat)):
            valiVaihe = self.lentokentat[i]
            if valiVaihe.getValloitus() == False:
                voitto = False
        return voitto

    def onkoHavinnyt(self):
        return self.havinnyt

    '''def Kauppa(self):
        self.kauppa.Kauppa()'''

    def luoSotilaatLentokentille(self):
        for i in range(len(self.lentokentat)):
            if self.lentokentat[i].onkoValloitettu() == False:
                self.lentokentat[i].luoSotilaat()

    def pelaajaTiedot(self):
        pelaaja = {
            "nimi": self.pelaaja.GetNimi(),
            "raha": self.pelaaja.GetRaha(),
            "pAine": self.pelaaja.GetPolttoAine(),
            "sotilaat": self.pelaaja.GetSotilaat(),
            "score": self.pelaaja.GetScore(),
            "sijainti": self.pelaaja.GetSijainti()
        }
        return pelaaja

    def maksu(self, hinta, maara, tyyppi):
        polttoAine = float(self.pelaaja.GetPolttoAine())
        raha = float(self.pelaaja.GetRaha())
        omatSotilaat = float(self.pelaaja.GetSotilaat())
        if tyyppi == "polttoaine":
            raha -= hinta
            polttoAine += maara
            self.pelaaja.SetRaha(raha)
            self.pelaaja.SetPolttoAine(polttoAine)
        elif tyyppi == "sotilas":
            raha -= hinta
            omatSotilaat += maara
            self.pelaaja.SetRaha(raha)
            self.pelaaja.SetSotilaat(omatSotilaat)

    def ostaPolttoAinetta(self, maara):
        # 2km = 1€
        self.maksu(maara / 2, maara, "polttoaine")

    def ostaSotilaita(self, maara):
        # 1s = 2€
        self.maksu(maara * 2, maara, "sotilas")



