import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

import "./common"

Item {
    id: droneInfoPanel
    width: 280
    height: parent.height

    Rectangle {
        anchors.fill: parent
        color: "#2d2d2d"
        radius: 8

        Column {
            anchors.fill: parent
            anchors.margins: 16
            spacing: 16

            // Header
            Text {
                text: "DRONE STATUS"
                color: "#808080"
                font.pixelSize: 12
                font.weight: Font.DemiBold
                font.letterSpacing: 1.5
                anchors.horizontalCenter: parent.horizontalCenter
            }

            // Status and Connect Button Group
            Column {
                width: parent.width

                // Status Card
                Rectangle {
                    width: parent.width
                    height: 60
                    color: "#1e1e1e"
                    radius: 8

                    Row {
                        height: statusText.height
                        anchors.centerIn: parent
                        spacing: 8

                        // Status Indicator
                        Rectangle {
                            width: 8
                            height: 8
                            radius: 4
                            color: app.is_connected ? "#4CAF50" : "#f44336"
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        Text {
                            id: statusText
                            text: app.is_connected ? "Connected" : "Disconnected"
                            color: "white"
                            font.pixelSize: 24
                        }
                    }
                }

                // Connect/Disconnect Button
                Button {
                    id: connectButton
                    width: parent.width
                    height: 40
                    font.pixelSize: 14
                    text: app.is_connected ? "Disconnect" : "Connect"

                    contentItem: Text {
                        text: connectButton.text
                        font: connectButton.font
                        color: "white"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    background: Rectangle {
                        color: {
                            if (connectButton.pressed) {
                                return app.is_connected ? "#d32f2f" : "#1976D2"
                            }
                            return app.is_connected ? "#f44336" : "#2196F3"
                        }
                        radius: 5
                    }

                    onClicked: app.is_connected ? app.disconnect_drone() : app.connect_drone()
                }
            }

            Divider {
                fillColor: "#363636"
            }

            InfoCard {
                label: "Battery Level"
                value: app.battery_level + "%"
                valueColor: app.battery_level > 20 ? "#4CAF50" : "#f44336"
            }

            InfoCard {
                label: "Temperature"
                value: app.temperature + "°C"
                valueColor: app.temperature < 60 ? "#4CAF50" : "#f44336"
            }

            InfoCard {
                label: "Height"
                value: app.height + " cm"
            }
        }
    }
}
