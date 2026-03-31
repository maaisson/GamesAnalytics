import requests
import os
import json
import time
from datetime import datetime, timezone

from loaders.minio_loader import upload_json

def get_app_list():
    all_apps = []
    last_appid = 0
    
    while True:
        params = {
            "key": os.getenv("STEAM_API_KEY"),
            "max_results": 50000,
            "last_appid": last_appid
        }
        
        response = requests.get(f"https://api.steampowered.com/IStoreService/GetAppList/v1/", params=params, timeout=30)                               
        response.raise_for_status()
        
        data = response.json()["response"]        
        apps = data.get("apps", [])
        all_apps.extend(apps)
        
        print(f"Coletados: {len(all_apps)} apps")
        
        if not data.get("have_more_results", False):
            break
        
        last_appid = data.get("last_appid", 0)
        
        time.sleep(1)  # Evitar sobrecarregar a API
        
    payload = {
        "source": "steam_istoreservice_getapplist_v1",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_apps": len(all_apps),
        "apps": all_apps
    }
        
    return payload

def save_to_minio(data):
    bucket_name = os.getenv("RAW_BUCKET","raw")
    data_ref = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    object_name = f"steam/app_list/{data_ref}/steam_apps_list.json"
    
    content = json.dumps(data, ensure_ascii=False).encode("utf-8")
    upload_json(bucket_name, object_name, content)
    
    print(f"Dados salvos no MinIO: s3://{bucket_name}/{object_name}")                            
        
if __name__ == "__main__":
    all_apps = get_app_list()
    save_to_minio(all_apps)