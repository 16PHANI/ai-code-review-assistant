# Contributing

## Setup

```bash
git clone https://github.com/16PHANI/ai-code-review-assistant.git
cd ai-code-review-assistant
echo GROQ_API_KEY=your_key> groq.env
docker-compose up --build
```

## Project layout

- `app/main.py` — all API routes and Groq prompt logic
- `app/database.py` — MongoDB operations
- `templates/index.html` — frontend HTML
- `static/css/style.css` — all styles
- `static/js/app.js` — frontend JavaScript

## Making changes

1. Fork the repository
2. Create a branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Test locally with `docker-compose up --build`
5. Commit: `git commit -m "feat: description"`
6. Push and open a pull request

## Commit format

```
feat: add new feature
fix: fix a bug
docs: update documentation
style: formatting only
refactor: code change, no feature or fix
```
