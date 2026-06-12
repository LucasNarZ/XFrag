function formatarData(data) {
    return new Date(data).toLocaleDateString("pt-BR");
}

function formatarSexo(sexo) {
    if (sexo === "M") return "Masculino";
    if (sexo === "F") return "Feminino";

    return sexo;
}

function formatarRecomendacao(recomendacao) {
    if (recomendacao === "ENCAMINHAR") return "Encaminhar";
    if (recomendacao === "NAO_ENCAMINHAR") return "Não encaminhar";

    return recomendacao;
}

function classeRecomendacao(recomendacao) {
    return recomendacao === "ENCAMINHAR" ? "warn" : "good";
}

async function carregarRelatorio() {
    const avaliacaoId = sessionStorage.getItem("avaliacao_id");

    if (!avaliacaoId) {
        alert("Avaliação não informada.");
        window.location.href = "avaliacoes.html";
        return;
    }

    const response = await fetch(`http://localhost:3000/api/avaliacoes/${avaliacaoId}/relatorio`, {
        credentials: "include"
    });
    const relatorio = await response.json();

    if (!response.ok) {
        alert(relatorio.detail || "Erro ao carregar relatório.");
        return;
    }

    const heroPaciente = document.querySelector(".report-hero .eyebrow");
    const heroTitulo = document.querySelector(".report-hero h2");
    const heroMensagem = document.querySelector(".report-hero .muted");
    const score = document.querySelector(".score-ring");
    const cards = document.querySelectorAll(".grid.two .card");
    const dadosPaciente = cards[0].querySelectorAll("p");
    const resumo = cards[1].querySelectorAll("p");
    const sintomasPresentes = relatorio.sintomas ? relatorio.sintomas.filter((item) => item.presente).length : 0;
    const totalSintomas = relatorio.sintomas ? relatorio.sintomas.length : 0;
    const recomendacao = formatarRecomendacao(relatorio.recomendacao);
    const classe = classeRecomendacao(relatorio.recomendacao);

    heroPaciente.textContent = relatorio.paciente.nome;
    heroTitulo.textContent = `Recomendação: ${recomendacao}`;
    heroMensagem.textContent = relatorio.mensagem_recomendacao;
    score.textContent = Number(relatorio.score_total).toFixed(2);

    dadosPaciente[0].innerHTML = `<strong>Nome:</strong> ${relatorio.paciente.nome}`;
    dadosPaciente[1].innerHTML = `<strong>Nascimento:</strong> ${formatarData(relatorio.paciente.data_nascimento)}`;
    dadosPaciente[2].innerHTML = `<strong>Sexo:</strong> ${formatarSexo(relatorio.paciente.sexo)}`;
    dadosPaciente[3].innerHTML = `<strong>Responsável:</strong> ${relatorio.paciente.responsavel}`;

    resumo[0].innerHTML = `<strong>Sintomas presentes:</strong> ${sintomasPresentes} de ${totalSintomas}`;
    resumo[1].innerHTML = `<strong>Limite usado:</strong> ${Number(relatorio.limiar).toFixed(4)}`;
    resumo[2].innerHTML = `<strong>Resultado:</strong> <span class="status ${classe}">${recomendacao}</span>`;
}

carregarRelatorio();
