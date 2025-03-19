import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

import "./components"
import "./views"

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

        Column {
            anchors.fill: parent
            spacing: 16

            NavBar {
                id: navbar
                onHomeClicked: stackView.replace(homeView)
                onSettingsClicked: stackView.replace(settingsView)
            }

            StackView {
                id: stackView
                width: parent.width
                height: parent.height - navbar.height - parent.spacing
                initialItem: homeView
            }

            Component {
                id: homeView
                Home {
                    width: stackView.width
                    height: stackView.height
                }
            }

            Component {
                id: settingsView
                Settings {
                    width: stackView.width
                    height: stackView.height
                }
            }
        }
    }
}
