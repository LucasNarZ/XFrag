async function getdata(cadastro) {
    console.log(cadastro)
  const response = await fetch("http://localhost:3000/api/medicos", {
    method: "POST",
    headers: {
      "Content-Type": "application/json" // informa que o corpo é JSON
    },
    body: JSON.stringify(cadastro)
  });

  const data = await response.json(); // aguarda a resposta convertida em JSON
  console.log("Resposta da API:", data);
}
const form = document.getElementById("form_cadastro_medico");
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

  window.location.href = "login.html"
});
