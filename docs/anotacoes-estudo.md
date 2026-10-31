# Anotações de Estudo

### Fontes consultadas
https://tiangolo.com/guides/virtual-environments/


## Dependências do projeto:

### SQLAlchemy
ORM utilizado pra mapear classes pra dentro do banco de dados, trazendo abstração de gerenciamento do BD sem precisar escrever SQL.
Traz uma camada de aplicação acima da API de conexão ao banco de dados. Dessa forma, o código de persistência e mapeamento das classes é o mesmo
pra qualquer BD utilizado.
Isso se deve à divisão do SQLAlchemy em duas APIs: ORM (mapeamento das classes) e Core (persistência, gerenciamento e conexão do BD)


### Comando utilizados
`python -m venv .venv`: cria virtual environment na pasta .venv usando o module de venv do Python
`.venv/Scripts/Activate`: ativa o venv 
`python -m pip install --upgrade pip`: chama o module pip pra fazer upgrade do pip antes de instalar as dependencies
`pip install -r requirements.txt`: le as dependencies do requirements.txt e instala 
`pip-compile --upgrade --output-file=requirements.txt requirements.in`: le o requirements.txt, verifica as dependencies diretas e localiza as transitórias. 
                                                                        escreve o novo requirements.txt com as dependencies com suas versões exatas.
