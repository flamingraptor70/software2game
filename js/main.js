'use strict'

const sw = L.latLng(-90, -180), ne = L.latLng(90, 180);
const bounds = L.latLngBounds(sw, ne);
let aValittu = false;
let tiedotLadattu = false;
const lataaja = document.getElementById("lataus");
const taisteluDialog = document.getElementById("taisteluDialog");
//const kysymysDialog = document.getElementById("kysymysDialog");
const loppuDialog = document.getElementById("loppuDialog");
const lKentat = []
let latamassaTietoja = false;

const map = L.map('map', { tap: false });
L.tileLayer('https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', {
  noWrap: true,
  bounds: [
    [-90, -180],
    [90, 180]
  ],
  minZoom: 4,
  maxZoom: 20,
  subdomains: ['mt0', 'mt1', 'mt2', 'mt3'],
}).addTo(map);
map.setView([60, 24], 7);
const markers = L.featureGroup().addTo(map);
map.setMaxBounds(bounds);

const nForm = document.getElementById("nameForm");
const pAineForm = document.getElementById("ostaPAineForm");
const sotilasForm = document.getElementById("ostaSotilaitaForm");

async function newGame(evt) {
  if(!latamassaTietoja && tiedotLadattu === false) {
    evt.preventDefault();
    tiedotLadattu = true;
    latamassaTietoja = true;
    lataaja.style.display = "block";
    const nimi =document.querySelector("input[name=nimi]").value;
    const response = await fetch("http://127.0.0.1:5000/newGame/" + nimi);
    const jsonData = await response.json();
    paivitaTiedot();
    lataaja.style.display = "none";
    console.log(jsonData);
    paikatKarttaan(jsonData);
  }
}

async function getPelaajanTiedot() {
  const response = await fetch("http://127.0.0.1:5000/pelaajaTiedot");
  return await response.json();
}

async function lKenttaTiedot(icao) {
  const response = await fetch("http://127.0.0.1:5000/getPaikka/" + icao);
  return await response.json();
}

async function paivitaTiedot() {
  const pelaaja = await getPelaajanTiedot();

  document.getElementById("pelaajaNimi").innerHTML = "";
  document.getElementById("balance").innerHTML = "";
  document.getElementById("fuel").innerHTML = "";
  document.getElementById("soldiers").innerHTML = "";

  document.getElementById("pelaajaNimi").appendChild(document.createTextNode(pelaaja.nimi));
  document.getElementById("balance").appendChild(document.createTextNode(pelaaja.raha));
  document.getElementById("fuel").appendChild(document.createTextNode(pelaaja.pAine));
  document.getElementById("soldiers").appendChild(document.createTextNode(pelaaja.sotilaat));
}

function paivitaValloitus() {
  let arvo = document.getElementById("countries").innerHTML;
  console.log(arvo);
  arvo = parseInt(arvo) + 1
  document.getElementById("countries").innerHTML = "";
  document.getElementById("countries").appendChild(document.createTextNode((arvo).toString()));
}

function paikatKarttaan(jsonData) {
  for(let i = 0; i < jsonData.length; i++) {
    lKentat.push(jsonData[i].icao);
    const lat = jsonData[i].lat;
    const lon = jsonData[i].lon;
    console.log(jsonData[i].lat + ", " + jsonData[i].lon)
    const marker = L.marker([lat, lon]).addTo(map);
    marker.addEventListener("click", () => {lKenttaPopup(jsonData[i], marker)});
    markers.addLayer(marker);
  }
  latamassaTietoja = false;
}

