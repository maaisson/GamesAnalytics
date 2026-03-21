# GamesAnalytics

## 📁 Estrutura do Projeto

```
game-price-analytics/
├─ docker-compose.yml
├─ .env.example
├─ requirements.txt
├─ src/
│  ├─ collectors/
│  │  ├─ steam_collector.py
│  │  └─ nuuvem_scraper.py
│  ├─ processors/
│  │  ├─ normalize.py
│  │  └─ compare_prices.py
│  ├─ loaders/
│  │  ├─ minio_client.py
│  │  └─ supabase_loader.py
│  ├─ app/
│  │  └─ streamlit_app.py
│  └─ main.py
├─ sql/
│  └─ create_tables.sql
└─ .streamlit/
   └─ secrets.toml.example
```