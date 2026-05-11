# JetSnack — Appium + pytest UI automation

Automated UI tests for the JetSnack Android sample application (`com.example.jetsnack`) using **Python**, **pytest**, **Appium 2** (UiAutomator2), and the **Appium-Python-Client**.

## Documentation

| Resource | Description |
|----------|-------------|
| [doc/SETUP.md](doc/SETUP.md) | Windows setup: Node/Appium, emulator, Inspector JSON, running pytest |
| [doc/test_cases.md](doc/test_cases.md) | User steps and expected results per test (aligned with `tests/*.py` docstrings) |

## Configuration

Edit **`assist/config.py`** for:

- **`APK_PATH`** — location of the `app-debug.apk` (or your build)
- **`UDID`** — output of `adb devices`
- **`APPIUM_SERVER_URL`** — default `http://127.0.0.1:4723`

## Run tests

With Appium running and a device connected:

```bash
python -m pip install -r requirements.txt
python -m pytest -v
```

Single module examples:

```bash
python -m pytest tests/test_home.py -v
python -m pytest tests/test_search.py -v
```

## Project layout

| Path | Role |
|------|------|
| `assist/` | `config.py`, `helpers.py`, `locators.py`, `pages/` |
| `tests/` | Pytest modules and `conftest.py` |
| `doc/` | Setup guide and test case descriptions |
| `scripts/` | Optional PowerShell/cmd helpers (Appium PATH, recording) |
