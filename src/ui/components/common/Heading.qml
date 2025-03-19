import QtQuick 2.15

Item {
    id: heading

    property string text: "Heading"
    property color color: "white"
    property int fontSize: 24

    width: parent.width
    height: headingText.height

    Text {
        id: headingText
        text: heading.text
        color: heading.color
        font.pixelSize: heading.fontSize
        anchors.horizontalCenter: parent.horizontalCenter
    }
}
