# Backend do XFrag

Este backend é a parte do sistema responsável por receber pedidos do frontend, validar as informações, consultar ou salvar dados no banco e devolver uma resposta.

Ele foi feito com FastAPI, uma ferramenta de Python usada para criar APIs. Uma API é como uma ponte: o frontend pede algo, o backend processa esse pedido e responde com os dados ou com uma mensagem de erro.

Para instalar e rodar o projeto, é necessário ter o `uv` instalado. Ele é uma ferramenta externa usada para gerenciar dependências e executar projetos Python. Se você ainda não tiver o `uv` instalado, veja a documentação oficial: <https://docs.astral.sh/uv/>

## O Que Este Backend Faz

O sistema trabalha principalmente com médicos, pacientes, sintomas e avaliações.

De forma simples, o fluxo principal é:

1. Um médico cria uma conta.
2. O médico faz login com email e senha.
3. Depois do login, o backend cria uma sessão para esse médico.
4. O médico cadastra e consulta seus pacientes.
5. O médico consulta a lista de sintomas disponíveis.
6. O médico cria uma avaliação para um paciente, marcando os sintomas como presentes ou ausentes.
7. O backend calcula uma pontuação e informa se a recomendação é encaminhar ou não encaminhar.
8. O médico pode consultar um relatório da avaliação.

## Tecnologias Usadas

- Python: linguagem usada no backend.
- FastAPI: framework usado para criar as rotas da API.
- SQLAlchemy: ferramenta usada para conversar com o banco de dados.
- Pydantic: ferramenta usada para validar os dados que entram e saem da API.
- Argon2: usado para proteger senhas, salvando apenas uma versão criptografada delas.
- Uvicorn: servidor usado para rodar a API localmente.
- uv: ferramenta externa usada para instalar dependências e executar comandos do projeto.

## Como Rodar o Backend

Entre na pasta do backend:

```bash
cd backend
```

Instale as dependências, caso ainda não estejam instaladas:

```bash
uv sync
```

Crie um arquivo `.env` na raiz do projeto com a URL do banco de dados:

```env
DATABASE_URL=mysql+aiomysql://usuario:senha@localhost:3306/nome_do_banco
```

Rode a API:

```bash
uv run uvicorn app.main:app --reload
```

Por padrão, a API fica disponível em:

```text
http://localhost:8000
```

A documentação automática do FastAPI pode ser acessada em:

```text
http://localhost:8000/docs
```

## Como a Autenticação Funciona

A autenticação é o processo usado para saber quem está usando o sistema.

Neste backend, ela funciona assim:

1. O médico envia email e senha para a rota de login.
2. O backend procura esse email no banco de dados.
3. Se a senha estiver correta, o backend cria um token de sessão.
4. Esse token é salvo no banco, ligado ao médico.
5. O backend também envia esse token para o navegador em um cookie chamado `session_token`.
6. Nas próximas requisições, o navegador envia esse cookie automaticamente.
7. O backend usa o cookie para descobrir qual médico está logado.

Esse cookie é HTTP-only. Isso significa que ele não pode ser acessado diretamente por JavaScript no navegador, o que ajuda a proteger a sessão do usuário.

A sessão tem tempo de validade. Por padrão, ela dura 86400 segundos, ou seja, 24 horas.

## Arquitetura Geral

O código está dividido em camadas simples. Isso ajuda a manter cada parte com uma responsabilidade clara, sem criar estruturas extras difíceis de entender.

A arquitetura foi mantida simples de propósito, sem camadas como repositories ou classes de domínio separadas. Para este projeto, a ideia é que o caminho da requisição seja fácil de acompanhar: rota, serviço, banco de dados e resposta.

### `app/main.py`

É o ponto de entrada da aplicação. Ele cria o app FastAPI, registra as rotas e configura o que deve acontecer quando o sistema inicia.

Quando o backend sobe, ele também cria as tabelas no banco caso elas ainda não existam e cadastra a lista inicial de sintomas se a tabela estiver vazia.

### `app/routers`

Contém as rotas da API. Uma rota é um endereço que o frontend pode chamar.

Exemplo: `POST /api/auth/login` é a rota usada para fazer login.

Os arquivos dessa pasta recebem os dados da requisição e chamam os serviços corretos para executar a regra de negócio.

### `app/services`

Contém as regras principais do sistema.

Exemplos:

- Verificar se a senha do médico está correta.
- Criar uma sessão de login.
- Cadastrar pacientes.
- Calcular a pontuação de uma avaliação.
- Gerar os dados do relatório.

### `app/models`

Contém a representação das tabelas do banco de dados.

Exemplos de tabelas:

- `medico`
- `paciente`
- `sintoma`
- `avaliacao`
- `avaliacao_sintoma`
- `session`

### `app/schemas`

Contém os formatos dos dados que entram e saem da API.

Por exemplo, ao criar um médico, o backend espera receber `nome`, `crm`, `especialidade`, `email` e `senha`.

### `app/core`

Contém partes mais internas da aplicação, como configuração, conexão com banco, segurança, dependências e tratamento de erros.

## Rotas Existentes

Todas as rotas abaixo começam com `/api`.

### Autenticação

| Método | Rota | Precisa estar logado? | Para que serve |
| --- | --- | --- | --- |
| POST | `/auth/login` | Não | Faz login com email e senha. |
| GET | `/auth/me` | Sim | Retorna os dados do médico logado. |

Exemplo de corpo para login:

```json
{
  "email": "medico@email.com",
  "senha": "senha1234"
}
```

### Médicos

