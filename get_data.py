import requests
import pandas as pd
import time


def get_data(cep):
    """
    Consulta a API ViaCEP para obter informações de um CEP.
    Args:
        cep: CEP no formato string (com ou sem hífen)
    Returns:
        dict: Dados do CEP se encontrado, None se houver erro
    """
    cep_limpo = cep.replace("-", "").strip()
    
    # Valida formato básico (8 dígitos)
    if not cep_limpo.isdigit() or len(cep_limpo) != 8:
        print(f"⚠️  CEP inválido: {cep}")
        return None
    
    endpoint = f"https://viacep.com.br/ws/{cep_limpo}/json/"
    
    try:
        response = requests.get(endpoint, timeout=5)
        
        if response.status_code == 200:
            cep_info = response.json()
            
            # IMPORTANTE: A API ViaCEP retorna {"erro": true} quando o CEP não é encontrado
            # Mesmo com status 200, pode haver erro no conteúdo
            if "erro" in cep_info and cep_info["erro"]:
                print(f"❌ CEP não encontrado: {cep}")
                return None
            else:
                print(f"✅ CEP encontrado: {cep} - {cep_info.get('localidade', 'N/A')}/{cep_info.get('uf', 'N/A')}")
                return cep_info
        else:
            print(f"⚠️  Erro HTTP {response.status_code} para CEP: {cep}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Erro na requisição para CEP {cep}: {e}")
        return None

users_path = "01-bronze-raw/users.csv"
users_df = pd.read_csv(users_path)
cep_list = users_df["cep"].tolist()

print(f"Consultando {len(cep_list)} CEPs...\n")

resultados = []
for cep in cep_list:
    cep_clean = cep.replace("-", "")
    cep_info = get_data(cep_clean)
    if cep_info:
        resultados.append(cep_info)
        
    time.sleep(0.7)

print(f"\n📊 Resumo: {len(resultados)} CEPs encontrados de {len(cep_list)} consultados")
