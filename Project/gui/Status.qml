import QtQuick 2.15
import QtQuick.Layouts 1.15
import "../"

RowLayout {
    spacing: 8
    property alias text: tag.text

    signal setNeutral()
    onSetNeutral: statusIcon.setNeutral()

    signal setLoading()
    onSetLoading: statusIcon.setLoading()

    signal setNegative()
    onSetNegative: statusIcon.setNegative()

    signal setPositive()
    onSetPositive: statusIcon.setPositive()


    Text {
        id: statusIcon

        font.family: Style.iconFonts.glyphter2.name
        text: "E"
        font.pixelSize: Style.fontSizes.medium
        color: Style.colors.iconNeutral

        NumberAnimation on rotation {
            id: rotate
            from: 0
            to: 360
            running: false
            loops: Animation.Infinite
            duration: 700
        }

        function setNeutral() {
            rotate.stop()
            rotation = 0
            font.family = Style.iconFonts.glyphter2.name
            text = "E"
            color = Style.colors.iconNeutral
        }
        function setLoading() {
            rotate.start()
            font.family = Style.iconFonts.glyphter2.name
            text = "O"
            color = Style.colors.iconLoading
        }
        function setNegative() {
            rotate.stop()
            rotation = 0
            font.family = Style.iconFonts.glyphter1.name
            text = "P"
            color = Style.colors.iconNegative
        }
        function setPositive() {
            rotate.stop()
            rotation = 0
            font.family = Style.iconFonts.glyphter1.name
            text = "N"
            color = Style.colors.iconPositive
        }
    }

    Text {
        id: tag
        text: ""
        font.family: Style.fonts.outfit.name
        font.pixelSize: Style.fontSizes.medium
        color: Style.colors.textLight
    }
}