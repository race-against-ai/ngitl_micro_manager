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
                buttonText: "   Open Folder"

                MouseArea {
                    anchors.fill: parent
                    onClicked: function(mouse) {
                            mouse.accepted = true
                            task_manager_model.settings.open_folder_request()
                        }
                }

            }

            BurgerButton{
                height: 50
                width: parent.width-6
                buttonText: "   Settings"

                MouseArea{
                    anchors.fill: parent
                    onClicked: function(mouse) {
                        var component = Qt.createComponent("SettingsWin.qml");
                        var newWindow = component.createObject(window);
                        newWindow.show();
                    }
                }
            }


            BurgerButton{
                height: 50
                width: parent.width - 6
                buttonText: "   Downloader"

                MouseArea {
                    anchors.fill: parent
                    onClicked: function(mouse) {
                        mouse.accepted = true
                        task_manager_model.project.download_request()
                    }
                }
            }


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
