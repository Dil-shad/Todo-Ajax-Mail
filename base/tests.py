import requests

response = requests.get('http://worldtimeapi.org/api/ip')
data = response.json()
server_time = data['utc_datetime']
print(server_time)
