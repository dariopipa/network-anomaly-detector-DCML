## Setup

Install dependencies using **uv**:

```bash
uv sync
```

Or using **pip**:

```bash
pip install -r requirements.txt
```

---

## How to Run

Open **4 terminals** and run the following commands **in order**.

### Terminal 1 — TCP Server

```bash
cd src/servers
python tcp_server.py
```

### Terminal 2 — UDP Server

```bash
cd src/servers
python udp_server.py
```

### Terminal 3 — Monitor (collects data)

```bash
cd src/monitoring
python main.py
```

### Terminal 4 — Fault Injector (runs attacks)

```bash
cd src/fault_injector
python main.py
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
