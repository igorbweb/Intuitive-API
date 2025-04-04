from fastapi import FastAPI, Query, HTTPException
import os
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

JSON_PATH = os.path.join(os.path.dirname(__file__), "Relatorio_cadop.json")

def carregar_dados():
    if not os.path.exists(JSON_PATH):
        raise HTTPException(status_code=404, detail="Arquivo JSON não encontrado")

    with open(JSON_PATH, "r", encoding="utf-8") as file:
        return json.load(file)
    
@app.get("/")
def home():
    return {
        "mensagem": "Bem-vindo à API da Intuitive Care.",
        "descricao": "Esta API permite consultar os dados públicos divulgados pelo Governo Federal à respeito das Operadoras cadastradas na ANS.",
        "rotas_disponiveis": {
            "/todos": "Exibe todos os dados disponíveis para consulta no Banco de Dados",
            "/buscar": "Busca avançada com múltiplos filtros (registro, CNPJ, cidade, UF, modalidade)",
            "/registro/{registro_ans}": "Consulta operadora pelo Registro ANS",
            "/cnpj/{cnpj}": "Consulta operadora pelo CNPJ",
            "/cidade/{cidade}": "Lista operadoras por cidade",
            "/uf/{uf}": "Lista operadoras por estado",
            "/modalidade/{modalidade}": "Lista operadoras por modalidade"
        },
        "exemplos_de_uso": {
            "Buscar por Registro ANS": "/registro/419761",
            "Buscar por CNPJ": "/cnpj/19541931000125",
            "Buscar operadoras em São Paulo": "/cidade/São Paulo",
            "Buscar operadoras em Minas Gerais": "/uf/MG",
            "Buscar operadoras de Odontologia": "/modalidade/Odontologia de Grupo",
            "Busca avançada (cidade + UF)": "/buscar?cidade=Belo Horizonte&uf=MG"
        }
    }

@app.get("/todos")
def todos():
    dados = carregar_dados()
    
    if not dados:
        raise HTTPException(status_code=404, detail="Nenhum dado encontrado")
    
    return {"total_registros": len(dados), "dados": dados}
    
@app.get("/registro/{registro_ans}")
def get_registro(registro_ans: str):
    dados = carregar_dados()
    
    resultado = [item for item in dados if item["Registro_ANS"].strip() == registro_ans.strip()]
    
    if not resultado:
        raise HTTPException(status_code=404, detail=f"Registro {registro_ans} não encontrado")

    return resultado

@app.get("/cnpj/{cnpj}")
def get_cnpj(cnpj: str):
    dados = carregar_dados()
    
    resultado = [item for item in dados if item["CNPJ"].strip() == cnpj.strip()]
    
    if not resultado:
        raise HTTPException(status_code=404, detail=f"CNPJ {cnpj} não encontrado")

    return resultado

@app.get("/cidade/{cidade}")
def get_cidade(cidade: str):
    dados = carregar_dados()
    
    resultado = [item for item in dados if item["Cidade"].strip().lower() == cidade.strip().lower()]
    
    if not resultado:
        raise HTTPException(status_code=404, detail=f"Nenhuma operadora encontrada na cidade {cidade}")

    return resultado

@app.get("/uf/{uf}")
def get_uf(uf: str):
    dados = carregar_dados()
    
    resultado = [item for item in dados if item["UF"].strip().upper() == uf.strip().upper()]
    
    if not resultado:
        raise HTTPException(status_code=404, detail=f"Nenhuma operadora encontrada no estado {uf}")

    return resultado

@app.get("/modalidade/{modalidade}")
def get_modalidade(modalidade: str):
    dados = carregar_dados()
    
    resultado = [item for item in dados if item["Modalidade"].strip().lower() == modalidade.strip().lower()]
    
    if not resultado:
        raise HTTPException(status_code=404, detail=f"Nenhuma operadora encontrada na modalidade {modalidade}")

    return resultado

@app.get("/buscar")
def buscar (
    registro_ans: str = Query(None, alias="registro"),
    cnpj: str = Query(None),
    cidade: str = Query(None),
    uf: str = Query(None),
    modalidade: str = Query(None) 
):
    dados = carregar_dados()
    
    resultado = [
        item for item in dados
        if (registro_ans is None or item["Registro_ANS"].strip() == registro_ans.strip()) and
        (cnpj is None or item["CNPJ"].strip() == cnpj.strip()) and
        (cidade is None or item["Cidade"].strip().lower() == cidade.strip().lower()) and
        (uf is None or item["UF"].strip().upper() == uf.strip().upper()) and
        (modalidade is None or item["Modalidade"].strip().lower() == modalidade.strip().lower())
    ]
    
    if not resultado:
        raise HTTPException(status_code=404, detail="Nenhum resultado encontrado com os filtros fornecidos")

    return resultado