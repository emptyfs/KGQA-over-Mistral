# Сервис KGQA на основе Mistral

## Системные требования
- Linux (debian)
- Python3.11
- Docker
- Модель 

## FAQ
- Документация доступна по endpoint-у **/swagger_spec**
- GUI для Neo4j доступна на порте 7474
- Сервис доступен на порте 42424

## Установка и запуск

Все команды запускать из корня проекта

1) Скачать модель, положить в проект по пути **/data/models/**

2) 
```bash
pip install -r src/requirements.txt
docker-compose up
python src/app.py
```

## Примеры работы
![alt text](data/images/image.png)
Документация

![alt text](data/images/image-1.png)
endpoint для построения ГЗ

![alt text](data/images/image-2.png)
Пример построенного ГЗ (из нескольких файлов) - можно загружать как один цельный, так и несколько. Как можно заметить по фото, вершины представляются эмбеддингами, но при этом сохраняют контекст (исходный текст) для демострации многошагового рассуждения

Примеры ответов на вопросы
![alt text](data/images/image-3.png)
![alt text](data/images/image-4.png)
```JSON
{
  "answer": {
    "answer": " POST (POST Request) - это метод HTTP, который используется для отправки данных к серверу. Он используется для создания новых ресурсов на сервере или для обновления существующих ресурсов. В POST-запросе данные передаются в теле запроса в формате JSON или форма-URL-encoded.",
    "sources": [
      {
        "score": 0.9043340682983398,
        "text": "Here are some facts extracted from the provided text:\n\nRefresh tokens -> Maximum -> 25 active per user at once\nApi calls -> Expire after -> 15 minutes\n\nAuthentication\nMost API calls require authentication. Access is controlled through OAUTH2 with JSON web tokens.\nFor security reasons, it is recommended that a separate user account be created for scripting API access.\nThis account should have the minimum permissions necessary to perform its duties.\nAPI access is controlled via OAUTH2 with JSON web tokens. In order to authenticate, the client script ﬁrst\nobtains an access token using a username/password and optionally, a refresh token:\n--> POST /api/mgmt.aaa/1.0/token\n{\n\"user_credentials\": {\n\"username\": \"<name>\",\n\"password\": \"<password>\"\n},\n\"generate_refresh_token\": true\n}\n<-- 201\n{\n\"access_token\": <access_token>,\n\"refresh_token\": <refresh_token>\n\"expires_at\": 900,\n\"token_type\": \"bearer\"\n}\nAll subsequent API requests must include an Authorization header containing the access token. Note that\nthe “B” in “Bearer” must be capitalized:\nAuthorization: Bearer <access_token>\nFor example:\n--> GET /api/npm.reports.sources/1.0/items/aggregates\nAuthorization: Bearer eyJhbGciOiJIUzI1NiIs..QzWXcXNrz0ogtVhfEd2o\n<-- 200 OK\n{...}\nAccess tokens expire after 15 minutes. Attempting to use an expired access token will result in 401/\nUnauthorized responses.\nTo obtain a new token, either resubmit a username/password request, as documented earlier, or use the\nrefresh token instead:\n--> POST /api/mgmt.aaa/1.0/token\n{\n\"refresh_token\": <refresh_token>\n}\n<-- 200 OK\n{\n\"access_token\": <access_token>,\n\"expires_in\": 900,\n\"token_type\": \"bearer\"\n}\nUsing refresh tokens is recommended, as they are more secure. When a script ﬁnishes, it should log out\nand revoke its refresh token, rendering it unusable by a third party. Additionally, if a refresh token is not\nused within 60 minutes, it will automatically be expired by the system.\nA maximum of 25 refresh tokens may be active per user at once. If a 26th token is requested, the oldest\ngranted token will be revoked immediately."
      },
      {
        "score": 0.9040031433105469,
        "text": "Here are some facts extracted from the provided text:\n\n275 shoreline drive -> Is located in -> Ca\n\nIf a key does not have one of them, it will be rejected. If th\nsecrets are provided for a TLS 1.3 connection but the Client and Server Traffic secrets are not available, ct_secret and\nst_secret can be provided as empty strings.For the normal use case the 'client_random' and the decryption secrets are\nenough.\nWhen a POST is performed to provide keys if there are no HTTP errors (HTTP 400, HTTP 401 etc...) returned by\nAppResponse this means that from the schema point of view the keys provided are valid and can be used by the system\ndecryption. If the error Missing JWT Signature is observed see S38578\nExample (bulk create)\nPOST /api/npm.ssl_dh_keys/1.1/keys/bulk_create\n{\n    \"items\": [\n{\n    \"client_random\": \"3c555b83e8db003fc35a4a5394e566c3234e2d325213b3a3a82ab2d651c8a151\",\n    \"master_key\":\n\"8dbc521092ca8466c573f5118e251553b635057bab0d7dc8da1cab24ee10b1d81e72e59c31e2a6c88bd170c50e6f\n},\n{\n                  275 Shoreline Drive,Suite 350,  Redwood City, CA 94065    riverbed.com"
      },
      {
        "score": 0.9023818969726562,
        "text": "Here are some facts extracted from the provided text:\n\nFr -> Is country code for -> France\n\nCategories:\nNetProﬁler (Cascade Proﬁler), NetProﬁler (Enterprise Cluster)\nSolution Number:\nS38358\nLast Modiﬁed:\n2024-08-08\nHow to create custom IP to country mappings in NetProﬁler for\ndisplay of country ﬂags in v10.21 and above\nDescription\nBeginning in software version 10.15, dashboards and reports will show country flags for hosts where geo-\nlocation data is available. This feature is enabled by default on the page \"Administration > UI Preferences\" with\nthe option \"Show country ﬂags\"\n \n• Country flags for many public IPs are automatically assigned.\n• Private IP address ranges (10/8, 192.168/16, 172.16/12) are not automatically mapped to country\ncodes.\n In this article , we will look into how to create custom IP to country mappings in NetProfiler for display of\ncountry flags in v10.21 and above.\n For other version , refer the below article:\nv10.19 and below  -  How to create custom IP to country mappings in NetProfiler for display of country flags in\nv10.19 and below\nv10.20 - How to create custom IP to country mappings in NetProfiler for display of country flags in v10.20\nSolution\nCustom mappings may be added through the use of a json file. Custom mappings take precedence over the\nautomatic mappings.\n1) Connect to Base/Management module of NetProfiler via SSH using mazu account.\n2) Create the following file in 'vi':\n$ vi /mnt/data/netproﬁler-conﬁg/geomap_local_mappings.json\n3) Add mappings by specifying the beginning and ending IP in a range and the country code in key/value\npairs as follows:\n \n{\n \"ip_mapping\": [\n     {\"ip_begin\" : \"10.10.10.0\",\n      \"ip_end\" : \"10.10.10.255\",\n      \"country\" : \"FR\"\n                  275 Shoreline Drive,Suite 350,  Redwood City, CA 94065    riverbed.com"
      },
      {
        "score": 0.9001379013061523,
        "text": "Here are some facts extracted from the provided text:\n\nFile path -> Is -> /tmp/tmpc6b2q2jo.pdf\n\nCategories:\nBest Practices, Principal Article, Networking, SteelHead (Appliance)\nSolution Number:\nS14848\nLast Modiﬁed:\n2021-10-15\nSimpliﬁed Routing (Best Practices)\nIssue\nWith some network topologies traffic is redirected back through a SteelHead.\nSolution\nIf a SteelHead appliance is installed in a subnet different than the clients or servers, the user currently has to\ndeﬁne one router as the default gateway and static routes for the other router so that traffic does not get\nredirected back through the SteelHead.\nIf the user does not add the static routes, it does not work in some cases because the ACLs (Access Control\nLists) on the default gateway drop traffic that should have gone through the other router.  To avoid forcing the\nuser to add those static routes, the MAC address received by the SteelHead for an IP address could be reused\nwhen sending out packets for the same address.\nSimpliﬁed routing is gathering the IP to next hop MAC address mapping from each packet it receives to use in\naddressing its own traffic. Pass-through traffic just naturally comes in one interface and goes out the other.\nOptimized traffic needs a destination as it's a new TCP connection, so when we send a packet out from the\ndevice, as a ﬁnal step after all the routing code has done its job simpliﬁed routing inserts the next hop it has\nassociated with the destination IP. This overrides everything else. We will only use the static routes or gateway\nin the case that simpliﬁed routing has no mapping.\nIf the next hop goes down we will learn the new next hop on the next packet that we receive to/from the new\nrouter on a per IP address basis, so if we learn the new route for 10.0.0.1, we will have to learn again for\n10.0.0.2, etc.\nThe things to look for are:\n• Layer-2 WANs\n• Are virtual routers being used? If so do they use a virtual MAC to send?\n• Can packets sent to/through the Steelhead be returned to the same router? If not source gathering must not be\nenabled.\nRequired Conﬁguration\n• Default route must exist on each SteelHead."
      }
    ]
  }
}
```