'use strict'

const nForm = document.getElementById("nameForm");
const aloitusPaikkaForm = document.getElementById("aPForm");
const pAineForm = document.getElementById("ostaPAineForm");
const sotilasForm = document.getElementById("ostaSotilaitaForm");
const paikatDiv = document.getElementById("paikatDiv");

async function newGame(evt) {
  evt.preventDefault();
  const nimi =document.querySelector("input[name=nimi]").value;
  const response = await fetch("http://127.0.0.1:5000/newGame/" + nimi);
  const jsonData = await response.json();
  console.log(jsonData);
  tulostaPaikat(jsonData);
}

function tulostaPaikat(jsonData) {
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
}

async function aloitusPaikka(evt) {
  evt.preventDefault();
  const aPaikka =document.querySelector("input[name=aPaikka]").value;
  const response = await fetch("http://127.0.0.1:5000/vAloitus/" + aPaikka);
  const jsonData = await response.json();
  console.log(jsonData);
}

async function ostaPolttoAine(evt) {
  evt.preventDefault();
  const maara = document.querySelector("input[name=pAineMaara]").value;
  const response = await fetch("http://127.0.0.1:5000/ostaPAine/" + maara);
  const jsonData = await response.json();
  console.log(jsonData);
  osto(jsonData);
}

function osto(jsonData) {
  if("vastaus" in jsonData) {
    console.log("ei onnistunut");
  } else {
    console.log("onnistui");
  }
}

async function ostaSotilaita(evt) {
  evt.preventDefault();
  const maara = document.querySelector("input[name=sotilasMaara]").value;
  const response = await fetch("http://127.0.0.1:5000/ostaSotilaita/" + maara);
  const jsonData = await response.json();
  console.log(jsonData);
}

nForm.addEventListener("submit", newGame);
aloitusPaikkaForm.addEventListener("submit", aloitusPaikka);
pAineForm.addEventListener("submit", ostaPolttoAine);
sotilasForm.addEventListener("submit", ostaSotilaita);