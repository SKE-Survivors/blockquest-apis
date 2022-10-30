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

- Manual

  - POST `/api/auth/signup`

    ```py
    body = {
      "email": "",
      "username": "",
      "password": "",
      "confirm-password": "",
    }
    ```

  - POST `/api/auth/login`

    ```py
    body = {
      "email": "",
      "password": "",
    }
    ```

  - GET `/api/auth/logout?email=[email]` (not supposed to be, but easier)
  - GET `/api/auth/check?email=[email]&token=[token]`

- Google
  - `/api/auth/google/login` (redirect)

### User

- GET: `/api/user/profile?mail=[email]`

- PUT `/api/user/profile?mail=[email]`

  ```py
  body = {
    "username": "",
    "password": "",
  }
  ```

- DELETE `/api/user/profile?mail=[email]`

### Update

- Section
  - POST `/api/update/section/unlock?mail=[email]&id=[id]`
  - POST `/api/update/section/lock?mail=[email]&id=[id]`
- Bag
  - POST `/api/update/bag/add?mail=[email]&item=[item]`
  - POST `/api/update/bag/remove?mail=[email]&item=[item]`
