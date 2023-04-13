import json


bat_list = ["Image Broker",
            "Visualization",
            "Camera",
            "Interface",
            "Control Panel",
            "Test Source",
            ]

tasks = []
for item in bat_list:
    setter = {"name": item,
              "enabled": False,
              "executable": "not implemented",
              "delay": 5,
              "working_directory": "not implemented",
              "config_file": "Insert Directory",
              "log_level": 'INFO'}

    tasks.append(setter)

j_dict = {"tasks": tasks}

file = json.dumps(j_dict,
                  indent=4)

with open("settings.json", 'w') as f:
    f.write(file)

with open('settings.json', 'r') as f:
    file = json.load(f)
    tasks = file["tasks"]
    for entry in tasks:
        print(entry["name"])
