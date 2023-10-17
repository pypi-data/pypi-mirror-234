import subprocess

# Clone the Git repository
subprocess.run(['git', 'clone', 'https://bitbucket.org/spekpy/spekpy_release.git'])

# Install the package using pip
subprocess.run(['pip', 'install', '-e', './spekpy_release'])
