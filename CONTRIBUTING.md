# Contributing to PropIQ

First off — thank you for taking the time to contribute! 🎉  
Every contribution, big or small, is genuinely appreciated.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Getting Started](#getting-started)
- [Branch Naming Convention](#branch-naming-convention)
- [Commit Message Convention](#commit-message-convention)
- [Pull Request Process](#pull-request-process)
- [What We'd Love Help With](#what-wed-love-help-with)

---

## Code of Conduct

This project follows a [Code of Conduct](CODE_OF_CONDUCT.md).  
By participating, you are expected to uphold it. Please be respectful to all contributors.

---

## How Can I Contribute?

### 🐛 Reporting Bugs
- Check if the bug is already reported in [Issues](https://github.com/Priyanshu-6/PropIQ/issues)
- If not, open a new issue using the **Bug Report** template
- Be as detailed as possible — include steps to reproduce, screenshots, and your OS/Python version

### 💡 Suggesting Features
- Open a new issue using the **Feature Request** template
- Explain the problem you're trying to solve, not just the solution
- We'll discuss it before you start coding — this saves everyone's time

### 🔧 Submitting Code
- Always open an issue first before starting work on a large change
- For small fixes (typos, minor bugs) you can go straight to a Pull Request

---

## Getting Started

**1. Fork the repository**

Click the **Fork** button on the top right of the repo page.

**2. Clone your fork**
```bash
git clone https://github.com/YOUR_USERNAME/PropIQ.git
cd PropIQ
```

**3. Set up the project**
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

pip install -r requirements.txt
python model.py                 # generates model artifacts
streamlit run app.py            # verify everything works
```

**4. Add the original repo as upstream**
```bash
git remote add upstream https://github.com/Priyanshu-6/PropIQ.git
```

**5. Create your branch**
```bash
git checkout -b feature/your-feature-name
```

---

## Branch Naming Convention

| Type | Format | Example |
|---|---|---|
| New feature | `feature/description` | `feature/add-mumbai-support` |
| Bug fix | `fix/description` | `fix/locality-encoding-error` |
| Documentation | `docs/description` | `docs/update-readme` |
| UI improvement | `ui/description` | `ui/improve-dark-theme` |

---

## Commit Message Convention

We follow a simple commit message format:

```
type: short description
```

| Type | When to use |
|---|---|
| `feat` | Adding a new feature |
| `fix` | Fixing a bug |
| `docs` | Documentation changes |
| `ui` | UI/styling changes |
| `chore` | Maintenance tasks |
| `refactor` | Code restructuring |

**Examples:**
```bash
git commit -m "feat: add support for Mohali-specific localities"
git commit -m "fix: correct area column name in similar properties"
git commit -m "docs: update installation steps in README"
```

---

## Pull Request Process

1. Make sure your branch is up to date with `main`:
```bash
git fetch upstream
git rebase upstream/main
```

2. Run the app and verify your changes work:
```bash
streamlit run app.py
```

3. Push your branch:
```bash
git push origin feature/your-feature-name
```

4. Open a Pull Request on GitHub:
   - Use a clear, descriptive title
   - Describe **what** you changed and **why**
   - Link the related issue (e.g. `Closes #12`)
   - Add screenshots if it's a UI change

5. Wait for review — we'll respond within a few days

---

## What We'd Love Help With

These are areas where contributions are especially welcome:

- 🏙️ **Multi-city support** — extend model.py to support other Indian cities from the india-housing-datasets library
- 🤖 **Better ML models** — experiment with XGBoost, LightGBM, or hyperparameter tuning
- 🗺️ **Map visualisation** — add a Folium or Pydeck map showing property locations
- 📱 **Mobile UI** — improve the Streamlit layout for smaller screens
- 🐛 **Bug fixes** — check open issues labelled `bug`
- 📝 **Documentation** — improve code comments and docstrings

Issues labelled `good first issue` are the best place to start if you're new! 👋

---

<p align="center">Happy contributing! 🚀</p>