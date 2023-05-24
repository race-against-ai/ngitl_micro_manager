import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle{

    width:parent.width
    height: width/25
    color:window.secondary_color

    border.color: window.primary_color
    border.width: 1

    Rectangle{
        id: task_name
        width: parent.width/8
        height: parent.height
        Text {
            id: name_tag
            text: qsTr("Task Name")
            color: window.lightFontColor
            anchors.centerIn: parent
        }
        color:"transparent"

        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: 10
    }
    Rectangle{
        id: task_delay
        height:parent.height
        width: parent.width/8
        Text {
            id: delay_tag
            text: qsTr("Start Delay")
            color: window.lightFontColor
            anchors.centerIn: parent
        }
        color:"transparent"
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: task_name.right
        anchors.leftMargin: 10

    }
    Rectangle{
        id: task_executable
        height:parent.height
        width: parent.width/8 + parent.height/1.5 + 5
        Text {
            id: exe_tag
            text: qsTr("File Path")
            color: window.lightFontColor
            anchors.centerIn: parent
        }
        color:"transparent"
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: task_delay.right
        anchors.leftMargin: 10
    }
    Rectangle{
        id: task_config
        height: task_executable.height
        width: task_executable.width
        Text{
            id: config_tag
            text: qsTr("Config File")
            color: window.lightFontColor
            anchors.centerIn: parent
        }
        color:"transparent"
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: task_executable.right
        anchors.leftMargin: 10
    }

    Rectangle{
        id: task_loglevel
        height: parent.height
        width:parent.width/10
        Text{
            id: log_tag
            text: qsTr("Log Level")
            color: window.lightFontColor
            anchors.centerIn: parent
        }
        color: "transparent"
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: task_config.right
        anchors.leftMargin: 10
    }

    Rectangle{
        id: task_autostart
        height:parent.height
        width: parent.width/6
        Text {
            id: autostart_tag
            text: qsTr("Autostart")
            color: window.lightFontColor
            anchors.centerIn: parent
        }
        color:"transparent"
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: task_loglevel.right
        anchors.leftMargin: 10
    }
}
