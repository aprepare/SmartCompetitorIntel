# Contributing

Thanks for your interest in SmartCompetitorIntel.

## Development Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

On Windows, activate the virtual environment with:

```powershell
.\venv\Scripts\activate
```

## Pull Request Guidelines

- Keep changes focused and easy to review.
- Include a short description of the problem and the chosen solution.
- Add or update documentation when behavior changes.
- Avoid committing secrets, local databases, virtual environments, or generated cache files.
- For retrieval or prompt changes, include a sample question and expected behavior.

## Useful Areas for Contributions

- Tests for document chunking, vector search, and API endpoints.
- Provider configuration improvements for OpenAI-compatible APIs.
- Docker deployment files.
- Real data connector abstractions.
- Examples for common competitor-analysis workflows.

## Reporting Issues

When opening an issue, include:

- what you expected to happen;
- what happened instead;
- reproduction steps;
- your Python version and operating system;
- relevant logs with secrets removed.
