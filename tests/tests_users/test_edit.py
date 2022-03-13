from requests import put, get

print(
    put(
        "http://127.0.0.1:5000/api/jobs/3",
        json={
            "id": 3,
            "team_leader_id": 1,
            "job": "Вынос мусора",
            "work_size": 3,
            "collaborators": None,
            "is_finished": False,
        },
    ).json()
)

print(
    put(
        "http://127.0.0.1:5000/api/jobs/11",
        json={
            "id": 11,
            "team_leader_id": 1,
            "job": "Вынос мусора",
            "work_size": 3,
            "collaborators": None,
            "is_finished": False,
        },
    ).json()
)

print(put("http://127.0.0.1:5000/api/jobs/12", json={}).json())

print(get("http://127.0.0.1:5000/api/jobs").json())