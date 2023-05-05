import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Button {

    property string buttonText: ""

    text: buttonText

    height: parent.height
    width: parent.width

    background: Rectangle{
        color: window.tertiary_color
        width: parent.width
        height: parent.height
        radius: 3


    }
}

