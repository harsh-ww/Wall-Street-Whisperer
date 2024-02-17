# CS261 Project

## Running Locally (Development)

### Docker

The easiest way to run the project is using Docker. 

The following command will start up a postgres server, along with the frontend and backend. Changes made to these projects will be reflected in real time.
```
docker compose --profile all up
```
The frontend is available at `localhost:8080` and the backend at `localhost:5000`.

If you find it easier to work with the code not running in a container, you can start the database only using `docker compose up`. You will need to run the backend and frontend separately using the commands found in the next section. This section will be updated with any issues encountered through this approach.

If you encounter issues running containers on your machine, GitHub offers a remote dev machine (Codespaces) for free for 180 hours/month for students. 


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