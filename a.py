import requests

email_address = "duresafeyis2022@gmail.com"

response = requests.get(
	"https://isitarealemail.com/api/email/validate", 
	params={'email': email_address})
status = response.json()['status']
print(status)