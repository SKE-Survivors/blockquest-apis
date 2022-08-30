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

### User handler

#### GET: `http://127.0.0.1:5000/user?mail=[email]`

#### POST: `http://127.0.0.1:5000/user`

body: `{ "mail": "email@email.com", "username": "username", "password": "password" }`

#### PUT `http://127.0.0.1:5000/user?mail=[email]`

body: `{ "username": "username", "password": "password" }`

#### DELETE `http://127.0.0.1:5000/user?mail=[email]`

### Section

#### POST `http://127.0.0.1:5000/update/section?mail=[email]&id=[id]`

#### Bag

#### POST `http://127.0.0.1:5000/update/section?mail=[email]&item=[item]`
