import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Dialogs

import "../"

Rectangle{
    id: main_window
    height: parent.height
    width: parent.width

    color: window.primary_color

    Rectangle{
        id: height_menu
        anchors.top: parent.top
        anchors.topMargin: 5
        anchors.right: parent.right
        anchors.rightMargin: 5
        color: window.secondary_color

        width: parent.width-10
        height: parent.height/7

        Text{
            text: "Resolution"
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 5
            color: window.lightFontColor

            font.pointSize: main_window.height/20
            wrapMode: Text.Wrap
        }
    }

    Rectangle{
        id: log_menu
        anchors.top: height_menu.bottom
        anchors.topMargin: 5
        anchors.right: parent.right
        anchors.rightMargin: 5
        color: window.secondary_color

        width: parent.width-10
        height: parent.height/7

        Text{
            text: "Log Level"
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 5
            color: window.lightFontColor

            font.pointSize: main_window.height/20
            wrapMode: Text.Wrap
        }
    }

    Rectangle{
        id: dev_menu
        anchors.top: log_menu.bottom
        anchors.topMargin: 5
        anchors.right: parent.right
        anchors.rightMargin: 5
        color: window.secondary_color

        width: parent.width-10
        height: parent.height/7

        Text{
            text: "Dev Mode"
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 5
            color: window.lightFontColor

            font.pointSize: main_window.height/20
            wrapMode: Text.Wrap

        }
        CheckBox{
            checked: window.devMode

            height: parent.height/1.5
            width: height
            onCheckedChanged: {
                window.devMode = !window.devMode
            }
            anchors.centerIn: parent


        }
    }

    Rectangle{
        id: theme_menu
        width: parent.width-10
        height: parent.height/3 - 5

        border.width: 1
        border.color: window.primary_color
        anchors.top: dev_menu.bottom
        anchors.topMargin: 5
        anchors.left: parent.left
        anchors.leftMargin: 5

        color: window.secondary_color

        Text{

            text: "Theme"
//            anchors.verticalCenter: parent.verticalCenter
            anchors.top: parent.top
            anchors.topMargin: 5
            anchors.left: parent.left
            anchors.leftMargin: 5
            color: window.lightFontColor

            font.pointSize: main_window.height/20
            wrapMode: Text.Wrap

        }

        Rectangle{
            id: theme_buttons
            width: parent.width/3*2
            height: parent.height - 10
            color: "transparent"
            anchors.right: parent.right
            anchors.rightMargin: 5
            anchors.verticalCenter: parent.verticalCenter
            ColorButton{
                id: dark_material
                primary: '#262b33'
                secondary: '#2f343f'
                tertiary: '#4c5e7c'
                onClicked: {
                    changeTheme(primary, secondary, tertiary)
                }
            }

            ColorButton{
                id: light_material
                anchors.left: dark_material.right
                theme_name: "RAAI"
                primary: "#e1e8f5"
                secondary: "#9bbefa"
                tertiary: "#274c87"
                onClicked: {
                    changeTheme(primary, secondary, tertiary)
                }

            }

            ColorButton{
                id: dark_mate
                anchors.top: dark_material.bottom
                theme_name: "Dark Mate"
                primary: "#3d2d15"
                secondary:"#59411a"
                tertiary: "#d79f43"
                onClicked: {
                    changeTheme(primary, secondary, tertiary)
                }
            }

            ColorButton{
                id: light_mate
                anchors.left: dark_mate.right
                anchors.top: dark_material.bottom
                theme_name: "Light Mate"
                primary: "#edd4b6"
                secondary:"#d5ab70"
                tertiary: "#b88428"
                onClicked: {
                    changeTheme(primary, secondary, tertiary)
                }
            }

            ColorButton{
                id: dark_ngitl
                anchors.top: dark_mate.bottom
                theme_name: "Dark NGITL"
                primary: "#192a2a"
                secondary:"#2a4646"
                tertiary: "#3b6363"
                onClicked: {
                    changeTheme(primary, secondary, tertiary)
                }
            }

            ColorButton{
                id: light_ngitl
                anchors.left: dark_ngitl.right
                anchors.top: dark_mate.bottom
                theme_name: "Light NGITL"
                primary: "#99b5b5"
                secondary:"#668e8e"
                tertiary: "#809999"

                onClicked: {
                    changeTheme(primary, secondary, tertiary)
                }
            }


        }

    }


    Rectangle{
        id: buttons
        width: parent.width
        height: parent.height/10

        color: window.secondary_color

        anchors.bottom: parent.bottom


        ButtonTemp{
            id: save_but
            width: parent.width/8
            height: parent.height/1.5
            buttonText: "Save Settings"
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: parent.right

        }
        ButtonTemp{
            id: add_button
            width: parent.width/8
            height: parent.height/1.5
            buttonText: "Reset Settings"
            anchors.verticalCenter: parent.verticalCenter
            anchors.right: save_but.left
            anchors.rightMargin: 10
            onClicked:{
            }
        }
    }
    function changeTheme(primary, secondary, tertiary){
        window.primary_color = primary
        window.secondary_color = secondary
        window.tertiary_color = tertiary
    }

}
