# Contributing to Jupiter Sonic

Thank you for your interest in contributing to Jupiter Sonic! We are building a modular, production-ready, fully local Speech Intelligence Platform.

By contributing to this repository, you help shape a high-performance audio engine that preserves user privacy and simplifies local AI deployment.

---

## 🗺️ Code of Conduct

We expect all contributors to adhere to standard respectful open-source communication:
* Treat others with respect and constructive professionalism.
* Focus on clean engineering, robustness, and readability of code.

---

## 🛠️ Development Setup

To configure a local developer environment without Docker:

### Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   # On Windows:
   .venv\Scripts\activate
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

4. **Verify installation**:
   Run tests using pytest:
   ```bash
   pytest
   ```

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install node dependencies**:
   ```bash
   npm install
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```

---

## 🎨 Style Guidelines

We enforce strict formatting rules to maintain repository cleanliness.

### Python Style Guide
* **Code Formatter**: We use [Black](https://github.com/psf/black) with standard parameters.
* **Linter & Import Sorter**: We use [Ruff](https://github.com/astral-sh/ruff) for linting and sorting imports.
* Before committing, run these commands inside the `backend` directory:
  ```bash
  # Check code style issues
  ruff check .
  # Format code
  black .
  ```

### TypeScript / React Style Guide
* **Formatter**: [Prettier](https://prettier.io/)
* **Linter**: [ESLint](https://eslint.org/)
* Before committing, run these commands inside the `frontend` directory:
  ```bash
  npm run lint
  npm run format
  ```

---

## 🧪 Testing Guidelines

We aim for high test coverage on core business pipelines and API routes.

### Writing Python Tests
* Add pytest tests inside the `backend/tests/` directory.
* Name files `test_*.py` and test functions `test_*`.
* Mock heavy neural model weight loadings. Tests should execute quickly.
* Run tests with:
   ```bash
   pytest
   ```

---

## 📤 Submission Checklist

Before submitting a Pull Request (PR):
1. **Ensure linting passes**: Make sure Ruff, Black, ESLint, and Prettier run without warnings or errors.
2. **Verify tests pass**: Run pytest to confirm backend stability.
3. **Format PR title**: Use clear prefixes like `feat:`, `fix:`, `docs:`, or `refactor:`.
4. **Link issues**: Mention if your PR fixes a specific open issue.
