#!/usr/bin/env bash

# Overwrite the user's crontab with a clean entry
( crontab -l 2>/dev/null | grep -v 'run_' ; echo "0 */4 * * * /Users/damonholland777/Desktop/trading_bot/run_strategies_switch_and_execute.sh >> /Users/damonholland777/Desktop/trading_bot/cron_log.txt 2>&1" ) | crontab -

echo "✅ Crontab updated successfully. Your bot will run every 4 hours."
