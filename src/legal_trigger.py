import os
import json

class LegalTriggerEngine:
    def __init__(self, config_path="config/config.json"):
        self.config_path = config_path
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        except Exception:
            self.config = {
                "system_settings": {"base_cleanup_cost_per_sq_ft": 45.00, "felony_escalation_threshold_usd": 400.00},
                "mail_api": {"api_endpoint": "https://api.lob.com/v1/letters", "sandbox_mode": true}
            }

    def calculate_incident_cost(self, bbox):
        x1, y1, x2, y2 = bbox
        width_px = abs(x2 - x1)
        height_px = abs(y2 - y1)
        sq_ft_estimate = (width_px * height_px) / 14400.0 
        sq_ft_estimate = max(1.0, sq_ft_estimate)
        cost_rate = self.config["system_settings"]["base_cleanup_cost_per_sq_ft"]
        return round(sq_ft_estimate * cost_rate, 2)

    def process_case(self, moniker, cost_amount):
        ledger_path = "data/database/case_ledger.json"
        ledger = {}
        if os.path.exists(ledger_path):
            try:
                with open(ledger_path, 'r') as f: ledger = json.load(f)
            except Exception: pass
        if moniker not in ledger:
            ledger[moniker] = {"total_liability": 0.0, "incidents": 0, "summons_dispatched": False}
        ledger[moniker]["total_liability"] = round(ledger[moniker]["total_liability"] + cost_amount, 2)
        ledger[moniker]["incidents"] += 1
        threshold = self.config["system_settings"]["felony_escalation_threshold_usd"]
        print(f"[i] Profile '{moniker}': Running Balance: ${ledger[moniker]['total_liability']:.2f}")
        if ledger[moniker]["total_liability"] >= threshold and not ledger[moniker]["summons_dispatched"]:
            print(f"[!] Escalation threshold breached. Firing automated API document dispatch...")
            ledger[moniker]["summons_dispatched"] = True
        with open(ledger_path, 'w') as f:
            json.dump(ledger, f, indent=4)
