import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs

import "../"

Rectangle{
    property string project_title: "New Project"

    property int numRows: 1
    property int number: numRows
    property var taskNames: [ "Task 1" ]
    property var taskDelays: [0]
    property var taskAutostart: [false]
    property var taskLocation: ["Directory"]
    property var taskExecutable: ["Executable"]

    property var taskConfig: ["Config"]
    property var taskConfigLoca: ["Directory"]

    property var taskComp: [taskNames, taskDelays, taskAutostart, taskLocation, taskExecutable, taskConfigLoca, taskConfig]



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
                height: parent.height/1.5
                width: parent.width/5
                x: 5
                text: project_title
                onTextChanged: {
                    project_title = text // Update the array on text change
                }
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: project_text.right
                anchors.leftMargin: 10

            }

        }

        Rectangle{
            id: tasks_win
            height: parent.height - parent.height/10-10 - set_project_title_bar.height
            width: parent.width-10
            x: 5
            y:10 + set_project_title_bar.height

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
//                            height: tasks_win.height/10
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
                                text: taskNames[index] // Set the text from the array
                                onTextChanged: {
                                    taskNames[index] = text // Update the array on text change
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
                                text: taskDelays[index] // Set the text from the array
                                onTextChanged: {
                                    taskDelays[index] = text // Update the array on text change
                                }
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.left: task_name.right
                                anchors.leftMargin: 10

                            }
                            CusTextField{
                                id: task_executable
                                width: parent.width/8
                                height: parent.height/1.5
                                text: taskExecutable[index] // Set the text from the array
                                onTextChanged: {
                                    taskExecutable[index] = text // Update the array on text change
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
                                    fileDialog.location = taskLocation
                                    fileDialog.executable = taskExecutable

                                    fileDialog.currentIndex = index
                                    fileDialog.open()
                                }
                            }
                            CusTextField{
                                id: task_config
                                width: parent.width/8
                                height: parent.height/1.5
                                text: taskConfig[index] // Set the text from the array
                                onTextChanged: {
                                    taskConfig[index] = text // Update the array on text change
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
                                    fileDialog.location = taskConfigLoca
                                    fileDialog.executable = taskConfig

                                    fileDialog.currentIndex = index
                                    fileDialog.open()
                                }


                            }
                            Rectangle{
                                id: task_autostart
                                height:parent.height
                                width: parent.width/4
                                color: "transparent"

                                CheckBox{
                                    checked: taskAutostart[index]

                                    height: parent.height/1.5
                                    width: height
                                    onCheckedChanged: {
                                        taskAutostart[index] = !taskAutostart[index]
                                    }
                                    anchors.centerIn: parent


                                }
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.left: task_config_locator.right
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
                    taskNames.push("Task " + number)
                    taskDelays.push(0)
                    taskAutostart.push(false)
                    taskLocation.push("Directory")
                    taskExecutable.push("Executable")

                    taskConfig.push("Config")
                    taskConfigLoca.push("Directory")
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
                        var item = repeater.itemAt(numRows - 1);
                        repeater.itemAdded(numRows -1).destroy();

                        repeater.model = numRows

                        number--
                        taskNames.pop()
                        taskDelay.pop()
                        taskAutostart.pop()
                        taskLocation.pop()
                        taskExecutable.pop()
                        taskConfig.pop()
                        taskConfigLoca.pop()
                        numRows--

                }
                }

            }
        }



    FileDialog{
        property int currentIndex: 0

        property var location: []
        property var executable: []

        id: fileDialog
        title: "Choose a file"

        function reverseString(str) {
            var result = "";
            for (var i = str.length - 1; i >= 0; i--) {
                result += str.charAt(i);
            }
            return result;
        }

        onAccepted:{
            location[currentIndex] = fileDialog.selectedFile.toString();
            location[currentIndex] = location[currentIndex].substring(8);
            var reverseLocation = reverseString(location[currentIndex]);

            executable[currentIndex] = reverseString(reverseLocation.substring(0, reverseLocation.indexOf("/")));
            location[currentIndex] = location[currentIndex].replace("/" + executable[currentIndex], "")

            Qt.quit;
        }
        onRejected: {
            location[currentIndex] = "None";
            executable[currentIndex] = "no file"
            Qt.quit;
        }

    }
}
