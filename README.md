# SimForge

A lightweight, locally-hosted wave balance simulator for game designers. Built with Flask and Chart.js — define your player and enemy curves, simulate every wave, and instantly spot danger spikes or trivial gaps.

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-black?logo=flask)
![License](https://img.shields.io/badge/License-MIT-green)
![Part of CMG Forge](https://img.shields.io/badge/CMG%20Forge-SimForge-ffaa00?labelColor=0d0d0d)

---

## Features

| Panel | What it does |
|---|---|
| **Wave Count** | Set simulation length between 5 and 50 waves |
| **Player Curve** | Define base HP, base DPS, and % power scaling per wave |
| **Enemy Curve** | Define base HP, base damage, and % difficulty scaling per wave |
| **Balance Chart** | Live Chart.js line graph — Player Power vs Enemy Difficulty across all waves |
| **Danger Zones** | Waves where enemies outscale the player highlighted in red |
| **Trivial Zones** | Waves where the player is twice as strong as enemies flagged in green |
| **Wave Summary** | Text breakdown listing exact wave numbers for danger and trivial states |

---

## Math

| Value | Formula |
|---|---|
| Player Power (wave *n*) | `base_dps × (1 + scale_pct / 100) ^ n` |
| Enemy Difficulty (wave *n*) | `base_hp × (1 + enemy_scale_pct / 100) ^ n` |
| Danger Wave | `enemy_difficulty > player_power` |
| Trivial Wave | `player_power > enemy_difficulty × 2` |

---

## Requirements

| Requirement | Version | Notes |
|---|---|---|
| [Python](https://www.python.org/downloads/) | 3.11+ | Required |

### Python packages

All listed in `requirements.txt`:

```
flask>=3.0.0
flask-limiter>=3.5.0
gunicorn>=21.0.0
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/CMgameplays/SimForge.git
cd SimForge
```

### 2. Create and activate a virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## Running locally

```bash
python simforge.py
```

The server starts on `http://127.0.0.1:5000`.

---

## Project structure

```
SimForge/
├── simforge.py          # Flask app — all routes and simulation logic
├── requirements.txt     # Python dependencies
├── Procfile             # Gunicorn entry point (for deployment)
├── templates/
│   └── index.html       # Single-page UI (HTML + CSS + JS + Chart.js)
└── LICENSE
```

---

## API Route

| Method | Route | Description |
|---|---|---|
| `GET` | `/` | Main UI page |
| `POST` | `/api/simulate` | Run a wave simulation, returns JSON |

### Request body (`/api/simulate`)

```json
{
  "wave_count":   20,
  "player_hp":    100,
  "player_dps":   50,
  "player_scale": 10,
  "enemy_hp":     80,
  "enemy_damage": 20,
  "enemy_scale":  15
}
```

### Response

```json
{
  "waves":            [1, 2, 3, "..."],
  "player_power":     [55.0, 60.5, "..."],
  "enemy_difficulty": [92.0, 105.8, "..."],
  "danger_waves":     [1, 2, 3],
  "trivial_waves":    [18, 19, 20]
}
```

---

## Deployment

The app is production-ready with Gunicorn. It can be deployed to any WSGI-compatible host.

**Render / Railway / Fly.io:**

The `Procfile` is already configured:

```
web: gunicorn simforge:app --workers 2 --timeout 60 --bind 0.0.0.0:$PORT
```

Just connect your GitHub repo and deploy — no additional configuration required.

---

## License

MIT — see [LICENSE](LICENSE) for details.

© CMG Forge
