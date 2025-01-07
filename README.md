# Projects Manager API

### Description:

API to manage _“projects”._

_“Project”_ in our terminology is a plot of land, that we will be analyzing by utilizing the
satellite imagery captured in selected date range.


### Questions:

Questions I should have asked. (but I did not, shame on me 😓)

1. How 'area of interest' is going to be send: POST file upload or POST request body?
2. Should the API support additional GeoJSON types like FeatureCollection or only Feature with MultiPolygon geometry?
3. Should the geojson data be stored in a structured format (as JSON or in a spatial database like PostGIS)?
4. Are there size or complexity limits for the GeoJSON file (maximum vertices, file size)?


## Prerequisites

Before starting, ensure you have the following installed on your machine:

1. **Docker**: [Install Docker](https://docs.docker.com/get-docker/)
2. **Docker Compose**: [Install Docker Compose](https://docs.docker.com/compose/install/)
3. **Git**: To clone the repository. [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

## Getting Started

Follow the steps below to run the application on your machine:

### 1. Clone the Repository

If you have Git installed, clone this repository:

```bash
git clone <repository_url>
cd <repository_name>
```

### 2. Configure Environment Variables
Ensure there is a .env file in the root of the project with the following content (**_file is already provided!!_**):
```env
POSTGRES_USER=your_postgres_username
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DB=projects_db
```

### 3. Build and Start the Application

Run the following command to build and start the application:

```bash
docker-compose up --build
```

This command will:

- Build the FastAPI application image using the provided Dockerfile.
- Automatically pull the postgis/postgis Docker image for the database.
- Create a PostgreSQL database with PostGIS support using the credentials (POSTGRES_USER, POSTGRES_PASSWORD) specified in the .env file.
- Start both the projects-manager-api and projects-db containers.

### 4. Access the Application
Once the containers are running:

Access the API:
- Open your browser and navigate to http://localhost:8000.
- Visit http://localhost:8000/docs to access the Swagger UI for the API.

### 5. Run in Detached Mode (Optional)
To run the containers in the background:

```bash
docker-compose up --build -d
```

### 6. Stop the Application
To stop the containers:

```bash
docker-compose down
```
This command will:
- Stop the running containers.
- Remove the temporary container state.


### Important Notes!
- **Database Creation:** Docker Compose automatically creates the PostgreSQL database with the user, password, and database name specified in the .env file.
- **Database Migrations:** Migrations are applied automatically when the app starts, as defined in the entrypoint.sh script.


### This setup is intended for local development. For production, additional configurations such as load balancing, security, and some other improvements may be required.