from requests import post

print(
    post(
        "http://127.0.0.1:5000/api/jobs",
        json={
            "id": 7,
            "team_leader_id": 1,
            "job": "Вынос мусора",
            "work_size": 3,
            "collaborators": None,
            "is_finished": False,
        },
    ).json()
)

print(
    post(
        "http://127.0.0.1:5000/api/jobs",
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

print(post("http://127.0.0.1:5000/api/jobs", json={}).json())

print(
    post(
        "http://127.0.0.1:5000/api/jobs",
        json={"id": 12, "job": "Вынос мусора", "work_size": 3, "collaborators": "1", "is_finished": False},
    ).json()
)
