<h1 align="center">
  Simple referral system
</h1>
<h2 align="center">
    Test task <br> for Hammer Systems
    <br>
</h2>

<div align="center">

[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-%23FE5196?logo=conventionalcommits&logoColor=white)](https://conventionalcommits.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)


</div>
<hr>

<p align="center">
  <a href="#features">Features</a> •
  <a href="#tech-stack">Tech stack</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#documentation">Documentation</a> •
  <a href="#additional-material">Additional material</a>
</p>


## Features

- Authentication by JWT token
- Authorization by phone number. First request to enter phone number.
- Simulate sending a 4-digit authorization code (1-2 sec delay on the server) using celery task
- In the user's profile, the user has the opportunity to enter one other person's invite code (when entering it, check for existence).
- In the user's profile the list of users (phone numbers) who have entered the current user's invite code is displayed.
- [Redoc](http://localhost:8000/redoc/)
- [Swagger](http://localhost:8000/swagger/)
- [flower](http://localhost:5555) for celery task monitoring


## Tech stack
- [Python 3.11](https://www.python.org/downloads/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Celery](https://docs.celeryq.dev/en/stable/index.html)
- [Resis](https://redis.io/)
- [Poetry](https://python-poetry.org/docs/)


## How To Use
<details>

<summary><strong>Use Docker</strong></summary>

1. Firstly clone repo
   ```bash
   git clone git@github.com:mrKazzila/test_python_dev_Hammer_Systems.git
   ```

2. Prepare env with make
   ```bash
   make prepare_env
   ```

3. Run docker compose with make
   ```bash
   make docker_run
   ```

4. Stop docker compose with make
   ```bash
   make docker_stop
   ```

</details>

<details>
<summary>Local commands</summary>

1. Firstly clone repo
   ```bash
   git clone git@github.com:mrKazzila/test_python_dev_Hammer_Systems.git
   ```

2. Prepare local env with make
   ```bash
   make prepare_local_env
   ```

3. Settings Poetry with make
   ```bash
   make poetry_setup
   ```

4. Run project dependencies, migrations, & run test server with make
   ```bash
   make django_run
   ```

5. Run Redis Server
   ```bash
   make redis_run
   ```

6. Run Celery
   ```bash
   make celery_run
   ```

7. Run test with make
   ```bash
   make test
   ```

8. Run pre-commit with make
   ```bash
   make test_linters
   ```

</details>


## Documentation
<details>
<summary><strong>API Documentation</strong></summary>

**`POST` | Getting an authentication code: [`http://localhost:8000/api/v1/auth/signup/`](http://localhost:8000/api/v1/auth/signup/)**

Example:
   - Request

      ```
      {
          "username": "Jhon",
          "phone_number": "12345678901"
      }
      ```

   - Response

      ```
      {
          "code": "1236"
      }
      ```

**`POST` | Getting an authentication token and referral code: [`http://localhost:8000/api/v1/auth/code/`](http://localhost:8000/api/v1/auth/code/)**

Example:
   - Request

        ```
        {
            "code": "1236"
        }
        ```
   - Response

      ```
      {
          "token": "bssiyw-f169337fbe692e91f373200fd087e533",
          "referral code": "Qz3Isl"
      }
      ```

**`GET` | Getting the users list: [`http://localhost:8000/api/v1/users/`](http://localhost:8000/api/v1/users/)**

Example:

   - Response

        ```
        [
            {
                "username": "Zak",
                "phone_number": "29535315881",
                "referral_code": "Qz3Isl",
                "used_referral_code": "",
                "referral_users_list": [
                    {
                        "phone": "19535315881"
                    }
                ]
            },
            {
                "username": "Jhon",
                "phone_number": "19535315881",
                "referral_code": "fxmSIJ",
                "used_referral_code": "Qz3Isl",
                "referral_users_list": []
            }
        ]
        ```

**`POST` | Creating user: [`http://localhost:8000/api/v1/users/`](http://localhost:8000/api/v1/users/)**

Example:

   - Request

        ```
        {
            "username": "Nick",
            "phone_number": "49535315881",
            "referral_code": "oxtSIn",
            "used_referral_code": ""
        }
        ```

   - Response

        ```
        {
            "username": "Nick",
            "phone_number": "49535315881",
            "referral_code": "oxtSIn",
            "used_referral_code": "",
            "referral_users_list": []
        }
        ```

**`GET` | Getting a user: [`http://localhost:8000/api/v1/users/<username>/`](http://localhost:8000/api/v1/users/<username>/)**

Example:

   - Response

        ```
        {
            "username": "Jhon",
            "phone_number": "19535315881",
            "referral_code": "fxmSIJ",
            "used_referral_code": "Qz3Isl",
            "referral_users_list": []
        }
        ```

**`PATCH` | Update user info: [`http://localhost:8000/api/v1/users/<username>/`](http://localhost:8000/api/v1/users/<username>/)**

Example:

   - Request

        ```
        {
            "username": "makwcy",
            "phone_number": "29535713841",
            "referral_code": "pfvIfl",
            "used_referral_code": "",
            "referral_users_list": []
        }
        ```
   - Response

        ```
        {
            "username": "makwcy",
            "phone_number": "29535713841",
            "referral_code": "pfvIfl",
            "used_referral_code": "",
            "referral_users_list": []
        }
        ```

**`PUT` | Update user info: [`http://localhost:8000/api/v1/users/<username>/`](http://localhost:8000/api/v1/users/<username>/)**

Example:

   - Request

        ```
        {
            "username": "makwcy",
            "phone_number": "29535713841",
            "referral_code": "pfvIfl",
            "used_referral_code": "",
            "referral_users_list": []
        }
        ```
   - Response

        ```
        {
            "username": "makwcy",
            "phone_number": "29535713841",
            "referral_code": "pfvIfl",
            "used_referral_code": "",
            "referral_users_list": []
        }
        ```

**`DELETE` | Delete user: [`http://localhost:8000/api/v1/users/<username>/`](http://localhost:8000/api/v1/users/<username>/)**

Example:

   - Response

        ```
        {
            "username": "makwcy",
            "phone_number": "29535713841",
            "referral_code": "pfvIfl",
            "used_referral_code": "",
            "referral_users_list": []
        }
        ```

</details>



## Additional material
* [test-assignment](https://disk.yandex.ru/i/-t5XQ6cmWkNNxQ)
