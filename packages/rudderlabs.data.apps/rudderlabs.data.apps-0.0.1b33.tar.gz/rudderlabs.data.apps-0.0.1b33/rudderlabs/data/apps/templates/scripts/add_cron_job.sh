#!/bin/sh

echo "Delete all cron jobs"
crontab -r

echo "Add pipeline cron job"
crontab -l | { cat; echo "@reboot sh /home/{{ user }}/run_pipeline.sh >> /home/{{ user }}/run_pipeline.log 2>&1"; } | crontab -
