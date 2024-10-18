import subprocess
def shell(command):
    return subprocess.run(command, stdout=subprocess.PIPE)#.stdout.decode('utf-8').strip()