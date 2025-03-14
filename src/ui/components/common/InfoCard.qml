import QtQuick 2.15

Rectangle {
    id: infoCard
    property string label: "Label"
    property string value: "Value"
    property color valueColor: "#ffffff"

    width: parent.width
    height: 80
    color: "#363636"
    radius: 8

    Column {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 4

        Text {
            text: infoCard.label
            color: "#888888"
            font.pixelSize: 12
        }

        Text {
            text: infoCard.value
            color: infoCard.valueColor
            font.pixelSize: 24
            font.weight: Font.Medium
        }
    }
}