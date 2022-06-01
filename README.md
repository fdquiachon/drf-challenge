# drf-challenge

----
## Requirements
* Python 3.9+
* virtualenv

### Third party libraries
```dotenv
Django==4.0.4
djangorestframework==3.13.1
django-environ==0.8.1
django-rest-authemail==2.1.2
django-oauth-toolkit==2.0.0
```

## Development Setup

---
### Installation of dependencies
```commandline
pip install -r requirements.txt
```

### Environment Variables
```dotenv
SECRET_KEY=<django-secret-key>
DEBUG=True

EMAIL_HOST=<email-host>
EMAIL_PORT=<email-port>
EMAIL_HOST_USER=<email-host-user>
EMAIL_HOST_PASSWORD=<email-host-password>
```
### Running the server
```commandline
python managepy makemigrations
python managepy migrate
python manage.py runserver
```

### Communicating with the server
Use this command to verify that the server is up and running.

```commandline
curl --request GET \
  --url http://127.0.0.1:8000/api/users/
```

## API Details

---
### Application API
Base URI: `http://host:port/`

---
#### User Registration
* API: `/api/users/register/`
* Method: POST
* Body: `application/json`
  * email (M)
  * password (M)
  * firstname (O)
  * lastname (O)
* Usage:
  ```commandline
  http://127.0.0.1:8000/api/users/register/
  {
    "first_name": "Steph",
    "last_name": "Curry",
    "email": "hello3@kiko.com",
    "password": "Test1"
  }
  ```
* Response: `201 Created`
    ```commandline
    {
      "user": {
        "email": "hello3@kiko.com",
        "first_name": "Steph",
        "last_name": "Curry"
      },
      "errors": null
    }
    ```
---
#### User Activation
* API: `/signup/verify/?code=<code-in-email>`
* Method: GET
* Usage:
  ```commandline
  http://127.0.0.1:8000/signup/verify/?code=<code>
  ```
* Response: `200 OK`
    ```commandline
    {
        "success": "Email address verified."
    }
    ```
---
#### User Login
* API: `/api/users/login/`
* Method: POST
* Body:
    * username
    * password
    * grant_type
    * client_id
    * client_secret
* Usage:
  ```commandline
  http://127.0.0.1:8000/api/users/login/
    {
        "grant_type": "password",
        "username": "hello@kiko.com",
        "password": "Test-pass",
        "client_id": "client-value",
        "client_secret": "secret-value"
    }
  ```
* Response: `200 OK`
    ```commandline
    {
        "access_token": "token-value",
        "expires_in": 86400,
        "token_type": "Bearer",
        "scope": "read write",
        "refresh_token": "refresh-token"
    }
    ```
---
#### User List
* API: `/api/users/`
* Method: GET
* Header:
 * Authorization: Bearer Token (Optional)
* Usage:
  ```commandline
  http://127.0.0.1:8000/api/users/
  ```
* Response: `200 OK`
    ```commandline
    [
      {
        "first_name": "Kiko",
        "last_name": "Admin",
        "email": "kiko@spectrumone.co"
      },
      {
        "first_name": "Steph",
        "last_name": "Curry",
        "email": "hello1@kiko.com"
      },
      ...
    ]
    ```
---
#### Password Change
* API: `/api/users/password/change`
* Method: PATCH
* Header:
  * Authorization: Bearer Token (Required)
* Usage:
  ```commandline
  http://127.0.0.1:8000/api/users/password/change
    {
        "password": "current-password",
        "new_password": "new-password"
    }
  ```
* Response: `200 OK`
    ```commandline
    {
        "message": "Password updated successfully"
    }
    ```

Thank you!
