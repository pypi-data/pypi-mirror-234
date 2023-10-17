# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'msr_cosmetic_patches_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_SamusReturnsCosmeticPatchesDialog(object):
    def setupUi(self, SamusReturnsCosmeticPatchesDialog):
        if not SamusReturnsCosmeticPatchesDialog.objectName():
            SamusReturnsCosmeticPatchesDialog.setObjectName(u"SamusReturnsCosmeticPatchesDialog")
        SamusReturnsCosmeticPatchesDialog.resize(396, 246)
        self.gridLayout = QGridLayout(SamusReturnsCosmeticPatchesDialog)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.reset_button = QPushButton(SamusReturnsCosmeticPatchesDialog)
        self.reset_button.setObjectName(u"reset_button")

        self.gridLayout.addWidget(self.reset_button, 2, 2, 1, 1)

        self.accept_button = QPushButton(SamusReturnsCosmeticPatchesDialog)
        self.accept_button.setObjectName(u"accept_button")

        self.gridLayout.addWidget(self.accept_button, 2, 0, 1, 1)

        self.cancel_button = QPushButton(SamusReturnsCosmeticPatchesDialog)
        self.cancel_button.setObjectName(u"cancel_button")

        self.gridLayout.addWidget(self.cancel_button, 2, 1, 1, 1)

        self.scrollArea = QScrollArea(SamusReturnsCosmeticPatchesDialog)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scroll_area_contents = QWidget()
        self.scroll_area_contents.setObjectName(u"scroll_area_contents")
        self.scroll_area_contents.setGeometry(QRect(0, 0, 376, 195))
        self.verticalLayout = QVBoxLayout(self.scroll_area_contents)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.scrollArea.setWidget(self.scroll_area_contents)

        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 3)


        self.retranslateUi(SamusReturnsCosmeticPatchesDialog)

        QMetaObject.connectSlotsByName(SamusReturnsCosmeticPatchesDialog)
    # setupUi

    def retranslateUi(self, SamusReturnsCosmeticPatchesDialog):
        SamusReturnsCosmeticPatchesDialog.setWindowTitle(QCoreApplication.translate("SamusReturnsCosmeticPatchesDialog", u"Metroid: Samus Returns - Cosmetic Options", None))
        self.reset_button.setText(QCoreApplication.translate("SamusReturnsCosmeticPatchesDialog", u"Reset to Defaults", None))
        self.accept_button.setText(QCoreApplication.translate("SamusReturnsCosmeticPatchesDialog", u"Accept", None))
        self.cancel_button.setText(QCoreApplication.translate("SamusReturnsCosmeticPatchesDialog", u"Cancel", None))
    # retranslateUi

