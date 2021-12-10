from Project.gui.base_app import BaseApplication
from Project.sharing_app.sharing_view_model import SharingViewModel


class SharingApplication(BaseApplication):
    QML_FILE = r'views\MainView.qml'

    def __init__(self):
        super(SharingApplication, self).__init__(self.QML_FILE, "Sharing Application")
        self._sharing_view_model = SharingViewModel()

    def _set_app_input(self):
        context = self._engine.rootContext()
        context.setContextProperty("sharingVM", self._sharing_view_model)


if __name__ == "__main__":
    app = SharingApplication()
    app.run()
