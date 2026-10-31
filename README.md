### Conferir plano_desenvolvimento_api_controle_compras.md

### Fontes consultadas
https://tiangolo.com/guides/virtual-environments/


### Comando utilizados
`python -m venv .venv`: cria virtual environment na pasta .venv usando o module de venv do Python
`.venv/Scripts/Activate`: ativa o venv 
`python -m pip install --upgrade pip`: chama o module pip pra fazer upgrade do pip antes de instalar as dependencies
`pip install -r requirements.txt`: le as dependencies do requirements.txt e instala 
`pip-compile --upgrade --output-file=requirements.txt requirements.in`: le o requirements.txt, verifica as dependencies diretas e localiza as transitórias. 
                                                                        escreve o novo requirements.txt com as dependencies com suas versões exatas.
