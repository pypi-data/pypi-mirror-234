import os
import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtWebEngineWidgets import *


class Window(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)

        # Add tab widgets to display web tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.setWindowTitle("Spinn Browser")
        self.setCentralWidget(self.tabs)

        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)

        self.setWindowIcon(QIcon(os.path.join(
            "icons", "cil-screen-desktop.png")))
        with open("browser.qss") as f:
            self.setStyleSheet(f.read())

        # Add navigation toolbar
        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(16, 16))
        self.addToolBar(navtb)

        # Add button to navigation toolbar
        back_btn = QAction(QIcon(os.path.join(
            "icons", "cil-arrow-circle-left.png")), "Back", self)
        back_btn.setStatusTip("Back to previous page")
        navtb.addAction(back_btn)
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())

        next_btn = QAction(QIcon(os.path.join(
            "icons", "cil-arrow-circle-right.png")), "Forward", self)
        next_btn.setStatusTip("Forward to next page")
        navtb.addAction(next_btn)
        next_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())

        reload_btn = QAction(QIcon(os.path.join(
            "icons", "cil-reload.png")), "Reload", self)
        reload_btn.setStatusTip("Reload page")
        navtb.addAction(reload_btn)
        reload_btn.triggered.connect(
            lambda: self.tabs.currentWidget().reload())

        home_btn = QAction(QIcon(os.path.join(
            "icons", "cil-home.png")), "Home", self)
        home_btn.setStatusTip("Go home")
        navtb.addAction(home_btn)
        # Navigate to default home page
        home_btn.triggered.connect(self.navigate_home)

        navtb.addSeparator()

        # Add label icon to show the security status of the loaded url
        self.httpsicon = QLabel()
        self.httpsicon.setPixmap(QPixmap(os.path.join(
            "icons", "cil-lock-unlocked.png")))
        navtb.addWidget(self.httpsicon)

        # Add line edit to show and edit urls
        self.urlbar = QLineEdit()
        navtb.addWidget(self.urlbar)

        # Load url when enter button is pressed
        self.urlbar.returnPressed.connect(self.navigate_to_url)

        # Add stop button to stop url loading
        stop_btn = QAction(QIcon(os.path.join(
            "icons", "cil-media-stop.png")), "Stop", self)
        stop_btn.setStatusTip("Stop loading current page")
        navtb.addAction(stop_btn)
        stop_btn.triggered.connect(lambda: self.tabs.currentWidget().stop())

        # Add top menu
        file_menu = self.menuBar().addMenu("&File")
        new_tab_action = QAction(QIcon(os.path.join(
            "icons", "cli-library-add.png")), "New Tab", self)
        new_tab_action.setStatusTip("Open a new tab")
        file_menu.addAction(new_tab_action)
        new_tab_action.triggered.connect(lambda: self.add_new_tab())

        help_menu = self.menuBar().addMenu("&Help")
        navigate_home_action = QAction(QIcon(os.path.join(
            "icons", "cli-exit-to-app.png")), "Homepage", self)
        navigate_home_action.setStatusTip("Go to Spinn Design Homepage")
        help_menu.addAction(navigate_home_action)
        self.add_new_tab(QUrl("http://baidu.com"), "Homepage")
        self.show()

    # Add new web tab
    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl('')
        browser = QWebEngineView()
        browser.setUrl(qurl)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)

        # Add browser event listeners
        browser.urlChanged.connect(
            lambda qurl, browser=browser:
            self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(
            lambda _, i=i, browser=browser:
            self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
        if q.scheme() == "https":
            self.httpsicon.setPixmap(
                QPixmap(os.path.join("icons", "cil-lock-locked.png")))
        else:
            self.httpsicon.setPixmap(
                QPixmap(os.path.join("icons", "cil-lock-unlocked.png")))
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return
        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle(f"{title} - Spinn Browser")

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == '':
            q.setScheme("http")
        self.tabs.currentWidget().setUrl(q)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.baidu.com"))


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Spinn Browser")
    app.setOrganizationName("Spinn Company")
    app.setOrganizationDomain("Spinn.org")

    window = Window()
    app.exec()
    sys.exit()


if __name__ == '__main__':
    main()
