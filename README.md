# GameForge QA

Python QA automation for the GameForgeStudio ecosystem.

This repo tests the apps as products:

- GameForgeStudio platform backend
- Buttonz backend
- GFS to Buttonz auth-code launch flow

The suite is local-first for now. It does not start the apps for you; start the app backends first, then run pytest.

## Current Coverage

- GFS health endpoint responds.
- Buttonz health endpoint responds.
- GFS logged-out `/api/user/current` returns `401`.
- Buttonz logged-out `/api/user/current` returns `401`.
- Buttonz config exposes the expected GFS public URL.
- GFS can create a Buttonz launch URL with a one-time code.
- Buttonz can exchange that code and create its own session.

## Setup

Confirm you are using a normal Python install:

```bash
where python
python --version
```

If `where python` points at a bundled app runtime, install Python from python.org or the Microsoft Store and put it on PATH before installing dependencies.

Install Python dependencies:

```bash
python -m pip install -r requirements.txt
```

Create a local QA env file:

```bash
copy .env.example .env
```

Then fill in:

```env
GFS_TEST_USERNAME=your-real-local-test-user
GFS_TEST_PASSWORD=your-real-local-test-password
```

Do not commit `.env`.

## Required Local Servers

Start the backends before running the QA suite.

GameForgeStudio:

```bash
cd "../gameforgestudio-platform"
npm run dev:server
```

Buttonz:

```bash
cd "../buttonz"
npm run dev:server
```

Default API URLs:

```env
GFS_API_URL=http://127.0.0.1:5000
BUTTONZ_API_URL=http://127.0.0.1:5001
GFS_PUBLIC_URL=http://localhost:5173
```

The tests use `127.0.0.1` for backend calls to avoid Windows/WSL `localhost` weirdness.

## Run Tests

Run everything:

```bash
python -m pytest -v
```

Run smoke tests only:

```bash
python -m pytest tests/test_smoke.py -v
```

Run cross-app launch tests only:

```bash
python -m pytest tests/test_cross_app_launch.py -v
```

If `GFS_TEST_USERNAME` or `GFS_TEST_PASSWORD` is missing, the cross-app auth test is skipped. That is intentional so basic smoke checks can still run without secrets.

## Roadmap

- Add role-access tests for Developer vs Gamer API behavior.
- Add GitHub Actions once local QA stabilizes.
- Split reusable fixtures for seeded Developer and Gamer accounts.
- Add deployment smoke checks when GFS and Buttonz have hosted environments.
