import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    visible: true
    width: 1280
    height: 720
    title: "Autonomous Drone Control"
    color: "#1e1e1e"

    Material.theme: Material.Dark
    Material.accent: Material.Blue

    Column {
        anchors.centerIn: parent
        spacing: 16

        // Header
        Text {
            text: "Autonomous Drone"
            anchors.horizontalCenter: parent.horizontalCenter
            font.pixelSize: 24
            color: "#ffffff"
            font.weight: Font.Medium
        }

        // Status Panel
        Rectangle {
            width: 300
            height: 80
            color: "#2d2d2d"
            radius: 10
            anchors.horizontalCenter: parent.horizontalCenter

            Column {
                anchors.centerIn: parent
                spacing: 8

                // Status indicator
                Rectangle {
                    id: statusIndicator
                    width: 20
                    height: 20
                    radius: 10
                    color: "#4CAF50"
                    anchors.horizontalCenter: parent.horizontalCenter
                }

                Text {
                    id: statusText
                    text: "Status: Ready"
                    color: "#ffffff"
                    font.pixelSize: 16
                    font.weight: Font.Medium
                    anchors.horizontalCenter: parent.horizontalCenter
                }
            }
        }

        // Control Buttons
        Row {
            spacing: 20
            anchors.horizontalCenter: parent.horizontalCenter

            Button {
                text: "Start Detection"
                width: 150
                height: 45
                font.pixelSize: 14
                font.weight: Font.Medium
                contentItem: Text {
                    text: parent.text
                    font: parent.font
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                background: Rectangle {
                    color: parent.pressed ? "#1976D2" : "#2196F3"
                    radius: 5
                }
                onClicked: {
                    app.start_detection()
                    statusText.text = "Status: Running"
                    errorText.visible = false
                    statusIndicator.color = "#2196F3"
                }
            }

            Button {
                text: "Stop Detection"
                width: 150
                height: 45
                font.pixelSize: 14
                font.weight: Font.Medium
                contentItem: Text {
                    text: parent.text
                    font: parent.font
                    color: "white"
                    horizontalAlignment: Text.AlignHCenter
                    verticalAlignment: Text.AlignVCenter
                }
                background: Rectangle {
                    color: parent.pressed ? "#d32f2f" : "#f44336"
                    radius: 5
                }
                onClicked: {
                    app.stop_detection()
                    statusText.text = "Status: Stopped"
                    statusIndicator.color = "#4CAF50"
                }
            }
        }
    }
}