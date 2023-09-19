from ocds_reader.db.backends.mongo import MongoClient
from ocds_reader.db.backends.postgresql import PosgresqlClient
from datetime import datetime, timezone
import requests
import json
import asyncio
import sys
import socket
import time

# Read db.ini file
# make Configuration a singleton class
mongo_client = MongoClient()
pg_client = PosgresqlClient()

# Make a class to manage database

async def query_page(page, url, read_process_id):
    paged_url = url + "&page=" + str(page)
    response = requests.get(paged_url)

    if response.status_code == 200:
        for proceso in response.json()['data']:
            proceso['_id'] = proceso['ocid']
            filter = {'_id': proceso['_id']}
            mongo_client.update_collection("procesos", proceso, filter, True)
            data = {
                    'read_timestamp':datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %z"), 
                    'read_process_id':str(read_process_id), 
                    'http_status': str(response.status_code),
                    'process_id': proceso['ocid'],
                    'page': str(page)
                }
            header_id = pg_client.insert('log_ocds_header',data)
            conume_ocds_detail(proceso['ocid'], read_process_id)
    else:
        data = {
                'read_timestamp': datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %z"), 
                'read_process_id': str(read_process_id), 
                'http_status': str(response.status_code),
                'page': str(page)
            }
        header_id = pg_client.insert('log_ocds_header',data)

def consume_ocds_headers(buyer_keyword, year, exec_uuid, processsing_info=''):
    url = "https://datosabiertos.compraspublicas.gob.ec/PLATAFORMA/api/search_ocds?year="+year+"&buyer="+buyer_keyword

    data = {
            'exec':exec_uuid,
            'start':datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %z"), 
            'status':'CREATED', 
            'year': year,
            'keyword': buyer_keyword,
            'host': socket.gethostname()
        }
    read_id = pg_client.insert('read_process',data)
    response = requests.get(url+"&page=1")

    if response.status_code == 200:
        total_pages = response.json()['pages']
        print("total pages: "+str(total_pages))
        data = { 'status':'STARTED', 'pages': total_pages, 'http_status': response.status_code }
        pg_client.update('read_process', read_id, data)

        for p in range(1, total_pages + 1):
            percentage_progress = (p / total_pages) * 100
            print("%s - progress: %d/%d (%3.2f%%)" % (processsing_info, p, total_pages,percentage_progress))
            asyncio.run(query_page(p, url, read_id))

        data = {
            'status':'SUCCESS',
            '"end"':datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %z")
        }
        pg_client.update('read_process', read_id, data)
    else:
        data = { 'status':'ERROR', 'http_status': response.status_code }
        pg_client.update('read_process', read_id, data)

def conume_ocds_detail(ocid, read_process_id):
    url = "https://datosabiertos.compraspublicas.gob.ec/PLATAFORMA/api/record?ocid="
    read_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S %z")
    response = requests.get(url + ocid)
    if response.status_code == 200:
        proceso_ocds = response.json()
        proceso_ocds['_id'] = ocid
        filter = {'_id': proceso_ocds['_id']}

        data = {
            'read_timestamp': read_time, 
            'read_process_id': str(read_process_id), 
            'http_status': str(response.status_code),
            'process_id': ocid,
            'updated': str(False)
        }

        if mongo_client.document_exist("proceso_ocds", ocid):
            print("doc "+ocid+" exists")
            proceso_ocds["license"]="carpio"
            if mongo_client.is_document_updated("proceso_ocds", ocid, proceso_ocds):
                print("doc "+ocid+" updated")
                data["updated"] = str(True)
                mongo_client.register_scd_diff("proceso_ocds", ocid, "proceso_ocds_scd", proceso_ocds, read_time)
            else:
                print("doc "+ocid+" NOT updated")
        else:
            print("doc "+ocid+" NOT exists")
            
        mongo_client.update_collection("proceso_ocds", proceso_ocds, filter, True)
        
        header_id = pg_client.insert('log_ocds_detail',data)

    else:
        data = {
                'read_timestamp': read_time, 
                'read_process_id': str(read_process_id), 
                'http_status': str(response.status_code)
            }
        header_id = pg_client.insert('log_ocds_detail',data)



def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)
