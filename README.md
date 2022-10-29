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

### User

- GET: `/api/user?mail=[email]`
<!-- - POST: `/api/user`

  body: `{ "mail": "email@email.com", "username": "username", "password": "password" }` -->

- PUT `/api/user?mail=[email]`

  body: `{ "username": "username", "password": "password" }`

- DELETE `/api/user?mail=[email]`

### Update

- Section
  - POST `/api/update/section?mail=[email]&id=[id]`
- Bag
  - POST `/api/update/section?mail=[email]&item=[item]`
