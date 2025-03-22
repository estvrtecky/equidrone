import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

Item {
    id: controlButton

    property string buttonText: "Button"
    property bool buttonEnabled: true
    property color buttonTextColor: "white"
    property color buttonTextColorHovered: "black"
    property color buttonTextColorPressed: "black"
    property color buttonBackgroundColor: "transparent"
    property color buttonBackgroundColorHovered: "white"
    property color buttonBackgroundColorPressed: "#e0e0e0"
    property color buttonBorderColor: "white"
    property color buttonBorderColorHovered: "white"
    property color buttonBorderColorPressed: "#e0e0e0"
    property var onButtonClicked: function() {
        console.log("Button clicked")
    }

    width: 200
    height: 40

    Button {
        id: controlButtonProperties
        width: parent.width
        height: parent.height
        text: controlButton.buttonText
        font.pixelSize: 14
        enabled: controlButton.buttonEnabled

        contentItem: Text {
            text: controlButtonProperties.text
            font: controlButtonProperties.font
            color: {
                if (controlButtonProperties.enabled) {
                    if (controlButtonProperties.pressed) {
                        return controlButton.buttonTextColorPressed
                    } else if (controlButtonProperties.hovered) {
                        return controlButton.buttonTextColorHovered
                    } else {
                        return controlButton.buttonTextColor
                    }
                } else {
                    return "#808080"
                }
            }
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter

            Behavior on color {
                ColorAnimation {
                    duration: 150
                }
            }
        }

        background: Rectangle {
            color: {
                if (controlButtonProperties.enabled) {
                    if (controlButtonProperties.pressed) {
                        return controlButton.buttonBackgroundColorPressed
                    } else if (controlButtonProperties.hovered) {
                        return controlButton.buttonBackgroundColorHovered
                    } else {
                        return controlButton.buttonBackgroundColor
                    }
                } else {
                    return "#363636"
                }
            }
            radius: 5
            border.color: {
                if (controlButtonProperties.enabled) {
                    if (controlButtonProperties.pressed) {
                        return controlButton.buttonBorderColorPressed
                    } else if (controlButtonProperties.hovered) {
                        return controlButton.buttonBorderColorHovered
                    } else {
                        return controlButton.buttonBorderColor
                    }
                } else {
                    return "#808080"
                }
            }
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

        onClicked: controlButton.onButtonClicked()
    }
}