async function lKenttaPopup(lKentta, marker) {
  const pelaaja = await getPelaajanTiedot();
  if(aValittu === true && pelaaja.sijainti === lKentta.icao) {
    const popup = document.createElement("article");
    const popupHeader = document.createElement("h2");
    const popupText = document.createElement("p");
    popupText.appendChild(document.createTextNode("You are here"));

    popupHeader.appendChild(document.createTextNode(lKentta.nimi));
    popup.appendChild(popupHeader);
    popup.appendChild(popupText);

    marker.bindPopup(popup);

  } else if(aValittu === true && pelaaja.sijainti !== lKentta.icao && (await lKenttaTiedot(
      lKentta.icao)).valloitettu === false) {
    lKentta = await lKenttaTiedot(lKentta.icao);
    const etaisyys = lKentta.etaisyys;
    const sotilaat = lKentta.sotilaat;
    const popup = document.createElement("article");
    const popupHeader = document.createElement("h2");
    const etaisyysText = document.createElement("p");
    const sotilasText = document.createElement("p");
    sotilasText.appendChild(document.createTextNode("Airports soldiers: " + sotilaat));
    etaisyysText.appendChild(document.createTextNode("Distance: " + etaisyys));
    const popupButton = document.createElement("button");
    popupButton.appendChild(document.createTextNode("Travel"));
    popupButton.addEventListener("click", () => {matkusta(marker, lKentta)});

    popupHeader.appendChild(document.createTextNode(lKentta.nimi));
    popup.appendChild(popupHeader);
    popup.appendChild(sotilasText);
    popup.appendChild(etaisyysText);
    popup.appendChild(popupButton);

    marker.bindPopup(popup);
  } else if(pelaaja.sijainti !== lKentta.icao && (await lKenttaTiedot(
      lKentta.icao)).valloitettu === true) {
    const popup = document.createElement("article");
    const popupHeader = document.createElement("h2");
    const popupText = document.createElement("p");
    popupText.appendChild(document.createTextNode("Conquered"));

    popupHeader.appendChild(document.createTextNode(lKentta.nimi));
    popup.appendChild(popupHeader);
    popup.appendChild(popupText);

    marker.bindPopup(popup);
  } else if(aValittu === false) {
    const popup = document.createElement("article");
    const popupHeader = document.createElement("h2");
    const popupButton = document.createElement("button");
    popupButton.appendChild(document.createTextNode("Choose starting location"));
    popupButton.addEventListener("click", () => {aloitus(marker, lKentta)});

    popupHeader.appendChild(document.createTextNode(lKentta.nimi));
    popup.appendChild(popupHeader);
    popup.appendChild(popupButton);

    marker.bindPopup(popup);
  }
}

async function aloitus(marker, lKentta) {
  lataaja.style.display = "block";
  const response = await fetch("http://127.0.0.1:5000/vAloitus/" + lKentta.icao);
  const jsonData = await response.json();
  console.log(jsonData);
  aValittu = true;
  lataaja.style.display = "none";

  lKenttaPopup(lKentta, marker);
  paivitaTiedot();
  paivitaValloitus();
  await voittoTarkistus();
}

async function kysymys() {
  const response = await fetch("http://127.0.0.1:5000/ongelma");
  const vastausJson = await response.json();
  const dialog = document.getElementById("kysymysDialog");
  document.getElementById("vT").textContent = "";
  document.getElementById("cB").style.display = "none";

  /*const dHeader = document.createElement("h2");
  dHeader.appendChild(document.createTextNode("Question:"));*/

  const qForm = document.getElementById("qForm");
  qForm.innerHTML = "";
  //qForm.onsubmit = false
  const kysymys = document.createElement("p");
  kysymys.appendChild(document.createTextNode(vastausJson.kysymys));
  const vastaus = document.createElement("input");
  vastaus.name = "qAnswer";
  vastaus.type = "text";
  const submit = document.createElement("input");
  submit.type = "submit";
  submit.value = "submit";

  qForm.appendChild(kysymys);
  qForm.appendChild(vastaus);
  qForm.appendChild(submit);

  qForm.addEventListener("submit", function eventHandler() {
    kysymyksenTarkistus(vastausJson.vastaus, dialog);
    this.removeEventListener("submit", eventHandler);
  });

  //dialog.appendChild(dHeader);
  dialog.appendChild(qForm);
  dialog.showModal();
}

