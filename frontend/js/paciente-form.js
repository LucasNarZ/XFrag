async function getdata(paciente) {
    console.log(paciente)
  const response = await fetch("http://localhost:3000/api/pacientes/", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json" // informa que o corpo é JSON
    },
    body: JSON.stringify(paciente)
  });

  const data = await response.json(); // aguarda a resposta convertida em JSON
  console.log("Resposta da API:", data);
  return response.ok
}

const form = document.getElementById("paciente_form");
form.addEventListener("submit", async function(event) {
  event.preventDefault();

  const dados = new FormData(form);

  // Converte FormData em objeto simples
  const paciente = {};
  for (let [chave, valor] of dados.entries()) {
    paciente[chave] = valor;
  }
  paciente.sexo = paciente.sexo[0]
  // Envia para a API

  let ok = await getdata(paciente);
  if (ok){window.location.href = "dashboard.html"}



});

