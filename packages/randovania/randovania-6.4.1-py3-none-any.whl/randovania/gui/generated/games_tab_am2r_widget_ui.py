# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'games_tab_am2r_widget.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from randovania.gui.widgets.generate_game_widget import *  # type: ignore

class Ui_AM2RGameTabWidget(object):
    def setupUi(self, AM2RGameTabWidget):
        if not AM2RGameTabWidget.objectName():
            AM2RGameTabWidget.setObjectName(u"AM2RGameTabWidget")
        AM2RGameTabWidget.resize(574, 449)
        self.tab_intro = QWidget()
        self.tab_intro.setObjectName(u"tab_intro")
        self.intro_layout = QVBoxLayout(self.tab_intro)
        self.intro_layout.setSpacing(6)
        self.intro_layout.setContentsMargins(11, 11, 11, 11)
        self.intro_layout.setObjectName(u"intro_layout")
        self.intro_cover_layout = QHBoxLayout()
        self.intro_cover_layout.setSpacing(6)
        self.intro_cover_layout.setObjectName(u"intro_cover_layout")
        self.game_cover_label = QLabel(self.tab_intro)
        self.game_cover_label.setObjectName(u"game_cover_label")

        self.intro_cover_layout.addWidget(self.game_cover_label)

        self.intro_label = QLabel(self.tab_intro)
        self.intro_label.setObjectName(u"intro_label")
        self.intro_label.setWordWrap(True)

        self.intro_cover_layout.addWidget(self.intro_label)


        self.intro_layout.addLayout(self.intro_cover_layout)

        self.quick_generate_button = QPushButton(self.tab_intro)
        self.quick_generate_button.setObjectName(u"quick_generate_button")

        self.intro_layout.addWidget(self.quick_generate_button)

        self.intro_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.intro_layout.addItem(self.intro_spacer)

        AM2RGameTabWidget.addTab(self.tab_intro, "")
        self.tab_generate_game = GenerateGameWidget()
        self.tab_generate_game.setObjectName(u"tab_generate_game")
        AM2RGameTabWidget.addTab(self.tab_generate_game, "")
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
        self.faq_scroll_area_contents.setGeometry(QRect(0, 0, 568, 417))
        self.faq_scroll_layout = QGridLayout(self.faq_scroll_area_contents)
        self.faq_scroll_layout.setSpacing(6)
        self.faq_scroll_layout.setContentsMargins(11, 11, 11, 11)
        self.faq_scroll_layout.setObjectName(u"faq_scroll_layout")
        self.faq_label = QLabel(self.faq_scroll_area_contents)
        self.faq_label.setObjectName(u"faq_label")
        self.faq_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.faq_label.setWordWrap(True)

        self.faq_scroll_layout.addWidget(self.faq_label, 0, 0, 1, 1)

        self.faq_scroll_area.setWidget(self.faq_scroll_area_contents)

        self.faq_layout.addWidget(self.faq_scroll_area, 0, 0, 1, 1)

        AM2RGameTabWidget.addTab(self.faq_tab, "")
        self.differences_tab = QWidget()
        self.differences_tab.setObjectName(u"differences_tab")
        self.verticalLayout_2 = QVBoxLayout(self.differences_tab)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.differences_scroll_area = QScrollArea(self.differences_tab)
        self.differences_scroll_area.setObjectName(u"differences_scroll_area")
        self.differences_scroll_area.setWidgetResizable(True)
        self.differences_scroll_contents = QWidget()
        self.differences_scroll_contents.setObjectName(u"differences_scroll_contents")
        self.differences_scroll_contents.setGeometry(QRect(0, 0, 536, 1402))
        self.verticalLayout = QVBoxLayout(self.differences_scroll_contents)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.differences_label = QLabel(self.differences_scroll_contents)
        self.differences_label.setObjectName(u"differences_label")
        self.differences_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.differences_label.setWordWrap(True)

        self.verticalLayout.addWidget(self.differences_label)

        self.differences_scroll_area.setWidget(self.differences_scroll_contents)

        self.verticalLayout_2.addWidget(self.differences_scroll_area)

        AM2RGameTabWidget.addTab(self.differences_tab, "")

        self.retranslateUi(AM2RGameTabWidget)

        AM2RGameTabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(AM2RGameTabWidget)
    # setupUi

    def retranslateUi(self, AM2RGameTabWidget):
        self.game_cover_label.setText(QCoreApplication.translate("AM2RGameTabWidget", u"TextLabel", None))
        self.intro_label.setText(QCoreApplication.translate("AM2RGameTabWidget", u"<html><head/><body><p>Traverse SR-388 and its depths, while collecting Metroid DNA in order to fight the Queen and bring the Baby to the Ship.</p><p>Two blocks will block the path to the Metroid Queen, unless you collected enough DNA. You can find them by defeating major bosses or Metroids. The default settings require you to collect 10 Metroid DNA.</p><p>The final Chozo log will provide a hint for the location of Ice Beam. Additionally, Wisdom Septoggs have settled themselves in some areas which will provide hints for the location of Metroid DNA.</p><p>For more details, check out the <a href=\"tab://FAQ\"><span style=\" text-decoration: underline; color:#007af4;\">FAQ</span></a> and <a href=\"tab://Differences\"><span style=\" text-decoration: underline; color:#007af4;\">Differences</span></a> tabs.</p><p>To get started, use the Quick Generate button to generate a game using the default settings!</p></body></html>", None))
        self.quick_generate_button.setText(QCoreApplication.translate("AM2RGameTabWidget", u"Quick generate", None))
        AM2RGameTabWidget.setTabText(AM2RGameTabWidget.indexOf(self.tab_intro), QCoreApplication.translate("AM2RGameTabWidget", u"Introduction", None))
        AM2RGameTabWidget.setTabText(AM2RGameTabWidget.indexOf(self.tab_generate_game), QCoreApplication.translate("AM2RGameTabWidget", u"Play", None))
        self.faq_label.setText(QCoreApplication.translate("AM2RGameTabWidget", u"# updated from code", None))
        AM2RGameTabWidget.setTabText(AM2RGameTabWidget.indexOf(self.faq_tab), QCoreApplication.translate("AM2RGameTabWidget", u"FAQ", None))
        self.differences_label.setText(QCoreApplication.translate("AM2RGameTabWidget", u"<html><head/><body><p>Randovania makes some changes to the original game in order to improve the game experience or to simply fix bugs in the original game.<br/>Many changes are optional and can be disabled in the options Randovania provides, but the following are <span style=\" font-weight:600;\">always</span> there:</p><ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The game will now use a different save directory.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The lava progression system has been changed. There is no lava in the game tied to Metroids anymore, which means you can access any area. However, in order to reach the Queen, you now have to collect 46 total DNA, with Randovania having an option on how much DNA you want to start with / stil"
                        "l need to collect. If you do not have the needed DNA, and try to reach the Queen, you will be met with two blocks standing in the way.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Due to killing Metroids not being as important now, the HUD now shows how much DNA is still needed to reach the Queen or how much total DNA you have collected, depending on the DNA setting in the display settings.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">All Metroids now give you items when they die.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The Charge Beam weakness for Metroids have been slightly revamped. They can now always be hit with Charge Beam (but all other Beams disabled), instead of having to need 0 Missiles / Super Missiles.</li><li style=\" margin-top:12px; margin-bottom"
                        ":12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The stats on the map screen have been revamped. They now show your current Health / Ammo and total Health / Ammo, instead of the amount of expansions you collected / total amount of expansions. A current DNA / total DNA counter has also been added.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">An option has been added to the pause menu that allows loading your last save from your starting location.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The final Chozo log entry in the Genetics Laboratory has been changed to give an Ice Beam hint.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Hints have been placed to reveal the location of DNA. These Hints are given by Wisdom Septoggs. Their locati"
                        "ons can be found in the FAQ.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">All Doors have been changed to use the look they have in Distribution Center. Their sprites have also been changed for accessibility reasons.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Normal Game, New Game+ and Random Game+ have all been replaced with a &quot;Randovania&quot; mode.</li></ul><ul style=\"margin-top: 0px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; -qt-list-indent: 1;\"><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Higher Difficulties don't reduce the amount of ammo per expansion. If you want that functionality, use Randovania's built-in feature to reduce the amount of ammo per expansion.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-rig"
                        "ht:0px; -qt-block-indent:0; text-indent:0px;\">Fusion Mode has been slightly revamped. The in-game difficulty has been changed to only deal 4x damage and is now named &quot;Brutal&quot;. The option to add the X Parasites and play with the Fusion Suit has been moved to a Randovania setting. This means, it is now possible to play with a 4x damage multiplier without the X Parasites, or to play with the X Parasites on Normal.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Brutal difficulty, the extra settings, and the ability to show the ammo stats on the pause screen don't require you to finish the game once, but instead are all unlocked by default.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The &quot;Varia Suit obtained&quot; cutscene was missing a visual effect; this has been restored.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-le"
                        "ft:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">When going through a Missile / Super Missile / Power Bomb door from behind, you automatically clear that door, without needing to hit it with the appropriate weapon.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Fighting the Tester before activating the Tower now enlightens the room during the fight.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Proboscums will be active without needing to activate the Tower.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Defeating Tester does not automatically enable the Tower anymore.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">EMP puzzles don't unlock all doors in the room anymore, but o"
                        "nly relevant ones.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The door to Plasma Chamber will now be blue after defeating Tester, instead of red.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Larva Metroids will now always give ammo drops when necessary, instead of having a small chance to drop nothing.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The file selection screen will now show a hash of the current seed.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The Item in Gravity Chamber will now always be in the open, with the Gravity Pod cutscene being disabled.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0p"
                        "x;\">The bomb blocks in &quot;The Tower - Tower Exterior North&quot; will now always be gone if you come from the &quot;Dark Maze&quot; room.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">When going down the Elevator from GFS Thoth, the Power Bomb Blocks will be automatically gone if you haven't cleared them before, as otherwise you'd be stuck.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Long Range Activation has been enabled for every room, allowing for more Zip strats.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">In GFS Thoth, both sides on the &quot;Thoth Bridge&quot; now have doors added for better Door Lock Randomizer compatibility.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">In"
                        " Hydro Station, the connection from &quot;Water Turbine Station&quot; to &quot;Hydro Station Exterior&quot; now has a door for better Door Lock Randomizer compatibility.</li><li style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The Geothermal Power Plant is always in its exploded state. The Power Bomb Expansion that was located there has been moved to &quot;Power Plant Destroyed Shaft&quot;.</li></ul></body></html>", None))
        AM2RGameTabWidget.setTabText(AM2RGameTabWidget.indexOf(self.differences_tab), QCoreApplication.translate("AM2RGameTabWidget", u"Differences", None))
        pass
    # retranslateUi

