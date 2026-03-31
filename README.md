# GamesAnalytics

Projeto de engenharia de dados para coleta e armazenamento de dados da Steam e Nuuvem, utilizando uma arquitetura baseada em data lake com MinIO.

---

## 🚀 O que já foi implementado

- Coleta da lista de jogos da Steam (`app_list`)
- Armazenamento dos dados brutos no MinIO (camada raw)
- Leitura dos dados armazenados para processamento
- Coleta de detalhes dos jogos (`app_details`) a partir dos `appids`
- Armazenamento dos dados por jogo (granularidade por `appid`)
- Estrutura inicial de pipeline organizada em collectors, loaders e processors

---

## 🧱 Arquitetura atual

Atualmente o projeto trabalha com a camada:

- **Raw (bronze)** → dados brutos da API da Steam armazenados no MinIO

Exemplo de estrutura:

```
raw/
  steam/
    app_list/
      2026-03-31/
        steam_apps_list.json
    app_details/
      date=2026-03-31/
        app_730_details.json
```

---

## ⚙️ Tecnologias utilizadas

- Python
- Docker / Docker Compose
- MinIO (S3 local)
- Requests

---

## 📁 Estrutura do Projeto

```
game-price-analytics/
├─ docker-compose.yml
├─ .env.example
├─ requirements.txt
├─ dockerfile
├─ src/
│  ├─ collectors/
│  │  ├─ get_app_list_steam.py
│  │  └─ get_app_details_steam.py
│  ├─ processors/
│  │  ├─ normalize.py
│  │  └─ compare_prices.py
│  ├─ loaders/
│  │  ├─ minio_loader.py
│  │  └─ supabase_loader.py
│  ├─ app/
│  │  └─ streamlit_app.py
│  └─ main.py
├─ sql/
│  └─ create_tables.sql
└─ .streamlit/
   └─ secrets.toml.example
```

## ▶️ Como rodar o projeto

### 1. Clonar o repositório

```bash
git clone <repo>
cd GameAnalytics
```

---

### 2. Configurar variáveis de ambiente

Crie um arquivo `.env` baseado no `.env.example`

Exemplo:

```env
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=minioadmin123

MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin123

RAW_BUCKET=raw

URL_BASE=https://store.steampowered.com/api/appdetails
```

---

### 3. Subir os containers

```bash
docker compose up -d
```

---

### 4. Acessar o container da aplicação

```bash
docker compose exec app sh
cd /app
```

---

### 5. Rodar a coleta de dados

#### Coletar lista de jogos

```bash
python -m src.collectors.get_app_list_steam
```

#### Coletar detalhes dos jogos (limitado para testes)

```bash
python -m src.collectors.get_app_details_steam
```

---

## 🔄 Atualizações no ambiente

Caso sejam feitas alterações em arquivos como:

- `Dockerfile`
- `requirements.txt`
- `.env`

é necessário recriar os containers para aplicar as mudanças:

```bash
docker compose down
docker compose up -d --build
```

---

## 🔎 Acessar o MinIO

Painel web:

http://localhost:9001

Login:

- user: minioadmin
- password: minioadmin123

---

## 📌 Observações

- Os dados são coletados da API pública da Steam
- A coleta de `app_details` é limitada para evitar rate limit
- Estrutura preparada para evolução futura (silver/gold, análise e dashboard)