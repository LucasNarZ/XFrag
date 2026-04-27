# Minimundo

O exame utilizado para confirmar o diagnóstico da Síndrome do X Frágil possui custo elevado, o que torna inviável a realização de testes em massa. Diante disso, existe a necessidade de identificar quais pessoas apresentam alta probabilidade de possuir a síndrome e, portanto, devem ser encaminhadas para o exame, e quais apresentam baixa probabilidade e podem não precisar dele em um primeiro momento.

Esse é o propósito do sistema. A aplicação deve permitir que um médico faça login, cadastre pacientes e registre os sintomas apresentados por cada um. Com base em uma tabela de pesos por sintoma, definida de forma específica para cada sexo, o sistema calcula um score para cada paciente. A partir desse score, é possível recomendar se o paciente deve ou não realizar o exame confirmatório.

O score do paciente deve ser calculado pela soma dos pesos correspondentes aos sintomas identificados, considerando o sexo informado no cadastro. Com esse resultado, o sistema pode classificar a probabilidade de o paciente possuir a Síndrome do X Frágil e apoiar a recomendação do exame confirmatório.

Os limiares validados para recomendação do exame são `0,56` para pacientes do sexo masculino e `0,55` para pacientes do sexo feminino. Sempre que a pontuação final for maior ou igual ao limiar correspondente, o paciente deve ser encaminhado para teste genético confirmatório.

A abordagem busca minimizar a perda de casos, com sensibilidade de `95%` em ambos os sexos. Como referência de desempenho diagnóstico, a área sob a curva (AUC) é de `0,73` para pacientes do sexo masculino e `0,76` para pacientes do sexo feminino.

Assim, o sistema atua como uma ferramenta de baixo custo para otimização de recursos, direcionando a realização do teste genético aos casos com maior probabilidade de confirmação.

Para permitir o processamento da triagem, os 12 sintomas devem ser convertidos em variáveis binárias, em que `1` representa sintoma presente e `0` representa sintoma ausente. A pontuação final de cada paciente deve ser calculada pela fórmula `Score = Σ (Peso_j x X_ij)`, em que `Peso_j` corresponde ao peso do sintoma e `X_ij` indica sua presença ou ausência para o paciente avaliado.

Com base nessa lógica, o sistema deve oferecer cadastro de paciente com informações como nome, sexo, idade e responsável, além de um formulário clínico interativo para registro dos 12 sintomas. Ao final do preenchimento, a aplicação deve calcular automaticamente a pontuação, comparar o resultado com o limiar correspondente ao sexo do paciente e indicar se há recomendação de encaminhamento para teste genético.

O sistema também deve permitir o cadastro de profissionais de saúde, com dados suficientes para identificação e controle de acesso, como nome, especialidade, registro profissional e credenciais de autenticação. Esse cadastro é necessário para vincular cada avaliação ao profissional responsável e garantir rastreabilidade no uso da ferramenta.

O sistema também deve manter histórico de avaliações e permitir a emissão de relatórios para profissionais de saúde, reforçando seu papel como ferramenta de apoio à decisão clínica, com baixo custo operacional e eficiência na priorização dos casos mais prováveis.

## Tabela de pesos

| Sintoma                      | Peso masculino | Peso feminino |
| ---------------------------- | -------------: | ------------: |
| Deficiência intelectual      |           0,32 |          0,20 |
| Face alongada/orelhas        |           0,29 |          0,09 |
| Macroorquidismo              |           0,26 |             - |
| Hipermobilidade articular    |           0,19 |          0,04 |
| Dificuldades de aprendizagem |           0,18 |          0,28 |
| Déficit de atenção           |           0,17 |          0,12 |
| Mov. repetitivos             |           0,17 |          0,05 |
| Atraso na fala               |           0,14 |          0,01 |
| Hiperatividade               |           0,12 |          0,04 |
| Evita contato visual         |           0,06 |          0,08 |
| Evita contato físico         |           0,04 |          0,07 |
| Agressividade                |           0,01 |          0,02 |

Para o sintoma `Macroorquidismo`, não há peso definido para pacientes do sexo feminino na tabela atual.

