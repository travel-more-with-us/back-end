# Backend for travel website

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


  
## Check project functionality

- Note: after running project you need to set values to RatingStar model through admin panel(e.g. 1, 2, 3, 4, 5)

Superuser credentials for test the functionality of this project:
- email address: `migrated@admin.com`;
- password: `migratedpassword`.


## Getting access

- Create user via /user/signup/
- Get access token via /user/token/ or 
- Get access token via /user/login

Enter:
- email address: `migrated@admin.com`;
- password: `migratedpassword`.


## Testing

- Run tests using different approach: `docker-compose run app sh -c "python manage.py test"`;
