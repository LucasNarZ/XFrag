async function getdata(login) {
    console.log(login)
  const response = await fetch("http://localhost:3000/api/auth/login", {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json" // informa que o corpo é JSON
    },
    body: JSON.stringify(login)
  });

  const data = await response.json(); // aguarda a resposta convertida em JSON
  console.log("Resposta da API:", data);
  return response.ok
}

const form = document.getElementById("login");
form.addEventListener("submit", async function(event) {
  event.preventDefault();

  const dados = new FormData(form);

  // Converte FormData em objeto simples
  const paciente = {};
  for (let [chave, valor] of dados.entries()) {
    paciente[chave] = valor;
  }

  // Envia para a API

  let ok = await getdata(paciente);
  if (ok){window.location.href = "dashboard.html"}



});
