// 1. Função genérica para enviar os dados para a API
async function enviarDados(url, dados) {
  try {
    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json" // informa que o corpo é JSON
      },
      body: JSON.stringify(dados)
    });
    
    const data = await response.json(); // aguarda a resposta convertida em JSON
    return data;
  } catch (erro) {
    console.error("Erro na requisição:", erro);
    throw erro; // Repassa o erro para ser tratado por quem chamou
  }
}

// 2. Função principal que configura o formulário
function configurarFormulario(idFormulario, urlApi, urlRedirecionamento) {
  const form = document.getElementById(idFormulario);

  // Verifica se o formulário realmente existe na página
  if (!form) {
    console.error(`Formulário com ID "${idFormulario}" não encontrado.`);
    return;
  }

  // Adiciona o evento de 'submit' (envio)
  form.addEventListener("submit", async function(event) {
    event.preventDefault(); // Evita que a página recarregue

    const dados = new FormData(form);
    const cadastro = {};

    // Converte FormData em objeto simples
    for (let [chave, valor] of dados.entries()) {
      cadastro[chave] = valor;
    }

    try {
      console.log("Enviando dados:", cadastro);
      
      // Envia para a API e AGUARDA a resposta (await)
      const respostaApi = await enviarDados(urlApi, cadastro);
      console.log("Resposta da API:", respostaApi);

      // Redireciona APÓS o envio dar certo
      if (urlRedirecionamento) {
        window.location.href = urlRedirecionamento;
      }
    } catch (erro) {
      alert("Falha ao realizar o cadastro. Tente novamente.");
    }
  });
}