from requests import get, post, delete

print(get('http://127.0.0.1:5000/api/v1/users').json())
print(get('http://127.0.0.1:5000/api/v1/users/1').json())
print(get('http://127.0.0.1:5000/api/v1/users/12321').json())
print(post('http://127.0.0.1:5000/api/v1/users', json={'name': 'Sonya'}).json())
print(post('http://127.0.0.1:5000/api/v1/users', json={'name': 'Sonya', 'position': 'junior programmer',
                                                       'surname': 'Wolf', 'age': 17, 'address': 'module_3',
                                                       'speciality': 'computer sciences',
                                                       'hashed_password': 'wolf', 'email': 'wolf@mars.org'}).json())
print(delete('http://127.0.0.1:5000/api/v1/users/7').json())
print(delete('http://127.0.0.1:5000/api/v1/users/777').json())
