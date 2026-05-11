from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.sintoma import Sintoma

SINTOMAS_SEED = [
    {
        "codigo": "DEFICIENCIA_INTELECTUAL",
        "descricao": "Deficiencia intelectual",
        "peso_m": Decimal("0.3200"),
        "peso_f": Decimal("0.2000"),
    },
    {
        "codigo": "FACE_ALONGADA_ORELHAS",
        "descricao": "Face alongada/orelhas",
        "peso_m": Decimal("0.2900"),
        "peso_f": Decimal("0.0900"),
    },
    {
        "codigo": "MACROORQUIDISMO",
        "descricao": "Macroorquidismo",
        "peso_m": Decimal("0.2600"),
        "peso_f": None,
    },
    {
        "codigo": "HIPERMOBILIDADE_ARTICULAR",
        "descricao": "Hipermobilidade articular",
        "peso_m": Decimal("0.1900"),
        "peso_f": Decimal("0.0400"),
    },
    {
        "codigo": "DIFICULDADES_APRENDIZAGEM",
        "descricao": "Dificuldades de aprendizagem",
        "peso_m": Decimal("0.1800"),
        "peso_f": Decimal("0.2800"),
    },
    {
        "codigo": "DEFICIT_ATENCAO",
        "descricao": "Deficit de atencao",
        "peso_m": Decimal("0.1700"),
        "peso_f": Decimal("0.1200"),
    },
    {
        "codigo": "MOVIMENTOS_REPETITIVOS",
        "descricao": "Movimentos repetitivos",
        "peso_m": Decimal("0.1700"),
        "peso_f": Decimal("0.0500"),
    },
    {
        "codigo": "ATRASO_FALA",
        "descricao": "Atraso na fala",
        "peso_m": Decimal("0.1400"),
        "peso_f": Decimal("0.0100"),
    },
    {
        "codigo": "HIPERATIVIDADE",
        "descricao": "Hiperatividade",
        "peso_m": Decimal("0.1200"),
        "peso_f": Decimal("0.0400"),
    },
    {
        "codigo": "EVITA_CONTATO_VISUAL",
        "descricao": "Evita contato visual",
        "peso_m": Decimal("0.0600"),
        "peso_f": Decimal("0.0800"),
    },
    {
        "codigo": "EVITA_CONTATO_FISICO",
        "descricao": "Evita contato fisico",
        "peso_m": Decimal("0.0400"),
        "peso_f": Decimal("0.0700"),
    },
    {
        "codigo": "AGRESSIVIDADE",
        "descricao": "Agressividade",
        "peso_m": Decimal("0.0100"),
        "peso_f": Decimal("0.0200"),
    },
]


async def seed_sintomas(session: AsyncSession) -> None:
    existing_codes = set(
        await session.scalars(
            select(Sintoma.codigo).where(
                Sintoma.codigo.in_(item["codigo"] for item in SINTOMAS_SEED)
            )
        )
    )
    for payload in SINTOMAS_SEED:
        if payload["codigo"] in existing_codes:
            continue
        session.add(Sintoma(**payload))
    await session.commit()


async def seed_sintomas_if_empty(session: AsyncSession) -> None:
    has_sintoma = await session.scalar(select(Sintoma.id).limit(1))

    if has_sintoma is None:
        await seed_sintomas(session)
