import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {

    id: task

    property var taskModel

    width: 800
    height: 64

    color: "black"
    border.width: 0
    radius: 20

    RowLayout {

        anchors.fill: parent

        spacing: 10

        Text {

            Layout.alignment: Qt.AlignVCenter
            Layout.maximumWidth: 400

            text: taskModel.name
            color: "white"

            Layout.margins: 20
        }

        Column {

            Layout.alignment: Qt.AlignVCenter

            Button {
                text: "Log"

                onClicked: taskModel.open_log_request()
            }

            Button {
                text: "Config"
                onClicked: taskModel.open_config_request()
            }
        }

        Switch {

            width: parent.width * 0.2
            height: parent.height

            Layout.alignment: Qt.AlignVCenter
            text: visualPosition == 1.0 ? "Running" : "Stopped"

        }

        Rectangle {
            id: state_visualizer_rectangle

            Layout.alignment: Qt.AlignVCenter

            color: "red"

            height: parent.height * 0.9
            width: height
        }

    }

}
