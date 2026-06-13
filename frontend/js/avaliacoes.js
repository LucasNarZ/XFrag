function Avaliacao(avaliacao) {

  return `
    <tr>
      <td>${avaliacao.paciente?.nome || "N/A"}</td>
      <td>${new Date(avaliacao.data_avaliacao).toLocaleDateString("pt-BR")}</td>
      <td>${Number(avaliacao.score_total).toFixed(2)}</td>
      <td>
        <span class="status ${avaliacao.recomendacao === "ENCAMINHAR" ? "warn" : "good"}">
          ${avaliacao.recomendacao === "ENCAMINHAR" ? "Encaminhar" : "Não encaminhar"}
        </span>
      </td>
      <td>
        <a class="btn secondary btn-ver-avaliacao" href="relatorio.html" data-id="${avaliacao.id}">
          Ver
        </a>
      </td>
    </tr>
  `;
}

async function carregarAvaliacoes() {
  const pacienteId = sessionStorage.getItem("paciente_id");

  if (!pacienteId) {
    alert("Nenhum paciente foi selecionado.");
    return;
  }

  try {
    const response = await fetch(
      `http://localhost:3000/api/pacientes/${pacienteId}/avaliacoes`,
      {
        method: "GET",
        credentials: "include",
        headers: {
          "Content-Type": "application/json"
        }
      }
    );

    if (!response.ok) {
      throw new Error(`Erro HTTP: ${response.status}`);
    }

    const avaliacoes = await response.json();
    const tbody = document.getElementById("tabela-avaliacoes");

    if (!tbody) return;

    if (avaliacoes.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" style="text-align: center;">Nenhuma avaliação encontrada para este paciente.</td></tr>`;
      return;
    }

    // Renderiza as linhas da tabela
    tbody.innerHTML = avaliacoes.map(avaliacao => Avaliacao(avaliacao)).join("");

    // Configura o evento de clique nos botões "Ver" de forma segura
    configurarEventosClique();

  } catch (error) {
    console.error("Erro ao carregar avaliações:", error);
    const tbody = document.getElementById("tabela-avaliacoes");
    if (tbody) {
      tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: red;">Erro ao carregar dados.</td></tr>`;
    }
  }
}

// Função para capturar o clique e salvar no sessionStorage
function configurarEventosClique() {
  const botoes = document.querySelectorAll(".btn-ver-avaliacao");
  botoes.forEach(botao => {
    botao.addEventListener("click", (e) => {
      const id = e.currentTarget.getAttribute("data-id");
      sessionStorage.setItem("avaliacao_id", id);
    });
  });
}

document.addEventListener("DOMContentLoaded", carregarAvaliacoes);