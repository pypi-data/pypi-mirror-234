#!/bin/sh

# Check if the pipeline is running in local mode
sagemaker_istance_type="{{ sagemaker_instance_type }}"
if [[ $sagemaker_istance_type == "local" ]]; then
    sudo systemctl status --no-pager docker.service
    export PATH=$PATH:/usr/local/bin
    echo $PATH
    
    echo "Docker compose location"
    which docker-compose
fi

eval "$(/home/{{user}}/miniconda3/bin/conda shell.bash hook)"
conda activate {{ conda_env }}

echo "Changing to working directory: {{ project_dir }}"
cd {{ project_dir }}

if [[ $sagemaker_istance_type == "local" ]]; then
    echo "Removing code zip"
    rm -rf /tmp/{{ project_name }}.zip
    
    echo "Cleaning previous docker containers"
    docker container prune -f
fi

echo "Running: {{ pipeline_run_command }}"
#continue on error so that aws instance can be stopped
{{ pipeline_run_command }} || true

# Run shutdown script after 5 minutes
# Thist gives user a chance to login to the system to check logs
# and stop the shutdown if needed
sleep 5m

echo "Stopping Instance {{ instance_id }}"
rlabs aws instance stop --instance-id {{ instance_id }} --credentials-file {{ credentials_file }}
