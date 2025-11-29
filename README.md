# Projeto ETL - Arquitetura Medalhão

Projeto prático de Engenharia de Dados implementando uma arquitetura Medalhão (Medallion Architecture) completa, desenvolvido como parte do curso "Curso Prático em Python: ETL Completo com Arquitetura Medalhão Passo a Passo" do canal **Data Engineer Help**.

## 📋 Sobre o Projeto

Este projeto implementa uma pipeline ETL (Extract, Transform, Load) utilizando a Arquitetura Medalhão, que organiza os dados em três camadas principais:

- **Bronze (Raw)**: Dados brutos, sem transformação
- **Silver (Cleansed)**: Dados limpos, validados e padronizados
- **Gold (Curated)**: Dados agregados, enriquecidos e prontos para consumo

## 🏗️ Estrutura do Projeto

```
P Arquiteturas Medalhão/
│
├── 01-bronze-raw/          # Camada Bronze - Dados brutos
│   ├── users.csv           # 70.000 registros de usuários
│   └── products.json       # 80.000 registros de produtos
│
├── 02-silver-validated/    # Camada Silver - Dados limpos
|   ├── cep_info.parquet        
|   ├── products.parquet
│   └── users.parquet     
│
├── 03-gold-enriched/       # Camada Gold - Dados enriquecidos
│
├── gerar_dados.py          # Script para gerar dados de usuários
├── gerar_produtos.py       # Script para gerar dados de produtos
├── get_data.py             # Script para consultar API ViaCEP
├── arquitetura_medalhao.png # Diagrama da arquitetura
├── db.py # CRUD para o banco de dados
├── docker-compose.yml # Infraestrutura do PostGreSQL Em um container na Docker
│
├── requirements.txt        # Dependências do projeto
├── README.md              # Este arquivo
└── .gitignore             # Arquivos ignorados pelo Git
```

## 📊 Dados

### Users (users.csv)
Arquivo CSV contendo 70.000 registros de usuários com os seguintes campos:
- `id`: Identificador único
- `nome`: Nome completo
- `email`: Endereço de email
- `telefone`: Telefone com DDD no formato (XX) XXXXX-XXXX
- `cep`: CEP brasileiro (870 variações reais)
- `data_nascimento`: Data no formato yyyy-mm-dd
- `genero`: M ou F

### Products (products.json)
Arquivo JSON contendo 80.000 registros de produtos com os seguintes campos:
- `id`: Identificador único
- `nome`: Nome do produto
- `categoria`: Categoria do produto
- `preco`: Preço (float)
- `marca`: Marca do produto
- `descricao`: Descrição do produto
- `estoque`: Quantidade em estoque
- `avaliacao`: Avaliação (float de 3.0 a 5.0)
- `tags`: Array de tags para pesquisa

## 🚀 Como Usar

### 1. Instalação

Clone o repositório:

```bash
git clone <url-do-repositorio>
cd "P Arquiteturas Medalhão"
```

#### Opção 1: Usar o ambiente virtual (recomendado)

Crie e ative o ambiente virtual:

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

Depois instale as dependências:
```bash
pip install -r requirements.txt
```

#### Opção 2: Instalação global

```bash
pip install -r requirements.txt
```

### 2. Gerar Dados

Para gerar os dados de usuários:

```bash
python gerar_dados.py
```

Para gerar os dados de produtos:

```bash
python gerar_produtos.py
```

### 3. Consultar API ViaCEP

O script `get_data.py` demonstra como consultar a API ViaCEP para enriquecer os dados de CEP:

```python
from get_data import get_data

cep_info = get_data("30112000")
print(cep_info)
```

## 🎯 Arquitetura Medalhão

### Bronze Layer (Raw)
- **Propósito**: Armazenar dados brutos exatamente como recebidos
- **Características**: 
  - Sem transformação
  - Backup completo
  - Auditoria e histórico
  - Landing zone

### Silver Layer (Cleansed)
- **Propósito**: Dados limpos e validados
- **Transformações**:
  - Validação de dados
  - Deduplicação
  - Enriquecimento (ex: dados do ViaCEP)
  - Padronização e tipagem

### Gold Layer (Curated)
- **Propósito**: Dados prontos para consumo
- **Características**:
  - Agregações de negócio
  - Tabelas dimensionais
  - Dados enriquecidos
  - Prontos para dashboards, relatórios e ML

## 📚 Tecnologias Utilizadas

- **Python 3.x**: Linguagem principal
- **Pandas**: Manipulação e análise de dados
- **Requests**: Requisições HTTP para APIs
- **NumPy**: Operações numéricas

## 📖 Referências

- Curso: "Curso Prático em Python: ETL Completo com Arquitetura Medalhão Passo a Passo"
- Canal: [Data Engineer Help](https://www.youtube.com/@DataEngineerHelp)
- API ViaCEP: https://viacep.com.br/

## 📝 Estrutura de Dados

### CEPs Utilizados
O projeto utiliza 870 CEPs reais do Brasil, cobrindo:
- Capitais e grandes cidades
- Diferentes estados brasileiros
- CEPs válidos para consulta na API ViaCEP

### DDDs Utilizados
37 DDDs brasileiros incluindo todas as capitais e principais regiões.

## 🤝 Contribuindo

Este é um projeto educacional. Sinta-se à vontade para:
- Fazer fork do projeto
- Criar branches para suas melhorias
- Submeter pull requests

## 📄 Licença

Este projeto é de uso educacional e está disponível para fins de aprendizado.

## 👨‍💻 Autor

Desenvolvido como parte do curso de Engenharia de Dados.

---

**Nota**: Este projeto foi criado para fins educacionais e demonstração da Arquitetura Medalhão em Python.