async function kysymyksenTarkistus(oikeaVastaus, dialog) {
  /*const closeButton = document.createElement("button");
  closeButton.appendChild(document.createTextNode("close"));*/
  const closeButton = document.getElementById("cB");
  closeButton.addEventListener("click", function() {
    dialog.close();
  });

  const vastaus = document.querySelector("input[name=qAnswer]").value;
  const vastausText = document.getElementById("vT");

  if(vastaus === oikeaVastaus) {
    vastausText.appendChild(document.createTextNode("Correct answer. You get 1000€"));
    await fetch("http://127.0.0.1:5000/pelaajanRahat/" + 1000);
    paivitaTiedot();
    voittoTarkistus();
  } else {
    vastausText.appendChild(document.createTextNode("Incorrect answer"));
    voittoTarkistus();
  }

  dialog.appendChild(vastausText);
  document.getElementById("cB").style.display = "block";
  //dialog.appendChild(closeButton);
}

async function matkusta(marker, lKentta) {
  lKentta = await lKenttaTiedot(lKentta.icao);
  const pelaaja = await getPelaajanTiedot();

  if(lKentta.etaisyys > pelaaja.pAine) {

    const popup = document.createElement("article");
    const popupText = document.createElement("p");
    popupText.appendChild(document.createTextNode("Not enough fuel"));
    popup.appendChild(popupText);

    marker.bindPopup(popup);
  } else {
    const paaseeko = await taistelu(lKentta.icao)
    console.log(paaseeko)
    if(paaseeko === true) {
      await fetch("http://127.0.0.1:5000/matkusta/" + lKentta.icao);
      kysymys();
      lKenttaPopup(lKentta, marker);
      paivitaTiedot();
      paivitaValloitus();
      //await voittoTarkistus();

    } else {
      paivitaTiedot();
      await voittoTarkistus();
      const popup = document.createElement("article");
      const popupText = document.createElement("p");
      popupText.appendChild(document.createTextNode("Lost battle"));
      popup.appendChild(popupText);

      marker.bindPopup(popup);
    }
  }
}

const timer = ms => new Promise(res => setTimeout(res, ms));
async function taistelu(icao) {
  const pelaaja = await getPelaajanTiedot();
  const lKentta = await lKenttaTiedot(icao);

  console.log(pelaaja)

  let omatSotilaat = parseInt(pelaaja.sotilaat, 10);
  let viholliset = parseInt(lKentta.sotilaat, 10);

  console.log("Omat: " + omatSotilaat, " viholliset: " + viholliset)

  if(omatSotilaat > 0) {
    taisteluDialog.showModal();
    while(true) {
      console.log("http://127.0.0.1:5000/taisteluHyokkaykset/" + omatSotilaat + "/" + viholliset)
      const response = await fetch("http://127.0.0.1:5000/taisteluHyokkaykset/" + omatSotilaat + "/" + viholliset);
      const hyokkaykset = await response.json();
      console.log(hyokkaykset)
      document.getElementById("taisteluText").innerHTML = "";
      const tText = document.createTextNode("My soldiers: " + omatSotilaat + " -" + hyokkaykset.vihollisenHyokkays + "\nEnemy soldiers: " + viholliset + " -" + hyokkaykset.omaHyokkays);
      document.getElementById("taisteluText").appendChild(tText);

      omatSotilaat =  omatSotilaat - parseInt(hyokkaykset.vihollisenHyokkays, 10);
      viholliset = viholliset - parseInt(hyokkaykset.omaHyokkays, 10);

      await timer(1000);

      if(omatSotilaat <= 0) {
        omatSotilaat = 0;

        if(viholliset <= 0) {
          viholliset = 0;
        }

        document.getElementById("taisteluText").innerHTML = "";
        const tText = document.createTextNode("My soldiers: " + omatSotilaat + " -" + hyokkaykset.vihollisenHyokkays + "\nEnemy soldiers: " + viholliset + " -" + hyokkaykset.omaHyokkays);
        document.getElementById("taisteluText").appendChild(tText);

        await fetch("http://127.0.0.1:5000/pelaajanSotilaat/" + omatSotilaat);
        await fetch("http://127.0.0.1:5000/lKentanSotilaat/" + icao + "/" + viholliset);

        await timer(1000);
        taisteluDialog.close();
        return false;
      } else if(viholliset <= 0) {
        viholliset = 0;

        document.getElementById("taisteluText").innerHTML = "";
        const tText = document.createTextNode("My soldiers: " + omatSotilaat + " -" + hyokkaykset.vihollisenHyokkays + "\nEnemy soldiers: " + viholliset + " -" + hyokkaykset.omaHyokkays);
        document.getElementById("taisteluText").appendChild(tText);

        await fetch("http://127.0.0.1:5000/pelaajanSotilaat/" + omatSotilaat);
        await fetch("http://127.0.0.1:5000/lKentanSotilaat/" + icao + "/" + viholliset);

        await timer(1000);
        taisteluDialog.close();
        return true;
      }
    }
  } else {
    return false;
  }
}

