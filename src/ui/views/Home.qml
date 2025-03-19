import QtQuick 2.15

import "../components"

Item {
    id: homeView

    Row {
        anchors.fill: parent
        spacing: 16

        DroneInfoPanel {
            id: droneInfoPanel
        }

        ControlPanel {
            width: parent.width - droneInfoPanel.width - parent.spacing
            height: parent.height
        }
    }
}
