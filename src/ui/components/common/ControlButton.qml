import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

Item {
    id: controlButton

    property string buttonText: "Button"
    property bool buttonEnabled: true
    property color buttonTextColor: "white"
    property color buttonTextColorPressed: "black"
    property color buttonBackgroundColor: "#363636"
    property color buttonBackgroundColorPressed: "white"
    property color buttonBorderColor: "white"
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
            color: controlButtonProperties.enabled
                    ? (controlButtonProperties.pressed ? controlButton.buttonTextColorPressed : controlButton.buttonTextColor)
                    : "#808080"
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
        }

        background: Rectangle {
            color: controlButtonProperties.enabled
                    ? (controlButtonProperties.pressed ? controlButton.buttonBackgroundColorPressed : controlButton.buttonBackgroundColor)
                    : "#363636"
            radius: 5
            border.color: controlButtonProperties.enabled ? controlButton.buttonBorderColor : "#808080"
            border.width: 1

            Behavior on color {
                ColorAnimation {
                    duration: 150
                }
            }
        }

        onClicked: controlButton.onButtonClicked()
    }
}