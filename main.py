import sys
import io

from PyQt5 import uic
from PyQt5.QtGui import QPixmap, QFontDatabase
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout

from urllib.request import urlopen

import api
import apidb


class TrackElement(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # uic.loadUi("track_element.ui", self)
        uic.loadUi("untitled.ui", self)


class ArtistElement(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("artist_element.ui", self)


class AlbumElement(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("album_element.ui", self)


class SongApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui.ui", self)

        QFontDatabase.addApplicationFont('futura/unicode.futurab.ttf')
        QFontDatabase.addApplicationFont('futura/futura light bt.ttf')

        self.search_bar_text = ''
        self.search_bar.editingFinished.connect(self.search, Qt.QueuedConnection)

        self.widget = QWidget()
        self.vbox = QVBoxLayout()
        self.scroll_area_setup()

    def scroll_area_setup(self):
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.widget)

        self.widget.setLayout(self.vbox)
        self.vbox.addStretch()

    def search(self):
        if self.search_bar.text() == self.search_bar_text:
            return
        self.search_bar_text = self.search_bar.text()

        #data = api.search(self.search_bar.text())
        data = apidb.search(self.search_bar.text())
        print(f'tracks: {len(data["track"])} albums: {len(data["album"])} artists: {len(data["artist"])}')

        layout = self.vbox
        for i in reversed(range(layout.count() - 1)):
            layout.itemAt(i).widget().setParent(None)

        print('widget fucking..')
        # for element in data:
        #     if element['type'] == 'artist':
        #         widget = ArtistElement(self)
        #     else:
        #         if element['type'] == 'album':
        #             widget = AlbumElement(self)
        #
        #             element['name'] = self.shorten_long_text(element['name'], 18)
        #             element['artist'] = self.shorten_long_text(element['artist'], 24)
        #         else:
        #             widget = TrackElement(self)
        #
        #             widget.duration.setText(element['duration'])
        #
        #             widget.frame.setStyleSheet("QFrame {background-color: rgb(235, 235, 235)};")
        #
        #             self.stylize_widget(widget)
        #
        #         widget.artist.setText(element['artist'])
        #
        #     widget.name.setText(element['name'])
        #     self.set_cover(element['cover'], widget)
        #
        #     if widget:
        #         layout.insertWidget(layout.count() - 1, widget)


        for track in data['track']:
            print(track['name'])
            widget = TrackElement(self)

            widget.duration.setText(track['duration'])
            widget.artist.setText(track['artist'])

            widget.name.setText(track['name'])
            self.set_cover(track['cover'], widget)

            widget.frame.setStyleSheet("QFrame {background-color: rgb(235, 235, 235)};")
            self.stylize_widget(widget)

            if widget:
                layout.insertWidget(layout.count() - 1, widget)

        row = QHBoxLayout()
        for album in data['album'][:4]:
            print(album)
            widget = AlbumElement(self)

            album['name'] = self.shorten_long_text(album['name'], 18)
            album['artist'] = self.shorten_long_text(album['artist'], 24)

            widget.artist.setText(album['artist'])

            widget.name.setText(album['name'])
            self.set_cover(album['cover'], widget)

            row.addWidget(widget)
        layout.insertLayout(layout.count() - 1, row)



    def shorten_long_text(self, text, max_length):
        if len(text) > max_length:
            return text[:max_length - 1] + '...'
        return text

    def set_cover(self, url, widget):
        data = urlopen(url).read()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        pixmap = pixmap.scaled(widget.picture.minimumWidth(), widget.picture.minimumHeight(), Qt.KeepAspectRatio,
                               Qt.SmoothTransformation)
        widget.picture.setPixmap(pixmap)

    def stylize_widget(self, widget):
        widget.button.setStyleSheet("""
        QPushButton {  background-color: rgb(0, 0, 0, 0); } 
        QPushButton:hover {  background-color: rgb(0, 0, 0, 50); }""")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SongApp()
    ex.show()
    sys.exit(app.exec())
