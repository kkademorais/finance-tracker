# Plano de Desenvolvimento --- API de Controle de Compras Pessoais

**Stack principal:** Python, FastAPI, SQLAlchemy e SQLite/PostgreSQL\
**Abordagem:** desenvolvimento iterativo, arquitetura em camadas e
evolução gradual\
**Objetivo:** substituir o registro manual de compras em bloco de notas
por uma aplicação centralizada para registrar, consultar, analisar e
exportar despesas pessoais.

------------------------------------------------------------------------

## Sumário

1.  [Visão geral e objetivos](#1-visão-geral-e-objetivos)
2.  [Requisitos funcionais](#2-requisitos-funcionais)
3.  [Modelo de dados](#3-modelo-de-dados)
4.  [Decisão sobre banco de dados](#4-decisão-sobre-banco-de-dados)
5.  [Arquitetura proposta](#5-arquitetura-proposta)
6.  [Endpoints da API](#6-endpoints-da-api)
7.  [Plano iterativo de
    implementação](#7-plano-iterativo-de-implementação)
8.  [Tecnologias recomendadas](#8-tecnologias-recomendadas)
9.  [Requisitos transversais](#9-requisitos-transversais)
10. [Roadmap e definição do MVP](#10-roadmap-e-definição-do-mvp)
11. [Primeiros passos práticos](#11-primeiros-passos-práticos)
12. [Documentação oficial](#12-documentação-oficial)

------------------------------------------------------------------------

# 1. Visão geral e objetivos

## 1.1. Problema

Atualmente, as compras realizadas no cartão são registradas manualmente
em um bloco de notas. Esse processo dificulta a organização, a consulta
do histórico e a análise dos gastos ao final do mês.

A proposta é desenvolver uma API que centralize os registros de compras
e permita inserir despesas de maneira rápida, inicialmente por texto e,
em versões futuras, por Telegram, voz e imagem.

## 1.2. Objetivo geral

Construir uma aplicação de controle de compras pessoais capaz de:

-   Registrar compras com valor, data, cartão utilizado, estabelecimento e categoria.
-   Consultar compras por período, cartão, estabelecimento ou categoria.
-   Gerar extratos mensais.
-   Calcular total gasto e distribuição dos gastos por categoria.
-   Exportar extratos para Excel.
-   Enviar relatórios por e-mail.
-   Receber informações por diferentes canais: API REST, Telegram, texto
    livre, voz e imagem.
-   Apresentar indicadores e gráficos sobre os hábitos de consumo.

## 1.3. Fluxo conceitual

O fluxo principal da aplicação será:

1.  **Entrada:** recebimento de dados por texto, Telegram, áudio ou
    imagem.
2.  **Processamento:** extração, interpretação, normalização e validação
    das informações.
3.  **Persistência:** armazenamento dos registros no banco de dados.
4.  **Consulta e análise:** geração de extratos, totais, agrupamentos e
    indicadores.
5.  **Exportação:** geração de planilhas Excel e envio por e-mail.

Uma decisão arquitetural fundamental é separar a forma de entrada dos
dados da lógica de negócio e da persistência. Independentemente de uma
compra chegar por endpoint REST, Telegram, voz ou OCR, ela deve ser
convertida para uma estrutura padronizada e registrada pelo mesmo
serviço de negócio.

------------------------------------------------------------------------

# 2. Requisitos funcionais

## 2.1. Gerenciamento de compras

-   Registrar uma compra.
-   Consultar todas as compras.
-   Consultar uma compra específica.
-   Atualizar um registro.
-   Excluir um registro.
-   Filtrar por estabelecimento.
-   Filtrar por cartão utilizado.
-   Filtrar por categoria.
-   Filtrar por período.
-   Listar resultados com paginação.

## 2.2. Relatórios financeiros

-   Gerar extrato mensal.
-   Calcular o total gasto no período.
-   Calcular a quantidade de compras.
-   Calcular o total gasto por categoria.
-   Calcular a participação percentual de cada categoria no valor total.
-   Calcular o total gasto por estabelecimento.
-   Calcular o total gasto por cartão.
-   Comparar os gastos entre meses.

## 2.3. Integrações e processamento

-   Receber compras pelo Telegram.
-   Interpretar mensagens com Regex e regras de parsing.
-   Transcrever mensagens de voz.
-   Processar imagens de comprovantes ou extratos com OCR.
-   Exportar relatórios para Excel.
-   Enviar relatórios por e-mail.

## 2.4. Indicadores

-   Evolução dos gastos ao longo dos meses.
-   Distribuição dos gastos por categoria e por cartão.
-   Estabelecimentos com maior volume de compras.
-   Média de gastos por compra.
-   Média de gastos por dia.
-   Comparativo entre períodos.
-   Categorias com maior crescimento.
-   Maior compra registrada.

## 2.5. Dados de uma compra

Embora os requisitos iniciais mencionem valor, data e categoria, o campo
**estabelecimento** também é necessário para permitir consultas como
"quanto gastei no Mercado Livre?".

Estrutura inicial recomendada:

```
  Campo             Tipo conceitual            Obrigatório Exemplo
  ----------------- ------------------------ ------------- ------------------
  id                Inteiro                            Sim 1
  valor             Decimal                            Sim 129,90
  data_compra       Data                               Sim 2026-10-30
  estabelecimento   Texto                              Sim Mercado Livre
  cartao            Texto                              Sim Banco do Brasil
  categoria         Referência à categoria             Sim Compras online
  descricao         Texto                              Não Teclado mecânico
  forma_pagamento   Texto                              Não Crédito
  criado_em         Data e hora                        Sim Data do registro
```

**Importante:** `data_compra` representa quando a compra aconteceu;
`criado_em` representa quando ela foi registrada no sistema.

Para valores monetários, utilizar `Decimal`, e não `float`, para evitar
problemas de precisão em operações financeiras.

O parcelamento pode ser tratado em uma versão futura. Na primeira
versão, o registro pode representar o valor total da compra.
Posteriormente, será possível modelar parcelas e lançamentos mensais.

------------------------------------------------------------------------

# 3. Modelo de dados

## 3.1. Modelo inicial

Para a primeira versão, uma tabela `compras` atende às operações
fundamentais. Recomenda-se também uma tabela `categorias`, evitando
variações inconsistentes na escrita dos nomes.

### Tabela `categorias`

```
  Campo   Descrição
  ------- -------------------------
  id      Chave primária
  nome    Nome único da categoria
```

Exemplos: Alimentação, Transporte, Lazer, Compras online e Saúde.

### Tabela `cartoes`

```
  Campo   Descrição
  ------- -------------------------
  id      Chave primária
  nome    Nome único do cartão
```

Exemplos: Banco do Brasil, Carrefour, Itau

### Tabela `compras`

```
  Campo             Descrição
  ----------------- -------------------------------------
  id                Chave primária
  valor             Valor monetário da compra
  data_compra       Data em que a compra ocorreu
  estabelecimento   Local ou empresa da compra
  descricao         Descrição opcional
  categoria_id      Chave estrangeira para `categorias`
  cartoes_id        Chave estrangeira para `cartoes`
  forma_pagamento   Forma de pagamento opcional
  criado_em         Data e hora de criação do registro
```

Relacionamento: várias compras podem pertencer a uma mesma categoria
(**N:1**).

Relacionamento: várias compras podem pertencer a um mesmo cartão
(**N:1**).

Exemplo conceitual de SQL:

``` sql
CREATE TABLE Categorias (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Cartoes (
    id INTEGER PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Compras (
    id INTEGER PRIMARY KEY,
    valor DECIMAL(10, 2) NOT NULL,
    data_compra DATE NOT NULL,
    estabelecimento VARCHAR(150) NOT NULL,
    descricao TEXT,
    categoria_id INTEGER NOT NULL,
    cartao_id INTEGER NOT NULL,
    forma_pagamento VARCHAR(50),
    criado_em DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_categoria FOREIGN KEY (categoria_id) REFERENCES Categorias(id),
    CONSTRAINT fk_cartao FOREIGN KEY (cartao_id) REFERENCES Cartoes(id)
);
```

A sintaxe exata poderá variar conforme o banco utilizado.

## 3.2. Evoluções futuras do modelo

Conforme o escopo crescer, poderão ser adicionadas tabelas para:

-   Usuários, caso a aplicação deixe de ser exclusivamente pessoal.
-   Faturas.
-   Parcelas.
-   Fontes de registro, para identificar se a compra veio de texto,
    Telegram, voz ou OCR.
-   Anexos, caso seja necessário manter comprovantes.

Não é necessário implementar essas tabelas antecipadamente. O modelo
inicial deve permanecer simples, mas preparado para evoluir.

------------------------------------------------------------------------

# 4. Decisão sobre banco de dados

## 4.1. É necessário utilizar um banco?

**Sim. Recomenda-se utilizar um banco de dados desde a primeira
versão.**

A aplicação precisará armazenar registros continuamente, filtrar compras
por diversos critérios, realizar agrupamentos e cálculos, além de
receber operações potencialmente simultâneas pelo Telegram.

Arquivos JSON ou CSV poderiam ser utilizados em um protótipo muito
simples, mas não são a melhor base para esse projeto.

## 4.2. Alternativa: arquivos JSON

Um arquivo JSON poderia armazenar os registros:

``` json
[
  {
    "id": 1,
    "valor": 129.90,
    "data_compra": "2026-10-30",
    "estabelecimento": "Mercado Livre",
    "categoria": "Compras online",
    "cartao": "Itau"
  }
]
```

**Vantagens:**

-   Implementação simples.
-   Não exige instalação de banco.
-   Útil para experimentar conceitos iniciais.

**Desvantagens:**

-   Consultas e filtros são mais trabalhosos.
-   Atualizações simultâneas podem causar sobrescrita de dados.
-   Não oferece recursos relacionais e transacionais equivalentes aos de
    um SGBD.
-   Integridade e consistência precisam ser implementadas manualmente.
-   A manutenção se torna mais difícil conforme o volume cresce.

Não é recomendado como solução permanente.

## 4.3. Alternativa: SQLite

SQLite é um banco relacional embarcado que armazena os dados em um
arquivo local.

**Vantagens:**

-   Configuração simples.
-   Não exige servidor de banco separado.
-   Suporta SQL, transações, índices e restrições.
-   Excelente para desenvolvimento local.
-   Pode ser utilizado com SQLAlchemy.

**Limitações:**

-   Concorrência de escrita mais limitada que em um banco
    cliente-servidor.
-   Menos indicado para múltiplas instâncias da aplicação ou cenários de
    escrita concorrente mais intensa.

## 4.4. Alternativa: PostgreSQL

PostgreSQL é um SGBD relacional cliente-servidor, adequado para
produção.

**Vantagens:**

-   Suporte a múltiplas conexões.
-   Transações e integridade referencial.
-   Índices e consultas avançadas.
-   Recursos robustos de segurança e administração.
-   Adequado para crescimento da aplicação.

## 4.5. Decisão recomendada

```text
  -----------------------------------------------------------------------
  Etapa                   Banco                   Motivo
  ----------------------- ----------------------- -----------------------
  Desenvolvimento local   SQLite                  Simplicidade e ausência
                                                  de infraestrutura
                                                  adicional

  Produção                PostgreSQL              Robustez, concorrência
                                                  e operação contínua
  -----------------------------------------------------------------------
```

Utilizar **SQLAlchemy** como camada de acesso aos dados facilita a
transição entre SQLite e PostgreSQL. Grande parte do código de
persistência poderá ser mantida, alterando principalmente a configuração
da conexão e tratando eventuais diferenças entre os bancos.

Não é recomendável começar com JSON e migrar posteriormente, pois os
requisitos já justificam o uso de um banco relacional.

------------------------------------------------------------------------

# 5. Arquitetura proposta

## 5.1. Arquitetura em camadas

A aplicação deve separar responsabilidades:

1.  **Entrada:** endpoints REST e integração com Telegram.
2.  **Processamento:** parsing, Regex, OCR, transcrição e validação.
3.  **Serviços:** regras de negócio, registro, consultas, extratos e
    indicadores.
4.  **Persistência:** repositórios e SQLAlchemy.
5.  **Saídas:** respostas HTTP, Excel e e-mail.

Fluxo conceitual:

``` text
API REST                 Telegram
   |                         |
   +-----------+-------------+
               |
       Processamento
   (Parser / Regex / OCR /
      Speech-to-Text)
               |
        Validação Pydantic
               |
       Serviços de negócio
   (Compras / Extratos /
     Indicadores / Excel)
               |
          Repositórios
               |
       SQLAlchemy / ORM
               |
       SQLite ou PostgreSQL
```

O Telegram não deve conter a lógica de registro. Ele deve receber a
mensagem, identificar o usuário, interpretar ou encaminhar os dados e
chamar o serviço responsável pela operação. O mesmo serviço poderá ser
chamado por um endpoint REST.

## 5.2. Estrutura de diretórios sugerida

``` text
controle-compras/
│
├── app/
│   ├── main.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── compra.py
│   │   ├── cartao.py
│   │   └── categoria.py
│   │
│   ├── schemas/
│   │   ├── compra.py
│   │   └── extrato.py
│   │
│   ├── routers/
│   │   ├── compras.py
│   │   ├── extratos.py
│   │   └── indicadores.py
│   │
│   ├── services/
│   │   ├── compra_service.py
│   │   ├── extrato_service.py
│   │   ├── indicador_service.py
│   │   ├── excel_service.py
│   │   └── email_service.py
│   │
│   ├── repositories/
│   │   ├── compra_repository.py
│   │   └── categoria_repository.py
│   │
│   ├── parsers/
│   │   └── texto_parser.py
│   │
│   ├── integrations/
│   │   ├── telegram/
│   │   ├── speech/
│   │   └── ocr/
│   │
│   └── utils/
│       └── formatacao.py
│
├── tests/
│   ├── test_compras.py
│   ├── test_extratos.py
│   └── test_parsers.py
│
├── exports/
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### Responsabilidade de cada camada

```text
  Componente       Responsabilidade
  ---------------- -------------------------------------------------------
  `core`           Configurações e conexão com o banco
  `models`         Representação das tabelas
  `schemas`        Validação e estrutura de entrada e saída com Pydantic
  `routers`        Recebimento e encaminhamento das requisições
  `services`       Regras de negócio
  `repositories`   Operações de persistência
  `parsers`        Interpretação de mensagens
  `integrations`   Comunicação com serviços externos
  `utils`          Funções auxiliares
  `tests`          Testes automatizados
```

Distinções importantes:

-   **Model:** representa como os dados são armazenados.
-   **Schema:** representa como os dados são recebidos ou devolvidos
    pela API.
-   **Repository:** executa operações no banco.
-   **Service:** implementa regras de negócio.
-   **Router:** recebe a requisição e chama o serviço apropriado.

------------------------------------------------------------------------

# 6. Endpoints da API

Planejamento inicial:

```
  Método   Endpoint                       Responsabilidade
  -------- ------------------------------ ---------------------------------------
  POST     `/compras`                     Registrar uma compra estruturada
  GET      `/compras`                     Listar compras
  GET      `/compras/{id}`                Consultar uma compra
  PUT      `/compras/{id}`                Atualizar uma compra
  DELETE   `/compras/{id}`                Excluir uma compra
  POST     `/compras/texto`               Registrar a partir de texto formatado
  GET      `/extratos/mensal`             Consultar extrato mensal
  GET      `/extratos/categorias`         Resumo por categoria
  GET      `/extratos/cartoes`            Resumo por cartão
  GET      `/extratos/estabelecimentos`   Resumo por estabelecimento
  GET      `/extratos/exportar`           Exportar extrato para Excel
  POST     `/extratos/enviar-email`       Enviar extrato por e-mail
  GET      `/indicadores`                 Consultar indicadores
```

Exemplos de filtros:

``` http
GET /compras?estabelecimento=Mercado%20Livre
```

``` http
GET /compras?cartao=BancoBrasil
```

``` http
GET /compras?categoria=Alimentacao
```

``` http
GET /compras?data_inicio=2026-10-01&data_fim=2026-10-31
```

``` http
GET /extratos/mensal?mes=10&ano=2026
```

Exemplo de requisição para registrar uma compra:

``` json
{
  "valor": "129.90",
  "data_compra": "2026-10-30",
  "estabelecimento": "Mercado Livre",
  "categoria": "Compras online",
  "descricao": "Teclado mecânico"
}
```

Exemplo de resposta:

``` json
{
  "mensagem": "Compra registrada com sucesso",
  "compra": {
    "id": 1,
    "valor": "129.90",
    "data_compra": "2026-10-30",
    "estabelecimento": "Mercado Livre",
    "categoria": "Compras online"
  }
}
```

A representação de valores monetários como string decimal no JSON evita
que a precisão seja comprometida por conversões desnecessárias para
ponto flutuante.

## 6.1. Cálculo dos percentuais

O percentual de uma categoria deve representar sua participação no valor
total gasto:

\[ `\text{Percentual da categoria}`{=tex} =
`\frac{\text{Total da categoria}}{\text{Total geral}}`{=tex}
`\times 100`{=tex} \]

```
Exemplo:

  Categoria                  Total   Participação
  ------------- ------------------ --------------
  Alimentação           R\$ 500,00            40%
  Transporte            R\$ 250,00            20%
  Lazer                 R\$ 500,00            40%
  **Total**       **R\$ 1.250,00**       **100%**
```

A quantidade de compras por categoria pode ser apresentada como
indicador separado. Não se deve confundir percentual do valor gasto com
percentual da quantidade de transações.

------------------------------------------------------------------------

# 7. Plano iterativo de implementação

A ordem abaixo organiza as entregas por dependência técnica e valor
funcional. Algumas funcionalidades originalmente planejadas para versões
posteriores, como Excel, devem ser antecipadas para o MVP, pois fazem
parte do objetivo principal da aplicação.

## Fase 1 --- API local e gerenciamento de compras

**Objetivo:** construir uma API local funcional, capaz de registrar,
consultar, editar e excluir compras, além de gerar extratos.

### Etapa 1 --- Preparação do ambiente

-   [X] Instalar Python.
-   [X] Criar diretório do projeto.
-   [X] Criar ambiente virtual com `venv`.
-   [X] Instalar FastAPI.
-   [X] Instalar Uvicorn.
-   [X] Instalar SQLAlchemy.
-   [X] Instalar Pydantic.
-   [X] Instalar Alembic.
-   [X] Criar `requirements.txt`.
-   [X] Criar `.gitignore`.
-   [X] Criar `.env.example`.
-   [X] Inicializar repositório Git.


### Etapa 2 --- Configuração do banco

-   [ ] Criar `database.py`.
-   [ ] Configurar conexão com SQLite.
-   [ ] Criar função para fornecer sessões do banco.
-   [ ] Configurar SQLAlchemy.
-   [ ] Criar model `Compra`.
-   [ ] Criar model `Categoria`.
-   [ ] Configurar relacionamento entre as tabelas.
-   [ ] Criar primeira migration com Alembic.
-   [ ] Testar inserção e consulta diretamente no banco.

**Entrega:** banco local funcional.

### Etapa 3 --- Endpoints CRUD

-   [ ] Criar `main.py`.
-   [ ] Criar router de compras.
-   [ ] Implementar `POST /compras`.
-   [ ] Implementar `GET /compras`.
-   [ ] Implementar `GET /compras/{id}`.
-   [ ] Implementar `PUT /compras/{id}`.
-   [ ] Implementar `DELETE /compras/{id}`.
-   [ ] Implementar filtros por estabelecimento.
-   [ ] Implementar filtros por categoria.
-   [ ] Implementar filtros por período.
-   [ ] Implementar paginação.
-   [ ] Implementar tratamento de erros HTTP.
-   [ ] Testar endpoints pelo Swagger.

### Etapa 4 --- Extrato mensal

-   [ ] Criar `extrato_service.py`.
-   [ ] Implementar consulta por mês e ano.
-   [ ] Calcular total gasto.
-   [ ] Calcular quantidade de compras.
-   [ ] Calcular total por categoria.
-   [ ] Calcular percentual por categoria.
-   [ ] Calcular total por estabelecimento.
-   [ ] Implementar endpoint de extrato mensal.
-   [ ] Implementar endpoint de resumo por categoria.
-   [ ] Testar os cálculos com cenários conhecidos.

Exemplo de resposta:

``` json
{
  "periodo": "2026-10",
  "total_gasto": "1250.00",
  "quantidade_compras": 15,
  "categorias": [
    {
      "nome": "Alimentação",
      "total": "500.00",
      "percentual": 40.0
    },
    {
      "nome": "Transporte",
      "total": "250.00",
      "percentual": 20.0
    },
    {
      "nome": "Lazer",
      "total": "500.00",
      "percentual": 40.0
    }
  ]
}
```

### Etapa 5 --- Exportação Excel antecipada

-   [ ] Instalar `openpyxl`.
-   [ ] Criar `excel_service.py`.
-   [ ] Consultar registros do período.
-   [ ] Criar planilha de extrato.
-   [ ] Criar aba de resumo.
-   [ ] Criar aba de categorias.
-   [ ] Aplicar formatação monetária.
-   [ ] Aplicar formatação de datas.
-   [ ] Ajustar largura das colunas.
-   [ ] Criar endpoint de exportação.
-   [ ] Retornar o arquivo com `FileResponse` ou `StreamingResponse`.
-   [ ] Testar abertura e integridade do arquivo.

Estrutura sugerida:

**Aba 1 --- Extrato:** data, estabelecimento, categoria, descrição e
valor.

**Aba 2 --- Resumo:** total gasto, quantidade de compras e média por
compra.

**Aba 3 --- Categorias:** categoria, total e participação percentual.

Endpoint sugerido:

``` http
GET /extratos/exportar?mes=10&ano=2026
```

**Entrega da Fase 1:** uma API local que já substitui o bloco de notas e
permite consultar e exportar as compras.

------------------------------------------------------------------------

## Fase 2 --- Interpretação de texto

**Objetivo:** permitir registrar uma compra enviando uma mensagem
textual em formato definido.

Formato inicial:

``` text
129,90; 30/10/2026; Mercado Livre; Compras online
```

### Checklist

-   [ ] Criar `texto_parser.py`.
-   [ ] Definir formato de entrada.
-   [ ] Separar os campos recebidos.
-   [ ] Converter valores para `Decimal`.
-   [ ] Converter datas para o formato adequado.
-   [ ] Normalizar categorias.
-   [ ] Validar campos obrigatórios.
-   [ ] Tratar mensagens incompletas.
-   [ ] Tratar valores e datas inválidos.
-   [ ] Integrar o parser ao serviço de compras.
-   [ ] Criar endpoint `POST /compras/texto`.
-   [ ] Criar testes para diferentes entradas.

Separação de responsabilidades:

-   **Parser:** interpreta o texto e produz dados estruturados.
-   **Service:** valida regras de negócio e registra a compra.

Essa estrutura será reutilizada nas integrações futuras.

------------------------------------------------------------------------

## Fase 3 --- Integração com Telegram

**Objetivo:** utilizar a aplicação diretamente pelo celular.

O Telegram será uma interface de comunicação com a API, e não um
substituto para ela.

### Etapa 1 --- Criação do bot

-   [ ] Criar bot utilizando o BotFather.
-   [ ] Obter token de autenticação.
-   [ ] Criar módulo de integração Telegram.
-   [ ] Instalar `python-telegram-bot` ou biblioteca equivalente.
-   [ ] Configurar comunicação com os serviços da aplicação.

### Etapa 2 --- Comandos

```
  Comando         Ação
  --------------- ---------------------------------------
  `/start`        Iniciar interação
  `/ajuda`        Exibir instruções
  `/registrar`    Iniciar registro
  `/extrato`      Consultar extrato mensal
  `/total`        Consultar total gasto
  `/categorias`   Consultar divisão por categoria
  `/buscar`       Consultar compras por estabelecimento
```

Fluxo de registro:

1.  Usuário envia `/registrar`.
2.  Bot solicita os dados no formato definido.
3.  Usuário envia valor, data, estabelecimento e categoria.
4.  Bot encaminha os dados ao parser e serviço de compras.
5.  Aplicação registra a compra.
6.  Bot confirma o registro.

### Etapa 3 --- Segurança

-   [ ] Identificar o Telegram User ID autorizado.
-   [ ] Implementar lista de usuários permitidos.
-   [ ] Bloquear usuários desconhecidos.
-   [ ] Armazenar token em variável de ambiente.
-   [ ] Tratar erros de comunicação.
-   [ ] Evitar expor tokens e dados sensíveis em logs.

### Etapa 4 --- Consultas

-   [ ] Consultar extrato pelo Telegram.
-   [ ] Consultar por estabelecimento.
-   [ ] Consultar por categoria.
-   [ ] Consultar total gasto.
-   [ ] Formatar respostas para leitura no celular.

**Entrega:** aplicação utilizável pelo Telegram.

------------------------------------------------------------------------

## Fase 4 --- Implantação em produção

**Objetivo:** disponibilizar a API continuamente na internet.

Sugestão de arquitetura: VPS Linux, Docker, PostgreSQL e Nginx.

``` text
Telegram
   |
Internet / HTTPS
   |
VPS Linux
   |
Nginx (proxy reverso e HTTPS)
   |
Docker — FastAPI / Uvicorn
   |
PostgreSQL
```

### Checklist

-   [ ] Escolher provedor de VPS.
-   [ ] Configurar servidor Linux.
-   [ ] Instalar Docker e Docker Compose.
-   [ ] Criar Dockerfile.
-   [ ] Criar `docker-compose.yml`.
-   [ ] Configurar PostgreSQL.
-   [ ] Configurar variáveis de ambiente.
-   [ ] Configurar volume persistente do banco.
-   [ ] Configurar Nginx.
-   [ ] Configurar domínio e DNS.
-   [ ] Configurar certificado HTTPS.
-   [ ] Configurar Telegram via webhook, se adotado.
-   [ ] Configurar logs.
-   [ ] Configurar backup automático.
-   [ ] Testar recuperação de backup.
-   [ ] Configurar reinicialização dos serviços.

**Segurança:** não expor diretamente a porta do PostgreSQL à internet. O
banco deve ser acessível apenas pela aplicação e por meios
administrativos autorizados.

------------------------------------------------------------------------

## Fase 5 --- Interpretação flexível com Regex

**Objetivo:** deixar de exigir um formato rígido e permitir mensagens
mais naturais.

Exemplos:

``` text
Gastei 129,90 no Mercado Livre hoje, em compras online.
```

``` text
Hoje comprei um lanche de 35 reais no McDonald's.
```

### Checklist

-   [ ] Estudar expressões regulares em Python.
-   [ ] Identificar padrões de valores monetários.
-   [ ] Identificar padrões de datas.
-   [ ] Identificar estabelecimento.
-   [ ] Identificar categoria.
-   [ ] Criar regras para diferentes formatos.
-   [ ] Normalizar dados extraídos.
-   [ ] Validar campos identificados.
-   [ ] Tratar informações ausentes.
-   [ ] Solicitar confirmação em casos ambíguos.
-   [ ] Criar testes unitários do parser.

Exemplo simples de Regex:

``` python
import re

texto = "Gastei R$ 129,90 no Mercado Livre"

padrao = r"R?\\$?\\s*(\\d+(?:\\.\\d{3})*(?:,\\d{2})?)"

resultado = re.search(padrao, texto)

if resultado:
    print(resultado.group(1))
```

Regex identifica padrões, mas não resolve toda a interpretação de
linguagem natural.

Exemplo de ambiguidade:

> Comprei dois lanches por 35 reais no McDonald's.

É necessário determinar se R\$ 35 representa o total ou o preço
unitário. Regras de negócio e confirmação do usuário podem ser
necessárias.

Não é necessário adicionar um LLM nesta etapa. Primeiro, explorar Regex,
normalização e regras determinísticas.

------------------------------------------------------------------------

## Fase 6 --- Registro por voz

**Objetivo:** receber mensagens de áudio pelo Telegram, transcrevê-las e
interpretar os dados.

Exemplo de áudio:

> Comprei um almoço de quarenta e cinco reais hoje no restaurante do
> shopping, categoria alimentação.

Fluxo:

1.  Telegram recebe o áudio.
2.  Aplicação realiza o download.
3.  Serviço de Speech-to-Text transcreve o áudio.
4.  Texto é encaminhado ao parser.
5.  Dados são validados.
6.  Usuário confirma, quando necessário.
7.  Compra é registrada.

### Tecnologias possíveis

```
  -----------------------------------------------------------------------
  Tecnologia                          Utilização
  ----------------------------------- -----------------------------------
  OpenAI Whisper                      Reconhecimento automático de fala

  faster-whisper                      Implementação otimizada para
                                      transcrição local

  SpeechRecognition                   Integração Python com mecanismos de
                                      reconhecimento
  -----------------------------------------------------------------------
```

### Checklist

-   [ ] Estudar processamento de áudio.
-   [ ] Entender o formato recebido pelo Telegram.
-   [ ] Implementar download do áudio.
-   [ ] Implementar conversão de formato, se necessária.
-   [ ] Integrar serviço de Speech-to-Text.
-   [ ] Obter transcrição.
-   [ ] Encaminhar texto ao parser.
-   [ ] Validar dados identificados.
-   [ ] Solicitar confirmação quando necessário.
-   [ ] Excluir arquivos temporários após processamento.
-   [ ] Testar diferentes condições de áudio.

A transcrição pode conter erros. Por isso, valores, datas e
estabelecimentos devem passar por validação antes do registro.

------------------------------------------------------------------------

## Fase 7 --- Registro por imagem e OCR

**Objetivo:** permitir o envio de fotografias de comprovantes ou
extratos físicos.

Fluxo:

1.  Telegram recebe a imagem.
2.  API realiza o download.
3.  Imagem passa por pré-processamento.
4.  OCR identifica o texto.
5.  Parser interpreta os dados extraídos.
6.  Aplicação valida valores, datas e estabelecimentos.
7.  Usuário recebe uma prévia.
8.  Usuário confirma.
9.  Compras são registradas.

### Tecnologias possíveis

  Tecnologia      Aplicação
  --------------- ----------------------------------
  Tesseract OCR   Motor de reconhecimento de texto
  Pytesseract     Interface Python para Tesseract
  OpenCV          Pré-processamento de imagens
  Pillow          Manipulação de imagens

### Checklist

-   [ ] Estudar fundamentos de OCR.
-   [ ] Instalar Tesseract.
-   [ ] Instalar Pytesseract.
-   [ ] Implementar recebimento de imagens.
-   [ ] Implementar download da imagem.
-   [ ] Validar tipo e tamanho do arquivo.
-   [ ] Implementar pré-processamento com OpenCV.
-   [ ] Extrair texto utilizando OCR.
-   [ ] Identificar valores monetários.
-   [ ] Identificar datas.
-   [ ] Identificar estabelecimentos.
-   [ ] Identificar múltiplos itens ou compras.
-   [ ] Validar informações extraídas.
-   [ ] Criar etapa de confirmação.
-   [ ] Registrar compras confirmadas.
-   [ ] Implementar prevenção de duplicidades.

OCR pode interpretar valores incorretamente, por exemplo, `8,90` como
`3,90`. Portanto, não se deve registrar automaticamente tudo que for
identificado.

Também é necessário distinguir comprovantes de compra de faturas de
cartão. Uma fatura pode conter compras já registradas por outro canal.

------------------------------------------------------------------------

## Fase 8 --- Exportação para Excel

A exportação é uma funcionalidade central e deve ser antecipada para o
MVP, ainda que possa ser refinada nesta etapa.

Biblioteca recomendada: `openpyxl`.

### Estrutura sugerida

**Arquivo:** `Extrato_Compras_AAAA_MM.xlsx`

-   **Aba Extrato:** data, estabelecimento, categoria, descrição e
    valor.
-   **Aba Resumo:** total gasto, quantidade de compras e média por
    compra.
-   **Aba Categorias:** categoria, total gasto e percentual.

### Checklist

-   [ ] Instalar `openpyxl`.
-   [ ] Criar `excel_service.py`.
-   [ ] Consultar registros do período.
-   [ ] Criar arquivo Excel.
-   [ ] Criar aba de extrato.
-   [ ] Criar aba de resumo.
-   [ ] Criar aba de categorias.
-   [ ] Aplicar formatação monetária.
-   [ ] Aplicar formatação de datas.
-   [ ] Ajustar largura das colunas.
-   [ ] Criar endpoint de exportação.
-   [ ] Retornar arquivo com `FileResponse` ou `StreamingResponse`.
-   [ ] Testar abertura e integridade do arquivo.

Não é necessário manter o arquivo permanentemente no servidor. Ele pode
ser gerado em memória ou em armazenamento temporário e descartado após o
uso.

------------------------------------------------------------------------

## Fase 9 --- Envio do Excel por e-mail

**Objetivo:** enviar automaticamente o relatório gerado para o endereço
de e-mail configurado.

Serviço possível: Resend.

### Fluxo

1.  Usuário solicita o extrato.
2.  API consulta os registros.
3.  Excel é gerado.
4.  Arquivo é anexado ao e-mail.
5.  Serviço realiza o envio.
6.  Aplicação informa o resultado.

### Checklist

-   [ ] Criar conta no serviço de e-mail.
-   [ ] Configurar domínio de envio, se necessário.
-   [ ] Configurar credenciais em variáveis de ambiente.
-   [ ] Criar `email_service.py`.
-   [ ] Integrar geração do Excel ao serviço de e-mail.
-   [ ] Anexar arquivo `.xlsx`.
-   [ ] Criar endpoint de envio.
-   [ ] Implementar tratamento de falhas.
-   [ ] Testar envio e recebimento.
-   [ ] Implementar comando Telegram para solicitar envio.

------------------------------------------------------------------------

## Fase 10 --- Indicadores e gráficos

**Objetivo:** transformar os registros em informações úteis para
acompanhamento financeiro.

### Indicadores recomendados

```
  -----------------------------------------------------------------------
  Indicador                           Cálculo ou finalidade
  ----------------------------------- -----------------------------------
  Total mensal                        Soma das compras no mês

  Média por compra                    Total gasto dividido pela
                                      quantidade

  Gasto por categoria                 Soma agrupada por categoria

  Participação da categoria           Total da categoria dividido pelo
                                      total geral

  Gasto por estabelecimento           Soma agrupada por estabelecimento

  Evolução mensal                     Total de cada mês

  Maior compra                        Maior valor registrado

  Quantidade de compras               Contagem de registros

  Média diária                        Total do período dividido pelo
                                      número de dias considerado
  -----------------------------------------------------------------------
```

### Gráficos recomendados

1.  **Distribuição por categoria:** gráfico de rosca com participação de
    cada categoria.
2.  **Evolução dos gastos:** gráfico de linhas para comparar meses.
3.  **Gastos por estabelecimento:** gráfico de barras com os
    estabelecimentos de maior despesa.
4.  **Comparativo mensal:** comparação entre períodos.
5.  **Evolução por categoria:** acompanhamento de categorias ao longo do
    tempo.

### Checklist

-   [ ] Criar `indicador_service.py`.
-   [ ] Implementar consultas agregadas no banco.
-   [ ] Criar endpoint de indicadores.
-   [ ] Implementar evolução mensal.
-   [ ] Implementar distribuição por categoria.
-   [ ] Implementar ranking de estabelecimentos.
-   [ ] Implementar comparativo entre meses.
-   [ ] Definir formato de resposta JSON.
-   [ ] Implementar visualização dos gráficos.

FastAPI deve disponibilizar os dados; não precisa ser responsável por
desenhar os gráficos. Uma interface futura pode consumir os endpoints.
Streamlit é uma opção para criar um dashboard sem desenvolver
imediatamente um frontend tradicional.

------------------------------------------------------------------------

# 8. Tecnologias recomendadas

```
  Área              Tecnologia                Finalidade
  ----------------- ------------------------- ------------------------------
  Linguagem         Python                    Desenvolvimento
  Framework         FastAPI                   API REST
  Servidor          Uvicorn                   Execução da API
  Validação         Pydantic                  Validação de entradas
  ORM               SQLAlchemy                Persistência
  Banco local       SQLite                    Desenvolvimento
  Banco produção    PostgreSQL                Persistência em produção
  Migrations        Alembic                   Versionamento do banco
  Parser            `re`                      Expressões regulares
  Telegram          Telegram Bot API          Interface de mensagens
  Voz               faster-whisper            Transcrição
  OCR               Tesseract + Pytesseract   Extração de texto
  Imagens           OpenCV / Pillow           Pré-processamento
  Excel             openpyxl                  Geração de planilhas
  E-mail            Resend                    Envio de relatórios
  Testes            Pytest                    Testes automatizados
  Containerização   Docker                    Empacotamento
  Proxy reverso     Nginx                     HTTPS e encaminhamento
  Produção          VPS Linux                 Hospedagem
  Dashboard         Streamlit (opcional)      Visualização dos indicadores
```

Não é necessário instalar todas as dependências no início. Cada
tecnologia deve ser adicionada quando a funcionalidade correspondente
começar a ser desenvolvida.

------------------------------------------------------------------------

# 9. Requisitos transversais

Estes requisitos devem ser considerados ao longo de todo o
desenvolvimento, e não apenas em uma fase específica.

## 9.1. Testes automatizados

Utilizar Pytest e o `TestClient` do FastAPI.

Checklist:

-   [ ] Testar registro de compras.
-   [ ] Testar valores inválidos.
-   [ ] Testar datas inválidas.
-   [ ] Testar consultas por estabelecimento.
-   [ ] Testar consultas por período.
-   [ ] Testar cálculo do total mensal.
-   [ ] Testar cálculo de percentuais.
-   [ ] Testar atualização e exclusão.
-   [ ] Testar interpretação de mensagens.
-   [ ] Testar geração de Excel.
-   [ ] Testar permissões do Telegram.
-   [ ] Testar falhas de integrações externas.

Os testes financeiros devem utilizar valores conhecidos, incluindo
centavos, para verificar precisão e arredondamentos.

## 9.2. Segurança e privacidade

A aplicação armazenará informações sobre hábitos de consumo. Mesmo sendo
pessoal, precisa de cuidados básicos:

-   Não publicar credenciais no GitHub.
-   Utilizar `.env` em ambiente local.
-   Utilizar variáveis de ambiente em produção.
-   Proteger endpoints de consulta e alteração.
-   Restringir o acesso ao bot do Telegram.
-   Fazer backups periódicos.
-   Evitar armazenar imagens e áudios sem necessidade.
-   Limitar tamanho e tipo dos arquivos recebidos.
-   Não registrar tokens ou dados sensíveis nos logs.
-   Utilizar HTTPS em produção.

Se a aplicação futuramente aceitar outros usuários, será necessário
implementar autenticação, autorização e isolamento dos dados por
usuário.

## 9.3. Prevenção de duplicidades

A duplicidade merece atenção especialmente quando houver mais de um
canal de entrada.

Exemplo: uma compra é registrada pelo Telegram e, depois, o comprovante
da mesma compra é enviado por imagem.

A aplicação pode identificar possíveis duplicidades considerando:

-   Valor.
-   Estabelecimento.
-   Data.
-   Descrição.

Não se deve bloquear automaticamente duas compras apenas porque têm o
mesmo valor e data: podem ser transações legítimas diferentes.

A abordagem recomendada é sinalizar possíveis duplicidades e solicitar
confirmação.

## 9.4. Tratamento de arquivos

Para áudio e imagem:

-   Validar extensão e tipo real do arquivo.
-   Limitar tamanho.
-   Evitar confiar somente no nome ou extensão.
-   Processar em ambiente controlado.
-   Definir tempo máximo de processamento.
-   Remover arquivos temporários.
-   Não executar arquivos recebidos.
-   Tratar falhas de OCR e transcrição sem criar registros incompletos.

------------------------------------------------------------------------

# 10. Roadmap e definição do MVP

## 10.1. Roadmap consolidado

    Ordem Entrega                   Resultado
  ------- ------------------------- ------------------------------------------
        1 Fundação e persistência   FastAPI, SQLite, SQLAlchemy e CRUD
        2 Extratos e relatórios     Totais, categorias e estabelecimentos
        3 Entrada textual           Parser e validação de mensagens
        4 Exportação Excel          Extrato em planilha
        5 Telegram                  Registro e consulta pelo celular
        6 Produção                  PostgreSQL, Docker, VPS, HTTPS e backups
        7 Entrada por voz           Transcrição e interpretação
        8 Entrada por imagem        OCR, extração e validação
        9 E-mail                    Envio automatizado de relatórios
       10 Dashboard                 Gráficos e indicadores

A ordem pode ser ajustada conforme o aprendizado e as prioridades. O
ponto importante é concluir entregas funcionais antes de ampliar o
escopo.

## 10.2. Definição do MVP

O MVP deve resolver o problema original sem depender de integrações
complexas.

### Checklist do MVP

-   [ ] API FastAPI executando localmente.
-   [ ] Banco SQLite configurado.
-   [ ] Cadastro de compras.
-   [ ] Consulta de compras.
-   [ ] Filtros por data, categoria e estabelecimento.
-   [ ] Atualização e exclusão de registros.
-   [ ] Extrato mensal.
-   [ ] Total gasto no mês.
-   [ ] Divisão percentual por categoria.
-   [ ] Resumo por estabelecimento.
-   [ ] Exportação do extrato para Excel.
-   [ ] Testes automatizados básicos.

Depois de concluir o MVP, a aplicação já poderá substituir o bloco de
notas. Telegram, voz e OCR serão evoluções, não pré-requisitos para o
sistema ser útil.

------------------------------------------------------------------------

# 11. Primeiros passos práticos

A recomendação é iniciar pela Fase 1, sem tentar implementar todas as
funcionalidades simultaneamente.

## 11.1. Sequência inicial

1.  Criar o repositório GitHub.
2.  Configurar o ambiente virtual Python.
3.  Instalar FastAPI e Uvicorn.
4.  Criar a estrutura inicial de diretórios.
5.  Criar `main.py`.
6.  Executar a API localmente.
7.  Acessar a documentação automática do Swagger.
8.  Criar a conexão com SQLite.
9.  Implementar o model `Compra`.
10. Criar o primeiro endpoint de registro.

A documentação interativa do Swagger ficará disponível em:

``` text
http://127.0.0.1:8000/docs
```

## 11.2. Ciclos de aprendizagem

Uma abordagem prática é aprender cada tecnologia conforme a necessidade
do projeto:

**Ciclo 1 --- Fundamentos:** Python, FastAPI, Pydantic, SQLAlchemy e
SQL.

**Ciclo 2 --- Regras de negócio:** cadastro, consultas, filtros e
cálculos financeiros.

**Ciclo 3 --- Integrações:** Telegram, processamento textual, voz e OCR.

**Ciclo 4 --- Infraestrutura:** Docker, PostgreSQL, VPS e publicação.

**Ciclo 5 --- Relatórios:** Excel, e-mail e dashboard.

Não é necessário dominar todas as tecnologias antes de começar. O
projeto pode ser desenvolvido e utilizado como instrumento de
aprendizagem.

------------------------------------------------------------------------

# 12. Documentação oficial

Estas são as principais referências para acompanhar o desenvolvimento:

-   [FastAPI --- Documentação oficial](https://fastapi.tiangolo.com/)
-   [Pydantic --- Documentação
    oficial](https://docs.pydantic.dev/latest/)
-   [SQLAlchemy 2.0 --- Documentação
    oficial](https://docs.sqlalchemy.org/en/20/)
-   [Alembic --- Migrations](https://alembic.sqlalchemy.org/en/latest/)
-   [Python Telegram Bot](https://docs.python-telegram-bot.org/)
-   [OpenPyXL](https://openpyxl.readthedocs.io/)
-   [Pytest](https://docs.pytest.org/)
-   [Docker --- Documentação oficial](https://docs.docker.com/)

------------------------------------------------------------------------

# Conclusão e decisões arquiteturais

A arquitetura recomendada para o projeto é:

```
  Decisão                  Escolha
  ------------------------ --------------
  Linguagem                Python
  Backend                  FastAPI
  Banco inicial            SQLite
  Banco em produção        PostgreSQL
  ORM                      SQLAlchemy
  Validação                Pydantic
  Versionamento do banco   Alembic
  Interface inicial        Swagger
  Interface de uso         Telegram
  Exportação               OpenPyXL
  Envio de e-mail          Resend
  Hospedagem               VPS + Docker
```

O principal princípio arquitetural é construir primeiro um sistema
confiável de registro e consulta. Depois, adicionar diferentes formas de
entrada de dados.

Telegram, texto livre, voz e OCR são canais diferentes para alimentar o
mesmo sistema. O banco de dados, os serviços e as regras de negócio
devem permanecer centralizados.

Desde o primeiro commit, recomenda-se manter serviços e repositórios
separados, configurações centralizadas, segredos em variáveis de
ambiente e testes acompanhando cada funcionalidade.

**Próxima entrega recomendada:** implementar o ambiente Python, a
estrutura de diretórios, a conexão SQLite e o primeiro endpoint FastAPI
para registrar uma compra.
