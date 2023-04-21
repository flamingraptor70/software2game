'use strict'

const nForm = document.getElementById("nameForm");
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

      article.appendChild(header)
      article.appendChild(p)

    paikatDiv.appendChild(article)
  }
}

nForm.addEventListener("submit", newGame);