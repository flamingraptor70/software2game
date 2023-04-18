from lentokentta import Lentokentta
from kauppa import Kauppa
from pelaaja import Pelaaja

class Peli():
    def __init__(self):


    def LuoPeli(self, pNimi, polttoAine, omatSotilaat, raha, score):
        sql = "INSERT INTO Game(Fuel, Money, Troops, User_name, Score) VALUES('" + str(polttoAine) + "', '" + str(
            raha) + "', '" + str(omatSotilaat) + "', '" + pNimi + "', '" + str(score) + "')"
        kursori = yhteys.cursor()
        kursori.execute(sql)
        global PeliID
        sql2 = "SELECT MAX(Game_ID) FROM Game WHERE User_name = '" + pNimi + "'"
        kursori = yhteys.cursor()
        kursori.execute(sql2)
        tulos = kursori.fetchall()

        if kursori.rowcount > 0:
            for rivi in tulos:
                PeliID = rivi[0]
        return