# daselyamlclean

A simple Python script to update nested YAML fields in a manifest using [dasel](https://github.com/TomWright/dasel) and a minimal `values.yaml` file.

## ✅ Requirements

To set up and run this project, you'll need:

- [pyenv](https://github.com/pyenv/pyenv) to manage Python versions  
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) (optional but helpful)  
- [dasel](https://github.com/TomWright/dasel) — the CLI YAML/JSON/TOML selector/put tool  
- Python 3.12.x  
- pyyaml (installed into a virtual environment)

---

## Setup Steps

### 1. Install pyenv and dasel (if not already installed)

Using Homebrew (macOS):

```
    brew install pyenv pyenv-virtualenv dasel
```

### 2. Install Python 3.12.2 via pyenv

```
    pyenv install 3.12.2
    pyenv shell 3.12.2
```
Or use a `.python-version` file:

```
    echo "3.12.2" > .python-version
```
---

### 3. Create and activate a virtual environment

```
    python -m venv .venv
    source .venv/bin/activate
```

Make sure you're in the project root folder when running these.

---

### 4. Install required Python packages

If `requirements.txt` is already provided (pre-compiled), install from it directly:

```
    pip install -r requirements.txt
```

---

### 5. Run the script

```
    ./run_dasel
```

---
