import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
dashboard_path = BASE / "charts" / "dashboard.html"
html = dashboard_path.read_text(encoding="utf-8")

data_json = (BASE / "data" / "processed" / "dashboard_data.json").read_text(encoding="utf-8")

with open(BASE / "data" / "processed" / "trend_insights.json", encoding="utf-8") as f:
    insights = json.load(f)
insights_json = json.dumps(insights)

def replace_script_block(html, script_id, new_content):
    pattern = re.compile(
        r'(<script id="' + script_id + r'" type="application/json">).*?(</script>)',
        re.DOTALL,
    )
    return pattern.sub(lambda m: m.group(1) + new_content + m.group(2), html)

html = replace_script_block(html, "dashData", data_json)
html = replace_script_block(html, "insightsData", insights_json)
html = html.replace(
    "synthetic (simulated) data for pipeline demo — swap in real data via scripts/fetch_real_data.py",
    "real historical market data via yfinance",
)

dashboard_path.write_text(html, encoding="utf-8")
print("Updated:", dashboard_path, round(dashboard_path.stat().st_size / 1024, 1), "KB")