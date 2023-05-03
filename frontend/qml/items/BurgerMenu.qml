import QtQuick 2.0
import QtQuick.Controls 2.5
import QtQuick.Layouts 1.3

Item {
    id: root
    width: parent.width
    height: parent.height

    property var settingsModel
    settingsModel: window.settingsModel

    // Burger menu button
    Rectangle {
        id: burgerButton
        color: "transparent"
        width: height * 1.5
        height: parent.height
        anchors.right: parent.right
        anchors.verticalCenter: parent.verticalCenter

        // Burger icon
        Image {
            id: logo
            source: "../../images/logo_ngitl.svg"
            anchors.fill: parent
            fillMode: Image.PreserveAspectFit
                }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                burgerRect.visible = !burgerRect.visible;
                burgerMenu.visible = !burgerMenu.visible;

            }
        }
    }

    // The Actual Burger Menu
    Rectangle{

        id: burgerRect
        visible: false
        width: window.width - 800 / 3
        height: window.height - window.height/10

        color: 'transparent'



        Menu {
            id: burgerMenu
            width: 800 / 3
            height: parent.height
            x: parent.width
            y: window.height/10
            visible: false
            spacing: 30

            background: Rectangle{

                color: window.primary_color

                height: parent.height
                width: parent.width
                border.width: 2
                border.color: window.secondary_color

            }
            Behavior on x {
                NumberAnimation {
                    duration: 250
                }
            }

            MenuItem{
                enabled: false
                height: 5
                background: Rectangle{
                    color: 'transparent'
                    anchors.fill: parent
                }
            }

            // Menu items
            BurgerButton{
                    height: 50
                    width: parent.width-6
                    buttonText: "Open Folder"

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                                settingsModel.open_folder_request()
                            }
                    }

            }


            BurgerButton{
                    height: 50
                    width: parent.width - 6
                    buttonText: "< Settings"

                    MouseArea {
                        anchors.fill: parent
                        onClicked: function(mouse) {
                            mouse.accepted = true
                            settings_menu.visible = !settings_menu.visible;
                        }
                    }

            }

            BurgerButton{
                    height: 50
                    width: parent.width - 6
                    buttonText: "Downloader"
            }


        }

        SettingsMenu{
            id: settings_menu
            visible: false
            height: parent.height
            y: window.height/10
        }

        MouseArea {
            anchors.fill: parent
            onClicked: {
                burgerMenu.visible = false;
                burgerRect.visible = false;
            }
        }
    }
}
