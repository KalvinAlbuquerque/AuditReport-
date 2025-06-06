import requests
import json

# # URL base da API Flask
BASE_URL = "http://127.0.0.1:5000/listas"

#Passo 1: Criar uma nova lista
# nova_lista = {
#     "nomeLista": "Lista Teste"
# }

headers = {
    'Content-Type': 'application/json'
}

# response = requests.post(f"{BASE_URL}/criarLista/", data=json.dumps(nova_lista), headers=headers)

# if response.status_code == 200:
#     id_lista_criada = response.text
#     print(f"Lista criada com sucesso. ID: {id_lista_criada}")
# else:
#     print(f"Erro ao criar lista: {response.status_code} {response.text}")
#     exit()


# ===================================================================================
# url = "http://127.0.0.1:5000/scans/webapp/downloadscans/"

payload = {
    "nomeLista": "Lista Teste",
    "scans" : {
  "items": [
    {
        "config_id": "cdb5d917-d95c-4f96-9233-36509c2c7d5e",
        "created_at": "2025-03-23T04:12:11.551059Z",
        "description": "https://www.credenciamento.salvador.ba.gov.br/PCRE/",
        "imported": False,
        "in_remediation": False,
        "in_trash": False,
        "is_shared": False,
        "last_scan": {
            "application_uri": "https://www.credenciamento.salvador.ba.gov.br/PCRE/",
            "asset_id": "6d5398eb-456b-4a63-ac06-0816fc2e69eb",
            "cicd_scan": False,
            "config_id": "cdb5d917-d95c-4f96-9233-36509c2c7d5e",
            "config_metadata": {
            "template": {
                "description": "A scan that checks a web application for vulnerabilities.",
                "name": "scan",
                "template_id": "b223f18e-5a94-4e02-b560-77a4a8246cd3"
            },
            "user_template": {
                "description": None,
                "name": None,
                "owner_id": None,
                "user_template_id": None
            }
            },
            "created_at": "2025-03-23T04:12:12.757647Z",
            "finalized_at": "2025-03-23T08:12:21.372936Z",
            "metadata": {
            "audited_pages": 403,
            "audited_urls": 392,
            "found_urls": 2760,
            "queued_pages": 0,
            "queued_urls": 0,
            "request_count": 184281,
            "response_time": 0,
            "scan_status": "running"
            },
            "paused_at": [],
            "requested_action": "start",
            "resumed_at": [],
            "scan_id": "04ef1bf5-38e2-4e8f-bc0c-0f00563bc2a2",
            "scanner": {
            "name": "TNB-WAS01",
            "version": "2.30.7"
            },
            "started_at": "2025-03-23T04:12:48.556127Z",
            "status": "aborted",
            "target": "https://www.credenciamento.salvador.ba.gov.br/PCRE/",
            "template_name": "scan",
            "updated_at": "2025-03-23T08:12:21.373406Z",
            "user_id": "52301418-1bc6-46c3-a114-3494bd82c831"
        },
        "name": "https://www.credenciamento.salvador.ba.gov.br/PCRE/",
        "owner_id": "52301418-1bc6-46c3-a114-3494bd82c831",
        "schedule": None,
        "target": "https://www.credenciamento.salvador.ba.gov.br/PCRE/",
        "target_count": 1,
        "template_id": "b223f18e-5a94-4e02-b560-77a4a8246cd3",
        "updated_at": "2025-03-23T04:12:11.551060Z",
        "user_permissions": "configure",
        "user_template": None
        },
        {
        "config_id": "2e26b493-d367-486d-8a92-e1ca9a617fa8",
        "created_at": "2025-03-23T04:11:55.887699Z",
        "description": "http://gct.salvador.ba.gov.br/\n\n ",
        "imported": False,
        "in_remediation": False,
        "in_trash": False,
        "is_shared": False,
        "last_scan": {
            "application_uri": "http://gct.salvador.ba.gov.br/",
            "asset_id": "e403ed48-e8ed-44c1-868c-f6fe2b23efab",
            "cicd_scan": False,
            "config_id": "2e26b493-d367-486d-8a92-e1ca9a617fa8",
            "config_metadata": {
            "template": {
                "description": "A scan that checks a web application for vulnerabilities.",
                "name": "scan",
                "template_id": "b223f18e-5a94-4e02-b560-77a4a8246cd3"
            },
            "user_template": {
                "description": None,
                "name": None,
                "owner_id": None,
                "user_template_id": None
            }
            },
            "created_at": "2025-03-23T04:11:57.244305Z",
            "finalized_at": "2025-03-23T04:16:36.631633Z",
            "metadata": {
            "audited_pages": 2,
            "audited_urls": 2,
            "found_urls": 2,
            "queued_pages": 0,
            "queued_urls": 0,
            "request_count": 5491,
            "response_time": 0,
            "scan_status": "running"
            },
            "paused_at": [],
            "requested_action": "start",
            "resumed_at": [],
            "scan_id": "15ef46ac-6836-46fb-8af0-737c2469ce80",
            "scanner": {
            "name": "TNB-WAS02",
            "version": "2.30.7"
            },
            "started_at": "2025-03-23T04:12:22.887932Z",
            "status": "completed",
            "target": "http://gct.salvador.ba.gov.br/",
            "template_name": "scan",
            "updated_at": "2025-03-23T04:16:36.632178Z",
            "user_id": "52301418-1bc6-46c3-a114-3494bd82c831"
        },
        "name": "http://gct.salvador.ba.gov.br/",
        "owner_id": "52301418-1bc6-46c3-a114-3494bd82c831",
        "schedule": None,
        "target": "http://gct.salvador.ba.gov.br/",
        "target_count": 1,
        "template_id": "b223f18e-5a94-4e02-b560-77a4a8246cd3",
        "updated_at": "2025-03-23T04:11:55.887700Z",
        "user_permissions": "configure",
        "user_template": None
        },
        {
        "config_id": "193fd816-51fb-4d72-bdc0-1bdd253ee65b",
        "created_at": "2025-03-23T04:11:41.162537Z",
        "description": "http://dom.salvador.ba.gov.br/\n\n ",
        "imported": False,
        "in_remediation": False,
        "in_trash": False,
        "is_shared": False,
        "last_scan": {
            "application_uri": "http://dom.salvador.ba.gov.br/",
            "asset_id": "62ed81c7-ff03-4c75-93c5-af12e16534e1",
            "cicd_scan": False,
            "config_id": "193fd816-51fb-4d72-bdc0-1bdd253ee65b",
            "config_metadata": {
            "template": {
                "description": "A scan that checks a web application for vulnerabilities.",
                "name": "scan",
                "template_id": "b223f18e-5a94-4e02-b560-77a4a8246cd3"
            },
            "user_template": {
                "description": None,
                "name": None,
                "owner_id": None,
                "user_template_id": None
            }
            },
            "created_at": "2025-03-23T04:11:43.170365Z",
            "finalized_at": "2025-03-23T05:12:34.090574Z",
            "metadata": {
            "audited_pages": 22,
            "audited_urls": 21,
            "found_urls": 66,
            "queued_pages": 0,
            "queued_urls": 0,
            "request_count": 60403,
            "response_time": 0,
            "scan_status": "running"
            },
            "paused_at": [],
            "requested_action": "start",
            "resumed_at": [],
            "scan_id": "40023ef8-0acd-4775-9ea7-ef49526f50fb",
            "scanner": {
            "name": "TNB-WAS01",
            "version": "2.30.7"
            },
            "started_at": "2025-03-23T04:12:18.198839Z",
            "status": "completed",
            "target": "http://dom.salvador.ba.gov.br/",
            "template_name": "scan",
            "updated_at": "2025-03-23T05:12:34.091332Z",
            "user_id": "52301418-1bc6-46c3-a114-3494bd82c831"
        },
        "name": "http://dom.salvador.ba.gov.br/",
        "owner_id": "52301418-1bc6-46c3-a114-3494bd82c831",
        "schedule": None,
        "target": "http://dom.salvador.ba.gov.br/",
        "target_count": 1,
        "template_id": "b223f18e-5a94-4e02-b560-77a4a8246cd3",
        "updated_at": "2025-03-23T04:11:41.162537Z",
        "user_permissions": "configure",
        "user_template": None
        },
        {
        "config_id": "847c8d36-53c7-4a1e-a9ad-9c760484bf19",
        "created_at": "2025-03-23T04:11:25.735826Z",
        "description": "https://www.cargos.salvador.ba.gov.br/",
        "imported": False,
        "in_remediation": False,
        "in_trash": False,
        "is_shared": False,
        "last_scan": {
            "application_uri": "https://www.cargos.salvador.ba.gov.br/",
            "asset_id": "9edcdcc5-786f-4686-a96c-c5c8e6b725c0",
            "cicd_scan": False,
            "config_id": "847c8d36-53c7-4a1e-a9ad-9c760484bf19",
            "config_metadata": {
            "template": {
                "description": "A scan that checks a web application for vulnerabilities.",
                "name": "scan",
                "template_id": "b223f18e-5a94-4e02-b560-77a4a8246cd3"
            },
            "user_template": {
                "description": None,
                "name": None,
                "owner_id": None,
                "user_template_id": None
            }
            },
            "created_at": "2025-03-23T04:12:31.423152Z",
            "finalized_at": "2025-03-23T04:13:26.602041Z",
            "metadata": {
            "audited_pages": 0,
            "audited_urls": 0,
            "found_urls": 1,
            "queued_pages": 0,
            "queued_urls": 0,
            "request_count": 2,
            "response_time": 0,
            "scan_status": "running"
            },
            "paused_at": [],
            "requested_action": "start",
            "resumed_at": [],
            "scan_id": "4addfaba-5f22-46eb-876f-05950b657350",
            "scanner": {
            "name": "TNB-WAS01",
            "version": "2.30.7"
            },
            "started_at": "2025-03-23T04:13:18.901549Z",
            "status": "aborted",
            "target": "https://www.cargos.salvador.ba.gov.br/",
            "template_name": "scan",
            "updated_at": "2025-03-23T04:13:26.602795Z",
            "user_id": "52301418-1bc6-46c3-a114-3494bd82c831"
        },
        "name": "https://www.cargos.salvador.ba.gov.br/",
        "owner_id": "52301418-1bc6-46c3-a114-3494bd82c831",
        "schedule": None,
        "target": "https://www.cargos.salvador.ba.gov.br/",
        "target_count": 1,
        "template_id": "b223f18e-5a94-4e02-b560-77a4a8246cd3",
        "updated_at": "2025-03-23T04:11:25.735826Z",
        "user_permissions": "configure",
        "user_template": None
        },
        {
        "config_id": "8c4fd30d-5f13-46c0-9bca-cf3f0a4682f3",
        "created_at": "2025-03-23T04:10:51.570797Z",
        "description": "http://agenciadenoticias.salvador.ba.gov.br/",
        "imported": False,
        "in_remediation": False,
        "in_trash": False,
        "is_shared": False,
        "last_scan": {
            "application_uri": "http://agenciadenoticias.salvador.ba.gov.br/",
            "asset_id": "de87a110-d789-4135-a503-d4f78e7340aa",
            "cicd_scan": False,
            "config_id": "8c4fd30d-5f13-46c0-9bca-cf3f0a4682f3",
            "config_metadata": {
            "template": {
                "description": "A scan that checks a web application for vulnerabilities.",
                "name": "scan",
                "template_id": "b223f18e-5a94-4e02-b560-77a4a8246cd3"
            },
            "user_template": {
                "description": None,
                "name": None,
                "owner_id": None,
                "user_template_id": None
            }
            },
            "created_at": "2025-03-23T04:10:53.258835Z",
            "finalized_at": "2025-03-23T06:05:56.512510Z",
            "metadata": {
            "audited_pages": 2,
            "audited_urls": 2,
            "found_urls": 79,
            "queued_pages": 0,
            "queued_urls": 0,
            "request_count": 5797,
            "response_time": 4,
            "scan_status": "running"
            },
            "paused_at": [],
            "requested_action": "start",
            "resumed_at": [],
            "scan_id": "31ca0614-aefa-475c-8841-d9849f09481c",
            "scanner": {
            "group_name": "Group_WAS",
            "name": "TNB-WAS03",
            "version": "2.30.7"
            },
            "started_at": "2025-03-23T04:12:17.318781Z",
            "status": "aborted",
            "target": "http://agenciadenoticias.salvador.ba.gov.br/",
            "template_name": "scan",
            "updated_at": "2025-03-23T06:05:56.514131Z",
            "user_id": "52301418-1bc6-46c3-a114-3494bd82c831"
        },
        "name": "http://agenciadenoticias.salvador.ba.gov.br/",
        "owner_id": "52301418-1bc6-46c3-a114-3494bd82c831",
        "schedule": None,
        "target": "http://agenciadenoticias.salvador.ba.gov.br/",
        "target_count": 1,
        "template_id": "b223f18e-5a94-4e02-b560-77a4a8246cd3",
        "updated_at": "2025-03-23T04:10:51.570797Z",
        "user_permissions": "configure",
        "user_template": None
        },
        {
        "config_id": "079e11fa-e770-4e58-ac49-f420b119e71c",
        "created_at": "2025-03-23T04:10:32.946519Z",
        "description": "https://comunicacao.salvador.ba.gov.br/",
        "imported": False,
        "in_remediation": False,
        "in_trash": False,
        "is_shared": False,
        "last_scan": {
            "application_uri": "https://comunicacao.salvador.ba.gov.br/",
            "asset_id": "146b5fe2-7084-421d-8d55-8a344403a7f2",
            "cicd_scan": False,
            "config_id": "079e11fa-e770-4e58-ac49-f420b119e71c",
            "config_metadata": {
            "template": {
                "description": "A scan that checks a web application for vulnerabilities.",
                "name": "scan",
                "template_id": "b223f18e-5a94-4e02-b560-77a4a8246cd3"
            },
            "user_template": {
                "description": None,
                "name": None,
                "owner_id": None,
                "user_template_id": None
            }
            },
            "created_at": "2025-03-23T04:10:34.248574Z",
            "finalized_at": "2025-03-23T12:11:19.684199Z",
            "metadata": {
            "audited_pages": 100,
            "audited_urls": 56,
            "found_urls": 19080,
            "queued_pages": 0,
            "queued_urls": 0,
            "request_count": 91061,
            "response_time": 1,
            "scan_status": "running"
            },
            "paused_at": [],
            "requested_action": "start",
            "resumed_at": [],
            "scan_id": "93c8fe61-958e-4a20-ba02-0901b2408664",
            "scanner": {
            "group_name": "Group_WAS",
            "name": "TNB-WAS02",
            "version": "2.30.7"
            },
            "started_at": "2025-03-23T04:10:52.078483Z",
            "status": "completed",
            "target": "https://comunicacao.salvador.ba.gov.br/",
            "template_name": "scan",
            "updated_at": "2025-03-23T12:11:19.684614Z",
            "user_id": "52301418-1bc6-46c3-a114-3494bd82c831"
        },
        "name": "https://comunicacao.salvador.ba.gov.br/",
        "owner_id": "52301418-1bc6-46c3-a114-3494bd82c831",
        "schedule": None,
        "target": "https://comunicacao.salvador.ba.gov.br/",
        "target_count": 1,
        "template_id": "b223f18e-5a94-4e02-b560-77a4a8246cd3",
        "updated_at": "2025-03-23T04:10:32.946520Z",
        "user_permissions": "configure",
        "user_template": None
        }
    ],
    "pagination": {
        "limit": 10,
        "offset": 0,
        "sort": [
        {
            "name": "configs.updated_at",
            "order": "desc"
        }
        ],
        "total": 6
    }
    }}

