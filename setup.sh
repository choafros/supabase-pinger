#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON="$SCRIPT_DIR/.venv/bin/python"
CRON_CMD="* * * * * cd $SCRIPT_DIR && $PYTHON pinger.py >> $SCRIPT_DIR/keeper.log 2>&1"

echo "================================="
echo " Supabase Keeper Setup"
echo "================================="

cd "$SCRIPT_DIR"

echo ""
echo "1. Creating Python virtual environment..."

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

echo "2. Installing dependencies..."

"$SCRIPT_DIR/.venv/bin/pip" install -r requirements.txt

echo ""
echo "3. Checking Python script..."

"$PYTHON" pinger.py

echo ""
echo "4. Installing cron job..."

# Remove previous Supabase Keeper cron entries
(crontab -l 2>/dev/null || true) | grep -v "$SCRIPT_DIR/pinger.py" | crontab -

# Add new job
(crontab -l 2>/dev/null || true; echo "$CRON_CMD") | crontab -

echo ""
echo "================================="
echo " Setup complete!"
echo "================================="
echo ""
echo "Cron job:"
echo "$CRON_CMD"
echo ""
echo "Current crontab:"
crontab -l
echo ""
echo "Log:"
echo "$SCRIPT_DIR/keeper.log"