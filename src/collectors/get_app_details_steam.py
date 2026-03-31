import requests
import os
import json
import time
from datetime import datetime, timezone
from src.loaders.minio_loader import upload_json, read_json, list_objects

def get_app_details(appid: int):
    params = {        
        "appids": appid,
        "cc": "br"        
    }
    
    url = os.getenv("URL_BASE")
    print(f"Requisição para appid {appid}: {url} com params {params}")
    
    response = requests.get(url, params=params, timeout=30)
    print(response.url)
    print(f"Status code: {response.status_code}")
    response.raise_for_status()
    
    data = response.json()        
    return data

def save_to_minio(appid: int, data):
    bucket_name = os.getenv("RAW_BUCKET","raw")
    date_ref = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    object_name = f"steam/app_details/date={date_ref}/app_{appid}_details.json"
    
    content = json.dumps(data, ensure_ascii=False).encode("utf-8")
    upload_json(bucket_name, object_name, content)
    
    print(f"Dados do app {appid} salvos no MinIO: s3://{bucket_name}/{object_name}")
    
def get_latest_app_list_object(bucket_name: str) -> str:
    prefix = "steam/app_list/"
    objects = list_objects(bucket_name, prefix)

    json_files = [
        obj for obj in objects
        if obj.endswith(".json") and obj.split("/")[-1] == "steam_apps_list.json"
    ]

    if not json_files:
        raise FileNotFoundError(
            f"Nenhum arquivo app_list encontrado em s3://{bucket_name}/{prefix}"
        )

    latest_object = sorted(json_files)[-1]
    return latest_object
    
def run(limit: int = 20):
    bucket = os.getenv("RAW_BUCKET", "raw")

    print("Buscando app_list mais recente no MinIO...")
    object_name = get_latest_app_list_object(bucket)
    print(f"Arquivo mais recente encontrado: s3://{bucket}/{object_name}")

    print("Lendo app_list do MinIO...")
    data = read_json(bucket, object_name)

    apps = data.get("apps", [])
    appids = [app["appid"] for app in apps if "appid" in app]

    print(f"Total de apps encontrados: {len(appids)}")
    print(f"Processando apenas {limit} apps...")

    for i, appid in enumerate(appids[:limit], start=1):
        try:
            print(f"[{i}/{limit}] Buscando app {appid}...")

            details = get_app_details(appid)
            save_to_minio(appid, details)

            time.sleep(1)

        except Exception as e:
            print(f"Erro no app {appid}: {e}")

    print("Finalizado.")


if __name__ == "__main__":
    run()