import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

import "./components"

ApplicationWindow {
    visible: true
    width: 1280
    height: 720
    title: "Autonomous Drone"
    color: "#1e1e1e"

    Material.theme: Material.Dark
    Material.accent: Material.Blue

    // Main container for the app layout
    Rectangle {
        anchors.fill: parent
        anchors.margins: 16
        color: "transparent"

        Row {
            anchors.fill: parent
            spacing: 16

            // Sidebar
            Column {
                width: 280
                height: parent.height
                spacing: 24

                // Header
                Text {
                    id: appHeader
                    text: "Autonomous Drone"
                    anchors.horizontalCenter: parent.horizontalCenter
                    topPadding: 8
                    font.pixelSize: 24
                    color: "#ffffff"
                    font.weight: Font.Medium
                }

                DroneInfoPanel {
                    id: leftSidebar
                    width: parent.width
                    height: parent.height - parent.spacing - appHeader.height
                }
            }

            ControlPanel {
                width: parent.width - leftSidebar.width - parent.spacing
                height: parent.height
            }
        }
    }
}