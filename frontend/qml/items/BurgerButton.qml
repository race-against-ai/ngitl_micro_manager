import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

MenuItem {
        id: menu_button

        property string buttonText: ""

        text: buttonText
        anchors.horizontalCenter: parent.horizontalCenter

        background: Rectangle{
            anchors.horizontalCenter: parent.horizontalCenter
            color: '#4c5e7c'
            width: parent.width - 5
            height: parent.height - 5
            radius: 3


        }

    }

