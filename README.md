# CS261 Project - Wall Street Whisperer

## Running Locally (Development)

The application consists of several components:
- PostgresSQL Database
- Flask Web Server
- React frontend app

### Docker

The easiest way to run the project is using Docker. 

The following command will run all of the services needed for the application in development mode. Changes made to these projects will be reflected in real time.

```
docker compose --profile all up
```

This command starts the following services:
- Frontend - `localhost:5173`
- Backend - `localhost:5000`
- Postgres - `localhost:5432` - also accessible using hostname `db` via adminer
- Adminer - database management - `localhost:8080`

You must also create a `.env` file containing secrets in the root directory of the project. This file can be found on Teams.
The development mode for the project will also load some sample data into the database.

If you find it easier to work with the code not running in a container, you can start the database only using `docker compose up`. You will need to run the backend and frontend separately using the commands found in the next section. This section will be updated with any issues encountered through this approach.

### Without Docker (not recommended)
If you choose not to use docker, you will have to follow the steps below. Keep in mind that there is an option to run just the database through docker and run the frontend and backend independently as described above.

#### Installation
```
cd backend
pip install -r requirements.txt
cd ../frontend
npm install
```
In addition, you will need to run a postgres server. If you choose not to run postgres in a docker container, you will need to install the server yourself.
#### Running
```
cd backend/app & flask run
cd frontend & npm run dev
```