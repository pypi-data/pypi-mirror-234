# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preset_msr_patches.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_PresetMSRPatches(object):
    def setupUi(self, PresetMSRPatches):
        if not PresetMSRPatches.objectName():
            PresetMSRPatches.setObjectName(u"PresetMSRPatches")
        PresetMSRPatches.setEnabled(True)
        PresetMSRPatches.resize(642, 535)
        self.root_widget = QWidget(PresetMSRPatches)
        self.root_widget.setObjectName(u"root_widget")
        self.root_widget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout = QVBoxLayout(self.root_widget)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area = QScrollArea(self.root_widget)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setMinimumSize(QSize(438, 0))
        self.scroll_area.setWidgetResizable(True)
        self.scroll_contents = QWidget()
        self.scroll_contents.setObjectName(u"scroll_contents")
        self.scroll_contents.setGeometry(QRect(0, 0, 640, 533))
        self.scroll_contents.setMinimumSize(QSize(0, 469))
        self.scroll_layout = QVBoxLayout(self.scroll_contents)
        self.scroll_layout.setSpacing(6)
        self.scroll_layout.setContentsMargins(11, 11, 11, 11)
        self.scroll_layout.setObjectName(u"scroll_layout")
        self.scroll_layout.setContentsMargins(0, 2, 0, 0)
        self.top_spacer = QSpacerItem(20, 8, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.scroll_layout.addItem(self.top_spacer)

        self.environment_group = QGroupBox(self.scroll_contents)
        self.environment_group.setObjectName(u"environment_group")
        self.verticalLayout_3 = QVBoxLayout(self.environment_group)
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.area3_interior_shortcut_no_grapple_check = QCheckBox(self.environment_group)
        self.area3_interior_shortcut_no_grapple_check.setObjectName(u"area3_interior_shortcut_no_grapple_check")

        self.verticalLayout_3.addWidget(self.area3_interior_shortcut_no_grapple_check)

        self.area3_interior_shortcut_no_grapple_label = QLabel(self.environment_group)
        self.area3_interior_shortcut_no_grapple_label.setObjectName(u"area3_interior_shortcut_no_grapple_label")
        self.area3_interior_shortcut_no_grapple_label.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.area3_interior_shortcut_no_grapple_label)

        self.elevator_grapple_blocks_check = QCheckBox(self.environment_group)
        self.elevator_grapple_blocks_check.setObjectName(u"elevator_grapple_blocks_check")

        self.verticalLayout_3.addWidget(self.elevator_grapple_blocks_check)

        self.elevator_grapple_blocks_label = QLabel(self.environment_group)
        self.elevator_grapple_blocks_label.setObjectName(u"elevator_grapple_blocks_label")
        self.elevator_grapple_blocks_label.setMouseTracking(True)
        self.elevator_grapple_blocks_label.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.elevator_grapple_blocks_label)

        self.surface_crumbles_check = QCheckBox(self.environment_group)
        self.surface_crumbles_check.setObjectName(u"surface_crumbles_check")

        self.verticalLayout_3.addWidget(self.surface_crumbles_check)

        self.surface_crumbles_label = QLabel(self.environment_group)
        self.surface_crumbles_label.setObjectName(u"surface_crumbles_label")
        self.surface_crumbles_label.setMouseTracking(True)
        self.surface_crumbles_label.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.surface_crumbles_label)

        self.area1_crumbles_check = QCheckBox(self.environment_group)
        self.area1_crumbles_check.setObjectName(u"area1_crumbles_check")

        self.verticalLayout_3.addWidget(self.area1_crumbles_check)

        self.area1_crumbles_label = QLabel(self.environment_group)
        self.area1_crumbles_label.setObjectName(u"area1_crumbles_label")
        self.area1_crumbles_label.setMouseTracking(True)
        self.area1_crumbles_label.setWordWrap(True)

        self.verticalLayout_3.addWidget(self.area1_crumbles_label)


        self.scroll_layout.addWidget(self.environment_group)

        self.misc_group = QGroupBox(self.scroll_contents)
        self.misc_group.setObjectName(u"misc_group")
        self.verticalLayout_2 = QVBoxLayout(self.misc_group)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.nerf_power_bombs_check = QCheckBox(self.misc_group)
        self.nerf_power_bombs_check.setObjectName(u"nerf_power_bombs_check")

        self.verticalLayout_2.addWidget(self.nerf_power_bombs_check)

        self.nerf_power_bombs_label = QLabel(self.misc_group)
        self.nerf_power_bombs_label.setObjectName(u"nerf_power_bombs_label")
        self.nerf_power_bombs_label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.nerf_power_bombs_label)

        self.nerf_super_missiles_check = QCheckBox(self.misc_group)
        self.nerf_super_missiles_check.setObjectName(u"nerf_super_missiles_check")

        self.verticalLayout_2.addWidget(self.nerf_super_missiles_check)

        self.nerf_super_missiles_label = QLabel(self.misc_group)
        self.nerf_super_missiles_label.setObjectName(u"nerf_super_missiles_label")
        self.nerf_super_missiles_label.setWordWrap(True)

        self.verticalLayout_2.addWidget(self.nerf_super_missiles_label)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.scroll_layout.addWidget(self.misc_group)

        self.scroll_area.setWidget(self.scroll_contents)

        self.verticalLayout.addWidget(self.scroll_area)

        PresetMSRPatches.setCentralWidget(self.root_widget)

        self.retranslateUi(PresetMSRPatches)

        QMetaObject.connectSlotsByName(PresetMSRPatches)
    # setupUi

    def retranslateUi(self, PresetMSRPatches):
        PresetMSRPatches.setWindowTitle(QCoreApplication.translate("PresetMSRPatches", u"Other", None))
        self.environment_group.setTitle(QCoreApplication.translate("PresetMSRPatches", u"Room Changes", None))
        self.area3_interior_shortcut_no_grapple_check.setText(QCoreApplication.translate("PresetMSRPatches", u"Grapple Block in Area 3 - Transport to Area 3 Interior West", None))
        self.area3_interior_shortcut_no_grapple_label.setText(QCoreApplication.translate("PresetMSRPatches", u"<html><head/><body><p>Removes the Grapple Block in the room next to the elevator to Area 3 Interior West in Area 3 Interior East, allowing earlier access from this side.</p></body></html>", None))
        self.elevator_grapple_blocks_check.setText(QCoreApplication.translate("PresetMSRPatches", u"Grapple Blocks leaving areas", None))
        self.elevator_grapple_blocks_label.setText(QCoreApplication.translate("PresetMSRPatches", u"<html><head/><body><p>Removes the Grapple Blocks that are near the exit elevators of certain areas. These include:</p><ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" margin-top:12px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Area 4 West to Area 4 East </li><li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Area 5 Entrance to Area 6 </li><li style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Area 6 to Area 7 </li><li style=\" margin-top:0px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Area 7 to Area 8 </li></ul></body></html>", None))
        self.surface_crumbles_check.setText(QCoreApplication.translate("PresetMSRPatches", u"Crumble Blocks in Surface - One-Way Drop", None))
        self.surface_crumbles_label.setText(QCoreApplication.translate("PresetMSRPatches", u"Changes the Crumble Blocks after Scan Pulse to Power Beam Blocks, allowing for a two-way path through the room. This makes this section less dangerous without Charge Beam.", None))
        self.area1_crumbles_check.setText(QCoreApplication.translate("PresetMSRPatches", u"Crumble Blocks in Area 1 - Chozo Seal", None))
        self.area1_crumbles_label.setText(QCoreApplication.translate("PresetMSRPatches", u"Changes the Crumble Blocks leaving Area 1 to Power Beam Blocks, allowing for earlier access to Area 2 with only Morph Ball. This helps make item placement less restrictive.", None))
        self.misc_group.setTitle(QCoreApplication.translate("PresetMSRPatches", u"Miscellaneous", None))
        self.nerf_power_bombs_check.setText(QCoreApplication.translate("PresetMSRPatches", u"Nerf Power Bombs", None))
        self.nerf_power_bombs_label.setText(QCoreApplication.translate("PresetMSRPatches", u"Removes the Power Bomb weakness from beam doors. This gives each respective beam more logical value.", None))
        self.nerf_super_missiles_check.setText(QCoreApplication.translate("PresetMSRPatches", u"Nerf Super Missiles", None))
        self.nerf_super_missiles_label.setText(QCoreApplication.translate("PresetMSRPatches", u"Removes the Super Missile weakness from Missile doors.", None))
    # retranslateUi

