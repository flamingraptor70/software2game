import json
import os

from flask import Flask
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
    peli.luoKysymykset()
    return peli.getPaikat()

@app.route("/vAloitus/<icao>")
def vAloitus(icao):
    peli.ValitseAloitus(icao)
    peli.luoSotilaatLentokentille()
    return peli.pelaajaTiedot()

@app.route("/getPaikka/<icao>")
def getPaikka(icao):
    return peli.getPaikka(icao)

@app.route("/matkusta/<icao>")
def matkusta(icao):
    peli.Matkusta(icao)
    return peli.pelaajaTiedot()

@app.route("/taisteluHyokkaykset/<omat>/<viholliset>")
def taisteluHyokkaykset(omat, viholliset):
    return peli.hyokkaykset(omat, viholliset)

@app.route("/pelaajanSotilaat/<sotilaat>")
def pelaajanSotilaat(sotilaat):
    peli.setPelaajanSotilaat(sotilaat)
    vastaus = {
        "vastaus": "tehty"
    }
    print(peli.pelaaja.GetSotilaat())
    return vastaus

@app.route("/lKentanSotilaat/<icao>/<sotilaat>")
def lKentanSotilaat(icao, sotilaat):
    peli.setLKentanSotilaat(icao, sotilaat)
    vastaus = {
        "vastaus": "tehty"
    }
    return vastaus
@app.route("/pelaajaTiedot")
def pelaajaTiedot():
    return peli.pelaajaTiedot()

@app.route("/ostaPAine/<maara>")
def ostaPAine(maara):
    maara = float(maara)
    if peli.pelaaja.GetRaha() - maara / 2 >= 0:
        peli.ostaPolttoAinetta(maara)
        return peli.pelaajaTiedot()
    else:
        vastaus = {
            "vastaus": "Not enough money"
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
            "vastaus": "Not enough money"
        }
        return vastaus

@app.route("/ongelma")
def ongelma():
    return peli.matemaattinenOngelma()

@app.route("/pelaajanRahat/<muutos>")
def pelaajanRahat(muutos):
    raha = peli.pelaajaTiedot().get("raha")
    raha += float(muutos)
    peli.pelaaja.SetRaha(raha)
    vastaus = {
        "vastaus": "Tehty"
    }
    return vastaus


if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=5000)
'''peli = Peli("Atte")

peli.ArvoPaikat()
peli.luoSotilaatLentokentille()
peli.Matkat()
peli.Kauppa()'''