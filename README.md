# Blockquest API

## Quick Start

1. create/config [.env](.env.sample)

2. run docker-compose

   ```bash
   docker compose up
   ```

## Docs

- [mongoengine](http://docs.mongoengine.org/tutorial.html): ORM

## Endpoints

### Auth

- GET: `/api/auth/logout?email=[email]&token=[token]` (not supposed to be, but easier)
- GET: `/api/auth/check?email=[email]&token=[token]`

- Manual

  - POST: `/api/auth/signup`

    ```py
    body = {
      "email": "",
      "username": "",
      "password": "",
      "confirm-password": "",
    }
    ```

  - POST: `/api/auth/login`

    ```py
    body = {
      "email": "",
      "password": "",
    }
    ```

- OAuth
  - GET: `/api/auth/login/google`
  - GET: `/api/auth/login/github`

### User

- GET: `/api/user/profile?email=[email]`

- PUT: `/api/user/profile?email=[email]&token=[token]`

  ```py
  body = {
    "username": "",
    "password": "",
    "confirm-password": "",
  }
  ```

- DELETE: `/api/user/profile?email=[email]&token=[token]`

### Update

- Section
  - POST: `/api/update/section/unlock?email=[email]&id=[id]&token=[token]`
  - POST: `/api/update/section/lock?email=[email]&id=[id]&token=[token]`
- Bag
  - POST: `/api/update/bag/add?email=[email]&item=[item]&token=[token]`
  - POST: `/api/update/bag/remove?email=[email]&item=[item]&token=[token]`
