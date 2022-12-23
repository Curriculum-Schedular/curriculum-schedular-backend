import requests

url = "http://localhost:8000/api/v1/upload-curriculum"
file = open("curriculum_with_prerequisites.csv", "rb")

response = requests.post(url, data={"name": "Curriculum"}, files={"file": file})

print(response.status_code)  # prints the HTTP status code
print(response.json())  # prints the JSON response
