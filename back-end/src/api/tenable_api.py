from dotenv import load_dotenv
import os, time
from httpx import Client

load_dotenv("credentials.env")

class TenableApi():

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TenableApi, cls).__new__(cls)
        return cls._instance

    def __init__(self):

        if hasattr(self, "_initialized") and self._initialized:
            return

        self.secret_key = os.getenv("SECRET_KEY")
        self.access_key = os.getenv("ACCESS_KEY")

        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "X-ApiKeys": f"accessKey={self.access_key}; secretKey={self.secret_key}",
        }


        self.client = Client(base_url="https://cloud.tenable.com", verify=False, headers=self.headers)

    def get_user_id_from_username(self, user_name):

        url = "/users"

        users_json = self.client.get(url).json()["users"]

        for user in users_json:

            if (user["user_name"] == user_name):

                return user["uuid"]

        return None

    def get_all_web_app_scans_from_username(self, user_name: str) -> dict:

        user_id = self.get_user_id_from_username(user_name)

        total_scans = self.client.post("/was/v2/configs/search").json()["pagination"]["total"]
        itens_per_request = 200

        webb_app_scans: dict = {}

        for offset in range(0, total_scans, itens_per_request):
            limit = min(itens_per_request, total_scans - offset)

            scans = self.client.post(f"/was/v2/configs/search?limit={limit}&offset={offset}").json()["items"]

            for scan in scans:

                if (scan["owner_id"] == user_id):
                    webb_app_scans[scan["config_id"]] = scan
        
        return webb_app_scans
    
    def get_web_app_scans_from_folder_of_user(self, folder_name: str, user_name: str):

        url = "https://cloud.tenable.com/was/v2/configs/search"

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-ApiKeys": f"accessKey={self.access_key}; secretKey={self.secret_key}",
            'X-Impersonate' : f"username={user_name}"
        }

        params = {
            "limit" : 200
        }

        payload = {
            "field": "folder_name",
            "operator": "match",
            "value": folder_name,
        }

        scans = self.client.post(url, headers=headers, json=payload, params=params).json()

        current = 200
        total = scans['pagination']['total']

        if total > current:

            params['offset'] = current

            response = self.client.post(url, headers=headers, json=payload, params=params).json()

            print(response)

            for scan in response['items']:
                scans['items'].append(scan)

            current += 200

        return scans


    def get_web_app_folders_from_username(self, user_name: str) -> dict:

        url = f"/was/v2/folders"

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-ApiKeys": f"accessKey={self.access_key}; secretKey={self.secret_key}",
            'X-Impersonate' : f"username={user_name}"
        }
        
        response = self.client.get(url=url, headers=headers).json()

        return response
    
    def get_web_app_scans_from_targetname_and_username(self, target_name: str, user_name: str) -> dict:

        all_scans_from_username: dict = self.get_all_web_app_scans_from_username(user_name)

        result = {}

        for scan_id, scan_data in all_scans_from_username.items():

            if (target_name in scan_data["target"]):
                result[scan_id] = scan_data
        
        return result
    
    def download_scans_results_json(self, target_dir: str, scans: dict) -> None:

        scans = scans["items"]

        for data in scans:

            scan_id = data["last_scan"]["scan_id"]

            url = f"/was/v2/scans/{scan_id}/report"

            response = self.client.put(url)

            if response.status_code == 200:
                response = self.client.get(url)

                #
                #   Salvando dados do scan
                #
                with open(f"{target_dir}/{scan_id}.json", "w", encoding="utf-8") as file:
                    file.write(response.text)

    def get_vmscans_from_name(self, name: str) -> dict:

        url = "/scans"

        scans_json = self.client.get(url).json()["scans"]

        for scan in scans_json:

            if (scan["name"] == name):

                return scan

        return None
    
    def download_vmscans_csv(self, target_dir: str, id_scan: str, story_id: str) -> None:

        print(id_scan)
        print(story_id)

        url = f"https://cloud.tenable.com/scans/{id_scan}/export?history_id={story_id}"

        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-ApiKeys": f"accessKey={self.access_key}; secretKey={self.secret_key}",
        }

        payload = {
            "chapters": "",
            "format": "csv"
        }

        client = Client(headers=headers)

        response = client.post(url, json=payload).json()

        print(response)

        # temp_token = response["temp_token"]

        file = response["file"]

        response = client.get(f"https://cloud.tenable.com/scans/{id_scan}/export/{file}/status").json()["status"]

        while (response != "ready"):
            response = client.get(f"https://cloud.tenable.com/scans/{id_scan}/export/{file}/status").json()["status"]
            time.sleep(1)

        response = client.get(
            f"https://cloud.tenable.com/scans/{id_scan}/export/{file}/download")

        with open(f"{target_dir}/servidores_scan.csv", "w", encoding="utf-8") as file:
            file.write(response.text)

            






