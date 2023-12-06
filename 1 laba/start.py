import subprocess

script_paths = ["1 laba\TG_and_VK.py", "1 laba\\analyzer.py"]

for script in script_paths:
    subprocess.run(["python", script])
