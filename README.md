# NGITL Micromanager


The NGITL MicroManager helps with starting and managing all of the Race-Against-AI modules.
Usage includes Component managing, so you're able to let only the components you need to run and replace existing components with your own that you're currently working on

It also includes a Project Creator in its settings window, to set up a project.

> **Note:** The build does not include a pre-made project.

## Setup environment

To set up a development environment and install all requirements, run the following commands:

windows

    python -m venv venv
    venv/Scripts/activate
    python -m pip install -r requirements.txt

unix-based systems (macOS, Linux)

    python3 -m venv venv
    source venv/bin/activate
    python3 -m pip install -r requirements.txt

## Run

    python backend/main.py

## Structure

### Basics
The Application is just a basic QML Application with python as a backend <br>
task_manager.py reads out the settings file and based on these it creates the Frontend window. <br>

While creating the Window it also connects the model file with the command:
    
    self.engine.rootContext().setContextProperty("task_manager_model", self.task_manager_model)

With that the Frontend knows where to call backend tasks.

In the model file the different types of Backend Tasks are connected in the class **TaskManagerModel**<br>
With that creating the Tasks also starts. <br>

### Task Creation
Tasks are created within the **ProjectModel** <br>
This Model is where all project specific tasks are located, including the creation of Tasks<br>

The Function responsible for task Creation is called

    handle_project_change_request(file):

the file is the project json. Every task that is inside the Json file will get read out and a new Task Object will
be created based on that<br>
the Tasks are created from the **TaskModel** which contains every Task specific function. meaning how it gets executed and 
how to open the settings/log file <br>

Running Tasks only uses **subprocess.Popen** with the CREATE_NEW_CONSOLE Flag, 
so it's easy to see if it runs. <br>
If the Tasks runs the Red Dot is also supposed to be Turning Green

Every Task is located inside `ProjectModel._task_list

### Settings
As of yet, changing the actual settings isn't available but the settings only consist on the Frontend, meaning
it's not really important.<br>
The only important thing probably is enabling Dev Mode. <br>
Dev mode only allows to control if autostart should be enabled for a specific task or not

Other than that it also changes the colour theme of the Application (Dark Material and Light NGITL are the best ones ;) )

### Project Creator
Component is just Frontend.<br>
It uses a now deprecated version of `FileDialog after you insert all the Information into it, the Info gets send over to <br>
the backend where it then gets saved as a JSON file
