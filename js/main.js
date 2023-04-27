'use strict'

const sw = L.latLng(-90, -180), ne = L.latLng(90, 180);
const bounds = L.latLngBounds(sw, ne);
let aValittu = false;
const lataaja = document.getElementById("lataus");
const taisteluDialog = document.getElementById("taisteluDialog");

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
  evt.preventDefault();
  lataaja.style.display = "block";
  const nimi =document.querySelector("input[name=nimi]").value;
  const response = await fetch("http://127.0.0.1:5000/newGame/" + nimi);
  const jsonData = await response.json();
  lataaja.style.display = "none";
  console.log(jsonData);
  paikatKarttaan(jsonData);
}

async function getPelaajanTiedot() {
  const response = await fetch("http://127.0.0.1:5000/pelaajaTiedot");
  return await response.json();
}

async function lKenttaTiedot(icao) {
  const response = await fetch("http://127.0.0.1:5000/getPaikka/" + icao);
  return await response.json();
}

function paikatKarttaan(jsonData) {
  for(let i = 0; i < jsonData.length; i++) {
    const lat = jsonData[i].lat;
    const lon = jsonData[i].lon;
    console.log(jsonData[i].lat + ", " + jsonData[i].lon)
    const marker = L.marker([lat, lon]).addTo(map);
    marker.addEventListener("click", () => {lKenttaPopup(jsonData[i], marker)});
    markers.addLayer(marker);
  }
}

async function lKenttaPopup(lKentta, marker) {
  if(aValittu === true && await getPelaajanTiedot().sijainti === lKentta.icao) {
    const popup = document.createElement("article");
    const popupHeader = document.createElement("h2");
    const popupText = document.createElement("p");
    popupText.appendChild(document.createTextNode("Olet täällä"));

    popupHeader.appendChild(document.createTextNode(lKentta.nimi));
    popup.appendChild(popupHeader);
    popup.appendChild(popupText);

    marker.bindPopup(popup);

  } else if(aValittu === true && await getPelaajanTiedot().sijainti !== lKentta.icao && (await lKenttaTiedot(
      lKentta.icao)).valloitettu === false) {
    const etaisyys = (await lKenttaTiedot(lKentta.icao)).etaisyys;
    const popup = document.createElement("article");
    const popupHeader = document.createElement("h2");
    const etaisyysText = document.createElement("p");
    etaisyysText.appendChild(document.createTextNode("Etäisyys: " + etaisyys));
    const popupButton = document.createElement("button");
    popupButton.appendChild(document.createTextNode("Matkusta"));
    popupButton.addEventListener("click", () => {matkusta(marker, lKentta)});

    popupHeader.appendChild(document.createTextNode(lKentta.nimi));
    popup.appendChild(popupHeader);
    popup.appendChild(etaisyysText);
    popup.appendChild(popupButton);

    marker.bindPopup(popup);
  } else if(await getPelaajanTiedot().sijainti !== lKentta.icao && (await lKenttaTiedot(
      lKentta.icao)).valloitettu === true) {
    const popup = document.createElement("article");
    const popupHeader = document.createElement("h2");
    const popupText = document.createElement("p");
    popupText.appendChild(document.createTextNode("Valloitettu"));

    popupHeader.appendChild(document.createTextNode(lKentta.nimi));
    popup.appendChild(popupHeader);
    popup.appendChild(popupText);

    marker.bindPopup(popup);
  } else if(aValittu === false) {
    const popup = document.createElement("article");
    const popupHeader = document.createElement("h2");
    const popupButton = document.createElement("button");
    popupButton.appendChild(document.createTextNode("Valitse aloituspaikka"));
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
}

async function matkusta(marker, lKentta) {
  if(taistelu(lKentta)) {
    lataaja.style.display = "block";
    const response = await fetch("http://127.0.0.1:5000/matkusta/" + lKentta.icao);
    const jsonData = await response.json();
    console.log(jsonData);
    lataaja.style.display = "none";

    lKenttaPopup(lKentta, marker);
  } else {

  }
}

async function taistelu(lKentta) {

}

function osto(jsonData) {
  if("vastaus" in jsonData) {x
    console.log("ei onnistunut");
  } else {
    console.log("onnistui");
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