import QtQuick 2.15
import QtQuick.Controls 2.15

TextField{

    id: task_name
    width: parent.width
    height: parent.height
    color: window.lightFontColor

    background: Rectangle{
        color: window.primary_color
        radius: 5
        border.color: window.secondary_color
        border.width: 1
    }
}
