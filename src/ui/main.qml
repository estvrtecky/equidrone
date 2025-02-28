import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 640
    height: 480
    title: "Autonomous Drone"

    Column {
        anchors.centerIn: parent
        spacing: 10

        Text {
            text: "Welcome to the Autonomous Drone App!"
        }

        Button {
            text: "Start Detection"
            anchors.horizontalCenter: parent.horizontalCenter
            onClicked: {
                app.start_detection()
            }
        }

        Button {
            text: "Stop Detection"
            anchors.horizontalCenter: parent.horizontalCenter
            onClicked: {
                app.stop_detection()
            }
        }
    }
}