function formatarData(data) {
  return new Date(`${data}T00:00:00`).toLocaleDateString("pt-BR");
}

function formatarSexo(sexo) {
  if (sexo === "M") return "Masculino";
  if (sexo === "F") return "Feminino";

  return sexo;
}

function Paciente(paciente) {
  return `
    <tr>
      <td>${paciente.nome}</td>
      <td>${formatarData(paciente.data_nascimento)}</td>
      <td>${formatarSexo(paciente.sexo)}</td>
      <td>${paciente.responsavel}</td>
      <td><span class="status good">Sem avaliação</span></td>
      <td><a class="btn secondary" href="avaliacao.html">Avaliar</a></td>
    </tr>
  `;
}

async function carregarPacientes() {
  const tbody = document.querySelector("tbody");
  if (!tbody) return;

  const response = await fetch("http://localhost:3000/api/pacientes/", {
    credentials: "include"
  });
  const pacientes = await response.json();

  const avaliacoesResponse = await fetch("http://localhost:3000/api/avaliacoes", {
    credentials: "include"
  });
  const avaliacoes = await avaliacoesResponse.json();
  const metricas = document.querySelectorAll(".metric-number");

  tbody.innerHTML = pacientes.map(Paciente).join("");

  metricas[0].textContent = pacientes.length;
  metricas[1].textContent = avaliacoes.length;
  metricas[2].textContent = avaliacoes.filter((avaliacao) => avaliacao.recomendacao === "ENCAMINHAR").length;
}

carregarPacientes();
