# Illustrates how to run simultaneous simulations
# pkill -f shell.py

nohup python3 pandemic/shell.py large_town geometry n 0.6 geometry i 0.6 &
nohup python3 pandemic/shell.py large_town geometry n 0.8 geometry i 0.8 &
nohup python3 pandemic/shell.py large_town geometry n 1.2 geometry i 1.2 &
nohup python3 pandemic/shell.py large_town geometry n 1.4 geometry i 1.4 &










