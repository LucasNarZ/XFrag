function formatarData(data) {
    return new Date(`${data}T00:00:00`).toLocaleDateString("pt-BR");
}

function formatarSexo(sexo) {
    if (sexo === "M") return "Masculino";
    if (sexo === "F") return "Feminino";

    return sexo;
}

async function getdata(avaliacao, pacienteId) {
    console.log(avaliacao);

    const response = await fetch(`http://localhost:3000/api/pacientes/${pacienteId}/avaliacoes`, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(avaliacao)
    });

    const data = await response.json();
    console.log("Resposta da API:", data);

    if (!response.ok) {
        alert(data.detail || "Erro ao criar avaliação.");
        return false;
    }

    return data;
}

async function carregarSintomas() {
    const response = await fetch("http://localhost:3000/api/sintomas/", {
        credentials: "include"
    });
    const sintomas = await response.json();
    const checkboxes = document.querySelectorAll("input[data-symptom]");

    checkboxes.forEach((checkbox) => {
        const texto = checkbox.closest("label").textContent;
        const resultado = texto.match(/Código:\s*([A-Z_]+)/);
        const codigo = resultado ? resultado[1] : "";
        const sintoma = sintomas.find((item) => item.codigo === codigo);

        checkbox.name = "sintomas";
        checkbox.value = sintoma ? sintoma.codigo : codigo;
    });

    return sintomas;
}

async function carregarPaciente(pacienteId) {
    const response = await fetch(`http://localhost:3000/api/pacientes/${pacienteId}`, {
        credentials: "include"
    });
    const paciente = await response.json();

    const campos = document.querySelectorAll(".patient-inline-card span");
    campos[0].textContent = paciente.nome;
    campos[1].textContent = formatarSexo(paciente.sexo);
    campos[2].textContent = `Nascimento: ${formatarData(paciente.data_nascimento)}`;
}

function atualizarPrevia() {
    const sintomas = document.querySelectorAll("input[data-symptom]");
    const selecionados = document.querySelectorAll("input[data-symptom]:checked");
    const contador = document.querySelector("[data-selected-count]");

    contador.textContent = `${selecionados.length} de ${sintomas.length}`;
}

async function iniciarPagina() {
    const params = new URLSearchParams(window.location.search);
    const pacienteId = params.get("paciente_id") || sessionStorage.getItem("paciente_id");
    const form = document.querySelector("form");

    if (!pacienteId) {
        alert("Paciente não informado.");
        return;
    }

    carregarPaciente(pacienteId);
    const sintomas = await carregarSintomas();

    form.addEventListener("change", function(event) {
        if (event.target.matches("input[data-symptom]")) {
            atualizarPrevia();
        }
    });

    form.addEventListener("submit", async function(event) {
        event.preventDefault();

        const dados = new FormData(form);
        const selecionados = dados.getAll("sintomas");
        const avaliacao = {
            sintomas: sintomas.map((sintoma) => ({
                codigo: sintoma.codigo,
                presente: selecionados.includes(sintoma.codigo) ? 1 : 0
            })),
            observacoes: dados.get("observacoes")
        };

        const resultado = await getdata(avaliacao, pacienteId);

        if (resultado) {
            window.location.href = `relatorio.html?avaliacao_id=${resultado.id}`;
        }
    });
}

iniciarPagina();
