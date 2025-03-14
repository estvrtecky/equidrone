import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

Rectangle {
    color: "#2d2d2d"
    radius: 8

    Column {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 16

        Text {
            anchors.horizontalCenter: parent.horizontalCenter
            text: "Control Panel"
            color: "#ffffff"
            font.pixelSize: 24
            font.weight: Font.Medium
        }

        // Divider
        Rectangle {
            width: parent.width
            height: 1
            color: "#363636"
        }

        // Controls
        Column {
            width: parent.width
            spacing: 8

            // Start Detection Button
            Button {
                width: parent.width
                height: 40
                font.pixelSize: 14
                font.weight: Font.Medium
                text: "Start Detection"
                enabled: app.is_connected

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

                onClicked: app.start_detection()
            }

            // Stop Detection Button
            Button {
                width: parent.width
                height: 40
                font.pixelSize: 14
                font.weight: Font.Medium
                text: "Stop Detection"
                enabled: app.is_connected

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

                onClicked: app.stop_detection()
            }
        }
    }
}