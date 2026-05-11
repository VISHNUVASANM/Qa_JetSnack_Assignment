# Setup —  JetSnack Appium automation

End-to-end environment steps for running the pytest suite against the JetSnack Android sample (`com.example.jetsnack`). Do the steps in order.

**Documentation in this repo**


| File                           | Purpose                                                  |
| ------------------------------ | -------------------------------------------------------- |
| `**doc/SETUP.md`** (this file) | Machine setup, Appium, Inspector, running tests          |
| `**doc/test_cases.md**`        | User-style steps and expected results per automated test |


---

## Already done on some machines (you can skip)

- Python packages: `pip install -r requirements.txt` (pytest + Appium-Python-Client).
- Appium CLI: Appium **2.11.5** globally (Appium 3 needs a newer Node than 20.18 on some setups).
- Driver: `appium driver list --installed` should show **uiautomator2**.
- Emulator id often `emulator-5554` — must match `assist/config.py` → `UDID`.
- Appium Inspector: not installed automatically; see **step 3**.

**Repeat setup on another PC:**

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\one_time_setup.ps1
```

If `adb` or `appium` is not recognized in a new terminal: open a **new** terminal after PATH changes, or double-click `**scripts/run_appium.cmd`** (starts Appium with PATH fixed for that window only).

**Java:** JDK **17+** for UiAutomator2. If Appium errors about Java, install Temurin 17 and set `**JAVA_HOME`**.

---

## 1) Phone or emulator

1. Install Android Studio, create a virtual device **or** plug in a phone with USB debugging on.
2. Run:
  ```bash
   adb devices
  ```
3. Copy the device id (example: `emulator-5554`) into `**assist/config.py**` as `**UDID**`.

---

## 2) Appium server (Java JDK 17+ recommended)

1. Install Node.js from [https://nodejs.org](https://nodejs.org).
2. One-time (if not done):
  ```bash
   npm install -g appium@2.11.5
   appium driver install uiautomator2
  ```
3. Start the server (leave the window open):
  ```bash
   appium
  ```
   Or double-click `**scripts/run_appium.cmd**`.
4. Leave this window open. When the server is ready you should see a line like **Appium REST http interface listener started** on `**http://0.0.0.0:4723`** (or `127.0.0.1:4723`).
5. Default server URL: `**http://127.0.0.1:4723**` (same as `**assist/config.py**` → `**APPIUM_SERVER_URL**`). Quick check: open `**http://127.0.0.1:4723/status**` in a browser — you should get JSON (if this fails, Inspector cannot connect either).

---

## 3) Connect Appium Inspector (optional — locators when a test fails)

