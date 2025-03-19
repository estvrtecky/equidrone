import QtQuick 2.15

Item {
    id: infoCard

    property string label: "Label"
    property string value: "Value"
    property color labelColor: "#808080"
    property color valueColor: "white"

    width: parent.width
    height: 80

    Rectangle {
        width: parent.width
        height: parent.height
        color: "#363636"
        radius: 8

        Column {
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.margins: 16

            Text {
                text: infoCard.label
                color: infoCard.labelColor
                font.pixelSize: 12
            }

            Text {
                text: infoCard.value
                color: infoCard.valueColor
                font.pixelSize: 20
            }
        }
    }
}
