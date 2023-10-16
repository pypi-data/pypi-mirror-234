from artd_nequi.models import NequiCredential, NequiTransaction, NequiTransactionHisory
import datetime
import requests
import base64
import json
import random
import time
import hashlib


class NequiUtil:
    def __init__(self, nequi_credential: NequiCredential):
        self.nequi_credential = nequi_credential
        self.client_id = nequi_credential.client_id
        self.client_secret = nequi_credential.client_secret
        self.api_key = nequi_credential.api_key
        self.test_cellphone = nequi_credential.test_cellphone
        if self.nequi_credential.test_mode:
            self.auth_url = "https://oauth.sandbox.nequi.com"
            self.url = "https://api.sandbox.nequi.com"
        else:
            self.auth_url = "https://oauth.nequi.com"
            self.url = "https://api.nequi.com"

    def get_auth(self) -> str:
        string_to_encode = f"{self.client_id}:{self.client_secret}"
        string_bytes = string_to_encode.encode("ascii")
        base64_bytes = base64.b64encode(string_bytes)
        base64_string = base64_bytes.decode("ascii")
        return base64_string

    def get_token(self) -> tuple:
        url = f"{self.auth_url}/oauth2/token?grant_type=client_credentials"
        base_64_string = self.get_auth()
        payload = {}
        headers = {
            "Authorization": f"Basic {base_64_string}",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=payload,
        )
        json_response = json.loads(response.text)
        if "access_token" in json_response and "expires_in" in json_response and "token_type" in json_response:
            return (
                json_response["access_token"],
                json_response["expires_in"],
                json_response["token_type"],
            )
        else:
            return False, False, False

    def generate_aleatory_message_id(self) -> str:
        numero_aleatorio = str(random.randint(10**9, 10**10 - 1))
        timestamp_actual = str(int(time.time()))
        hash_aleatorio = hashlib.sha256(str(random.getrandbits(256)).encode()).hexdigest()
        string_aleatorio = numero_aleatorio + timestamp_actual + hash_aleatorio
        return string_aleatorio

    def create_paymentservice_unregisteredpayment(
        self,
        clien_id: str,
        cellphone: str,
        value: str,
        reference1: str,
    ) -> dict:
        access_token, expires_in, token_type = self.get_token()
        if not access_token:
            return False
        url = f"{self.url}/payments/v2/-services-paymentservice-unregisteredpayment"
        request_date = datetime.datetime.now() + datetime.timedelta(minutes=5)
        request_date = request_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        message_id = self.generate_aleatory_message_id()

        payload_dict = {
            "RequestMessage": {
                "RequestHeader": {
                    "Channel": "PNP04-C001",
                    "RequestDate": request_date,
                    "MessageID": message_id,
                    "ClientID": clien_id,
                    "Destination": {
                        "ServiceName": "PaymentsService",
                        "ServiceOperation": "unregisteredPayment",
                        "ServiceRegion": "C001",
                        "ServiceVersion": "1.2.0",
                    },
                },
                "RequestBody": {
                    "any": {
                        "unregisteredPaymentRQ": {
                            "phoneNumber": cellphone,
                            "code": "NIT_1",
                            "value": value,
                            "reference1": reference1,
                        }
                    }
                },
            }
        }
        payload = json.dumps(payload_dict)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
            "x-api-key": f"{self.api_key}",
        }

        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=payload,
        )
        json_response = json.loads(response.text)
        print(json_response)
        status_code = json_response["ResponseMessage"]["ResponseHeader"]["Status"]["StatusCode"]
        status_description = json_response["ResponseMessage"]["ResponseHeader"]["Status"]["StatusDesc"]
        try:
            transaction_id = json_response["ResponseMessage"]["ResponseBody"]["any"]["unregisteredPaymentRS"]["transactionId"]
            status = True
        except:
            transaction_id = None
            status = False
        NequiTransaction.objects.create(
            nequi_credential=self.nequi_credential,
            message_id=message_id,
            client_id=clien_id,
            status_code=status_code,
            status_description=status_description,
            transaction_id=transaction_id,
            transaction_type="PAYMENT",
            other_data=json_response,
            status=status,
            value=value,
        )

        return json_response

    def get_status_payment(self, transaction_id: int) -> dict:
        if NequiTransaction.objects.filter(id=transaction_id).count() == 0:
            print("No existe la transaccion")
            return False
        access_token, expires_in, token_type = self.get_token()
        if not access_token:
            print("No existe el token")
            return False
        url = f"{self.url}/payments/v2/-services-paymentservice-getstatuspayment"
        request_date = datetime.datetime.now() + datetime.timedelta(minutes=5)
        request_date = request_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        message_id = self.generate_aleatory_message_id()
        nequi_transaction = NequiTransaction.objects.filter(id=transaction_id).first()
        payload_dict = {
            "RequestMessage": {
                "RequestHeader": {
                    "Channel": "PNP04-C001",
                    "RequestDate": request_date,
                    "MessageID": message_id,
                    "ClientID": nequi_transaction.client_id,
                    "Destination": {
                        "ServiceName": "PaymentsService",
                        "ServiceOperation": "getStatusPayment",
                        "ServiceRegion": "C001",
                        "ServiceVersion": "1.0.0",
                    },
                },
                "RequestBody": {"any": {"getStatusPaymentRQ": {"codeQR": transaction_id}}},
            }
        }
        payload = json.dumps(payload_dict)
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
            "x-api-key": f"{self.api_key}",
        }

        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=payload,
        )
        json_response = json.loads(response.text)
        print(json_response)
        status_code = json_response["ResponseMessage"]["ResponseHeader"]["Status"]["StatusCode"]
        status_description = json_response["ResponseMessage"]["ResponseHeader"]["Status"]["StatusDesc"]
        try:
            payment_status = json_response["ResponseMessage"]["ResponseBody"]["any"]["getStatusPaymentRS"]["status"]
            name = json_response["ResponseMessage"]["ResponseBody"]["any"]["getStatusPaymentRS"]["name"]
            value = json_response["ResponseMessage"]["ResponseBody"]["any"]["getStatusPaymentRS"]["value"]
        except:
            payment_status = None
            name = None
            value = None
        NequiTransactionHisory.objects.create(
            nequi_transaction=nequi_transaction,
            message_id=message_id,
            payment_status=payment_status,
            value=value,
            name=name,
            status_code=status_code,
            status_description=status_description,
        )
        if payment_status == "34" or payment_status == "69" or payment_status == "70" or payment_status == "71" or payment_status == None:
            nequi_transaction.status = False

        nequi_transaction.status_code = status_code
        nequi_transaction.status_description = status_description
        nequi_transaction.save()

        return json_response
