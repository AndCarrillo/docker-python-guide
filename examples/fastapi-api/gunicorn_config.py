# Gunicorn configuration for production deployment
# This file demonstrates production-ready WSGI server configuration

import multiprocessing
import os

# Server socket
bind = f"0.0.0.0:{os.getenv('PORT', 8000)}"
backlog = 2048

# Worker processes
workers = min(multiprocessing.cpu_count() * 2 + 1, 8)  # Cap at 8 workers
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100

# Performance settings
preload_app = True
worker_tmp_dir = "/dev/shm"  # Use memory for worker temp files
keepalive = 5

# Timeout settings
timeout = 30
graceful_timeout = 30
worker_timeout = 30

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = os.getenv("LOG_LEVEL", "info")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "fastapi-app"

# Server mechanics
daemon = False
pidfile = None
user = None
group = None
tmp_upload_dir = None

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Development settings (only if DEBUG is set)
if os.getenv("DEBUG", "false").lower() == "true":
    reload = True
    workers = 1
    loglevel = "debug"
else:
    reload = False
