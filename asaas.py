import requests
import json
from sqlalchemy import Date
from datetime import date



charkey = "$aact_YTU5YTE0M2M2N2I4MTliNzk0YTI5N2U5MzdjNWZmNDQ6OjAwMDAwMDAwMDAwMDAwNjkxOTE6OiRhYWNoXzhmYjI1Mjc5LTZmNjUtNGE5Mi1hNzc1LTBjOTM5ZDM4MzJjMQ=="


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


def criarpix(cliente_id):
    url = "https://sandbox.asaas.com/api/v3/payments"
    
    data_atual = date.today()
    tempo = str(data_atual)
    payload = {
        "billingType": "PIX",
        "customer": cliente_id["id"],
        "value": cliente_id["valor"],
        "dueDate": tempo
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "access_token": charkey
    }

    response = requests.post(url, json=payload, headers=headers)

    pagamento = json.loads(response.content)
    invoice_url = pagamento.get("invoiceUrl")
    id_pay = pagamento.get("id")

    return invoice_url, id_pay


def payment(id_pay):
    url = "https://sandbox.asaas.com/api/v3/payments/"

    uri = url + id_pay

    headers = {
    "accept": "application/json",
    "access_token": charkey
    }

    response = requests.get(uri, headers=headers)
    result = json.loads(response.content)
    status = result.get("status")
    return status



