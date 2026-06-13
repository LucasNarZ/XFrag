async function carregarNomeDoutor() {
  try {
    const response = await fetch("http://localhost:3000/api/auth/me", {
      credentials: "include"
    });
    
    if (!response.ok) throw new Error("Não foi possível autenticar o usuário.");
    
    const doutor = await response.json();

    // CORREÇÃO AQUI: Mudamos de "medicos" para "nome-doutor"
    const nomeDoutorEl = document.getElementById("nome-doutor");
    
    if (nomeDoutorEl && doutor.nome) {
      nomeDoutorEl.textContent = `Dr(a). ${doutor.nome}`;
    }
  } catch (erro) {
    console.error("Erro ao carregar os dados do doutor:", erro);
    
    // CORREÇÃO AQUI TAMBÉM: Atualizando o ID no bloco de erro
    const nomeDoutorEl = document.getElementById("nome-doutor");
    if (nomeDoutorEl) nomeDoutorEl.textContent = "Erro ao carregar";
  }
}

// Executa a função assim que o script for carregado
carregarNomeDoutor();