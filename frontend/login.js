async function getdata(login) {
    console.log(login)
  const response = await fetch("http://localhost:3000/api/auth/login", {
    method: "POST",
    headers: {
      "Content-Type": "application/json" // informa que o corpo é JSON
    },
    body: JSON.stringify(login)
  });

  const data = await response.json(); // aguarda a resposta convertida em JSON
  console.log("Resposta da API:", data);
}
const form = document.getElementById("login");
form.addEventListener("submit", function(event) {
  event.preventDefault();

  const dados = new FormData(form);

  // Converte FormData em objeto simples
  const paciente = {};
  for (let [chave, valor] of dados.entries()) {
    paciente[chave] = valor;
  }

  // Envia para a API
  getdata(paciente);

  window.location.href = "dashboard.html"
});
