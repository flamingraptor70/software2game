from lentokentta import Lentokentta
from kauppa import Kauppa
from pelaaja import Pelaaja
from populatedb import conn as yhteys

class Peli():
    def __init__(self):
        self.lentokentat = []
        self.peliID = ""

    def LuoPeli(self, pNimi, polttoAine, omatSotilaat, raha, score):
        Pelaaja(pNimi, raha, polttoAine, omatSotilaat, score, yhteys)
        sql2 = "SELECT MAX(Game_ID) FROM Game WHERE User_name = '" + pNimi + "'"
        kursori = yhteys.cursor()
        kursori.execute(sql2)
        tulos = kursori.fetchall()

        if kursori.rowcount > 0:
            for rivi in tulos:
                self.peliID = rivi[0]
        return

    def ArvoPaikat(self):
        sql = "SELECT iso_country FROM airport WHERE continent = 'EU' GROUP BY iso_country ORDER BY RAND() LIMIT 3"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()

        if kursori.rowcount > 0:
            for rivi in tulos:
                sql2 = "SELECT ident FROM airport WHERE iso_country = '" + rivi[0] + "' ORDER BY RAND() LIMIT 1"
                kursori.execute(sql2)
                tulos2 = kursori.fetchall()
                if kursori.rowcount > 0:
                    for rivi2 in tulos2:
                        paikka = Lentokentta(rivi[0], yhteys)
                        self.lentokentat.append(paikka)
        self.ValitseAloitus()
        return

    def Taistelu(ident):
        omat = float(GetSotilaat())
        viholliset = float(GetLentokentanSotilaat(ident))
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
                    SetSotilaat(omat)
                    SetLentokentanSotilaat(ident, viholliset)
                    return False
                if viholliset <= 0:
                    viholliset = 0
                    SetLentokentanSotilaat(ident, viholliset)
                    if omat > 0:
                        print("Voitit taistelun.")
                        SetSotilaat(omat)
                        return True
        else:
            print("Tarvitset sotilaita vallataksesi lentoaseman.")
            return False

    def ValitseAloitus(self):
        global nykySijainti
        asemat = "Valitse aloitusasema kirjoittamalla lentokentän icao-koodi:\n"
        for i in range(len(self.lentokentat)):
            valiVaihe = self.lentokentat[i]
            asemat += "Icao-koodi: " + valiVaihe[0] + ", nimi: " + valiVaihe[1] + ", maa: " + valiVaihe[2] + "\n"
            '''
            Tallenna tietokantaan muutokset
            '''
        print(asemat)
        aloitusAsema = input("Aloitusasema: ")
        nykySijainti = aloitusAsema
        Valloita(nykySijainti)
        return

    def Matkat(lista):
        matkat = "Valitse matka kirjoittamalla lentokentän icao-koodi:\n"
        tyhja = True
        polttoAine = float(GetPolttoAine())
        for i in range(len(lista)):
            valiVaihe = lista[i]
            etaisyys = geodesic(Haekoordinaatit(nykySijainti), Haekoordinaatit(valiVaihe[0])).km
            if valiVaihe[0] != nykySijainti:
                if etaisyys <= float(polttoAine) and valiVaihe[3] != "Valloitettu":
                    tyhja = False
                    matkat += "Icao-koodi: " + valiVaihe[0] + ", nimi: " + valiVaihe[1] + ", maa: " + valiVaihe[2] \
                                + ", matka: " + str(etaisyys) + ", " + valiVaihe[3] + ", sotilaat: " + str(
                        GetLentokentanSotilaat(valiVaihe[0])) + "\n"
        if tyhja == True:
            return print("Et voi matkustaa mihinkään.")
        else:
            print(matkat)
            kohde = input("Matkustuskohde: ")
            Matkusta(kohde)
            return
        return

    def Matkusta(kohde):
            global nykySijainti
            polttoAine = float(GetPolttoAine())
            etaisyys = geodesic(Haekoordinaatit(nykySijainti), Haekoordinaatit(kohde)).km
            if etaisyys <= polttoAine and GetValloitus(kohde) != "Valloitettu":
                if Taistelu(kohde):
                    polttoAine -= etaisyys
                    nykySijainti = kohde
                    SetPolttoAine(polttoAine)
                    Valloita(nykySijainti)
                    MatemaattinenOngelma()
            else:
                return print("Epäkelpo vastaus.")
            return

        def MatemaattinenOngelma():
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
                        raha = float(GetRaha()) + float(1000)
                        SetRaha(raha)
                    else:
                        print("Vastaus väärin.")
            return

        def HavinnytTarkistus(lista):
            global nykySijainti
            polttoAine = GetPolttoAine()
            raha = GetRaha()
            lahin = ""
            global havinnyt
            for i in range(len(lista)):
                valiVaihe = lista[i]
                if valiVaihe[0] != nykySijainti and valiVaihe[3] != "Valloitettu":
                    if lahin == "":
                        lahin = valiVaihe[0]
                    elif geodesic(Haekoordinaatit(nykySijainti), Haekoordinaatit(lahin)).km > geodesic(
                            Haekoordinaatit(nykySijainti), Haekoordinaatit(valiVaihe[0])).km:
                        lahin = valiVaihe[0]
            etaisyys = geodesic(Haekoordinaatit(nykySijainti), Haekoordinaatit(lahin)).km
            maxPolttoAine = float(polttoAine) + (float(raha) * 2)

            if float(raha) < 2 and int(GetSotilaat()) == 0:
                havinnyt = True
                return print("Hävisit pelin")
            elif etaisyys > maxPolttoAine:
                havinnyt = True
                return print("Hävisit pelin")
            return

        def VoittoTarkistus(lista):
            voitto = True
            for i in range(len(lista)):
                valiVaihe = lista[i]
                if valiVaihe[3] == "Ei valloitettu":
                    voitto = False
            return voitto

