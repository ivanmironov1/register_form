from requests import delete, get

print(delete("http://127.0.0.1:5000/api/jobs/11").json())
print(delete("http://127.0.0.1:5000/api/jobs/213").json())
print(delete("http://127.0.0.1:5000/api/jobs/dsgfsdgsdg").json())

print(get("http://127.0.0.1:5000/api/jobs").json())