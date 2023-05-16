""""
Copyright (C) 2023 twyleg, PhilippTrashman
"""

import subprocess
from time import sleep

filepath = r'C:\Users\VW2SMDW\Repos\race_against_ai\software'

file_list = ["start_live_image_broker.bat", "start_live_image_test_source.bat", "start_live_visualization.bat"]
proc_dict: (str, subprocess) = {}
# file_list = [r'python C:\Users\VW2SMDW\Repos\ngitl_micro_manager\backend\while_true.py']
delay = 3
for object in file_list:

    proc_dict[object] = subprocess.Popen(f"{object}",
                                         cwd=f'{filepath}',
                                         creationflags=subprocess.CREATE_NEW_CONSOLE)
    # The Bat window has been hidden, you can read the output or the errors like this
    # output, errors = p.communicate()
    # print(output.decode()) or print(error.decode())

    print(f'opened {object}')

    sleep(delay)

timer = 5
counter = timer
print("Closing in:")
for y in range(timer):
    counter -= 1
    print(f'        {counter}')
    sleep(0.5)

for key in proc_dict:
    proc_dict[key].terminate()
    # subprocess.call(['taskkill', '/F', '/T', '/PID', str(proc_dict[key].pid)])
