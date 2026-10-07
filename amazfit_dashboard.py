import json
from pathlib import Path
from datetime import datetime

def generate_html():
    history_file = Path(__file__).parent / "history.json"
    html_file = Path(__file__).parent / "dashboard.html"
    
    data = []
    if history_file.exists():
        with open(history_file, "r") as f:
            try:
                data = json.load(f)
            except:
                data = []

    # Format labels to show clean dates (e.g., "Oct 07")
    labels = []
    for entry in data:
        dt = datetime.strptime(entry["timestamp"].split(" ")[0], "%Y-%m-%d")
        labels.append(dt.strftime("%b %d"))

    steps = [entry["steps"] for entry in data]
    battery = [entry["battery"] for entry in data]
    calories = [entry["calories"] for entry in data]

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Amazfit GTR Daily Summary</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            background-color: #121212;
            color: #e0e0e0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 900px;
            margin: auto;
        }}
        h1 {{
            text-align: center;
            color: #00adb5;
        }}
        .card {{
            background: #1e1e1e;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        }}
        canvas {{
            width: 100% !important;
            height: 300px !important;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Amazfit GTR Daily Progress</h1>
        
        <div class="card">
            <h3>Daily Steps (Latest Reading per Day)</h3>
            <canvas id="stepsChart"></canvas>
        </div>
        
        <div class="card">
            <h3>Battery & Calories</h3>
            <canvas id="metricsChart"></canvas>
        </div>
    </div>

    <script>
        const labels = {json.dumps(labels)};
        const steps = {json.dumps(steps)};
        const battery = {json.dumps(battery)};
        const calories = {json.dumps(calories)};

        new Chart(document.getElementById('stepsChart'), {{
            type: 'bar',
            data: {{
                labels: labels,
                datasets: [{{
                    label: 'Steps',
                    data: steps,
                    backgroundColor: 'rgba(0, 173, 181, 0.6)',
                    borderColor: '#00adb5',
                    borderWidth: 1
                }}]
            }},
            options: {{ responsive: true, maintainAspectRatio: false }}
        }});

        new Chart(document.getElementById('metricsChart'), {{
            type: 'line',
            data: {{
                labels: labels,
                datasets: [
                    {{
                        label: 'Battery (%)',
                        data: battery,
                        borderColor: '#ff5722',
                        backgroundColor: 'rgba(255, 87, 34, 0.1)',
                        yAxisID: 'y',
                        tension: 0.2
                    }},
                    {{
                        label: 'Calories (kcal)',
                        data: calories,
                        borderColor: '#4caf50',
                        backgroundColor: 'rgba(76, 175, 80, 0.1)',
                        yAxisID: 'y1',
                        tension: 0.2
                    }}
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                scales: {{
                    y: {{ type: 'linear', position: 'left', title: {{ display: true, text: 'Battery %' }} }},
                    y1: {{ type: 'linear', position: 'right', grid: {{ drawOnChartArea: false }}, title: {{ display: true, text: 'Calories' }} }}
                }}
            }}
        }});
    </script>
</body>
</html>
"""

    with open(html_file, "w") as f:
        f.write(html_content)
    
    print(f"Dashboard updated at: {html_file}")

if __name__ == "__main__":
    generate_html()
