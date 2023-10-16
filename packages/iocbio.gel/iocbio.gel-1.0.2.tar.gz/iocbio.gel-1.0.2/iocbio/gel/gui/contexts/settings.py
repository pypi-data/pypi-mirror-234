#
#  This file is part of IOCBIO Gel.
#
#  SPDX-FileCopyrightText: 2022-2023 IOCBIO Gel Authors
#  SPDX-License-Identifier: GPL-3.0-or-later
#


from PySide6.QtCore import Qt, QUrl, QCoreApplication
from PySide6.QtGui import QDesktopServices, QShowEvent
from PySide6.QtWidgets import QLabel, QWidget, QVBoxLayout, QPushButton, QMessageBox, QScrollArea

from iocbio.gel.application.event_registry import EventRegistry
from iocbio.gel.application.image.image_source_setup import ImageSourceSetup
from iocbio.gel.db.database_client import DatabaseClient
from iocbio.gel.db.database_setup import DatabaseSetup


class SettingsWidget(QScrollArea):
    SUCCESS_LABEL = "Changes saved"

    def __init__(
        self,
        db_client: DatabaseClient,
        db_setup: DatabaseSetup,
        image_source_setup: ImageSourceSetup,
        event_registry: EventRegistry,
        image_form_provider,
        db_form_provider,
        logs_folder,
    ):
        super().__init__()

        self.db_client = db_client
        self.db_setup = db_setup
        self.image_source_setup = image_source_setup
        self.event_registry = event_registry
        self.logs_folder = logs_folder

        self.image_success = QLabel()
        self.image_success.setAlignment(Qt.AlignRight)
        self.db_success = QLabel()
        self.db_success.setAlignment(Qt.AlignRight)

        self.image_form = QWidget()
        self.image_form.setLayout(
            image_form_provider(accept_callback=self.on_image_save, change_callback=self.on_change)
        )

        self.db_form = QWidget()
        self.db_form.setLayout(
            db_form_provider(accept_callback=self.on_db_save, change_callback=self.on_change)
        )

        log_location_hint = QLabel("Logs stored in " + logs_folder)
        log_location_hint.setWordWrap(True)
        open_logs_button = QPushButton("Open folder with logs")
        open_logs_button.clicked.connect(self.open_logs_window)

        clear_button = QPushButton("Clear sensitive data")
        clear_button.clicked.connect(self.clear_data)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.addWidget(QLabel("<h1>Settings</h1>"))

        self.layout.addWidget(QLabel("<h2>Image source</h2>"))
        self.layout.addWidget(self.image_form)
        self.layout.addWidget(self.image_success)

        self.layout.addWidget(QLabel("<h2>Database connection</h2>"))
        self.layout.addWidget(self.db_form)
        self.layout.addWidget(self.db_success)

        self.layout.addWidget(QLabel("<h2>Privacy</h2>"))
        self.layout.addWidget(QLabel("Remove database connection settings and OMERO user password"))
        self.layout.addWidget(clear_button, stretch=0, alignment=Qt.AlignRight)

        self.layout.addWidget(QLabel("<h2>Logs</h2>"))
        self.layout.addWidget(log_location_hint)
        self.layout.addWidget(open_logs_button, stretch=0, alignment=Qt.AlignRight)

        self.layout.addStretch(1)
        widget = QWidget()
        widget.setLayout(self.layout)
        self.setWidget(widget)
        self.setWidgetResizable(True)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self.db_form.layout().select_type_from_settings()

    def on_change(self):
        """
        Clear success messages changing the form.
        """
        self.image_success.setText("")
        self.db_success.setText("")

    def on_image_save(self):
        """
        Show success message for changing image source parameters.
        """
        self.image_success.setText(self.SUCCESS_LABEL)
        self.db_success.setText("")

    def on_db_save(self):
        """
        Show success message for changing database parameters.
        Start a new client session.
        """
        self.db_success.setText(self.SUCCESS_LABEL)
        self.image_success.setText("")
        self.db_client.start_session()
        self.event_registry.db_connected.emit()

    def clear_data(self):
        self.db_setup.clear_connection_string()
        self.image_source_setup.clear_omero_login()

        box = QMessageBox()
        box.setText("Closing application after clearing sensitive data")
        box.setIcon(QMessageBox.Information)
        box.exec()
        QCoreApplication.quit()

    def open_logs_window(self):
        QDesktopServices.openUrl(QUrl(self.logs_folder, QUrl.TolerantMode))
