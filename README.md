# InfraLab

InfraLab is a personal infrastructure and observability project built with FastAPI and PostgreSQL.

The goal of the project is to monitor systems, collect metrics, visualize historical data and experiment with backend, networking and infrastructure concepts.

---

## Features

- FastAPI backend
- PostgreSQL database
- Live dashboard
- Historical charts
- Client tracking
- Request logging
- Metrics storage
- Real-time updates
- Modular architecture

---

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- HTML
- CSS
- JavaScript
- Chart.js
- Uvicorn
- WSL2

---

## Installation

Clone repository:

```bash
git clone https://github.com/RomanDV22/Proyecto-InfraLab.git
```

Enter project:

```bash
cd Infralab
```

Create virtual environment:

```bash
python3 -m venv venv
```

Activate environment:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the PostgreSQL database schema:

```bash
psql -U postgres -d infralab -f database/schema.sql
```

More details are available in [docs/database.md](docs/database.md).

---

## Run Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## Dashboard

Open browser:

```text
http://SERVER_IP:8000/dashboard
```

---

## Current Capabilities

- Metrics visualization
- Historical monitoring
- Request tracking
- Live dashboard updates
- Database persistence

---

## Future Improvements

- Docker support
- Authentication
- Multi-agent monitoring
- WebSockets
- Alerts system
- Advanced analytics
- Prometheus integration

---

## Architecture

```text
Client
   ↓
FastAPI
   ↓
Services
   ↓
PostgreSQL
```
