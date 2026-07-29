# Backend/DevOps Engineer Interview

A small content service: users, posts, comments, tags. Django + Ninja + PostgreSQL.

# Running the project

The project can be run either with **Docker (recommended)** or directly on your local machine.

---

## Option 1 – Docker (recommended)

### Prerequisites

- Docker Desktop

### Start the application

```bash
cp .env.example .env

docker compose up
```

> If you modify the `Dockerfile` or project dependencies, rebuild the image with:

```bash
docker compose up --build
```

The application automatically:

- Starts PostgreSQL
- Applies database migrations
- Starts the API using Gunicorn

### Load sample data

The sample dataset is intentionally not loaded automatically because it creates approximately **100k posts** and **500k comments**.

Run it once after the containers are running:

```bash
docker compose exec web uv run python manage.py seed
```

### API documentation

<http://localhost:8000/api/docs>

---

## Option 2 – Local development

### Prerequisites

- [mise](https://mise.jdx.dev/) — manages the Python toolchain and uv.
- PostgreSQL 16 running locally.

### Install dependencies

```bash
mise install
uv sync
```

### Configure the environment

Copy the example configuration:

```bash
cp .env.example .env
```

Create the database:

```bash
createdb -U postgres backend_devops_interview
```

> If your PostgreSQL installation uses a different user, password or database configuration, update the values in your `.env` file before running the migrations.

### Apply migrations

```bash
uv run python manage.py migrate
```

### Load sample data

```bash
uv run python manage.py seed
```

> The seed generates approximately **100k posts** and **500k comments**, so this step may take a few minutes.

### Start the development server

```bash
uv run python manage.py runserver
```

### API documentation

<http://localhost:8000/api/docs>

---

## Environment variables

The project uses a `.env` file. A sample configuration is provided in `.env.example`.

| Variable | Default |
|----------|---------|
| SECRET_KEY | change-me |
| DEBUG | True |
| ALLOWED_HOSTS | localhost,127.0.0.1 |
| DB_NAME | backend_devops_interview |
| DB_USER | postgres |
| DB_PASSWORD | postgres |
| DB_HOST | localhost (local) / db (Docker) |
| DB_PORT | 5432 |

---

## What the API does

| Method | Path | Description |
| ------ | ---- | ----------- |
| GET | `/api/posts` | Published posts, newest first |
| GET | `/api/posts/search?q=` | Full-text-ish search across title and body |
| GET | `/api/posts/by-tag/{slug}` | Posts carrying a given tag |
| GET | `/api/posts/{id}` | Post detail with comments |
| POST | `/api/posts` | Create a post |
| POST | `/api/posts/{id}/comments` | Add a comment to a post |
| GET | `/api/users/{id}` | User profile with post and comment counts |
| GET | `/api/users/find?email=` | Look up a user by email |

## The assignment

We want to see how you take a working prototype and turn it into something a team can develop on and operate. Pick the changes that give the strongest signal about how you'd improve this codebase if you owned it. There are three areas we care about:

1. **Developer experience.** Getting this running on a fresh laptop is harder than it should be. Make it easier.
2. **Performance.** Once the database is seeded, exercise the endpoints. Some of them are slow. Find out why and fix what you can.
3. **Production readiness.** This service is a long way from something you'd put behind a load balancer. Move it closer — pick whichever deployment target you'd reach for at work (Helm chart, ECS task def, Kubernetes manifests, Fly.io, Render, plain Docker + systemd, etc.).

**Depth beats breadth.** Pick 2–3 things and go deep rather than touching ten things shallowly. Write a short `NOTES.md` covering:

- What you did and why.
- What you deliberately *didn't* do.
- What you'd do next if you had another day.

## Non-goals

- **Authentication / authorization** is intentionally absent. If you want to suggest a direction in `NOTES.md`, great — but no need to implement anything.
- **Test coverage** is not what we're grading. The smoke tests are there so you have something to wire into CI.
- **Reshaping the domain model** isn't expected. Adjust it if a performance fix needs it; otherwise leave it.

## Time

Soft cap of 2–6 hours, depending on your experience and what tooling you have available (AI agents are fine — just mention it in `NOTES.md` and include the chat transcripts).

We're looking at signal, not hours.

## Deliverable

Whatever's easy for you to share: a GitHub link, a git bundle, `git format-patch`, or similar.

Please don't open a PR against this repository.