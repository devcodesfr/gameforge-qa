# GameForge QA

Python QA automation for the GameForgeStudio ecosystem.

This repo tests the apps as products:

- GameForgeStudio platform backend
- Buttonz backend
- GFS to Buttonz auth-code launch flow

The suite can run locally against your dev servers, or in GitHub Actions against disposable Postgres databases and checked-out copies of GFS and Buttonz.

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
GFS_ADMIN_USERNAME=your-local-admin-test-user
GFS_ADMIN_PASSWORD=your-local-admin-test-password
GFS_DEVELOPER_USERNAME=your-local-developer-test-user
GFS_DEVELOPER_PASSWORD=your-local-developer-test-password
GFS_GAMER_USERNAME=your-local-gamer-test-user
GFS_GAMER_PASSWORD=your-local-gamer-test-password
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

The cross-app auth test runs once for each configured role-specific account. If neither account has usable credentials, the test is skipped so basic smoke checks can still run without secrets.

## GitHub Actions

The `GameForge Integration Tests` workflow runs this suite automatically for QA repo pushes and pull requests that touch the test harness. It also runs every Monday at 10:00 UTC and supports manual runs from the Actions tab.

In CI, the workflow:

- Checks out `devcodesfr/gameforgestudio-platform`, `devcodesfr/buttonz`, and this QA repo.
- Starts separate disposable Postgres services for GFS and Buttonz.
- Pushes both app schemas into those temporary databases.
- Seeds deterministic GFS QA accounts:
  - Developer: `qa_developer`
  - Gamer: `qa_gamer`
  - Password: `test-password`
- Starts both backends.
- Runs `python -m pytest -v --tb=short`.

CI does not use Neon, your local `.env`, or your personal platform account. If the app repos become private, update the workflow checkout steps to use a GitHub token with read access to those repos.

## Roadmap

- Add role-access tests for Developer vs Gamer API behavior.
- Split reusable fixtures for seeded Developer and Gamer accounts.
- Add deployment smoke checks when GFS and Buttonz have hosted environments.
