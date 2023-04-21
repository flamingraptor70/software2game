'use strict'

const form = document.getElementById("nameForm")

async function newGame(evt) {
  evt.preventDefault()
  const nimi =document.querySelector("input[name=nimi]").value
  const response = await fetch("http://127.0.0.1:5000/newGame/" + nimi)
  const jsonData = await response.json()
  console.log(jsonData)
}

form.addEventListener("submit", newGame)