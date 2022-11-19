# API integration

This API's is developed in fastapi and are documented using swagger.

## Getting Started

To run the API locally follow the steps below:

1. Clone the repository
2. Create a virtual environment
3. Install the dependencies
4. Run the API
5. Access the API documentation `http://localhost:8000/docs`

![Screenshot 2022-11-19 at 3 39 33 PM 2](https://user-images.githubusercontent.com/36413448/202856534-865e47d6-b450-4ebf-8248-4b56054c44b2.png)


To run through docker follow the steps below:

1. Clone the repository
2. Run the `docker-compose up`

### Prerequisites

1. To run the API locally, you need to have docker installed.
2. Add a .env file
3. Add the following environment variables to the .env file

```
PROJECT_NAME=backend
BACKEND_CORS_ORIGINS=["http://localhost:8000", "https://localhost:8000", "http://localhost", "https://localhost"]


API_KEY=
API_SECRET=
API_URL=https://hiring.api.synthesia.io

CACHE_ACTIVE=True

REDIS_HOST=redis
REDIS_PORT=6379
REDIS_DB=1

```

### Installing

If you run the project locally without github you will need python 3.8 and pipenv installed.

## Running the tests

To run tests use pytest

```
pytest tests
```
(Run this command withing the backend folder in the container)

### Break down into end to end tests

The tests are located in the tests folder and are divided on modules. 


### And coding style tests

The code is formatted using black and as the code is built in python, the code is formatted using PEP8.


## Deployment

The project is deployed on heroku link: 

## Built With

* [FastAPI](https://fastapi.tiangolo.com/) - The web framework used
* [Redis](https://redis.io/) - Used to cache the data
* [RabbitMQ](https://www.rabbitmq.com/) - Used to send messages to the workers
