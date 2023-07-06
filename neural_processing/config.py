import os

from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.environ.get("REDIS_HOST_LOCAL")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'
QUEUE_NAME = os.environ.get("QUEUE_NAME")

KEEP_FPS = os.environ.get("KEEP_FPS")
KEEP_FRAMES = os.environ.get("KEEP_FRAMES")
ALL_FACES = os.environ.get("ALL_FACES")

MAX_MEMORY = int(os.environ.get("MAX_MEMORY"))
GPU_THREADS = int(os.environ.get("GPU_THREADS"))
GPU_VENDOR = os.environ.get("GPU_VENDOR")

CPU_CORES = int(os.environ.get("CPU_CORES"))

NUM_WORKERS = int(os.environ.get("NUM_WORKERS"))
TIMEOUT_TASK = int(os.environ.get("TIMEOUT_TASK"))

DOWNLOADS_DIR = os.environ.get("DOWNLOADS_DIR")
UPLOADS_DIR = os.environ.get("UPLOADS_DIR")
DELETE_INTERVAL = int(os.environ.get("DELETE_INTERVAL"))
