import json
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
template_path = BASE / "scripts" / "dashboard_template.html"
template = template_path.read_text(encoding="utf-8")

data_json = (BASE / "data" / "processed" / "dashboard_data.json").read_text(encoding="utf-8")

with open(BASE / "data" / "processed" / "trend_insights.json", encoding="utf-8") as f:
    insights = json.load(f)
insights_json = json.dumps(insights)

note = "real historical market data via yfinance"

html = template.replace("__DATA_JSON__", data_json)
html = html.replace("__INSIGHTS_JSON__", insights_json)
html = html.replace("__DATA_SOURCE_NOTE__", note)

out_path = BASE / "charts" / "dashboard.html"
out_path.write_text(html, encoding="utf-8")
print("Written:", out_path, round(out_path.stat().st_size / 1024, 1), "KB")