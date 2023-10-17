# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preset_am2r_goal.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_PresetAM2RGoal(object):
    def setupUi(self, PresetAM2RGoal):
        if not PresetAM2RGoal.objectName():
            PresetAM2RGoal.setObjectName(u"PresetAM2RGoal")
        PresetAM2RGoal.resize(1196, 274)
        self.centralWidget = QWidget(PresetAM2RGoal)
        self.centralWidget.setObjectName(u"centralWidget")
        self.centralWidget.setMaximumSize(QSize(16777215, 16777215))
        self.goal_layout = QVBoxLayout(self.centralWidget)
        self.goal_layout.setSpacing(6)
        self.goal_layout.setContentsMargins(11, 11, 11, 11)
        self.goal_layout.setObjectName(u"goal_layout")
        self.goal_layout.setContentsMargins(4, 8, 4, 8)
        self.description_label = QLabel(self.centralWidget)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setWordWrap(True)

        self.goal_layout.addWidget(self.description_label)

        self.dna_slider_layout = QHBoxLayout()
        self.dna_slider_layout.setSpacing(6)
        self.dna_slider_layout.setObjectName(u"dna_slider_layout")
        self.dna_slider = QSlider(self.centralWidget)
        self.dna_slider.setObjectName(u"dna_slider")
        self.dna_slider.setMaximum(46)
        self.dna_slider.setPageStep(2)
        self.dna_slider.setOrientation(Qt.Horizontal)
        self.dna_slider.setTickPosition(QSlider.TicksBelow)

        self.dna_slider_layout.addWidget(self.dna_slider)

        self.dna_slider_label = QLabel(self.centralWidget)
        self.dna_slider_label.setObjectName(u"dna_slider_label")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dna_slider_label.sizePolicy().hasHeightForWidth())
        self.dna_slider_label.setSizePolicy(sizePolicy)
        self.dna_slider_label.setMinimumSize(QSize(20, 0))
        self.dna_slider_label.setAlignment(Qt.AlignCenter)

        self.dna_slider_layout.addWidget(self.dna_slider_label)


        self.goal_layout.addLayout(self.dna_slider_layout)

        self.placement_group = QGroupBox(self.centralWidget)
        self.placement_group.setObjectName(u"placement_group")
        self.placement_layout = QVBoxLayout(self.placement_group)
        self.placement_layout.setSpacing(6)
        self.placement_layout.setContentsMargins(11, 11, 11, 11)
        self.placement_layout.setObjectName(u"placement_layout")
        self.placement_label = QLabel(self.placement_group)
        self.placement_label.setObjectName(u"placement_label")
        self.placement_label.setWordWrap(True)

        self.placement_layout.addWidget(self.placement_label)

        self.prefer_metroids_check = QCheckBox(self.placement_group)
        self.prefer_metroids_check.setObjectName(u"prefer_metroids_check")

        self.placement_layout.addWidget(self.prefer_metroids_check)

        self.prefer_bosses_check = QCheckBox(self.placement_group)
        self.prefer_bosses_check.setObjectName(u"prefer_bosses_check")

        self.placement_layout.addWidget(self.prefer_bosses_check)


        self.goal_layout.addWidget(self.placement_group)

        self.spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.goal_layout.addItem(self.spacer)

        PresetAM2RGoal.setCentralWidget(self.centralWidget)

        self.retranslateUi(PresetAM2RGoal)

        QMetaObject.connectSlotsByName(PresetAM2RGoal)
    # setupUi

    def retranslateUi(self, PresetAM2RGoal):
        PresetAM2RGoal.setWindowTitle(QCoreApplication.translate("PresetAM2RGoal", u"Goal", None))
        self.description_label.setText(QCoreApplication.translate("PresetAM2RGoal", u"<html><head/><body><p>In addition to just collecting the Baby, it's now necessary to collect Metroid DNA in order to reach the Queen.</p></body></html>", None))
        self.dna_slider_label.setText(QCoreApplication.translate("PresetAM2RGoal", u"0", None))
        self.placement_group.setTitle(QCoreApplication.translate("PresetAM2RGoal", u"Placement", None))
        self.placement_label.setText(QCoreApplication.translate("PresetAM2RGoal", u"<html><head/><body><p>The following options limit where Metroid DNA will be placed. There can only be as many DNA shuffled as there are preferred locations enabled, with a limit of 46 total DNA to be shuffled. The first option adds 46 preferred locations, the second 6.</p></body></html>", None))
        self.prefer_metroids_check.setText(QCoreApplication.translate("PresetAM2RGoal", u"Prefer Metroids (23 Alphas, 15 Gammas, 4 Zetas, 4 Omegas)", None))
        self.prefer_bosses_check.setText(QCoreApplication.translate("PresetAM2RGoal", u"Prefer Bosses (Guardian, Arachnus, Torizo, The Tester, Serris and Genesis)", None))
    # retranslateUi

