import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

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

            Item {
                width: parent.width
                height: cameraFeedModeComboBox.height

                Text {
                    text: "Drone camera feed mode:"
                    color: "white"
                    font.pixelSize: 16
                    anchors.left: parent.left
                    anchors.verticalCenter: parent.verticalCenter
                }

                ComboBox {
                    id: cameraFeedModeComboBox
                    width: 200
                    height: 40
                    anchors.right: parent.right
                    model: ["Off", "On", "Dev Mode"]
                    currentIndex: app.camera_feed_mode
                    onCurrentIndexChanged: {
                        app.camera_feed_mode = currentIndex
                    }
                }
            }
        }
    }
}
