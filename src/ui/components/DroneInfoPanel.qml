import QtQuick 2.15
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
                            color: app.is_connected ? "#4caf50" : "#f44336"
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
                ControlButton {
                    id: connectButton
                    width: parent.width
                    buttonText: app.is_connected ? "Disconnect" : "Connect"
                    buttonTextColor: "white"
                    buttonTextColorHovered: "white"
                    buttonTextColorPressed: "white"
                    buttonBackgroundColor: app.is_connected ? "#f44336" : "#4caf50"
                    buttonBackgroundColorHovered: app.is_connected ? "#d32f2f" : "#388e3c"
                    buttonBackgroundColorPressed: app.is_connected ? "#d32f2f" : "#388e3c"
                    buttonBorderColor: app.is_connected ? "#f44336" : "#4caf50"
                    buttonBorderColorHovered: app.is_connected ? "#d32f2f" : "#388e3c"
                    buttonBorderColorPressed: app.is_connected ? "#d32f2f" : "#388e3c"
                    onButtonClicked: function() {
                        app.is_connected ? app.disconnect_drone() : app.connect_drone()
                    }
                }
            }

            Divider {
                fillColor: "#363636"
            }

            InfoCard {
                label: "Battery Level"
                value: app.battery_level + "%"
                valueColor: app.battery_level > 20 ? "#4caf50" : "#f44336"
            }

            InfoCard {
                label: "Temperature"
                value: app.temperature + "°C"
                valueColor: app.temperature < 60 ? "#4caf50" : "#f44336"
            }

            InfoCard {
                label: "Height"
                value: app.height + " cm"
            }
        }
    }
}
