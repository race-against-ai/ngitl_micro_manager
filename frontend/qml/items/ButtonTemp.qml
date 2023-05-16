import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Button {

    property string buttonText: ""
    property color bcolor: window.tertiary_color

    text: buttonText

    height: parent.height
    width: parent.width

    background: Rectangle{
        color: bcolor
        width: parent.width
        height: parent.height
        radius: 3


    }
}

