# Story McStorface

Story McStorface is a simple an minimal Warehouse Management Software written out of frustration.

The main Design Goal was to make this software so easy to use that complexity can't be used as an excuse why something wasn't correctly booked.

## Screenshots

See [docs](docs/).


## Installation

```bash
git clone https://github.com/momorientes/storymcstorface.git
cd storymcstorface
$EDITOR docker-compose.override.yml #set STORY_DOMAIN to your domain when proxying.
docker-compose build
docker-compose up -d

docker-compose exec django ./manage.py migrate
docker-compose exec django ./manage.py collectstatic
docker-compose exec django ./manage.py createsuperuser
```

## First steps

### Login
The main management is done via the Django Admin. Navigate to `https://localhost:8000/admin` and sign in with the previously created superuser.

### Adding Users
Users can be added in the users tab. Normal Users can use the frontend. If a user should be able to perform admin actions set the "Superuser Status" checkbox.

### Create a facility

A facility is a warehouse, it doesn't matter if it's a small cabinet or a full house.
First assign a speaking name.
In the table below you can add rows and colums to your liking, e.g. (Row: A Column: 1, Row: A Column: 2). They will be sorted by row name primarily and secondarily by Column number.


### Create Categories

Categories are used to help users find product alternatives. Create as many you'd like.


### Create Vendors and Products

First Create a Vendor name e.g. `ACME Inc.` Then add as many products as necessary in the table below, the Vendor PN is optional.
Products exist on a global basis, they can be assigned different slots in your warehouse.

### View the Log

All Removals and Insertions are Logged, view the Stora

### Passowrd Change

I didn't yet find a nice place to put the password change button. For now it is hidden at `/password/`.

## Development

To run locally with a `sqlite3` database and without docker:

```bash
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

export DJANGO_DEVELOPMENT=true
cd storymcstorface
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```