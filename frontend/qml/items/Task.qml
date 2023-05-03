import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {

    id: task

    property var taskModel

//    width: parent.width
    width: burgerMenu.visible ? (parent.width - burgerMenu.width) : taskWidth
    height: parent.height

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
//            color: 'blue'

            height: parent.height * 0.9
            width: parent.width/8
            Layout.leftMargin: height/6

//            radius: height/3

            Text {

//                Layout.alignment: Qt.AlignVCenter
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

            Layout.alignment: Qt.AlignVCenter

            height: parent.parent.parent.height
            width: parent.parent.width/16
            spacing: parent.parent.height/18

            Button {
                id: log_button
                text: "Log"
                Layout.fillHeight: true
                background: Rectangle{
                    color: window.tertiary_color
                    width: parent.parent.width
                    height: parent.parent.height/2.5
                    radius: 3


                }

                onClicked: {
                    taskModel.open_log_request()
                }
            }

            Button {
                id: config_button
                text: "Config"
                Layout.fillHeight: true
                background: Rectangle{
                    color: window.tertiary_color
                    width: parent.parent.width
                    height: parent.parent.height/2.5
                    radius: 3

                }

                onClicked: taskModel.open_config_request()
            }
        }

//        Switch {

//            width: parent.width * 0.2
//            height: parent.parent.parent.height/10

//            Layout.alignment: Qt.AlignVCenter
//            text: visualPosition == 1.0 ? "Running" : "Stopped"

//            onClicked: {
//                if (visualPosition == 1.0){
//                    taskModel.run_exe_request()
//                    state_visualizer_rectangle.color = 'green'
//                }
//                if (visualPosition == 0.0){
//                    taskModel.close_exe_request()
//                    state_visualizer_rectangle.color = 'red'
//                }
//            }

//        }

        CuSwitch{
            id: run_switch

            width: parent.width/10
            height: parent.parent.height/2.5

            Layout.alignment: Qt.AlignVCenter
            ontext: "Running"
            offtext: "Stopped"


            oncolor: window.tertiary_color

            MouseArea{
                anchors.fill: parent
                onClicked: {
                                run_switch.switchOn = !run_switch.switchOn

                                if (run_switch.switchOn){
                                    taskModel.run_exe_request()
                                    state_visualizer_rectangle.color = 'green'
                                }
                                if (!run_switch.switchOn){
                                    taskModel.close_exe_request()
                                    state_visualizer_rectangle.color = 'red'
                                }
                            }
            }

        }

        Rectangle {
            id: state_visualizer_rectangle

            Layout.alignment: Qt.AlignVCenter

            color: "red"

            height: parent.height/8
            width: height

            radius: height

//            Text {
//                id: status
//                text: qsTr("Closed")
////                font.pointSize: Math.min(width * 0.5, height * 0.5)
//                wrapMode:  Text.Wrap
//                textFormat:  Text.PlainText
//                anchors.centerIn: parent
//            }
        }

    }

}
