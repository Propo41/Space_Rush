import os

# this file fetches the current directory of the game folder and automatically runs the game

dir_path = os.getcwd()
# print("current directory is : " + dir_path)
print("initializing game...")
run_file = dir_path + "\\start.py"
os.system('python ' + run_file)
