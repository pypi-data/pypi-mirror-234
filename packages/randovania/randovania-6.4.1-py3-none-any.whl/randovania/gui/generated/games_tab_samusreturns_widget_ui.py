# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'games_tab_samusreturns_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from randovania.gui.widgets.generate_game_widget import *  # type: ignore

class Ui_SamusReturnsGameTabWidget(object):
    def setupUi(self, SamusReturnsGameTabWidget):
        if not SamusReturnsGameTabWidget.objectName():
            SamusReturnsGameTabWidget.setObjectName(u"SamusReturnsGameTabWidget")
        SamusReturnsGameTabWidget.resize(637, 497)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(SamusReturnsGameTabWidget.sizePolicy().hasHeightForWidth())
        SamusReturnsGameTabWidget.setSizePolicy(sizePolicy)
        self.tab_intro = QWidget()
        self.tab_intro.setObjectName(u"tab_intro")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tab_intro.sizePolicy().hasHeightForWidth())
        self.tab_intro.setSizePolicy(sizePolicy1)
        self.intro_layout = QVBoxLayout(self.tab_intro)
        self.intro_layout.setSpacing(6)
        self.intro_layout.setContentsMargins(11, 11, 11, 11)
        self.intro_layout.setObjectName(u"intro_layout")
        self.intro_layout.setSizeConstraint(QLayout.SetMinimumSize)
        self.intro_cover_layout = QHBoxLayout()
        self.intro_cover_layout.setSpacing(6)
        self.intro_cover_layout.setObjectName(u"intro_cover_layout")
        self.game_cover_label = QLabel(self.tab_intro)
        self.game_cover_label.setObjectName(u"game_cover_label")

        self.intro_cover_layout.addWidget(self.game_cover_label)

        self.intro_label = QLabel(self.tab_intro)
        self.intro_label.setObjectName(u"intro_label")
        sizePolicy1.setHeightForWidth(self.intro_label.sizePolicy().hasHeightForWidth())
        self.intro_label.setSizePolicy(sizePolicy1)
        self.intro_label.setWordWrap(True)

        self.intro_cover_layout.addWidget(self.intro_label)


        self.intro_layout.addLayout(self.intro_cover_layout)

        self.quick_generate_button = QPushButton(self.tab_intro)
        self.quick_generate_button.setObjectName(u"quick_generate_button")

        self.intro_layout.addWidget(self.quick_generate_button)

        self.intro_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.intro_layout.addItem(self.intro_spacer)

        SamusReturnsGameTabWidget.addTab(self.tab_intro, "")
        self.tab_generate_game = GenerateGameWidget()
        self.tab_generate_game.setObjectName(u"tab_generate_game")
        SamusReturnsGameTabWidget.addTab(self.tab_generate_game, "")
        self.faq_tab = QWidget()
        self.faq_tab.setObjectName(u"faq_tab")
        self.faq_layout = QGridLayout(self.faq_tab)
        self.faq_layout.setSpacing(6)
        self.faq_layout.setContentsMargins(11, 11, 11, 11)
        self.faq_layout.setObjectName(u"faq_layout")
        self.faq_layout.setContentsMargins(0, 0, 0, 0)
        self.faq_scroll_area = QScrollArea(self.faq_tab)
        self.faq_scroll_area.setObjectName(u"faq_scroll_area")
        self.faq_scroll_area.setWidgetResizable(True)
        self.faq_scroll_area_contents = QWidget()
        self.faq_scroll_area_contents.setObjectName(u"faq_scroll_area_contents")
        self.faq_scroll_area_contents.setGeometry(QRect(0, 0, 631, 468))
        self.gridLayout_8 = QGridLayout(self.faq_scroll_area_contents)
        self.gridLayout_8.setSpacing(6)
        self.gridLayout_8.setContentsMargins(11, 11, 11, 11)
        self.gridLayout_8.setObjectName(u"gridLayout_8")
        self.faq_label = QLabel(self.faq_scroll_area_contents)
        self.faq_label.setObjectName(u"faq_label")
        self.faq_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.faq_label.setWordWrap(True)

        self.gridLayout_8.addWidget(self.faq_label, 0, 0, 1, 1)

        self.faq_scroll_area.setWidget(self.faq_scroll_area_contents)

        self.faq_layout.addWidget(self.faq_scroll_area, 0, 0, 1, 1)

        SamusReturnsGameTabWidget.addTab(self.faq_tab, "")
        self.differences_tab = QScrollArea()
        self.differences_tab.setObjectName(u"differences_tab")
        self.differences_tab.setWidgetResizable(True)
        self.differences_contents = QWidget()
        self.differences_contents.setObjectName(u"differences_contents")
        self.differences_contents.setGeometry(QRect(0, 0, 631, 468))
        self.verticalLayout = QVBoxLayout(self.differences_contents)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.differences_label = QLabel(self.differences_contents)
        self.differences_label.setObjectName(u"differences_label")
        self.differences_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.differences_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.differences_label)

        self.differences_tab.setWidget(self.differences_contents)
        SamusReturnsGameTabWidget.addTab(self.differences_tab, "")
        self.hints_tab = QWidget()
        self.hints_tab.setObjectName(u"hints_tab")
        self.hints_tab_layout = QVBoxLayout(self.hints_tab)
        self.hints_tab_layout.setSpacing(0)
        self.hints_tab_layout.setContentsMargins(11, 11, 11, 11)
        self.hints_tab_layout.setObjectName(u"hints_tab_layout")
        self.hints_tab_layout.setContentsMargins(0, 0, 0, 0)
        self.hints_scroll_area = QScrollArea(self.hints_tab)
        self.hints_scroll_area.setObjectName(u"hints_scroll_area")
        self.hints_scroll_area.setWidgetResizable(True)
        self.hints_scroll_area_contents = QWidget()
        self.hints_scroll_area_contents.setObjectName(u"hints_scroll_area_contents")
        self.hints_scroll_area_contents.setGeometry(QRect(0, 0, 631, 468))
        self.hints_scroll_layout = QVBoxLayout(self.hints_scroll_area_contents)
        self.hints_scroll_layout.setSpacing(6)
        self.hints_scroll_layout.setContentsMargins(11, 11, 11, 11)
        self.hints_scroll_layout.setObjectName(u"hints_scroll_layout")
        self.hints_label = QLabel(self.hints_scroll_area_contents)
        self.hints_label.setObjectName(u"hints_label")
        self.hints_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.hints_label.setWordWrap(True)

        self.hints_scroll_layout.addWidget(self.hints_label)

        self.hints_scroll_area.setWidget(self.hints_scroll_area_contents)

        self.hints_tab_layout.addWidget(self.hints_scroll_area)

        SamusReturnsGameTabWidget.addTab(self.hints_tab, "")
        self.hint_item_names_tab = QWidget()
        self.hint_item_names_tab.setObjectName(u"hint_item_names_tab")
        self.hint_item_names_layout = QVBoxLayout(self.hint_item_names_tab)
        self.hint_item_names_layout.setSpacing(0)
        self.hint_item_names_layout.setContentsMargins(11, 11, 11, 11)
        self.hint_item_names_layout.setObjectName(u"hint_item_names_layout")
        self.hint_item_names_layout.setContentsMargins(0, 0, 0, 0)
        self.hint_item_names_scroll_area = QScrollArea(self.hint_item_names_tab)
        self.hint_item_names_scroll_area.setObjectName(u"hint_item_names_scroll_area")
        self.hint_item_names_scroll_area.setWidgetResizable(True)
        self.hint_item_names_scroll_area.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.hint_item_names_scroll_contents = QWidget()
        self.hint_item_names_scroll_contents.setObjectName(u"hint_item_names_scroll_contents")
        self.hint_item_names_scroll_contents.setGeometry(QRect(0, 0, 631, 468))
        self.hint_item_names_scroll_layout = QVBoxLayout(self.hint_item_names_scroll_contents)
        self.hint_item_names_scroll_layout.setSpacing(6)
        self.hint_item_names_scroll_layout.setContentsMargins(11, 11, 11, 11)
        self.hint_item_names_scroll_layout.setObjectName(u"hint_item_names_scroll_layout")
        self.hint_item_names_label = QLabel(self.hint_item_names_scroll_contents)
        self.hint_item_names_label.setObjectName(u"hint_item_names_label")
        self.hint_item_names_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.hint_item_names_label.setWordWrap(True)

        self.hint_item_names_scroll_layout.addWidget(self.hint_item_names_label)

        self.hint_item_names_tree_widget = QTableWidget(self.hint_item_names_scroll_contents)
        if (self.hint_item_names_tree_widget.columnCount() < 4):
            self.hint_item_names_tree_widget.setColumnCount(4)
        __qtablewidgetitem = QTableWidgetItem()
        self.hint_item_names_tree_widget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.hint_item_names_tree_widget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.hint_item_names_tree_widget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.hint_item_names_tree_widget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        self.hint_item_names_tree_widget.setObjectName(u"hint_item_names_tree_widget")
        self.hint_item_names_tree_widget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.hint_item_names_tree_widget.setSortingEnabled(True)

        self.hint_item_names_scroll_layout.addWidget(self.hint_item_names_tree_widget)

        self.hint_item_names_scroll_area.setWidget(self.hint_item_names_scroll_contents)

        self.hint_item_names_layout.addWidget(self.hint_item_names_scroll_area)

        SamusReturnsGameTabWidget.addTab(self.hint_item_names_tab, "")
        self.hint_locations_tab = QWidget()
        self.hint_locations_tab.setObjectName(u"hint_locations_tab")
        self.hint_tab_layout = QVBoxLayout(self.hint_locations_tab)
        self.hint_tab_layout.setSpacing(6)
        self.hint_tab_layout.setContentsMargins(11, 11, 11, 11)
        self.hint_tab_layout.setObjectName(u"hint_tab_layout")
        self.hint_tab_layout.setContentsMargins(0, 0, 0, 0)
        self.hint_locations_scroll_area = QScrollArea(self.hint_locations_tab)
        self.hint_locations_scroll_area.setObjectName(u"hint_locations_scroll_area")
        self.hint_locations_scroll_area.setWidgetResizable(True)
        self.hint_locations_scroll_area.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.hint_locations_scroll_contents = QWidget()
        self.hint_locations_scroll_contents.setObjectName(u"hint_locations_scroll_contents")
        self.hint_locations_scroll_contents.setGeometry(QRect(0, 0, 631, 468))
        self.hint_scroll_layout = QVBoxLayout(self.hint_locations_scroll_contents)
        self.hint_scroll_layout.setSpacing(6)
        self.hint_scroll_layout.setContentsMargins(11, 11, 11, 11)
        self.hint_scroll_layout.setObjectName(u"hint_scroll_layout")
        self.hint_locations_label = QLabel(self.hint_locations_scroll_contents)
        self.hint_locations_label.setObjectName(u"hint_locations_label")
        self.hint_locations_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.hint_locations_label.setWordWrap(True)

        self.hint_scroll_layout.addWidget(self.hint_locations_label)

        self.hint_locations_tree_widget = QTreeWidget(self.hint_locations_scroll_contents)
        self.hint_locations_tree_widget.setObjectName(u"hint_locations_tree_widget")

        self.hint_scroll_layout.addWidget(self.hint_locations_tree_widget)

        self.hint_locations_scroll_area.setWidget(self.hint_locations_scroll_contents)

        self.hint_tab_layout.addWidget(self.hint_locations_scroll_area)

        SamusReturnsGameTabWidget.addTab(self.hint_locations_tab, "")

        self.retranslateUi(SamusReturnsGameTabWidget)

        SamusReturnsGameTabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SamusReturnsGameTabWidget)
    # setupUi

    def retranslateUi(self, SamusReturnsGameTabWidget):
        self.game_cover_label.setText(QCoreApplication.translate("SamusReturnsGameTabWidget", u"TextLabel", None))
        self.intro_label.setText(QCoreApplication.translate("SamusReturnsGameTabWidget", u"<html><head/><body><p align=\"justify\">Navigate SR388, etc</p></body></html>", None))
        self.quick_generate_button.setText(QCoreApplication.translate("SamusReturnsGameTabWidget", u"Quick generate", None))
        SamusReturnsGameTabWidget.setTabText(SamusReturnsGameTabWidget.indexOf(self.tab_intro), QCoreApplication.translate("SamusReturnsGameTabWidget", u"Introduction", None))
        SamusReturnsGameTabWidget.setTabText(SamusReturnsGameTabWidget.indexOf(self.tab_generate_game), QCoreApplication.translate("SamusReturnsGameTabWidget", u"Play", None))
        self.faq_label.setText(QCoreApplication.translate("SamusReturnsGameTabWidget", u"# updated from code", None))
        SamusReturnsGameTabWidget.setTabText(SamusReturnsGameTabWidget.indexOf(self.faq_tab), QCoreApplication.translate("SamusReturnsGameTabWidget", u"FAQ", None))
        self.differences_label.setText(QCoreApplication.translate("SamusReturnsGameTabWidget", u"<html><head/><body><p>Randovania makes some changes to the original game in order to improve the game experience or to simply fix bugs in the original game.</p><p>TODO</p></body></html>", None))
        SamusReturnsGameTabWidget.setTabText(SamusReturnsGameTabWidget.indexOf(self.differences_tab), QCoreApplication.translate("SamusReturnsGameTabWidget", u"Differences", None))
        self.hints_label.setText(QCoreApplication.translate("SamusReturnsGameTabWidget", u"<html><head/><body><p align=\"justify\">TODO</p></body></html>", None))
        SamusReturnsGameTabWidget.setTabText(SamusReturnsGameTabWidget.indexOf(self.hints_tab), QCoreApplication.translate("SamusReturnsGameTabWidget", u"Hints", None))
        self.hint_item_names_label.setText(QCoreApplication.translate("SamusReturnsGameTabWidget", u"<html><head/><body><p>When items are referenced in a hint, multiple names can be used depending on how precise the hint is. These additional names are not used by hints in Metroid: Samus Returns, but can be used if hinted by another game such as Metroid Prime 2: Echoes.</p><p>The names each item can use are the following: </p></body></html>", None))
        ___qtablewidgetitem = self.hint_item_names_tree_widget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("SamusReturnsGameTabWidget", u"Item", None));
        ___qtablewidgetitem1 = self.hint_item_names_tree_widget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("SamusReturnsGameTabWidget", u"Precise Category", None));
        ___qtablewidgetitem2 = self.hint_item_names_tree_widget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("SamusReturnsGameTabWidget", u"General Category", None));
        ___qtablewidgetitem3 = self.hint_item_names_tree_widget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("SamusReturnsGameTabWidget", u"Broad Category", None));
        SamusReturnsGameTabWidget.setTabText(SamusReturnsGameTabWidget.indexOf(self.hint_item_names_tab), QCoreApplication.translate("SamusReturnsGameTabWidget", u"Hint Item Names", None))
        self.hint_locations_label.setText(QCoreApplication.translate("SamusReturnsGameTabWidget", u"<html><head/><body><p>Hints\n"
"                                                are placed in the game by replacing Logbook scans. The\n"
"                                                following are the scans that may have a hint added to\n"
"                                                them:</p></body></html>\n"
"                                            ", None))
        ___qtreewidgetitem = self.hint_locations_tree_widget.headerItem()
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("SamusReturnsGameTabWidget", u"Location", None));
        SamusReturnsGameTabWidget.setTabText(SamusReturnsGameTabWidget.indexOf(self.hint_locations_tab), QCoreApplication.translate("SamusReturnsGameTabWidget", u"Hints Locations", None))
        pass
    # retranslateUi

