async function getdata(cadastro) {
  const response = await fetch("http://localhost:3000/api/medicos/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(cadastro)
  });

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || "Erro ao cadastrar médico.");
  }

  return data;
}

const form = document.getElementById("form_cadastro_medico");
form.addEventListener("submit", async function(event) {
  event.preventDefault();

  const dados = new FormData(form);
  const medico = {};

  for (let [chave, valor] of dados.entries()) {
    medico[chave] = valor;
  }

  try {
    await getdata(medico);
    window.location.href = "login.html";
  } catch (error) {
    alert(error.message);
  }
});