async function voittoTarkistus() {
  let voititko = true;
  for(let i = 0; i < lKentat.length; i++){
    const lKentta = await lKenttaTiedot(lKentat[i]);
    if(lKentta.valloitettu === false) {
      voititko = false
    }
  }
  if(voititko === true) {
    console.log("Peli voitettu");
    voitto()
  } else {
    havinnytTarkistus();
  }
}

async function havinnytTarkistus() {
  const pelaaja = await getPelaajanTiedot();


  if(pelaaja.raha < 2) {
    if(pelaaja.sotilaat < 1) {
      console.log("Hävinnyt");
      havio();
    }
  }
  console.log("Tarkistamassa häviötä")
  let lahin = "";

  for(let i = 0; i < lKentat.length; i++) {
    const lKentta = await lKenttaTiedot(lKentat[i]);
    if(lKentta.ident !== pelaaja.sijainti && lKentta.valloitettu === false) {
      if(lahin === "") {
        lahin = lKentta;
      } else if(lahin.etaisyys > lKentta.etaisyys) {
        lahin = lKentta;
      }
    }
  }

  const maxPolttoAine = pelaaja.pAine + (pelaaja.raha * 2);

  if(lahin.etaisyys > maxPolttoAine) {
    console.log("Hävinnyt");
    havio();
  }
}

function voitto() {
  loppuDialog.getElementsByTagName("h2")[0].appendChild(document.createTextNode("You won"));
  loppuDialog.getElementsByTagName("button")[0].addEventListener("click", uusiPeli);
  loppuDialog.showModal();
}

function havio() {
  loppuDialog.getElementsByTagName("h2")[0].appendChild(document.createTextNode("You lost"));
  loppuDialog.getElementsByTagName("button")[0].addEventListener("click", uusiPeli);
  loppuDialog.showModal();
}

function uusiPeli() {
  loppuDialog.close();
  location.reload();
  return false;
}

function osto(jsonData) {
  if("vastaus" in jsonData) {
    console.log("ei onnistunut");
  } else {
    console.log("onnistui");
    paivitaTiedot();
    havinnytTarkistus();
  }
}

async function ostaPolttoAine(evt) {
  evt.preventDefault();
  const maara = document.querySelector("input[name=pAineMaara]").value;
  const response = await fetch("http://127.0.0.1:5000/ostaPAine/" + maara);
  const jsonData = await response.json();
  console.log(jsonData);
  osto(jsonData);
}

async function ostaSotilaita(evt) {
  evt.preventDefault();
  const maara = document.querySelector("input[name=sotilasMaara]").value;
  const response = await fetch("http://127.0.0.1:5000/ostaSotilaita/" + maara);
  const jsonData = await response.json();
  console.log(jsonData);
  osto(jsonData);
}

nForm.addEventListener("submit", newGame);
pAineForm.addEventListener("submit", ostaPolttoAine);
sotilasForm.addEventListener("submit", ostaSotilaita);