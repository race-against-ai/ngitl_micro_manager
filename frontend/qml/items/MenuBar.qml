import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: menu_bar
    height: parent.height
    width: parent.width
    color: 'transparent'

    Rectangle {
        id: top_half
        height: parent.height/2
        width: parent.width
        color: '#4c5e7c'
    }

    Rectangle {
        id: filler
        height: parent.height/2.5
        width: parent.width
        color: '#4c5e7c'
        y: top_half.height/2
    }

    Rectangle {
        id: bottom_half

        y: top_half.height/2

        height: parent.height * 0.75
        width: parent.width

        radius: 20
        color: '#4c5e7c'

//        RowLayout{
//            Button{
//                id: start_all_button

//            }

//            Button{

//            }
        }
    }

