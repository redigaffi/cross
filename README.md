### Running the Application
### Prerequisites

- Python 3.11 or higher
- Poetry
- Docker
- Docker Compose
- Running Locally with Python

### Mandatory environment variables

- CANDIDATE_ID: Set this environment variable to the candidate ID you want to use.

### Running Locally with Python
1. Clone the repository:
2. Install dependencies:

`
poetry install
`

### Run the application:

`
python -m cross
`

### Running with Docker
1. Build the Docker image:

`
docker build -t cross-app .
`

2. Run the Docker container:

`
docker run cross-app
`

### Running with Docker Compose
1. Start the application using Docker Compose:

`
docker-compose up --build
`
