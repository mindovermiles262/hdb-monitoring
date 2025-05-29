# HarperDB Test Environment

This repository contains a test environment for HarperDB, including a Docker Compose setup, automated testing pipeline, and container monitoring.

## Prerequisites

- Docker and Docker Compose
- Python 3.9 or higher
- Git

## Setup

1. Clone the repository:
```bash
$ git clone git@github.com:mindovermiles262/hdb-monitoring.git
$ cd hdb-monitoring
```

2. Set up environment variables. Edit the `environment` section of the docker compose file. Also change the `main.py` file

3. Install Python dependencies (Use of venv recomended)

```bash
$ python3 -m venv venv
$ source venv/bin/activate

(venv) $ pip install -r requirements.txt
```

## Running Locally

1. Start the HarperDB container and monitoring stack:

**NOTE** If using an OS other than Linux Mint, you may experience difficulties getting cadvisor to work. Please edit the docker-compose.yaml file as needed to get the right combination of mounts for your system to run cadvisor. You should be able to see your containers as "Subcontainers" at http://localhost:8080/containers/

```bash
$ docker compose up -d
```

This should start the Grafana, Prometheus, Cadvisor, and the hdb-application.

2. Run the test script. In a new terminal run

```bash
(venv) $ python main.py
```

3. View the metrics in a Grafana dashboard: http://localhost:3000 >> Dashboards >> Services >> Docker Monitoring Test

4. Stop the containers when done:

```bash
$ docker-compose down
```

## Monitoring

The environment includes a complete monitoring stack:

- **cAdvisor**: Container metrics collection (http://localhost:8080)
- **Prometheus**: Metrics storage and querying (http://localhost:9090)
- **Grafana**: Metrics visualization (http://localhost:3000)

### Accessing Grafana

1. Open http://localhost:3000 in your browser
2. Login with the credentials set in environment variables (default: admin/admin)
3. The HarperDB dashboard will be automatically imported

### Available Metrics

The monitoring stack collects the following metrics:
- CPU Usage
- Memory Usage
- Network I/O
- Container Health Status

## Performance Metrics

The test script collects the following metrics for each operation:
- Duration
- Operation success/failure status

These metrics are displayed in the console output after the test completes.

## Security Notes

- Default credentials are provided in the Docker Compose file but should be overridden in production
- Secrets are handled through environment variables
- Monitoring services are exposed on localhost only
