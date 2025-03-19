import QtQuick 2.15

import "../components/common"

Item {
    id: settingsView

    Rectangle {
        anchors.fill: parent
        color: "#2d2d2d"
        radius: 8

        Column {
            anchors.fill: parent
            anchors.margins: 16
            spacing: 16

            Heading {
                text: "Settings"
            }

            Divider {
                fillColor: "#363636"
            }
        }
    }
}
