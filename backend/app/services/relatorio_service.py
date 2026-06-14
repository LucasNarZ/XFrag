from app.schemas.avaliacao import RelatorioAvaliacaoResponse
from app.schemas.medico import MedicoResumo
from app.schemas.paciente import PacienteResumo


class RelatorioService:
    @staticmethod
    def build_message(recomendacao: str) -> str:
        if recomendacao == "ENCAMINHAR":
            return "Paciente deve ser encaminhado para teste genetico confirmatorio."
        return "Paciente nao necessita encaminhamento para teste genetico confirmatorio neste momento."

    @classmethod
    def build(cls, avaliacao) -> RelatorioAvaliacaoResponse:
        paciente = PacienteResumo(
            id=avaliacao.paciente.id,
            nome=avaliacao.paciente.nome,
            data_nascimento=avaliacao.paciente.data_nascimento,
            sexo=avaliacao.paciente.sexo,
            responsavel=avaliacao.paciente.responsavel,
        )
        medico = MedicoResumo(
            id=avaliacao.medico.id,
            nome=avaliacao.medico.nome,
            crm=avaliacao.medico.crm,
            especialidade=avaliacao.medico.especialidade,
        )
        return RelatorioAvaliacaoResponse(
            avaliacao_id=avaliacao.id,
            paciente=paciente,
            medico=medico,
            data_avaliacao=avaliacao.data_avaliacao,
            score_total=avaliacao.score_total,
            limiar=avaliacao.limiar,
            recomendacao=avaliacao.recomendacao,
            mensagem_recomendacao=cls.build_message(avaliacao.recomendacao),
            observacoes=avaliacao.observacoes,
            sintomas=avaliacao.sintomas,
        )
