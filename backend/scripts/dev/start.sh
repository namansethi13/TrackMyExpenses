#!/bin/sh
# Dev-only startup scripts.
# As the app grows, add new startup concerns here — one line per script.
# Each script should be non-blocking (run in background with &).

python dev_util_scripts/localhost_webhook_to_tg.py &

wait
