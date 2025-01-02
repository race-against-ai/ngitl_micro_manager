import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs

import "./settings"

Window {
    id: pj

    width: 800
    height: 400

    minimumWidth: 800
    minimumHeight: 400
    visible: true

    property string top_title: "Settings"

    color: window.primary_color
//    color: "black"

    title: "Settings"

    Rectangle{
        id: title_bar

        width: pj.width
        height: pj.height/7

        color: window.tertiary_color

        Text{
            id: title
            text: top_title
            color: window.lightFontColor
            font.pointSize: parent.height/2
            leftPadding: height/6
            wrapMode: Text.Wrap
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
        }
        Image{
            id: logo
            source: {if (!window.devMode){
                       "../../images/logo_ngitl.svg"
                                }
                    else{
                    "../../images/logo_dev_ngitl.svg"
                }

            }
            height: parent.height/1.2
            fillMode: Image.PreserveAspectFit
            anchors.right: parent.right
            anchors.rightMargin: 5
            anchors.verticalCenter: parent.verticalCenter

        }
    }

    Rectangle{
        id: pj_menu

        width: pj.width/8
        height: pj.height - title_bar.height
//        visible: true

        y: title_bar.height

        color: window.secondary_color
//        color: "grey"

        Column{
            id: button_column
            y: 5
            height: parent.height
            width: parent.width
            spacing: 5

            ButtonTemp{
                width: parent.width
                height: parent.height/10
                buttonText: "Settings"
                radius_var: 0

                onClicked:{
                    top_title = "Settings"
                    if(tasks.visible){
                        tasks.visible = false
                    }
                    settings.visible = !settings.visible
                }
            }

            ButtonTemp{
                width: parent.width
                height:parent.height/10
                buttonText: "Project Creator"
                radius_var: 0

                onClicked: {
                    top_title = "Project Creator"

                    tasks.visible = !tasks.visible

                    if(settings.visible){
                    settings.visible = false
                    }
                }
            }
        }
    }


    Rectangle{
        id: set_win

        width: pj.width-pj_menu.width
        color: window.primary_color
        height: pj_menu.height

        x: pj_menu.width
        y: title_bar.height

        SettingsTab{
            id: settings
            visible: false
            }

        CreatorTab{
            id: tasks
            visible: false
        }

    }

    Item {
        id: customDialog
        width: pj.width
        height: pj.height
        visible: task_manager_model.settings.save_dialog

        Rectangle {
            anchors.fill: parent
            color: "transparent"

            MouseArea {
                anchors.fill: parent
                onClicked: task_manager_model.settings.disable_save_dialog()
            }
        }

        Rectangle {
            width: parent.width
            height: parent.height
            color: "#80000000" // Semi-transparent darkening overlay
            border.color: "transparent"

            Rectangle {
                anchors.centerIn: parent
                width: parent.width / 3
                height: parent.height / 3
                color: window.primary_color
                border.color: window.secondary_color
                border.width: 2
                radius: 10
                clip: true

                Text {
                    text: "Saved File as: \n" + task_manager_model.settings.file_name
                    font.pixelSize: parent.height/5
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                    color: window.lightFontColor
                    anchors.centerIn: parent

                }
            }
        }
    }

}
