#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import dmatalgo
import dmatdb
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton,
                             QLineEdit, QLabel, QGridLayout,
                             QTabWidget, QHBoxLayout, QComboBox,
                             QTextBrowser, QSlider, QCheckBox, QLCDNumber)


class UI(QWidget):
    def __init__(self):
        super(UI, self).__init__()
        self.initUI()

    def initUI(self):
        # ウィジェットの外枠の設定
        qtab = QTabWidget()
        qtab.addTab(Tab1Widget(parent=self), '登録フォーム')
        qtab.addTab(Tab2Widget(parent=self), 'チーム編成')
        hbox = QHBoxLayout()
        hbox.addWidget(qtab)
        self.setLayout(hbox)
        self.setGeometry(600, 600, 600, 800)
        self.setWindowTitle('DMAT チーム編成')
        self.show()


class Tab1Widget(QWidget):

    def __init__(self, parent=None):
        super(Tab1Widget, self).__init__(parent)
        self.init_ui()
        self.show()

    def init_ui(self):
        # レイアウト
        layout = QGridLayout()
        # 名前の欄
        self.nline = QLineEdit()
        self.nlabel = QLabel('名前')
        # 職業の欄
        self.sline2 = QLineEdit()
        self.sline = QComboBox()
        self.sline.addItem('')
        self.sline.addItem('doctor')
        self.sline.addItem('nurse')
        self.sline.addItem('staff')
        self.sline.activated[str].connect(self.act)
        self.slabel = QLabel('職業')
        # エリアの欄
        self.aline = QLineEdit()
        self.alabel = QLabel('出動元')
        # 出動可否の欄
        global plist
        plist = []
        self.pline = QLabel()
        self.b1 = QCheckBox('True')
        self.b2 = QCheckBox('False')
        self.plabel = QLabel('出動可否')
        # アウトプットの欄
        self.outputline = QTextBrowser()
        self.outputline.setReadOnly(True)
        # 登録ボタン
        self.button = QPushButton('登録する')
        self.button.clicked.connect(self.register)
        # レイアウト整形
        layout.addWidget(self.nlabel, 0, 0)
        layout.addWidget(self.nline, 0, 1, 1, 6)
        layout.addWidget(self.slabel, 1, 0)
        layout.addWidget(self.sline, 1, 1, 1, 6)
        layout.addWidget(self.alabel, 2, 0)
        layout.addWidget(self.aline, 2, 1, 1, 6)
        layout.addWidget(self.plabel, 3, 0)
        layout.addWidget(self.b1, 3, 1, 1, 1)
        layout.addWidget(self.b2, 3, 2, 1, 1)
        layout.addWidget(self.button, 4, 9)
        layout.addWidget(self.outputline, 4, 0, 3, 8)
        self.setLayout(layout)

    def btnstate(self, b, plist):
        if b.isChecked() is True:
            plist.append(b.text())
            pl = ','.join(map(str, sorted(plist)))
        else:
            plist.remove(b.text())
            pl = ','.join(map(str, plist))
        self.act_che(pl)

    def register(self):
        ntext = self.nline.text()
        atext = self.aline.text()
        stext = self.sline2.text()
        ptext = self.pline.text()
        dmatdb.setContent(ntext, stext, atext, ptext)
        self.outputline.setText(ntext + ',' + stext + ','
                                + atext + ',' + ptext
                                + 'で登録しました')

    def act_che(self, pl):
        self.pline.setText(pl)

    def act(self, stext):
        self.sline2.setText(stext)


class Tab2Widget(QWidget):
    def __init__(self, parent=None):
        super(Tab2Widget, self).__init__(parent)
        self.init_ui()
        self.show()

    def init_ui(self):
        global plist2
        plist2 = []
        # 編成ボタン
        self.button2 = QPushButton('編成する')
        self.button2.clicked.connect(self.teamcomb)
        # 結果の表示
        self.resultline = QTextBrowser()
        # レイアウトの整形
        layout2 = QGridLayout()
        layout2.addWidget(self.button2, 3, 9)
        layout2.addWidget(self.resultline, 3, 0, 3, 8)
        self.setLayout(layout2)

    def btnstate(self, b, plist):
        if b.isChecked() is True:
            plist.append(b.text())
            pl = ','.join(map(str, sorted(plist)))
        else:
            plist.remove(b.text())
            pl = ','.join(map(str, plist))
        self.act_che(pl)

    def act_che(self, pl):
        self.pline.setText(pl)

    def teamcomb(self):
        dmat = dmatalgo.main()
        self.resultline.setText(dmat)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UI()
    sys.exit(app.exec_())