| Método | Rota | Precisa estar logado? | Para que serve |
| --- | --- | --- | --- |
| POST | `/medicos/` | Não | Cria uma conta de médico. |
| GET | `/medicos/` | Sim | Lista os médicos cadastrados. |
| GET | `/medicos/{medico_id}` | Sim | Busca um médico pelo ID. |

Exemplo de corpo para criar médico:

```json
{
  "nome": "Dra. Ana Silva",
  "crm": "123456",
  "especialidade": "Pediatria",
  "email": "ana@email.com",
  "senha": "senha1234"
}
```

A senha precisa ter pelo menos 8 caracteres.

### Pacientes

| Método | Rota | Precisa estar logado? | Para que serve |
| --- | --- | --- | --- |
| POST | `/pacientes/` | Sim | Cadastra um paciente para o médico logado. |
| GET | `/pacientes/` | Sim | Lista os pacientes do médico logado. |
| GET | `/pacientes/{paciente_id}` | Sim | Busca um paciente pelo ID. |
| PUT | `/pacientes/{paciente_id}` | Sim | Atualiza os dados de um paciente. |

Exemplo de corpo para criar ou atualizar paciente:

```json
{
  "nome": "João Silva",
  "data_nascimento": "2015-08-20",
  "sexo": "M",
  "responsavel": "Maria Silva",
  "observacoes": "Paciente acompanhado pela mãe."
}
```

O campo `sexo` aceita `M` para masculino ou `F` para feminino.

Cada médico acessa apenas os próprios pacientes.

### Sintomas

| Método | Rota | Precisa estar logado? | Para que serve |
| --- | --- | --- | --- |
| GET | `/sintomas/` | Sim | Lista todos os sintomas disponíveis. |
| GET | `/sintomas/{sintoma_id}` | Sim | Busca um sintoma pelo ID. |

Os sintomas são cadastrados automaticamente quando o backend inicia, caso a tabela esteja vazia.

Cada sintoma possui um código, uma descrição e pesos diferentes para masculino e feminino.

### Avaliações

| Método | Rota | Precisa estar logado? | Para que serve |
| --- | --- | --- | --- |
| POST | `/pacientes/{paciente_id}/avaliacoes` | Sim | Cria uma avaliação para um paciente. |
| GET | `/pacientes/{paciente_id}/avaliacoes` | Sim | Lista as avaliações de um paciente. |
| GET | `/avaliacoes` | Sim | Lista todas as avaliações do médico logado. |
| GET | `/avaliacoes/{avaliacao_id}` | Sim | Busca uma avaliação pelo ID. |
| GET | `/avaliacoes/{avaliacao_id}/relatorio` | Sim | Retorna um relatório da avaliação. |

Exemplo de corpo para criar avaliação:

```json
{
  "sintomas": [
    {
      "codigo": "DEFICIENCIA_INTELECTUAL",
      "presente": 1
    },
    {
      "codigo": "FACE_ALONGADA_ORELHAS",
      "presente": 0
    }
  ],
  "observacoes": "Avaliação inicial."
}
```

Na prática, a avaliação precisa enviar os 12 sintomas cadastrados no sistema.

O campo `presente` aceita:

- `1`: sintoma presente.
- `0`: sintoma ausente.

## Como o Cálculo da Avaliação Funciona

Cada sintoma tem um peso. Esse peso pode ser diferente para pacientes do sexo masculino e feminino.

Quando uma avaliação é criada, o backend soma os pesos dos sintomas marcados como presentes.

Depois, ele compara essa soma com um limite:

- Masculino: `0.5600`
- Feminino: `0.5500`

Se a pontuação for maior ou igual ao limite, a recomendação será:

```text
ENCAMINHAR
```

Se a pontuação for menor que o limite, a recomendação será:

```text
NAO_ENCAMINHAR
```

## Testes

Os testes servem para verificar se partes importantes do backend continuam funcionando depois de alguma alteração.

Eles ajudam a responder perguntas como:

- O login ainda funciona?
- O cadastro e a listagem de pacientes continuam corretos?
- O cálculo da avaliação ainda retorna a recomendação esperada?
- As rotas principais ainda existem e respondem como deveriam?

Neste projeto, os testes ficam na pasta `tests`.

Para rodar todos os testes, entre na pasta `backend` e execute:

```bash
uv run pytest
```

Para rodar apenas um arquivo de teste específico, use o caminho do arquivo:

```bash
uv run pytest tests/unit/services/test_auth_service.py
```

Se todos os testes passarem, isso não garante que o sistema nunca terá problemas, mas dá mais confiança de que as principais regras continuam funcionando.

## Tratamento de Erros

Quando algo dá errado, o backend tenta responder com uma mensagem padronizada.

Exemplo de erro:

```json
{
  "error": {
    "code": "AUTHENTICATION_ERROR",
    "message": "Sessão ausente."
  }
}
```

Alguns erros comuns:

- `401`: usuário não autenticado ou sessão inválida.
- `404`: item não encontrado.
- `409`: conflito, como tentar cadastrar algo duplicado.
- `422`: dados inválidos.
- `500`: erro interno inesperado.

## Regras Importantes

- A maioria das rotas exige login.
- O login salva a sessão em cookie.
- Cada médico vê apenas os seus próprios pacientes e avaliações.
- Senhas não são salvas em texto puro; elas são protegidas com hash.
- A lista de sintomas inicial é cadastrada automaticamente se ainda não existir.
- A avaliação precisa conter os 12 sintomas esperados pelo sistema.

## Resumo Para Quem Está Começando

Pense no backend como o atendente do sistema.

O frontend pergunta ou envia dados. O backend verifica se está tudo certo, consulta ou salva no banco de dados e devolve uma resposta.

Neste projeto, o backend cuida principalmente de login, médicos, pacientes, sintomas, avaliações e relatórios.
