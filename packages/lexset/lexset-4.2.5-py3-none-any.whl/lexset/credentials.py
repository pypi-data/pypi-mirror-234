import base64
import requests
import os

"""
    This helper is used for managing your credentials and the credentials of external 
    resources.
"""


class linkAccounts(object):
    """
        Link your GCP account:
            Please login to GCP create a new service account for lexset. When done download the
            service account json file.
        Name: Give your credential a unique name
        Service Account Json File Path: Path to the service account file downloaded from gcp.
        Token: Your lexset access token.
    """

    @staticmethod
    def link_gcp_account(self, service_account_json_file_path, name_of_credential, token):
        if not os.path.isfile(service_account_json_file_path):
            print("Please provide a valid file path for the gcp service account file.")
        else:
            with open(service_account_json_file_path) as f:
                json_data = f.readlines()
                json_encoded = base64.b64encode(json_data.encode("utf-8"))
                encoded_cred = str(json_encoded, "utf-8")

                url = "https://seahaven.lexset.ai/api/cloudresources/LinkGCPAccount"

                payload = {'name': name_of_credential,
                           'base64jsondata': encoded_cred}

                headers = {
                    'Authorization': f'Bearer {token}',
                }

                response = requests.request("POST", url, headers=headers, data=payload)
                if response.status_code == 200:
                    print("Your gcp credentials have been linked successfully.")
                elif response.status_code == 401:
                    print("Please provide a valid access token. Your token is located in your lexset dashboard.")
                else:
                    print("There was an unknown error please try again later.")
