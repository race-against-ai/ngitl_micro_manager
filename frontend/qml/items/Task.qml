import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {

    id: task

    property var taskModel

    property color state_color: "red"
    property bool switch_state: false

    width: parent.width
    height: width/14

    color: window.secondary_color
    border.width: 0
    radius: 20

    RowLayout {

        anchors.fill: parent

        spacing: 10

        Rectangle {
            id: title_rectangle

            Layout.alignment: Qt.AlignVCenter

            color: 'transparent'

            height: task.height * 0.9
            width: task.width/8
            Layout.leftMargin: height/6

            Text {

                Layout.maximumWidth: 400

                wrapMode: Text.Wrap
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                font.pixelSize: parent.height/3

                text: taskModel.name
                color: window.lightFontColor
            }
        }

        Column {

            id: button_column

            Layout.alignment: Qt.AlignVCenter

            height: task.height
            width: window.width/8
            spacing: height/18

            ButtonTemp{

                width: window.width/8
                height: task.height/2.5

                buttonText: "Log"
                onClicked: {
                    taskModel.open_log_request()
                }
            }

            ButtonTemp {

                width: window.width/8
                height: task.height/2.5

                buttonText: "Config"
                onClicked: taskModel.open_config_request()
            }
        }

        CuSwitch{
            id: run_switch

            width: task.width/10
            height: task.height/2.5

            Layout.alignment: Qt.AlignVCenter
            ontext: "Running"
            offtext: "Stopped"

            oncolor: window.tertiary_color

            onSwitchOnChanged: {
                if (switchOn) {
                    switchOn = true
                    taskModel.run_exe_request()

                } else {
                    switchOn = false
                    taskModel.kill_exe_request()

                }

            }

            Component.onCompleted: {
                switchOn = switch_stage
            }

        }

        Rectangle {
            id: state_visualizer_rectangle

            Layout.alignment: Qt.AlignVCenter

            color: taskModel.state_color

            height: parent.height/8
            width: height

            radius: height

        }

    }

}
