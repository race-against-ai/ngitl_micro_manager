import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs

import "../"

Rectangle{
    property string project_title: "New Project"

    property int numRows: 1
    property int number: numRows

    property var task_dict: [{
            "name" : "Task 1",
            "executable" : "None",
            "working_directory" : "Directory",
            "delay" : 0,
            "config_file" : "None",
            "config_dir" : "Directory",
            "log_level" : "INFO",
            "autostart" : false,
        }]



    id: tasks
    width: parent.width
    height: parent.height

    color: "transparent"

    Rectangle{
        id: set_project_title_bar
        width: parent.width - 10
        height: width/20
        color: window.secondary_color
        x: 5
        y: 5
        border.color: window.primary_color
        border.width: 1

        Rectangle{
            id:project_text
            width: parent.width/8
            height: parent.height
            color:"transparent"
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            enabled: false

            Text{
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                text: "Title:"
                font.pointSize: parent.height/2
                leftPadding: height/6
                color: window.lightFontColor

            }
        }
        CusTextField{
            id: title_textfield
            height: parent.height/1.5
            width: parent.width/5
            text: ""
            onTextChanged: {
                project_title = text // Update the array on text change
            }
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: project_text.right
            anchors.leftMargin: 10

            enabled: false

            }
        ButtonTemp{
            height: parent.height/1.5
            width: parent.width/5
            anchors.right: parent.right
            anchors.rightMargin: 10
            anchors.verticalCenter: parent.verticalCenter
            buttonText: "Create New Project"

            onClicked: {
                project_title: "New Project"
                title_textfield.enabled = true
                title_textfield.text = project_title

                task_dict = [{
                    "name" : "Task 1",
                    "executable" : "None",
                    "working_directory" : "Directory",
                    "delay" : 0,
                    "config_file" : "None",
                    "config_dir" : "Directory",
                    "log_level" : "INFO",
                    "autostart" : false,
                }]

                numRows = 1
                number = numRows
                tasks_win.visible = true
                save_but.enabled = true

            }

        }
    }

    Rectangle{
        id: tasks_win
        height: parent.height - parent.height/10-10 - set_project_title_bar.height
        width: parent.width-10
        x: 5
        y:10 + set_project_title_bar.height

        visible: false

        color:window.primary_color
//                color:"green"

        ScrollView {
            id:scrollView
            anchors.fill: parent
            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff // Disable horizontal scrollbar

            ScrollBar.vertical: ScrollBar{
                id: scrollBar

                hoverEnabled: true
                policy: ScrollBar.AsNeeded
                width: 1

                parent: scrollView.parent
                x: scrollView.mirrored ? 0 : scrollView.width - width

                height: scrollView.availableHeight


                background: Rectangle {
                    color: tertiary_color // Change the color of the track

                    }
             }

            Column{
                anchors.fill: parent

                CreatorDescriptor{
                    width: tasks_win.width
                }

                Repeater{
                    id: repeater
                    model: numRows
                    delegate: Rectangle{
                        width: tasks_win.width
                        height:tasks_win.height/10
                        color:window.secondary_color
                        border.color: window.primary_color
                        border.width:1
//                                color:"purple"

                        CusTextField{
                            id: task_name
                            width: parent.width/8
                            height: parent.height/1.5
//                                text: taskNames[index] // Set the text from the array
                            text: task_dict[index]["name"]
                            onTextChanged: {
//                                    taskNames[index] = text // Update the array on text change
                                task_dict[index]["name"] = text
                            }
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.left: parent.left
                            anchors.leftMargin: 10

                        }
                        CusTextField{
                            id: task_delay
                            validator: IntValidator{
                                bottom: 0
                            }
                            inputMethodHints: Qt.ImhDigitsOnly
                            width: parent.width/8
                            height: parent.height/1.5
                            text: task_dict[index]["delay"] // Set the text from the array
                            onTextChanged: {
                                task_dict[index]["delay"] = text // Update the array on text change
                            }
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.left: task_name.right
                            anchors.leftMargin: 10

                        }
                        CusTextField{
                            id: task_executable
                            width: parent.width/8
                            height: parent.height/1.5
                            text: task_dict[index]["executable"] // Set the text from the array
                            onTextChanged: {
                                task_dict[index]["executable"] = text // Update the array on text change
                            }
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.left: task_delay.right
                            anchors.leftMargin: 10

                        }
                        Button{
                            id: task_executable_locator
                            height:parent.height/1.5
                            width: height
                            text: "..."
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.left: task_executable.right
                            anchors.leftMargin: 5

                            onClicked: {
//                                        task_manager_model.settings.file_path_request(index)
//                                    fileDialog.location = taskLocation
//                                    fileDialog.executable = task_dict

                                fileDialog.location = "working_directory"
                                fileDialog.executable = "executable"
                                fileDialog.filetype = ["Executables (*.exe)", "bat files (*.bat)"]
                                fileDialog.title = "Choose an Exe or Bat File"

                                fileDialog.currentIndex = index
                                fileDialog.open()

                                task_executable.text = task_dict[index]["executable"]
                            }
                        }
                        CusTextField{
                            id: task_config
                            width: parent.width/8
                            height: parent.height/1.5
                            text: task_dict[index]["config_file"] // Set the text from the array
                            onTextChanged: {
                                task_dict[index]["config_file"] = text // Update the array on text change
                            }
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.left: task_executable_locator.right
                            anchors.leftMargin: 10

                        }
                        Button{
                            id: task_config_locator
                            height:parent.height/1.5
                            width: height
                            text: "..."
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.left: task_config.right
                            anchors.leftMargin: 5

                            onClicked: {
                                //                                        task_manager_model.settings.file_path_request(index)
//                                    fileDialog.location = taskConfigLoca
//                                    fileDialog.executable = taskConfig

                                fileDialog.location = "config_dir"
                                fileDialog.executable = "config_file"
                                fileDialog.filetype = ["Text Files (*.txt)"]
                                fileDialog.title = "Choose a Config File"

                                fileDialog.currentIndex = index
                                fileDialog.open()
                            }


                        }

                        Rectangle{
                            id: log_box
                            height: parent.height/1.2
                            width: parent.width/10
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.left: task_config_locator.right
                            anchors.leftMargin: 10
                            color: "transparent"

                            ComboBox{
                                width: parent.width
                                height: parent.height
                                currentIndex: 0

                                model: ["INFO", "DEBUG"]

                                anchors.verticalCenter: parent.verticalCenter
                                anchors.horizontalCenter: parent.horizontalCenter

                                delegate: {
                                    width: parent.width
                                    contentItem:Text
                                        color: window.lightFontColor


                                }
                                background: Rectangle{
                                    color: window.primary_color
                                    radius:5
                                    }

                                onCurrentIndexChanged: {
                                    if(currentIndex === 0){
                                        task_dict[index]["log_level"] = "INFO"
                                    }
                                    else{
                                        task_dict[index]["log_level"] = "DEBUG"
                                    }
                                }

                                }
                            }


                        Rectangle{
                            id: task_autostart
                            height:parent.height
                            width: parent.width/6
                            color: "transparent"

                            CheckBox{
                                checked: task_dict[index]["autostart"]

                                height: parent.height/1.5
                                width: height
                                onCheckedChanged: {
                                    task_dict[index]["autostart"] = checked
                                }
                                anchors.centerIn: parent


                            }
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.left: log_box.right
                        anchors.leftMargin: 10
                        }


                    }
                }
            }
            }
    }

    Rectangle{
        id: tasks_commands
        width: parent.width
        height: parent.height/10

//                color: "yellow"
        color: window.secondary_color

        anchors.bottom: parent.bottom


        ButtonTemp{
            id: save_but
            width: parent.width/8
            height: parent.height/1.5
            buttonText: "Save Project"
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: parent.right
            enabled: false
            onClicked:{
                var stringArg = "Hello"
                var listArg = [1,2,3]
                task_manager_model.settings.create_json_request(stringArg, [{"title": project_title},{"tasks": task_dict}], project_title)
            }

        }
        ButtonTemp{
            id: add_button
            width: parent.width/8
            height: parent.height/1.5
            //                    color: "green"
            buttonText: "Add Task"
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: save_but.left
            anchors.rightMargin: 10
            onClicked:{
                number++
                task_dict.push({
                                   "name" : "Task " + number,
                                   "executable" : "None",
                                   "working_directory" : "Directory",
                                   "delay" : 0,
                                   "config_file" : "None",
                                   "config_dir" : "None",
                                   "log_level" : "INFO",
                                   "autostart" : false,
                               })
                numRows++
            } // Add a new task name to the array

        }
        ButtonTemp{
            width: add_button.width
            height: add_button.height

            buttonText: "Remove Task"
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: add_button.left
            anchors.rightMargin: 10

            onClicked:{
                if(numRows > 1){

                    number--
                    task_dict.pop()
                    numRows--

                    var item = repeater.itemAt(numRows - 1);
                    repeater.itemAdded(numRows -1).destroy();

                    repeater.model = numRows
              }
            }

        }
    }


    FileDialog{
        property int currentIndex: 0

        property string location: ""
        property string executable: ""

        property var filetype: []

        id: fileDialog
        title: "Choose a file"

        function reverseString(str) {
            var result = "";
            for (var i = str.length - 1; i >= 0; i--) {
                result += str.charAt(i);
            }
            return result;
        }

        nameFilters: filetype

        onAccepted:{
            task_dict[currentIndex][location] = fileDialog.selectedFile.toString().substring(8);
//            task_dict[currentIndex][location] = task_dict[currentIndex][location].substring(8);
            var reverseLocation = reverseString(task_dict[currentIndex][location]);

            task_dict[currentIndex][executable] = reverseString(reverseLocation.substring(0, reverseLocation.indexOf("/")));

            task_dict[currentIndex][location] = task_dict[currentIndex][location].replace("/" + task_dict[currentIndex][executable], "");

            // Refreshes the Repeater to show the change :/
            numRows++
            numRows--

            Qt.quit;
        }
        onRejected: {
            Qt.quit;
        }

    }
}
