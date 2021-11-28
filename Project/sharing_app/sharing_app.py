from Project.gui.base_app import BaseApplication


class SharingApplication(BaseApplication):
    QML_FILE = r'views\MainView.qml'

    def __init__(self):
        super(SharingApplication, self).__init__(self.QML_FILE, "Sharing Application")


if __name__ == "__main__":
    app = SharingApplication()
    app.run()
