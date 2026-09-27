import os
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = os.getenv("bn_club_name")
SUPABASE_URL = os.getenv("bn_club_supabase_url")
SUPABASE_KEY = os.getenv("bn_club_supabase_key")
SUPABASE_TABLE = os.getenv("bn_club_supabase_table")

if not PROJECT_NAME:
    raise RuntimeError("SUPABASE_PROJECT_NAME is missing from .env")

if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL is missing from .env")

if not SUPABASE_KEY:
    raise RuntimeError("SUPABASE_KEY is missing from .env")

if not SUPABASE_TABLE:
    raise RuntimeError("SUPABASE_TABLE is missing from .env")


def ping_supabase():
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    }

    params = {
        "select": "id",
        "limit": 1,
    }

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=15,
        )

        if response.ok:
            print(
                f"[{timestamp}] {PROJECT_NAME}: OK ({response.status_code})",
                flush=True,
            )
        else:
            print(
                f"[{timestamp}] {PROJECT_NAME}: FAILED "
                f"({response.status_code})",
                flush=True,
            )
            print(response.text, flush=True)

    except requests.RequestException as e:
        print(
            f"[{timestamp}] {PROJECT_NAME}: CONNECTION ERROR - {e}",
            flush=True,
        )


if __name__ == "__main__":
    ping_supabase()