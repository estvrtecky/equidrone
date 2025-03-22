import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

Item {
    id: navbar
    height: 50
    width: parent.width

    signal homeClicked()
    signal settingsClicked()

    // Logo
    Row {
        id: logo
        spacing: 16
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: 16

        Image {
            id: logoImage
            source: "../assets/logo-neg.png"
            height: 32
            width: 32
            anchors.verticalCenter: parent.verticalCenter
        }

        Text {
            id: logoText
            text: "Autonomous Drone"
            font.pixelSize: 24
            font.family: "Orbitron"
            color: "white"
            anchors.verticalCenter: parent.verticalCenter
        }
    }

    // Navigation buttons
    Row {
        id: navbarButtons
        spacing: 16
        anchors.verticalCenter: parent.verticalCenter
        anchors.right: parent.right
        anchors.rightMargin: 16

        Button {
            id: homeButton
            text: "Home"
            font.pixelSize: 16

            contentItem: Text {
                text: homeButton.text
                font: homeButton.font
                color: homeButton.pressed ? "black" : "white"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            background: Rectangle {
                color: homeButton.pressed ? "white" : "transparent"
                radius: height / 2
                border.color: homeButton.hovered ? "white" : "transparent"
                border.width: 1

                Behavior on color {
                    ColorAnimation {
                    duration: 150
                    }
                }
                Behavior on border.color {
                    ColorAnimation {
                    duration: 150
                    }
                }
            }

            onClicked: navbar.homeClicked()
        }

        Button {
            id: settingsButton
            text: "Settings"
            font.pixelSize: 16

            contentItem: Text {
                text: settingsButton.text
                font: settingsButton.font
                color: settingsButton.pressed ? "black" : "white"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }
            background: Rectangle {
                color: settingsButton.pressed ? "white" : "transparent"
                radius: height / 2
                border.color: settingsButton.hovered ? "white" : "transparent"
                border.width: 1

                Behavior on color {
                    ColorAnimation {
                    duration: 150
                    }
                }
                Behavior on border.color {
                    ColorAnimation {
                    duration: 150
                    }
                }
            }

            onClicked: navbar.settingsClicked()
        }
    }
}
