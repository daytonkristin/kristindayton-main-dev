# AV-Sec Architect

**NIST RMF Compliance Dashboard for Audiovisual Infrastructure**

Automatically evaluates AV devices against NIST 800-53 controls and surfaces prioritized remediation steps.

---

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

Opens at http://localhost:8501

---

## What you can do

**Risk table** — all devices scored High / Medium / Low with RMF control mapping

**Add a device** — use the sidebar form to add any AV device by name, IP, type, and room sensitivity

**Export** — download the full risk report as CSV with one click

**Ask the assistant** — type a device name, risk level, or keyword (e.g. "camera", "high risk", "IA-5")

**Network scan** — if nmap is installed, scan your network directly from the sidebar

---

## Risk rules (NIST RMF)

| Condition | Severity | Control |
|---|---|---|
| High-sensitivity room | 🔴 High | AC-2 |
| Camera device | 🟡 Medium | IA-5 |
| Legacy/Old device | 🟡 Medium | SI-2 |
| Default | 🟢 Low | — |

---

## Optional: enable network scanning

```bash
# macOS/Linux
brew install nmap   # or: sudo apt install nmap
pip install python-nmap

# Windows
# Download nmap from https://nmap.org/download.html
pip install python-nmap
```

---

## Test

```bash
python -m pytest tests/ -v
```
