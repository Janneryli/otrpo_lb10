from flask import Flask, Response
import os
import psutil
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route("/")
def metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    disk_usage = psutil.disk_usage('/')

    metrics_data = f"""
# HELP cpu_usage_percent Использование процессора в процентах
# TYPE cpu_usage_percent gauge
cpu_usage_percent {cpu_usage}

# HELP memory_total Общий объем оперативной памяти (в байтах)
# TYPE memory_total gauge
memory_total {memory_info.total}

# HELP memory_used Используемая оперативная память (в байтах)
# TYPE memory_used gauge
memory_used {memory_info.used}

# HELP disk_total Общий объем дискового пространства (в байтах)
# TYPE disk_total gauge
disk_total {disk_usage.total}

# HELP disk_used Используемое дисковое пространство (в байтах)
# TYPE disk_used gauge
disk_used {disk_usage.used}
"""
    return Response(metrics_data, mimetype="text/plain")


if __name__ == "__main__":
    host = os.getenv("EXPORTER_HOST", "0.0.0.0")
    port = int(os.getenv("EXPORTER_PORT", 8000))
    app.run(host=host, port=port)
