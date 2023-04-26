'use strict'

const sw = L.latLng(-90, -180), ne = L.latLng(90, 180);
const bounds = L.latLngBounds(sw, ne);
let aValittu = false;

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
const aloitusPaikkaForm = document.getElementById("aPForm");
const pAineForm = document.getElementById("ostaPAineForm");
const sotilasForm = document.getElementById("ostaSotilaitaForm");

async function newGame(evt) {
  evt.preventDefault();
  const nimi =document.querySelector("input[name=nimi]").value;
  const response = await fetch("http://127.0.0.1:5000/newGame/" + nimi);
  const jsonData = await response.json();
  console.log(jsonData);
  paikatKarttaan(jsonData);
}

async function getPelaajanArvot() {
  const response = await fetch("http://127.0.0.1:5000/pelaajaTiedot");
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

function lKenttaPopup(lKentta, marker) {
  if(aValittu === true && getPelaajanArvot().sijainti !== lKentta.icao) {
    console.log("Ei tänne")
    const popup = document.createElement("article");
    const popupHeader = document.createElement("h2");
    const popupButton = document.createElement("button");
    popupButton.appendChild(document.createTextNode("Matkusta"))
    //popupButton.addEventListener("click", () => {matkusta(lKentta.icao)})

    popupHeader.appendChild(document.createTextNode(lKentta.nimi));
    popup.appendChild(popupHeader);
    popup.appendChild(popupButton);

    marker.bindPopup(popup);
  } else if(aValittu === true && getPelaajanArvot().sijainti === lKentta.icao) {
    console.log("tänne")
    const popup = document.createElement("article");
    const popupHeader = document.createElement("h2");
    const popupText = document.createElement("p");
    popupText.appendChild(document.createTextNode("Olet täällä"));

    popupHeader.appendChild(document.createTextNode(lKentta.nimi));
    popup.appendChild(popupHeader);
    popup.appendChild(popupText);

    marker.bindPopup(popup);
  } else {
    const popup = document.createElement("article");
    const popupHeader = document.createElement("h2");
    const popupButton = document.createElement("button");
    popupButton.appendChild(document.createTextNode("Valitse aloituspaikka"))
    popupButton.addEventListener("click", () => {aloitus(marker, lKentta)})

    popupHeader.appendChild(document.createTextNode(lKentta.nimi));
    popup.appendChild(popupHeader);
    popup.appendChild(popupButton);

    marker.bindPopup(popup);
  }
}

async function aloitus(marker, lKentta) {
  const response = await fetch("http://127.0.0.1:5000/vAloitus/" + lKentta.icao);
  const jsonData = await response.json();
  console.log(jsonData);
  aValittu = true;

  lKenttaPopup(lKentta, marker);
}

async function matkusta(icao) {

}

async function aloitusPaikka(evt) {
  evt.preventDefault();
  const aPaikka =document.querySelector("input[name=aPaikka]").value;
  const response = await fetch("http://127.0.0.1:5000/vAloitus/" + aPaikka);
  const jsonData = await response.json();
  console.log(jsonData);
}

function osto(jsonData) {
  if("vastaus" in jsonData) {
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
aloitusPaikkaForm.addEventListener("submit", aloitusPaikka);
pAineForm.addEventListener("submit", ostaPolttoAine);
sotilasForm.addEventListener("submit", ostaSotilaita);