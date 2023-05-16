import QtQuick 2.15
import QtQuick.Controls 2.15

Button{
    id: main_button

    property string theme_name: "Dark Material"

    property color primary: '#262b33'
    property color secondary: '#2f343f'
    property color tertiary: '#4c5e7c'

    width:parent.width/2
    height: parent.height/3
    background: Rectangle{
        width: parent.width
        height: parent.height
        color: window.secondary_color
        border.width: 1
        border.color: window.primary_color
        radius: height/5

        Rectangle{
            id: color_preview
            width: main_button.width/10*3
            height: main_button.height/2
            color: secondary
            border.width: 1
            border.color: "black"

            anchors.right: parent.right
            anchors.rightMargin: 10
            anchors.verticalCenter: parent.verticalCenter

            Rectangle{
                id: primary_cube
                width:parent.width/3
                height: parent.height-2
                color: primary
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.leftMargin: 1
            }

            Rectangle{
                id: tertiary_cube
                width: parent.width/3
                height: parent.height-2
                color: tertiary
                x: parent.border.width
                anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.right
                anchors.rightMargin: 1
            }

        }

        Rectangle{
            color:"transparent"
            width: main_button.width - color_preview.width - color_preview.anchors.rightMargin*3
            height: main_button.height
            anchors.left: parent.left
            anchors.leftMargin: 10
            Text{
                text: theme_name
                color: window.lightFontColor
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                font.pointSize: parent.height/3
                wrapMode: Text.Wrap


            }
        }

    }

}
