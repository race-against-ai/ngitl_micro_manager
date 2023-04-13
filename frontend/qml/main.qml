// Copyright (C) 2022 twyleg
import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

import "./items"

Window {
	id: window

    width: 800
    height: 600
	visible: true
    title: qsTr("NGITL MicroManager")

    color: "#101010"


    Column {
        id: column

		anchors.fill: parent
        spacing: 3

        Repeater {
            id: repeater

            model: task_manager_model.task_list

            Task {
                taskModel: modelData

            }

        }

	}
}
