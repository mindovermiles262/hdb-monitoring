# HarperDB Test Environment

This repository contains a test environment for HarperDB, including a Docker Compose setup, automated testing pipeline, and container monitoring.

## Prerequisites

- Docker and Docker Compose
- Python 3.9 or higher
- Git

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Set up environment variables (optional, defaults are provided):
```bash
export HDB_ADMIN_USERNAME=your_username
export HDB_ADMIN_PASSWORD=your_password
export GRAFANA_ADMIN_USER=your_grafana_username
export GRAFANA_ADMIN_PASSWORD=your_grafana_password
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Running Locally

1. Start the HarperDB container and monitoring stack:
```bash
docker-compose up -d
```

2. Run the test script:
```bash
python harper_operations.py
```

3. Stop the containers when done:
```bash
docker-compose down
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

## GitHub Actions Pipeline

The repository includes a GitHub Actions workflow that:
1. Starts a HarperDB container
2. Runs the test script
3. Collects performance metrics
4. Validates the results

To use the pipeline:
1. Fork this repository
2. Add the following secrets to your repository:
   - `HDB_ADMIN_USERNAME`
   - `HDB_ADMIN_PASSWORD`
   - `GRAFANA_ADMIN_USER`
   - `GRAFANA_ADMIN_PASSWORD`
3. Push to the main branch or create a pull request

## Performance Metrics

The test script collects the following metrics for each operation:
- Duration
- Operation success/failure status

These metrics are displayed in the console output after the test completes.

## Security Notes

- Default credentials are provided in the Docker Compose file but should be overridden in production
- Secrets are handled through environment variables
- The GitHub Actions workflow uses repository secrets for sensitive data
- Monitoring services are exposed on localhost only 