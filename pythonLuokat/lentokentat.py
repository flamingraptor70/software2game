import random

class Lentokentat():
    def __init__(self):
        self.paikat = []
    def ArvoPaikat(self):
        sql = "SELECT iso_country FROM airport WHERE continent = 'EU' GROUP BY iso_country ORDER BY RAND() LIMIT 3"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()

        if kursori.rowcount > 0:
            for rivi in tulos:
                sql2 = "SELECT ident, name FROM airport WHERE iso_country = '" + rivi[0] + "' ORDER BY RAND() LIMIT 1"
                kursori.execute(sql2)
                tulos2 = kursori.fetchall()
                if kursori.rowcount > 0:
                    for rivi2 in tulos2:
                        paikka = [rivi2[0], rivi2[1], rivi[0], "Ei valloitettu"]
                        self.paikat.append(paikka)
        self.ValitseAloitus()
        return

    def LuoSotilaat(self, lista):
        for i in range(len(lista)):
            valiVaihe = lista[i]
            if valiVaihe[3] != "Valloitettu":
                noppa = random.randint(1, 3)
                maara = 0
                if noppa == 1:
                    maara = 500
                elif noppa == 2:
                    maara = 750
                elif noppa == 3:
                    maara = 1000
                sql = "INSERT INTO Troops(Airport_ID, Count, Visited) VALUES('" + valiVaihe[0] + "', '" + str(
                    maara) + "', 0)"
                kursori = yhteys.cursor()
                kursori.execute(sql)
        return

    def ValitseAloitus(self):
        global nykySijainti
        asemat = "Valitse aloitusasema kirjoittamalla lentokentän icao-koodi:\n"
        for i in range(len(self.paikat)):
            valiVaihe = self.paikat[i]
            asemat += "Icao-koodi: " + valiVaihe[0] + ", nimi: " + valiVaihe[1] + ", maa: " + valiVaihe[2] + "\n"
        '''
        Tallenna tietokantaan muutokset
        '''
        print(asemat)
        aloitusAsema = input("Aloitusasema: ")
        nykySijainti = aloitusAsema
        '''Valloita(nykySijainti)'''
        return
    def GetLentokentanSotilaat(self, ident):
        sql = "SELECT Count FROM Troops WHERE Airport_ID = '" + ident + "'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()

        if kursori.rowcount > 0:
            for rivi in tulos:
                return rivi[0]
        return

    def SetLentokentanSotilaat(self, ident, maara):
        sql = "UPDATE Troops SET Count = '" + str(maara) + "' WHERE Airport_ID = '" + ident + "'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        return

    def LentokentanNimi(self, ident):
        sql = "SELECT name FROM airport WHERE ident = '" + ident + "'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()
        if kursori.rowcount > 0:
            for rivi in tulos:
                return str(rivi[0])
        return

    def Haekoordinaatit(self, ident):
        sql = "SELECT latitude_deg, longitude_deg FROM airport WHERE ident = '" + ident + "'"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        tulos = kursori.fetchall()
        if kursori.rowcount > 0:
            for rivi in tulos:
                return str(rivi[0]) + ", " + str(rivi[1])
        return