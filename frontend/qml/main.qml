// Copyright (C) 2022 twyleg
import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "./items"

Window {
    id: window

    width: 800
    height: 600

    property string titleText: "NGITL MicroManager"

    property color primary_color: "#262b33" // background
    property color secondary_color: "#2f343f" // complementary to the background
    property color tertiary_color: '#4c5e7c' // foreground

    property color lightFontColor: '#F4EEE0' // Kinda white but not really

    property bool devMode: false

    minimumWidth: 800
    minimumHeight: 600
    visible: true
    title: qsTr("NGITL MicroManager")


    color: primary_color

    Rectangle {
        id: fill_rect
        width: parent.width
        height: parent.height/3.8
        color: 'transparent'

        TitleBar {
               id: titleBar
               width: parent.width
               height: parent.parent.height/10
        }
    }
    Rectangle{
        id: task_rect
        color:"transparent"
        width: parent.width
        height: parent.height-fill_rect.height
        y: fill_rect.height

        ScrollView {
            id:scrollView
            anchors.fill: parent
            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff // Disable horizontal scrollbar

            ScrollBar.vertical: ScrollBar{
                id: scrollBar

                hoverEnabled: true
                policy: ScrollBar.AsNeeded
                width: 6

                parent: scrollView.parent
                x: scrollView.mirrored ? 0 : scrollView.width - width
//                y: scrollView.topPadding
                height: scrollView.availableHeight
//                active: scrollView.ScrollBar.horizontal.active

                background: Rectangle {
                    color: tertiary_color // Change the color of the track

                }

            }


            Column {
                id: column

                anchors.fill: parent
                spacing: 3

                Repeater {
                    id: repeater

                    model: task_manager_model.project.task_list

                    Task {
                        width: window.width-4
//                        height: window.height/10
                        taskModel: modelData

                    }
                }
            }
        }
    }


    Component.onCompleted: {
        console.debug("foo")
       console.log(task_manager_model.project.task_list)
    }

}
