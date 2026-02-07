## Setup

### Using uv (recommended)

With **uv**, the virtual environment is created automatically:

```bash
uv sync
```

No need to manually create or activate the venv `uv sync` does this automatically.

### Using pip

If using **pip**, you need to create and activate a virtual environment first:

**1. Create the virtual environment:**

```bash
python -m venv venv
```

**2. Activate the virtual environment:**

- **Windows (Command Prompt):**

  ```bash
  venv\Scripts\activate
  ```

- **Windows (PowerShell):**

  ```bash
  venv\Scripts\Activate.ps1
  ```

- **Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```

**3. Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## How to Run

Open **4 terminals** and run the following commands **in order** from the project root.

### Terminal 1 — TCP Server

```bash
python -m src.servers.tcp_server
```

### Terminal 2 — UDP Server

```bash
python -m src.servers.udp_server
```

### Terminal 3 — Monitor (collects data)

```bash
python -m src.monitoring.main
```

### Terminal 4 — Fault Injector (runs attacks)

```bash
python -m src.fault_injector.main
```

## Configuration

Edit:

```text
src/server_config.py
```

To change IPs and ports.

### Local testing (default)

- Uses `127.0.0.1`

### Two-computer setup

- Set `MONITOR_IP` to the victim PC IP
- Set `INJECTOR_IP` to the attacker PC IP
- Run **Terminals 1–3** on the monitor PC
- Run **Terminal 4** on the injector PC
