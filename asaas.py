import requests
import json
from sqlalchemy import Date
from datetime import date
from datetime import datetime



charkey = "$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwNjkxOTE6OiRhYWNoXzdlNWEyMDk5LWU5YjEtNGFmZC1hYjYwLTBjOTQ5YTVmZWU0Yw=="


def criarcliente(cliente_id):
    url = "https://sandbox.asaas.com/api/v3/customers"

    payload = {
        "name": cliente_id["name"],
        "email": cliente_id["email"],
        "cpfCnpj": cliente_id["cpf"]
    }


    headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "access_token": charkey
    }

    response = requests.post(url, json=payload, headers=headers)
    cliente_dados = json.loads(response.content)
    id_cliente = cliente_dados['id']

    

    return id_cliente


def pagamento(formato):
    current_date = datetime.now().date()
    url = "https://sandbox.asaas.com/api/v3/payments"
    date = str(current_date)
    print(date)
    payload = {
        "billingType": formato['tipo'],
        "customer": formato["id_assas"],
        "dueDate": date,
        "value": formato["valor"],
        "description": formato["nome_event"],
        "externalReference": 5225,
        "postalService": False
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "access_token": charkey
    }

    response = requests.post(url, json=payload, headers=headers)
    
    json_data = response.text
    data = json.loads(json_data)

# Capturar o campo invoiceUrl
    invoice_url = data["invoiceUrl"]
    id = data['id']
    return invoice_url, id


def payment(id_pay):
    url = "https://sandbox.asaas.com/api/v3/payments/"

    uri = url + id_pay

    headers = {
    "accept": "application/json",
    "access_token": charkey
    }

    response = requests.get(uri, headers=headers)
    result = response.text
    data = json.loads(result)
    status = data["status"]
    return status



