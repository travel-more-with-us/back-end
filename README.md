# Backend for travel website


You need to create `.env` file and add there the variables with your according values:
- `POSTGRES_DB`: this is databases name;
- `POSTGRES_USER`: this is username for databases;
- `POSTGRES_PASSWORD`: this is username password for databases;
- `POSTGRES_HOST`: this is host name for databases;
- `POSTGRES_PORT`: this is port for databases;
- `SECRET_KEY`: this is Django Secret Key - by default is set automatically when you create a Django project.
                You can generate a new key, if you want, by following the link: `https://djecrety.ir`;

  
## Check project functionality

- Note: after running project you need to set values to RatingStar model through admin panel(e.g. 1, 2, 3, 4, 5)

Superuser credentials for test the functionality of this project:
- email address: `migrated@admin.com`;
- password: `migratedpassword`.


## Create token pair for user

Token page: `http://127.0.0.1:8000/user/token/` or 
Login page: `http://127.0.0.1:8000/user/login/`

Enter:
- email address: `migrated@admin.com`;
- password: `migratedpassword`.
