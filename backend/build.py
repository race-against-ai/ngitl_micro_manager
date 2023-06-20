import json
import os
from pathlib import Path
import PyInstaller.__main__


def build_micromanager() -> None:
    """SHADOW WIZARD MONEY GANG! WE LOVE CASTING SPELLS"""
    work_path = Path(__file__).parent.parent
    work_path = str(work_path)
    os.chdir(work_path)
    print(f'Current Working Directory: {os.getcwd()}')

    spec_file = 'main.spec'
    # LEGALIZE NUCLEAR BOMBS

    PyInstaller.__main__.run(['--workpath', fr'{work_path}\build', '--distpath', fr'{work_path}/dist',
                              spec_file])

    # WE JUST NUKED THE WHOLE BUILDING


def build_settings():
    """
    script for building the standard RAAI settings file,
    Note the File will only work if the MicroManager is loaded as a Git Submodule for RAAI
    """
    if os.path.exists(fr'{Path(__file__).parent.parent.parent.parent}\software'):
        print("MicroManager Initialized as Submodule")
        work_path = fr'{Path(__file__).parent.parent.parent.parent}\software'
        work_path = work_path.replace("\\", "/")
        mm_path = Path(__file__).parent.parent

        settings = {
            "resolution": [800, 600],
            "theme": {
                "primary_color": "#262b33",
                "secondary_color": "#2f343f",
                "tertiary_color": "#4c5e7c"
            },
            "log_level": "INFO",
            "dev_mode": False,
            "standard_project": f"{mm_path}/dist/projects/race_against_ai.json"
        }

        project = {
            "title": "Race Against AI",
            "tasks": [
                {
                    "name": "Image Broker",
                    "executable": "live_image_broker.exe",
                    "working_directory": f"{work_path}/dist",
                    "delay": "1",
                    "config_file": "None",
                    "config_direction": "Directory",
                    "log_level": "INFO",
                    "autostart": True
                },
                {
                    "name": "Tracker Camera",
                    "executable": "start_camera_image_stream.bat",
                    "working_directory": fr"{work_path}",
                    "delay": "3",
                    "config_file": "None",
                    "config_direction": "Directory",
                    "log_level": "INFO",
                    "autostart": True
                },
                {
                    "name": "Tracker",
                    "executable": "start_tracker.bat",
                    "working_directory": fr"{work_path}",
                    "delay": "5",
                    "config_file": "None",
                    "config_direction": "Directory",
                    "log_level": "INFO",
                    "autostart": True
                },
                {
                    "name": "Timer",
                    "executable": "start_timer.bat",
                    "working_directory": fr"{work_path}",
                    "delay": "1",
                    "config_file": "None",
                    "config_direction": "Directory",
                    "log_level": "INFO",
                    "autostart": True
                },
                {
                    "name": "Live Visualization",
                    "executable": "live_visualization.exe",
                    "working_directory": fr"{work_path}/dist",
                    "delay": "5",
                    "config_file": "None",
                    "config_direction": "Directory",
                    "log_level": "INFO",
                    "autostart": True
                },
                {
                    "name": "Live Camera",
                    "executable": "start_live_camera.bat",
                    "working_directory": fr"{work_path}",
                    "delay": "1",
                    "config_file": "None",
                    "config_direction": "Directory",
                    "log_level": "INFO",
                    "autostart": True
                },
                {
                    "name": "Platform",
                    "executable": "start_dbox_platform_interface.bat",
                    "working_directory": fr"{work_path}",
                    "delay": "5",
                    "config_file": "None",
                    "config_direction": "",
                    "log_level": "INFO",
                    "autostart": True
                },
                {
                    "name": "Control Panel",
                    "executable": "control_panel.exe",
                    "working_directory": fr"{work_path}/dist",
                    "delay": "5",
                    "config_file": "config.json",
                    "config_direction": fr"{work_path}/dist",
                    "log_level": "INFO",
                    "autostart": True
                },
                {
                    "name": "Test Source",
                    "executable": "start_live_image_test_source.bat",
                    "working_directory": fr"{work_path}",
                    "delay": "0",
                    "config_file": "None",
                    "config_direction": "Directory",
                    "log_level": "INFO",
                    "autostart": False
                },
                {
                    "name": "Tracker Fallback",
                    "executable": "start_tracker_fallback.bat",
                    "working_directory": fr"{work_path}",
                    "delay": "0",
                    "config_file": "None",
                    "config_direction": "Directory",
                    "log_level": "INFO",
                    "autostart": False
                },
            ]
        }

        if not os.path.exists(f"{mm_path}\\dist"):
            os.makedirs(f"{mm_path}\\dist")

        print(work_path)

        if os.path.exists(f"{mm_path}/dist"):
            if not os.path.exists(f"{mm_path}/dist/projects"):
                os.makedirs(f"{mm_path}\\dist/projects")

            with open(f"{mm_path}/dist/settings.json", "w") as f:
                print("creating settings file")
                file = json.dumps(settings, indent=4)
                f.write(file)

            with open(f"{mm_path}/dist/projects/race_against_ai.json", "w") as f:
                print("creating RAAI project file")
                file = json.dumps(project, indent=4)
                f.write(file)

    else:
        print("---! Script only works if MicroManager is imported as a Submodule for RAAI !---")


build_micromanager()
build_settings()
