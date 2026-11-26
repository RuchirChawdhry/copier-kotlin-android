"""Collect available measurements without inventing missing results."""
import html
import json
import pathlib
import re
import shutil

ROOT = pathlib.Path("reports/performance")
ROOT.mkdir(parents=True, exist_ok=True)
metrics = {}
apk = ROOT / "apk-size.txt"
if apk.exists():
    for line in apk.read_text().splitlines():
        match = re.fullmatch(r"(.+) (\d+) bytes", line)
        if match:
            metrics[f"apk_bytes/{match[1]}"] = int(match[2])
memory = ROOT / "memory.txt"
if memory.exists():
    match = re.search(r"TOTAL PSS:\s*(\d+)", memory.read_text())
    if match:
        metrics["memory_pss_kib"] = int(match[1])
frames = ROOT / "frames.txt"
if frames.exists():
    for key, pattern in {
        "frames_total": r"Total frames rendered:\s*(\d+)",
        "frames_janky": r"Janky frames:\s*(\d+)",
    }.items():
        match = re.search(pattern, frames.read_text())
        if match:
            metrics[key] = int(match[1])
benchmarks = []
for path in pathlib.Path("benchmark/build/outputs").rglob("*benchmarkData.json"):
    data = json.loads(path.read_text())
    benchmarks.append({"source": str(path), "data": data})
    for benchmark in data.get("benchmarks", []):
        for name, values in benchmark.get("metrics", {}).items():
            median = values.get("median")
            if isinstance(median, (int, float)):
                metrics[f"{benchmark.get('name', 'benchmark')}/{name}/median"] = median
traces = ROOT / "traces"
for path in pathlib.Path("benchmark/build/outputs").rglob("*.perfetto-trace"):
    traces.mkdir(exist_ok=True)
    shutil.copy2(path, traces / path.name)
current = {"metrics": metrics, "benchmark_results": benchmarks}
(ROOT / "current.json").write_text(json.dumps(current, indent=2) + "\n")
baseline = ROOT / "baseline.json"
prior = json.loads(baseline.read_text()).get("metrics", {}) if baseline.exists() else {}
comparison = {
    key: {"baseline": prior[key], "current": value, "delta": value - prior[key]}
    for key, value in metrics.items() if key in prior
}
(ROOT / "comparison.json").write_text(json.dumps(comparison, indent=2) + "\n")
rows = "".join(
    f"<tr><td>{html.escape(key)}</td><td>{value}</td><td>{comparison.get(key, {}).get('delta', '—')}</td></tr>"
    for key, value in sorted(metrics.items())
)
(ROOT / "index.html").write_text(
    '<!doctype html><html lang="en"><meta charset="utf-8"><title>Performance</title>'
    '<style>body{font:16px system-ui;max-width:900px;margin:40px auto;padding:0 20px}'
    'table{border-collapse:collapse;width:100%}td,th{padding:10px;border-bottom:1px solid #aaa}</style>'
    '<h1>Android performance</h1><p>Only collected metrics appear. Compare equivalent devices and workloads.</p>'
    '<table><tr><th>Metric</th><th>Current</th><th>Change from baseline</th></tr>'
    + rows + '</table></html>'
)
print(ROOT / "index.html")
