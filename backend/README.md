# API integration

This API's is developed in fastapi and are documented using swagger.

## Getting Started

To run the API locally follow the steps below:

1. Clone the repository
2. Create a virtual environment
3. Install the dependencies
4. Run the API
5. Access the API documentation `/docs`

To run through docker follow the steps below:

1. Clone the repository
2. Run the `docker-compose up`

### Prerequisites

To run the API locally, you need to have docker installed.

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
