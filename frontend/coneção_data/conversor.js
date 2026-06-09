// Função genérica para enviar dados de um formulário
function enviarFormulario(form, url) {
  form.addEventListener("submit", async function(event) {
    event.preventDefault();

    // Captura os dados do formulário
    const dados = new FormData(form);

    // Converte para objeto simples
    const objeto = {};
    for (let [chave, valor] of dados.entries()) {
      objeto[chave] = valor;
    }

    try {
      // Faz a requisição POST
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(objeto)
      });

      // Converte a resposta em JSON
      const data = await response.json();
      console.log("Resposta da API:", data);
    } catch (erro) {
      console.error("Erro ao enviar:", erro);
    }
  });
}

