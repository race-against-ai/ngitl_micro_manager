import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle{
    id: title_bar

    width: parent.width
    height: parent.height

    color: window.tertiary_color

    BurgerMenu{
        width: parent.width
        height: parent.height
        settingsModel: task_manager_model.settings
    }

    Rectangle{
        id: upper_part
        width: parent.width - parent.height/6
        color: 'transparent'
        anchors.left: parent.left
        height: parent.height

        Text {
            id: title
            text: window.titleText
            color: window.lightFontColor
            font.pointSize: Math.min(parent.height/2, (parent.width - height/3) * 0.05)
            leftPadding: height/6
            wrapMode: Text.Wrap
            width: parent.width - BurgerMenu.burgerButton.width - height/3

            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
        }

    }

    Rectangle{

        id: command

        width: parent.width
        height: parent.height* 0.9
        y: upper_part.height
        color: window.secondary_color
        border.color: window.primary_color
        border.width: 6
        radius: 3


            CuSwitch{
                id: start_all
                x: command.height/4
                anchors.verticalCenter: parent.verticalCenter

                offtext: "Start all"
                ontext: "Stop all"

                height: command.height/2
                width: command.width/8

                onSwitchOnChanged: {
                    if (switchOn) {
                        task_manager_model.project.start_all_tasks_request()
                    } else {
                        task_manager_model.project.stop_all_tasks_request()
                    }
                }
            }

            ButtonTemp{
                id: project_change
                anchors.verticalCenter: parent.verticalCenter

                buttonText: "Change Project"

                height: command.height/2
                width: command.width/8

                x: command.width - width - command.height/4

                onClicked: {
                    task_manager_model.settings.project_change_request()
                }
            }


        }

     DescriptionBar{
         width: parent.width
         height: parent.height * 0.7
         y: upper_part.height + command.y - 12

     }

}
