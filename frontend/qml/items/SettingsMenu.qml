import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

Menu {
    width: 800 / 3
    height: 600
    x: window.width - width*2
    y: window.height/10
    visible: false
    spacing: 30

    background: Rectangle{

        color: "#262b33"
        height: parent.height
        width: parent.width
        border.width: 2
        border.color: '#2f343f'

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
            buttonText: "Theme"

    }


    BurgerButton{
            height: 50
            width: parent.width - 6
            buttonText: "Delay"

    }

}
