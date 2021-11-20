from datetime import datetime
import os
from os import listdir
from os.path import isfile, isdir, join, splitext, basename
from os import path
from typing import Optional, List, Callable
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, pyqtProperty, QVariant


class RemoteViewModel(QtCore.QObject):
    def __init__(self):
        super(RemoteViewModel, self).__init__()
