async function getdata(avaliacoes) {
    console.log(avaliacoes)
  const response = await fetch("http://localhost:3000/api/pacientes/{paciente_id}/avaliacoes", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json" // informa que o corpo é JSON
    },
    body: JSON.stringify(avaliacoes)
  });

  const data = await response.json(); // aguarda a resposta convertida em JSON
  console.log("Resposta da API:", data);
  return response.ok
}

const form = document.getElementById("avaliacao_form");
form.addEventListener("submit", async function(event) {
  event.preventDefault();

  const dados = new FormData(form);

  // Converte FormData em objeto simples
  const avliacoes = {};
  for (let [chave, valor] of dados.entries()) {
    avliacoes[chave] = valor;
  }

  // Envia para a API

  let ok = await getdata(avliacoes);
  if (ok){window.location.href = "dashboard.html"}



});

