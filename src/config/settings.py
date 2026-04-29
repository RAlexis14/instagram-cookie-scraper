import os
from dotenv import load_dotenv

load_dotenv()

TARGET_USERNAME = os.getenv("TARGET_USERNAME")
INSTAGRAM_COOKIE = os.getenv("INSTAGRAM_COOKIE")
POST_LIMIT = int(os.getenv("POST_LIMIT", 10))

if not TARGET_USERNAME:
    raise ValueError("TARGET_USERNAME is required")

if not INSTAGRAM_COOKIE:
    raise ValueError("INSTAGRAM_COOKIE is required")