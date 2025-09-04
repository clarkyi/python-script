import os

path = os.getcwd()
file = path + "/clear-git-branch/git_branch_cleaner.py"
os.system("sudo cp %s /usr/local/bin/git_branch_cleaner && sudo chmod +x /usr/local/bin/git_branch_cleaner" % file)