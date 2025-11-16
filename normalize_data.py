import os
import json
import time
import requests
import pandas as pd

input_dir = '01-bronze-raw' # diretório de entrada( ler os arquivos csv e json)
output_dir = '02-silver-validated' # diretório de saída( salvar com paquet)

os.makedirs(output_dir, exist_ok=True) # cria o diretório de saída se não existir

def get_cep_info(cep):
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
        return None
    
    endpoint = f"https://viacep.com.br/ws/{cep_limpo}/json/"
    
    try:
        response = requests.get(endpoint, timeout=5)
        
        if response.status_code == 200:
            cep_info = response.json()
            
            # IMPORTANTE: A API ViaCEP retorna {"erro": true} quando o CEP não é encontrado
            if "erro" in cep_info and cep_info["erro"]:
                return None
            else:
                return cep_info
        else:
            return None
            
    except requests.exceptions.RequestException:
        return None

for file in os.listdir(input_dir):
    input_path = os.path.join(input_dir, file)
    name, ext = os.path.splitext(file)
    output_path = os.path.join(output_dir, f'{name}.parquet')
    
    if ext.lower() == '.csv':
        df = pd.read_csv(input_path)
    elif ext.lower() == '.json':
        # tenta ler como lista de objetos
        try:
            df = pd.read_json(input_path)
        except ValueError:
            # se falhar tenta ler como linha separadas
            df = pd.read_json(input_path,  lines=True)
    else:
        print(f"Arquivo {file} ignorado (formato não suportado)")
        continue
    
    # Converte colunas do tipo list para string para permitir a drop_duplicates
    # Listas não são hashable e causam erro no drop_duplicates
    for col in df.columns:
        # Verifica se a coluna contém listas
        if df[col].apply(lambda x: isinstance(x, list)).any():
            # Converte listas para string JSON para manter a estrutura
            df[col] = df[col].apply(lambda x: json.dumps(x, ensure_ascii=False) if isinstance(x, list) else x)
    
    df = df.drop_duplicates().reset_index(drop=True)
    
    #salva em formato .parquet
    df.to_parquet(output_path, index=False)
    print(f"Arquivo {file} salvo em {output_path} ✅")
    
    # Se for o arquivo users.csv, gera também o cep_info.parquet
    if file.lower() == 'users.csv' and 'cep' in df.columns:
        print("\n🔄 Gerando cep_info.parquet com dados da API ViaCEP...")
        
        # Pega CEPs únicos
        ceps_unicos = df["cep"].unique().tolist()
        print(f"📋 Total de CEPs únicos para consultar: {len(ceps_unicos)}")
        
        # Consulta cada CEP único
        ceps_info = []
        ceps_encontrados = 0
        ceps_nao_encontrados = 0
        
        for i, cep in enumerate(ceps_unicos, 1):
            cep_info = get_cep_info(cep)
            
            if cep_info:
                # Adiciona o CEP original (com hífen) ao resultado
                cep_info['cep_original'] = cep
                ceps_info.append(cep_info)
                ceps_encontrados += 1
                
                if i % 50 == 0:
                    print(f"  [{i}/{len(ceps_unicos)}] ✅ {ceps_encontrados} encontrados, ❌ {ceps_nao_encontrados} não encontrados")
            else:
                ceps_nao_encontrados += 1
                if i % 50 == 0:
                    print(f"  [{i}/{len(ceps_unicos)}] ✅ {ceps_encontrados} encontrados, ❌ {ceps_nao_encontrados} não encontrados")
            
            # Delay para não sobrecarregar a API
            time.sleep(0.8)
        
        print("\n📊 Resumo CEPs:")
        print(f"  ✅ CEPs encontrados: {ceps_encontrados}")
        print(f"  ❌ CEPs não encontrados: {ceps_nao_encontrados}")
        if ceps_info:
            cep_df = pd.DataFrame(ceps_info)
            
            # Reordena colunas para ter cep_original primeiro
            cols = ['cep_original'] + [col for col in cep_df.columns if col != 'cep_original']
            cep_df = cep_df[cols]
            
            cep_df = cep_df.drop_duplicates(subset=['cep_original']).reset_index(drop=True)
            
            cep_output_path = os.path.join(output_dir, 'cep_info.parquet')
            cep_df.to_parquet(cep_output_path, index=False)
            print(f"✅ Arquivo cep_info.parquet salvo em {cep_output_path}")
            print(f"📊 Total de registros salvos: {len(cep_df)}\n")
        else:
            print("⚠️  Nenhum CEP foi encontrado.\n")
    
    

