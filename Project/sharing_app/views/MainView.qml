import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick 2.15
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.15
import QtQuick.Controls.Styles 1.4
import "../../gui"


Window {
    id: root
    height: 400
    width: 400
    maximumHeight: 400
    maximumWidth: 400
    minimumHeight: 400
    minimumWidth: 400
    color: Style.colors.backgroundDark

    Connections {
        target: sharingVM

        function onStateChanged(state) {
            switch(state) {
                case 1:
                    loadingProgress.connection.setPositive()
                    loadingProgress.encryption.setLoading()
                    break
                case 2:
                    loadingProgress.encryption.setPositive()
                    loadingProgress.streaming.setLoading()
                    break
                case 3:
                    loadingProgress.streaming.setPositive()
                    break
            }
        }
    }

    ColumnLayout {
        id: keyItem
        anchors.horizontalCenter: parent.horizontalCenter
        y: 150
        spacing: 30


        PropertyAnimation on y {
            id: raise
            running: false
            to: -20
            duration: 500
        }

        Text {
            id: instructions
            Layout.alignment: Qt.AlignCenter

            property alias hide: hide

            font.family: Style.fonts.outfit_light.name
            font.pixelSize: Style.fontSizes.medium
            color: Style.colors.textLight
            opacity: 100

            text: "Please enter the session key bellow."

            PropertyAnimation on opacity {
                id: hide
                running: false
                to: 0
                duration: 200
            }
        }

        TextField {
            id: keyEntry
            Layout.alignment: Qt.AlignCenter

            placeholderText: "XXXX-XXXX"
            horizontalAlignment: TextInput.AlignHCenter
            inputMask: "0000-0000"
            maximumLength: 8

            style: TextFieldStyle {
                textColor: Style.colors.textDark
                font.family: Style.fonts.outfit.name
                font.pixelSize: Style.fontSizes.large
                font.letterSpacing: 10

                background: Rectangle {
                    radius: 5
                    width: 280
                    border.color: Style.colors.borderLight
                    border.width: 3
                }
            }

            onEditingFinished: {
                var key = text.replace("-", "").replace(" ", "")

                if (key.length == 8) {
                    readOnly = true
                    parent.hideKeyEntry()
                    loadingProgress.show.start()
                    sharingVM.launchClient(key)
                }
            }
        }

        function hideKeyEntry() {
            raise.start()
            instructions.hide.start()
        }
    }

    ColumnLayout {
        id: loadingProgress
        anchors.centerIn: parent
        opacity: 0
        spacing: 30

        property alias show: show
        property alias connection: connection
        property alias encryption: encryption
        property alias streaming: streaming

        PropertyAnimation on opacity {
            id: show
            running: false
            to: 100
            duration: 500
        }

        Status {
            id: connection
            text: "Connected to server"

            Component.onCompleted: { setLoading() }
        }

        Status {
            id: encryption
            text: "Encrypted connection"
        }

        Status {
            id: streaming
            text: "Streaming screen"
        }
    }
}