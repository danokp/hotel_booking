# Hotel Booking

Hotel Booking - a FastAPI application that lets users register, view available rooms,
book rooms in the selected hotel, cancel bookings and view booked rooms by users.

## Installation
To download and install this project use the following commands:
```bash
git clone git@github.com:danokp/hotel_booking.git
cd hotel_booking
```

## Usage
1. Make sure that Docker and Docker-compose are installed.
```bash
docker -v
docker compose version
```
2. Create `.env-docker` file according to example (`.env-example`)
3. Run the application:
```bash
docker compose up
```
4. Open API docs to try the application in web browser at [http://127.0.0.1/v1/docs](http://127.0.0.1/v1/docs) 
or via admin interface at [http://127.0.0.1/admin](http://127.0.0.1/admin).
