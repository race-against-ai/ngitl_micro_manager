// Copyright (C) 2022 twyleg
import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "./items"

Window {
    id: window

    width: 800
    height: 600

    minimumWidth: 800
    minimumHeight: 600
    visible: true
    title: qsTr("NGITL MicroManager")

    property color primary_color: "#262b33" // background
    property color secondary_color: "#2f343f" // complementary to the background
    property color tertiary_color: '#4c5e7c' // foreground

    property color lightFontColor: '#F4EEE0' // Kinda white but not really

    color: primary_color

    Column {
        id: column

		anchors.fill: parent
        spacing: 3

        Rectangle {
            width: parent.width
            height: parent.height/5
            color: 'transparent'

            TitleBar {
                   id: titleBar
                   width: parent.width
                   height: parent.parent.height/10


            }

//            MenuBar {
//                    y: parent.parent.height/10
//                    width: parent.width
//                    height: parent.parent.height/20
//            }



        }


        Repeater {
            id: repeater

            model: task_manager_model.project.task_list

            Task {
                width: parent.width
                height: parent.height/10
                taskModel: modelData

            }

        }

    }

    Component.onCompleted: {
        console.debug("foo")
       console.log(task_manager_model.project.task_list)
    }

}
