import QtQuick 2.15

Item {
    id: divider

    property int thickness: 1
    property int cornerRadius: 0
    property color fillColor: "#808080"

    height: thickness
    width: parent.width

    Rectangle {
        width: parent.width
        height: parent.height
        color: divider.fillColor
        radius: divider.cornerRadius
    }
}