1. Install **Appium Inspector** from [https://github.com/appium/appium-inspector/releases](https://github.com/appium/appium-inspector/releases).
2. Start **Appium** (step 2) **before** Inspector and keep that terminal open; start the emulator; `**adb devices`** must show your device.
3. In Inspector: **Remote host** `127.0.0.1` · **Port** `4723` · **Path** `/`.
4. Open **Desired Capabilities** (or **Capability Builder**) and switch to **JSON Representation** if the UI offers it — paste **one** of the JSON objects below (valid JSON: double quotes, trailing commas not allowed).

### JSON for Inspector — same flow as pytest (install / launch from APK)

Use this when you want Inspector to behave like `**tests/conftest.py`**: install or update from `**assist/config.py**` → `**APK_PATH**`, then open the app.

- Set `**appium:udid**` to your `**adb devices**` id.
- Set `**appium:app**` to your real APK path. On Windows, each `\` in the path must be `**\\**` inside JSON.

```json
{
  "platformName": "Android",
  "appium:automationName": "UiAutomator2",
  "appium:udid": "emulator-5554",
  "appium:app": "C:\\path\\to\\app-debug.apk",
  "appium:appPackage": "com.example.jetsnack",
  "appium:appActivity": "com.example.jetsnack.ui.MainActivity",
  "appium:newCommandTimeout": 120
}
```

### JSON for Inspector — app already on device (no reinstall)

Use this when JetSnack is already installed and you only need to attach (faster; matches “don’t wipe” style sessions).

```json
{
  "platformName": "Android",
  "appium:automationName": "UiAutomator2",
  "appium:udid": "emulator-5554",
  "appium:appPackage": "com.example.jetsnack",
  "appium:appActivity": "com.example.jetsnack.ui.MainActivity",
  "appium:noReset": true,
  "appium:newCommandTimeout": 120
}
```


| JSON key                                   | Same as in project                                                                      |
| ------------------------------------------ | --------------------------------------------------------------------------------------- |
| `appium:udid`                              | `assist/config.py` → `UDID`                                                             |
| `appium:app`                               | `assist/config.py` → `APK_PATH` (pytest path; optional in the “already installed” JSON) |
| `appium:appPackage` / `appium:appActivity` | `APP_PACKAGE` / `APP_ACTIVITY`                                                          |
| `appium:newCommandTimeout`                 | Matches `**tests/conftest.py**` (`120` seconds)                                         |


1. Click **Start Session**. Tap the screenshot or tree; copy **accessibility id**, **resource-id**, or a short **XPath** into `**assist/locators.py`**.
2. **Stop the Inspector session** before running **pytest** again (only one client should control the device).

### Inspector error: “Could not connect to Appium server URL `http://127.0.0.1:4723`”

Your JSON capabilities are usually **not** the problem when you see this — Inspector never reached a running Appium server.

1. **Start Appium in a separate window first** (`appium` or `**scripts/run_appium.cmd`**). Wait until the log shows the listener started on port **4723**, then try **Start Session** again in Inspector.
2. **Confirm the URL:** Remote host `**127.0.0.1`**, port `**4723**`, path `**/**`. Appium **2.x** uses path `**/`**; do **not** use `**/wd/hub`** unless you deliberately started the server with that legacy base path.
3. **Port in use / wrong process:** Another program may be bound to 4723. In PowerShell: `Get-NetTCPConnection -LocalPort 4723 -ErrorAction SilentlyContinue` (or `netstat -ano | findstr :4723`). Stop the other process or start Appium on another port and match it in Inspector.
4. **Inspector in the browser:** If you use the web build, start the server with CORS allowed, for example: `appium --allow-cors` (see the error text Inspector shows).
5. **Firewall / VPN:** Rare on localhost; temporarily rule out strict VPN or “block local network” toggles if `**http://127.0.0.1:4723/status`** fails in the browser from the same PC.

---

## 4) Python

```bash
cd <path-to-your-clone-of-this-repository>
python -m pip install -r requirements.txt
```

---

## 5) Run tests

1. `**adb devices**` shows one device.
2. **Appium** is running.
3. `**tests/conftest.py`** uses a **module-scoped** `driver` fixture: **one** Appium session per test **file**—tests in that file run in the same app without restarting between them; the driver quits after the last test in the module.
4. **MY CART** is not cleared in fixtures. Optional UI emptying is `**tests/test_mycart.py`** → `**test_001_clear_cart_via_remove_item**` (best effort; see that file’s header).
5. **Full suite order:** `pytest` / `pytest tests/` runs modules as **Home → Search → My Cart → Profile** (`pytest_collection_modifyitems` in `**tests/conftest.py`**). Running a **single** file is unchanged.

```bash
python -m pytest -v
```

Run one module only:

```bash
python -m pytest tests/test_home.py -v
python -m pytest tests/test_search.py -v
python -m pytest tests/test_mycart.py -v
python -m pytest tests/test_profile.py -v
```

Tests are named `**test_001**`, `**test_002**`, … inside each file; each module has a header comment with **user steps** aligned with `**doc/test_cases.md`**.

**If a test cannot find a control:** use step 3 (Inspector) with the same capabilities as `**tests/conftest.py`**, then add or adjust locators in `**assist/locators.py**`.

---

## Folder layout


| Path           | Contents                                           |
| -------------- | -------------------------------------------------- |
| `**assist/**`  | `config.py`, `helpers.py`, `locators.py`, `pages/` |
| `**doc/**`     | This file (`SETUP.md`) and `**test_cases.md**`     |
| `**tests/**`   | Pytest tests and `**conftest.py**`                 |
| `**scripts/**` | `run_appium.cmd`, `one_time_setup.ps1`             |


**APK path** in `**assist/config.py`** must match the file on your machine (same value as `**appium:app**` in the Inspector JSON when you install from APK).