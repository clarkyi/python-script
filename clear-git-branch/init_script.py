import os

path = os.getcwd()
file = path + "/clear-git-branch/clear_branch.py"
os.system("sudo cp %s /usr/local/bin/clear_br.py && sudo chmod +x /usr/local/bin/clear_br.py" % file)