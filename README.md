# Backend for travel website

"""
Do you like travelling? Do you like resting with comfort? Welcome to TravelMore!
API service for choosing of travel places, stay places and booking accommodations written on DRF.
"""


- Python3 must be already installed
- Install PostgreSQL and create db


You need to create `.env` file and add there the variables with your according values:
- `POSTGRES_DB`: this is databases name;
- `POSTGRES_USER`: this is username for databases;
- `POSTGRES_PASSWORD`: this is username password for databases;
- `POSTGRES_HOST`: this is host name for databases;
- `POSTGRES_PORT`: this is port for databases;
- `SECRET_KEY`: this is Django Secret Key - by default is set automatically when you create a Django project.
                You can generate a new key, if you want, by following the link: `https://djecrety.ir`;



## Run with docker

Docker should be installed

- Create docker image: `docker-compose build`
- Run docker app: `docker-compose up`


### How to create superuser
- Run `docker-compose up` command, and check with `docker ps`, that 2 services are up and running;
- Create new admin user. Enter container `docker exec -it <container_name> bash`, and create in from there;



## Features

- JWT authentication;
- Admin panel /admin/;
- Documentation is located at /api/doc/swagger/;
- Creating amenity, destination, stays (only admin);
- Creating accommodation with amenities (only admin);
- Filtering accommodation by name, amenities;
- Filtering destinations by name & country;
- Filtering stays by name;
- Adding rating to destinations and stays (authenticated user);
- Leaving reviews to destinations and stays (authenticated user);


### What do APIs do

- [GET] /destinations/ - obtains a list of destinations with the possibility of filtering by name, country;
- [GET] /stays/ - obtains a list of stays with the possibility of filtering by name;
- [GET] /accommodations/ - obtains a list of accommodations with the possibility of filtering by name, amenities;

- [GET] /destinations/id/ - obtains the specific destination information data;
- [GET] /stays/id/ - obtains the specific stay data;
- [GET] /accommodations/id/ - obtains the specific accommodation data;

- [GET] /bookings/ - receives the bookings history for the current user;

- [POST] /destinations/ - creates a destination;
- [POST] /stays/ - creates a stay;
- [POST] /accommodations/ - creates an accommodation;
- [POST] /amenities/ - creates an amenity;
- [POST] /stay-frames/ - adds frames to stays;
- [POST] /room-frames/ - adds frames to accommodations;
- [POST] /rating-destinations/ - adds rating to destinations;
- [POST] /rating-stays/ - adds rating to stays;
- [POST] /review-destinations/ - adds reviews to destinations;
- [POST] /review-stays/ - adds reviews to stays;
- [POST] /bookings/ - creates booking of accommodations;


- [GET] /user/me/ - obtains the specific user information data;

- [POST] /user/signup/ - creates new users;
- [POST] /user/login/ - an user authorization, obtains an access token;
- [POST] /user/token/ - creates token pair for user;
- [POST] /user/token/refresh/ - gets new access token for user by refresh token;

- [PUT] /user/me/ - updates user data;



### Checking the endpoints functionality
- You can see detailed APIs at swagger page: via /api/doc/swagger/

  

## Check project functionality

- Note: after running project you need to set values to RatingStar model through admin panel(e.g. 1, 2, 3, 4, 5)

Superuser credentials for test the functionality of this project:
- email address: `migrated@admin.com`;
- password: `migratedpassword`.


## Getting access

- Create user via /user/signup/
- Get access token via /user/token/ 
- Get access token via /user/login

Enter:
- email address: `migrated@admin.com`;
- password: `migratedpassword`.


## Testing

- Run tests using different approach: `docker-compose run app sh -c "python manage.py test"`;
- If needed, also check the flake8: `docker-compose run app sh -c "flake8"`.
