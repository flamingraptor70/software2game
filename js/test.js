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

/*function tulostaPaikat(jsonData) {
  for(let i = 0; i < jsonData.length; i++) {
      const article = document.createElement("article");
      const header = document.createElement("h2");
      const hText = document.createTextNode(jsonData[i].nimi);
      header.appendChild(hText)
      const maaText = document.createTextNode("Maa: " + jsonData[i].maa + " ");
      const icao = document.createTextNode("Icao: " + jsonData[i].icao);

      const p = document.createElement("p");
      p.appendChild(maaText);
      p.appendChild(icao);

      article.appendChild(header);
      article.appendChild(p);

    paikatDiv.appendChild(article);
  }
}*/

const lkenttaDialog = document.getElementById("lKenttaTiedot");
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
  if(aValittu === true) {
    const popup = document.createElement("article");
    const popupHeader = document.createElement("h2");
    const popupButton = document.createElement("button");
    popupButton.appendChild(document.createTextNode("Matkusta"))
    //popupButton.addEventListener("click", () => {matkusta(lKentta.icao)})

    popupHeader.appendChild(document.createTextNode(lKentta.nimi));
    popup.appendChild(popupHeader);
    popup.appendChild(popupButton);

    marker.bindPopup(popup);
  } else {
    const popup = document.createElement("article");
    const popupHeader = document.createElement("h2");
    const popupButton = document.createElement("button");
    popupButton.appendChild(document.createTextNode("Valitse aloituspaikka"))
    popupButton.addEventListener("click", () => {aloitus(lKentta.icao)})

    popupHeader.appendChild(document.createTextNode(lKentta.nimi));
    popup.appendChild(popupHeader);
    popup.appendChild(popupButton);

    marker.bindPopup(popup);
  }
}

async function aloitus(icao) {
  const response = await fetch("http://127.0.0.1:5000/vAloitus/" + icao);
  const jsonData = await response.json();
  console.log(jsonData);
  aValittu = true
}

function matkusta(icao) {

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