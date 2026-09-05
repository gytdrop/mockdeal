# ⌨️ VantageOps Technical Keywords & Command Palette

When interacting with AI assistants (**Antigravity** or **Claude**) or operating in this repository, use these exact keywords to trigger specific workflows, persona isolation, and automated logging.

---

## 👤 Persona Activation Keywords

| Keyword Trigger | Activated Role | Assigned Module | Permitted Scope & Tasks |
| :--- | :--- | :--- | :--- |
| **`I am Akthar`** | **Akthar** (Commercial Control) | `custom_addons/vantage_governance/` | Margin governance, `action_confirm()` high-risk block, `mail.activity` chatter escalations, QWeb portal counter-offer UI, 3-round circuit breaker. **Forbidden from touching fulfillment or core.** |
| **`I am Ashrith`** | **Ashrith** (Operational Execution) | `custom_addons/vantage_fulfillment/` | `_compute_split_requirement()`, `action_split_fulfillments()` multi-warehouse auto-splitting, `margin_delta` on line items & optional products. **Forbidden from touching governance or core.** |
| **`I am Aftab`** / **`I am Afteb`** | **Aftab** (Restricted Contributor) | `mockdeal` active canvas only | **RESTRICTED: Forbidden from working in `VantageOps` and forbidden from pushing to `VantageOps`.** All work and commits must stay strictly within `mockdeal`. |

---

## 📝 Logging & Work Period Keywords

| Keyword Trigger | What It Does | Target Files Updated |
| :--- | :--- | :--- |
| **`write log`** | Commands the active agent to record the latest commit/action immediately. | Agent-specific log (`antigravity.log` or `claude.log`) + `workonmyperiod.log` |
| **`add to your period`** | Appends the current active working session, changes made, and files modified to the global timeline. | `workonmyperiod.log` |
| **`log period`** | Alias for `add to your period`. Flags a work milestone as complete. | `workonmyperiod.log` |
| **`show logs`** | Displays recent entries from all agent logs for auditing. | Terminal / Chat output |
| **`update explainer`** | Scans recent commits, code updates, and logs to synchronize and expand `EXPLAINER.md`. | `EXPLAINER.md` + `antigravity.log` / `workonmyperiod.log` |


---

## 🛑 Repository Guardrail Keywords

| Keyword Trigger | Rule Enforced | Context |
| :--- | :--- | :--- |
| **`mockdeal only`** | Confines all `git add`, `git commit`, and edits strictly to `mockdeal`. | Prevents accidental modification of production target. |
| **`freeze vantageops`** | Reminds agents that **NO AGENT IS ALLOWED TO COMMIT IN `VantageOps`**. | Final delivery destination is frozen to direct agent commits. |
| **`promote to vantageops`** | User command to safely mirror tested and verified modules from `mockdeal` canvas into `VantageOps`. | Only executed when code is 100% verified. |

---

## 🧪 Quick CLI Commands & Shortcuts

Run these directly in your terminal:

```bash
# Display this technical cheat-sheet anytime:
./keys
# or
cat KEYS.md

# Validate syntax across all Python & XML custom addons:
python3 -c "import py_compile, xml.etree.ElementTree as ET, glob; [py_compile.compile(f, doraise=True) for f in glob.glob('custom_addons/**/*.py', recursive=True)]; [ET.parse(f) for f in glob.glob('custom_addons/**/*.xml', recursive=True)]; print('✅ All Python & XML files valid!')"

# Launch local Odoo with VantageOps custom addons:
PYTHONPATH=/home/gytdrop/odoo /home/gytdrop/odoo/odoo-bin --addons-path=/home/gytdrop/odoo/addons,custom_addons -d vantage_db --dev=reload

# Inspect latest cross-agent work period log:
tail -n 30 workonmyperiod.log
```
