# SafeCity

SafeCity is a web-based surveillance monitoring system that uses real-time computer vision to detect potential safety incidents — crowding, weapons, and fire — from live camera feeds, and automatically alerts the responsible user by email with a snapshot and location.

Built with **Flask**, **YOLO (Ultralytics)**, and **OpenCV**, with a role-based dashboard for monitoring alerts and viewing analytics.

## Features

- **Live detection dashboard** — dual camera feeds processed in real time.
- **Multiple detection models**
  - *Crowd Model*: counts people per camera and flags when a configurable limit is exceeded.
  - *Gun Model*: detects guns, knives, and fire.
- **Automated alerts** — on detection, a snapshot is saved and an email is sent to the assigned user with the incident type, location, and a Google Maps link.
- **Alerts log** — searchable/filterable table of all past incidents (by detection type, location, user, and date range).
- **Analytics dashboard** — charts breaking down incidents by location, detection type, camera, and time (daily counts over a configurable range).
- **User management (admin)** — create, update, and delete users; assign each user a location and camera ID.
- **Authentication** — login/session handling via Flask-Login, with passwords hashed using Bcrypt.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Flask, Flask-Login, Flask-WTF, Flask-Bcrypt |
| Database | SQLite via Flask-SQLAlchemy |
| Computer Vision | Ultralytics YOLO, OpenCV, TensorRT |
| Frontend | Jinja2 templates, jQuery, Chart.js |
| Notifications | SMTP (Gmail) |

## Project Structure

```
safe-city/
├── README.md
└── Re-design/
    ├── run.py                 # entry point — starts the Flask app
    ├── create_user.py         # script to seed an initial user
    ├── mail.py                # email alert sender
    ├── query.py               # helper DB query (last saved image ref)
    ├── instance/
    │   └── SafeCity.db        # SQLite database
    └── SafeCity/
        ├── __init__.py        # Flask app, DB, login manager setup
        ├── models.py           # User, Snapshots, Camera models
        ├── forms.py            # WTForms: login & registration
        ├── routes.py           # all app routes/endpoints
        ├── YOLO_Video.py       # detection loop (crowd / gun / fire / knife)
        ├── static/             # CSS, JS, detection snapshots
        └── templates/          # HTML pages (home, admin, alerts, analytics, etc.)
```

## Getting Started

### Prerequisites

- Python 3.11.7 (required for compatibility with SQLAlchemy in this project)
- A CUDA-capable GPU (the detection models run with `device='cuda'`)
- A Gmail account with an [App Password](https://myaccount.google.com/apppasswords) for sending alert emails

### Installation

```bash
git clone https://github.com/Abdul-Rahman-Rafat/safe-city.git
cd safe-city/Re-design

pip install flask flask-wtf flask-sqlalchemy flask-login flask-bcrypt
pip install ultralytics opencv-python tensorrt
```

### Configuration

This project currently expects a few things to be set up locally before running:

1. **Environment variables** for secrets (do not hardcode these — see [Known Issues](#known-issues)):
   ```bash
   export SECRET_KEY="your-secret-key"
   export MAIL_ADDRESS="your-email@gmail.com"
   export MAIL_APP_PASSWORD="your-gmail-app-password"
   ```
2. **Video sources & model weights** — `YOLO_Video.py` currently points to local file paths for video input and `.pt` model weights. Update these paths to match your environment (or your live camera stream source).
3. **Database** — the SQLite database is created automatically via SQLAlchemy on first run.

### Create the admin user

```bash
python create_user.py
```

### Run the app

```bash
python run.py
```

The app will be available at `http://127.0.0.1:5000`.

## Usage

1. Sign in at `/signin`.
2. Admin users can add new users via `/signup`, each assigned to a location and camera.
3. `/livestream` shows the live detection feeds for the two configured cameras.
4. `/alerts` lists all detected incidents (filterable).
5. `/analytics` shows charts summarizing incidents over time, location, and type.

## Known Issues

This project was built as a learning/portfolio project and has a few things worth fixing before any real deployment:

- Hardcoded absolute file paths (video sources, model weights) that only work on the original developer's machine — should be moved to a config file or environment variables.
- Global mutable state used to track detection counters — not safe under concurrent requests.
- No `requirements.txt` yet — dependencies are currently listed manually above.
- No automated tests.

## Roadmap

- [ ] Move all secrets/paths to environment variables / a config file
- [ ] Add `requirements.txt`
- [ ] Add support for arbitrary numbers of cameras (currently fixed at two)
- [ ] Add unit tests for routes and detection logic

