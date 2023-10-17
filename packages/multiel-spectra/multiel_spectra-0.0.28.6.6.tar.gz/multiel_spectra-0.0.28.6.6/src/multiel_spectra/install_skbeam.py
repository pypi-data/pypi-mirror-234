import subprocess

# Activate the conda environment
conda_env = 'base'  # Replace with your actual conda environment name
subprocess.run(['conda', 'activate', conda_env], shell=True)

# Install scikit-beam using conda
subprocess.run(['conda', 'install', '-c', 'conda-forge', 'scikit-beam'], shell=True)
