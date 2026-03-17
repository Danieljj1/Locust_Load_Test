# Locust Load Test Dashboard

A performance testing dashboard that visualizes load test results from Locust. Upload CSV exports from different test runs and compare metrics side by side.

## What It Does

- Runs load tests against a public API using Locust
- Captures time-series performance data to CSV
- Visualizes requests per second and response time over time
- Supports uploading multiple test runs for comparison
- Filter by endpoint to isolate performance per route

## Tech Stack

- **Locust** — load generation and test execution
- **Streamlit** — interactive dashboard UI
- **pandas** — data processing and CSV parsing
- **matplotlib** — chart rendering

## Setup

Install dependencies:

```bash
pip install locust streamlit pandas matplotlib
```

## Usage

### 1. Run a load test

```bash
locust --csv=results --csv-full-history
```

This opens the Locust UI at `http://localhost:8089`. Enter your test settings:

- **Host:** `https://jsonplaceholder.typicode.com`
- **Number of users:** 5-20
- **Spawn rate:** 1

Let it run for 60+ seconds, then stop. This generates `results_stats_history.csv`.

### 2. Run additional tests for comparison

```bash
locust --csv=results2 --csv-full-history
```

Use different user counts or spawn rates to see how performance changes under different loads.

### 3. Launch the dashboard

```bash
streamlit run dashboard.py
```

Upload one or more `*_stats_history.csv` files to see the charts.

## Project Structure

```
├── locustfile.py      # Defines user behavior and test endpoints
├── dashboard.py       # Streamlit dashboard for visualizing results
└── README.md
```

## Test Target

Uses [JSONPlaceholder](https://jsonplaceholder.typicode.com), a free public API for testing. The locustfile hits two endpoints with weighted tasks:

- `GET /posts` (weight: 3) — fetches all posts
- `GET /posts/1` (weight: 1) — fetches a single post