response = requests.post(f"{BASE_URL}/adicionarWAPPScanALista/", data=json.dumps(payload), headers=headers)

print("Status:", response.status_code)
print("Resposta:", response.text)

# ===================================================================================

# payload = {
#     "nomeSecretaria": "Secretaria de Saúde",
#     "siglaSecretaria": "SMS",
#     "dataInicio": "01 de Janeiro de 2023",
#     "dataFim": "31 de Dezembro de 2023",
#     "ano": "2023",
#     "mes": "Dezembro",
#     "idLista": "68197b6bb2e12aa8ff4c974f"
# }

# response = requests.post(f"{BASE_URL}/gerarRelatorioDeLista/", data=json.dumps(payload), headers=headers)

# print("Status:", response.status_code)
# print("Resposta:", response.text)

# ===================================================================================

# payload = {
#     "idLista": "68213c6605f3a335b064064e",
# }

# response = requests.post(f"{BASE_URL}/excluirLista/", data=json.dumps(payload), headers=headers)

# print("Status:", response.status_code)
# print("Resposta:", response.text)


# ===================================================================================

# response = requests.get(f"{BASE_URL}/getTodasAsListas/", headers=headers)

# print("Status:", response.status_code)
# print("Resposta:", response.text)

# ===================================================================================

# payload = {
#     "nomeLista": "Lista Teste",
# }

# response = requests.post(f"{BASE_URL}/getScansDeLista/", headers=headers, data=json.dumps(payload))

# print("Status:", response.status_code)
# print("Resposta:", response.text)


# ===================================================================================

# response = requests.post(f"{BASE_URL}/limparScansDeLista/", headers=headers, data=json.dumps(payload))

# print("Status:", response.status_code)
# print("Resposta:", response.text)