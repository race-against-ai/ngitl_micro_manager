import subprocess
from time import sleep

filepath = r'C:\Users\VW2SMDW\Repos\race_against_ai\software'

file_list = ["start_live_image_broker.bat", "start_live_image_test_source.bat", "start_live_visualization.bat"]
proc_dict: (str, subprocess) = {}

delay = 3
for object in file_list:

    proc_dict[object] = subprocess.Popen(f"C:\\Users\\VW2SMDW\\Repos\\race_against_ai\\software\\{object}",
                                         cwd=r"C:\Users\VW2SMDW\Repos\race_against_ai\software",
                                         creationflags=subprocess.CREATE_NO_WINDOW,
                                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
    sleep(1)

for key in proc_dict:
    # proc_dict[key].kill()
    subprocess.call(['taskkill', '/F', '/T', '/PID', str(proc_dict[key].pid)])
