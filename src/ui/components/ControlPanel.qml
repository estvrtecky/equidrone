import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

import "./common"

Item {
    id: controlPanel
    width: 800
    height: parent.height

    Rectangle {
        anchors.fill: parent
        color: "#2d2d2d"
        radius: 8

        Column {
            anchors.fill: parent
            anchors.margins: 16
            spacing: 16

            Heading {
                text: "Control Panel"
            }

            Divider {
                fillColor: "#363636"
            }

            // Controls
            Column {
                width: parent.width
                spacing: 8

                // Start Detection Button
                Button {
                    id: startDetectionButton
                    width: parent.width
                    height: 40
                    font.pixelSize: 14
                    text: "Start Detection"
                    enabled: app.is_connected

                    contentItem: Text {
                        text: startDetectionButton.text
                        font: startDetectionButton.font
                        color: "white"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        color: startDetectionButton.pressed ? "#1976D2" : "#2196F3"
                        radius: 5
                    }

                    onClicked: app.start_detection()
                }

                // Stop Detection Button
                Button {
                    id: stopDetectionButton
                    width: parent.width
                    height: 40
                    font.pixelSize: 14
                    text: "Stop Detection"
                    enabled: app.is_connected

                    contentItem: Text {
                        text: stopDetectionButton.text
                        font: stopDetectionButton.font
                        color: "white"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        color: stopDetectionButton.pressed ? "#d32f2f" : "#f44336"
                        radius: 5
                    }

                    onClicked: app.stop_detection()
                }
            }
        }
    }
}
