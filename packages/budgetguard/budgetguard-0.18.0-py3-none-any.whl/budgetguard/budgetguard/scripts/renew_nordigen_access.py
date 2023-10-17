import requests
from uuid import uuid4
import argparse
from nordigen import NordigenClient

parser = argparse.ArgumentParser()

parser.add_argument(
    "-sid",
    "--secret_id",
    help="Nordigen secret id",
    type=str,
    required=True,
)

parser.add_argument(
    "-skey",
    "--secret_key",
    help="Nordigen secret key",
    type=str,
    required=True,
)

if __name__ == "__main__":
    args = parser.parse_args()
    client = NordigenClient(
        secret_id=args.secret_id,
        secret_key=args.secret_key,
    )
    token_data = client.generate_token()["access"]

    url = "https://bankaccountdata.gocardless.com/api/v2/agreements/enduser/"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_data}",
    }

    data = {
        "institution_id": "BANK_MILLENNIUM_BIGBPLPW",
        "max_historical_days": "90",
        "access_valid_for_days": "90",
        "access_scope": ["balances", "details", "transactions"],
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())

    url = "https://bankaccountdata.gocardless.com/api/v2/requisitions/"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_data}",
    }

    data = {
        "redirect": "http://www.yourwebpage.com",
        "institution_id": "BANK_MILLENNIUM_BIGBPLPW",
        "reference": str(uuid4()),
        "agreement": "557cbbc6-40da-4278-93c1-51b658cc6515",
        "user_language": "EN",
    }

    response = requests.post(url, headers=headers, json=data)

    print(response.status_code)
    print(response.json())
