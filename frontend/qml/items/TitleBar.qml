import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle{
    id: title_bar

    property color back_color: "#262b33" // background
    property color middle_color: "#2f343f" // complementary to the background
    property color fore_color: '#4c5e7c' // foreground

    property color lightFontColor: '#F4EEE0' // Kinda white but not really

    width: parent.width
    height: parent.height
    color: fore_color

//    color: 'red'
//    radius: 5
//    anchors.bottomMargin: parent.height/20


//          border.color: '#0d4671'
//          border.width: 2

    BurgerMenu{
        width: parent.width
        height: parent.height
    }

    Rectangle{
        width: parent.width - parent.height/6
        color: 'transparent'
        anchors.left: parent.left
        height: parent.height

        Text {
            id: title
            text: qsTr("NGITL MicroManager")
            color: lightFontColor
            font.pointSize: Math.min(parent.height/2, (parent.width - height/3) * 0.05)
            leftPadding: height/6
            wrapMode: Text.Wrap
            width: parent.width - logo.width - height/3

            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
        }

    }
}
