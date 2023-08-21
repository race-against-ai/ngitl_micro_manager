import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {

    id: task

    property var taskModel

    property bool switch_state: false

    width: parent.width
    height: width/14


    color: window.secondary_color

    border.width: 0
    radius: 20

    Rectangle {
        id: title_rectangle
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: 5

        height: parent.height
        width: parent.width/2.5

        color: "transparent"

        Text {
            Layout.maximumWidth: 400

            wrapMode: Text.Wrap
            font.pixelSize: title_rectangle.width/10

            text: taskModel.name

            color: "white"

            anchors.verticalCenter: parent.verticalCenter
        }
    }

    Rectangle{
        id: button_rectangle
        height: parent.height-parent.height/5
        width: parent.width/3

        anchors.verticalCenter: parent.verticalCenter
        anchors.left: title_rectangle.right
        anchors.leftMargin: 5

        color: "transparent"

        ButtonTemp{
            id: log_button
            width: parent.width/2
            height: parent.height/2.1

            buttonText: "Log"
            onClicked: {
                taskModel.open_log_request()
            }
        }

        ButtonTemp {

            width: parent.width/2
            height: parent.height/2.1

            buttonText: "Config"
            onClicked: taskModel.open_config_request()
            anchors.bottom: parent.bottom
        }

        Rectangle{
            height: parent.height
            width: parent.width/2
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: parent.right
            color: "transparent"

            ComboBox{
                id: log_box
                width: parent.parent.width/3
                height: parent.height/2.3
                model: ["INFO", "DEBUG"]

                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter

                background: Rectangle{
                    color: window.primary_color
                    radius:5

                }
                visible: {
                    if(window.devMode){
                        true
                    }
                    else{
                       false
                    }
                }
            }

            CheckBox{
                id: autostart_box
                height: parent.height/3
                width: height
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: log_box.right
                anchors.leftMargin: 5

                checked: false

                visible: {
                    if(window.devMode){
                        true
                    }
                    else{
                       false
                    }
                }
                onCheckedChanged: {
                    taskModel.autostart_state_request(checked)
                }
                Component.onCompleted: {
                    checked = taskModel.autostart_state
                }
            }
        }
    }

    Rectangle{
        id: switch_rectangle

        height: parent.height
        width: parent.width/6

        anchors.verticalCenter: parent.verticalCenter
        anchors.left: button_rectangle.right
        anchors.leftMargin: 5

        color:  "transparent"

        CuSwitch{
            id: run_switch

            anchors.verticalCenter: parent.verticalCenter
            anchors.horizontalCenter: parent.horizontalCenter

            width: parent.width/1.5
            height: task.heigth/2.5

            ontext: "Running"
            offtext: "Stopped"

            oncolor: window.tertiary_color

            switchOn: taskModel.switch_state


            MouseArea{
            anchors.fill: parent
            onClicked: taskModel.switch_state_request()
            }
        }
    }

    Rectangle{
        id: state_visualizer_rectangle

        anchors.verticalCenter: parent.verticalCenter
        anchors.left: switch_rectangle.right

        width: parent.width/100
        height: width
        radius: width

        anchors.leftMargin: width
        color: taskModel.state_color

    }

}
