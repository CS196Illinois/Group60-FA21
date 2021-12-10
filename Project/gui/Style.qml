pragma Singleton
import QtQuick 2.15
import QtQuick.Window 2.2

Item {
    property alias colors: colors
    property alias fontSizes: fontSizes
    property alias fonts: fonts
    property alias iconFonts: iconFonts


    QtObject {
        id: colors
        property color backgroundDark: "#00072D"
        property color backgroundLight: "#0E6BA8"

        property color textLight: "white"
        property color textDark: "#00072D"

        property color borderLight: "#0E6BA8"

        property color iconLoading: "#EEBA0B"
        property color iconNeutral: "#CCDBDC"
        property color iconNegative: "#C83E4D"
        property color iconPositive: "#1A936F"
    }

    QtObject {
        id: fontSizes

        property double small: 10.0
        property double medium: 18.0
        property double large: 24.0
    }

    QtObject {
        id: fonts

        property FontLoader outfit: FontLoader {
            source: "fonts/Outfit-Regular.ttf"
        }

        property FontLoader outfit_bold: FontLoader {
            source: "fonts/Outfit-Bold.ttf"
        }

        property FontLoader outfit_light: FontLoader {
            source: "fonts/Outfit-Light.ttf"
        }
    }

    QtObject {
        id: iconFonts

        property FontLoader glyphter: FontLoader {
            source: "fonts/Glyphter.ttf"
        }
    }
}