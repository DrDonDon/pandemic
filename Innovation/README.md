# Innovation

Rapid-prototyping sandbox. Each sub-folder is a self-contained project.

## Structure

```
Innovation/
├── base-requirements.txt   # shared deps for every project
├── new-project.sh          # scaffold a new project in seconds
└── <project-name>/
    ├── requirements.txt    # project-specific deps
    ├── main.py             # entry point
    └── test_browser.py     # gstack / Playwright browser tests
```

## Start a new project

```bash
cd Innovation
./new-project.sh my-idea
cd my-idea
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Run browser tests with gstack / Playwright

```bash
python test_browser.py          # headless by default
HEADED=1 python test_browser.py # watch the browser
```

## Tips

- Keep each project folder independent — its own venv, its own deps.
- Use `main.py` as the fast iteration loop; use `test_browser.py` for anything visual.
- Delete the project folder when you're done prototyping; promote to a real module if it sticks.
