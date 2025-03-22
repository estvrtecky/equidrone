import QtQuick 2.15
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
                id: controls
                width: parent.width
                height: parent.height - controls.y
                spacing: 10

                Row {
                    id: cameraFeedRow
                    width: parent.width
                    spacing: 16

                    ControlButton {
                        id: cameraFeedButton
                        width: 175
                        buttonText: app.is_processing ? "Camera Feed: On" : "Camera Feed: Off"
                        buttonEnabled: app.is_connected
                        buttonTextColor: app.is_processing ? "black" : "white"
                        buttonBackgroundColor: app.is_processing ? "white" : "#363636"
                        onButtonClicked: function() {
                            app.is_processing ? app.stop_feed() : app.start_feed()
                        }
                    }

                    Text {
                        id: cameraFeedMode
                        text: {
                            if (app.camera_feed_mode === 0) {
                                return "Camera Feed Mode: Hidden"
                            } else if (app.camera_feed_mode === 1) {
                                return "Camera Feed Mode: Visible"
                            } else if (app.camera_feed_mode === 2) {
                                return "Camera Feed Mode: Debug"
                            }
                        }
                        color: "white"
                        font.pixelSize: 16
                        anchors.verticalCenter: parent.verticalCenter
                    }

                    Text {
                        id: autopilotStatus
                        text: app.is_detecting ? "Autopilot: On" : "Autopilot: Off"
                        color: "white"
                        font.pixelSize: 16
                        anchors.verticalCenter: parent.verticalCenter
                    }
                }

                // Flight Controls
                Rectangle {
                    id: flightControls
                    width: parent.width
                    height: parent.height - flightControls.y
                    color: "#1e1e1e"
                    radius: 8

                    Column {
                        anchors.fill: parent
                        anchors.margins: 16

                        // Autopilot Button
                        ControlButton {
                            id: autopilotButton
                            width: parent.width
                            buttonText: "Autopilot"
                            buttonEnabled: app.is_processing
                            onButtonClicked: function() {
                                app.toggle_autopilot()
                            }
                        }
                    }
                }
            }
        }
    }
}
