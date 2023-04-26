import json
import os

import mysql.connector
from flask import Flask, request
from flask_cors import CORS
from peli import Peli

app = Flask(__name__)
cors = CORS(app)
app.config["CORS_HEADERS"] = "content-type"

peli = Peli()
@app.route("/newGame/<pNimi>")
def newGame(pNimi):
    peli.LuoPeli(pNimi, 1000, 1000, 1000, 0)
    peli.ArvoPaikat()
    return peli.getPaikat()

@app.route("/vAloitus/<icao>")
def vAloitus(icao):
    peli.ValitseAloitus(icao)
    return peli.pelaajaTiedot()

@app.route("/paikat")
def paikat():
    return peli.getPaikat()

@app.route("/ostaPAine/<maara>")
def ostaPAine(maara):
    maara = float(maara)
    if peli.pelaaja.GetRaha() - maara / 2 >= 0:
        peli.ostaPolttoAinetta(maara)
        return peli.pelaajaTiedot()
    else:
        vastaus = {
            "vastaus": "Rahat eivät riitä ostokseen"
        }
        return vastaus

@app.route("/ostaSotilaita/<maara>")
def ostaSotilaita(maara):
    maara = float(maara)
    if peli.pelaaja.GetRaha() - maara * 2 >= 0:
        peli.ostaSotilaita(maara)
        return peli.pelaajaTiedot()
    else:
        vastaus = {
            "vastaus": "Rahat eivät riitä ostokseen"
        }
        return vastaus



if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=5000)
'''peli = Peli("Atte")

peli.ArvoPaikat()
peli.luoSotilaatLentokentille()
peli.Matkat()
peli.Kauppa()'''