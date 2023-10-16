#!/bin/sh

cd /home/{{ user }}

if [ -d /home/{{ user }}/miniconda3 ]; then
    echo "Miniconda already installed"
    export PATH=/home/{{ user }}/miniconda3/bin:$PATH
else
    echo "Installing Miniconda"
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    bash miniconda.sh -b -p /home/{{ user }}/miniconda3
    rm miniconda.sh
    export PATH=/home/{{ user }}/miniconda3/bin:$PATH
    conda config --set auto_activate_base false
    conda config --set show_channel_urls true
    conda init bash

    echo "Creating environment"
    conda create -n {{ conda_env }} python=3.7 -y
fi

echo "Activating environment"
eval "$(conda shell.bash hook)"
conda activate {{ conda_env }}
pip install -r /home/{{ user }}/{{ project_name }}/requirements.txt
