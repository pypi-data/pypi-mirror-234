import requests
import csv
import base64


def get_access_token(settings):
    base_url = "https://zoom.us/oauth/token"
    credentials = f"{settings.client_id}:{settings.client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    payload = {
        'grant_type': 'account_credentials',
        'account_id': settings.account_id,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_credentials}"
    }
    try:
        response = requests.post(base_url, headers=headers, data=payload)
        if response.status_code == 200:
            response_data = response.json()
            access_token = response_data.get("access_token")
            return access_token
        else:
            print(f"Error getting access token. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def add_registrants(settings, meeting_id, csv_path):
    token = get_access_token(settings)
    if token:
        my_headers = {'Authorization': 'Bearer ' + token}

        try:
            with open(csv_path) as file_obj:
                reader_obj = csv.DictReader(file_obj)
                for row in reader_obj:
                    response = requests.post('https://api.zoom.us/v2/meetings/'+meeting_id+'/registrants', json={"first_name": row['FirstName'], "last_name": row['LastName'], "email": row['Email']}, headers=my_headers)
                    print(f"Added registrant: {row['Id']}, {row['FirstName']} {row['LastName']} ({row['Email']})")
                    print(response)

            print('Registrants added successfully')
        except FileNotFoundError:
            print(f"File not found: {csv_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Access token retrieval failed. Check your credentials.")

def add_registrant_api(settings,meeting_id,json_data):
    token = get_access_token(settings)
    if token:
        my_headers = {'Authorization': 'Bearer ' + token}
        try:
            response = requests.post('https://api.zoom.us/v2/meetings/'+meeting_id+'/registrants', json=json_data, headers=my_headers)
            print(response)
            print('Registrants added successfully')
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Access token retrieval failed. Check your credentials.")