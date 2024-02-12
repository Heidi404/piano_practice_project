import sys
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtWidgets import QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, \
    QGraphicsTextItem, QWidget, QVBoxLayout, QPushButton, QMainWindow
from PyQt6.QtGui import QBrush, QColor, QPen, QFont
from PyQt6.QtCore import Qt, QTimer, QDateTime, QUrl
from piano_staff import StaffWindow, Note

white_note_names = ["C", "D", "E", "F", "G", "A", "B", "C2", "D2", "E2", "F2", "G2", "A2", "B2"]
black_note_names = ["C#", "D#", "", "F#", "G#", "A#", "", "C#2", "D#2", "", "F#2", "G#2", "A#2", ""]

notes = {
    'C': 'c4.wav', 'C#': 'c#4.wav',
    'D': 'd4.wav', 'D#': 'd#4.wav',
    'E': 'e4.wav', 'F': 'f4.wav',
    'F#': 'f#4.wav', 'G': 'g4.wav',
    'G#': 'g#4.wav', 'A': 'a4.wav',
    'A#': 'a#4.wav', 'B': 'b4.wav',
    'C2': 'c5.wav', 'C#2': 'c#5.wav',
    'D2': 'd5.wav', 'D#2': 'd#5.wav',
    'E2': 'e5.wav', 'F2': 'f5.wav',
    'F#2': 'f#5.wav', 'G2': 'g5.wav',
    'G#2': 'g#5.wav', 'A2': 'a5.wav',
    'A#2': 'a#5.wav', 'B2': 'b5.wav'
}


# MainWindow combines the keyboard window and the staff window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.main = QWidget()
        self.setCentralWidget(self.main)
        self.setGeometry(100, 30, 1000, 600)
        self.setWindowTitle("Piano")
        self.layout = QVBoxLayout()
        self.window1 = Window()
        self.layout.addWidget(self.window1.staff)
        self.layout.addWidget(self.window1)
        self.main.setLayout(self.layout)
        button = QPushButton("Add Rest")
        button.clicked.connect(self.window1.staff.add_rest)
        self.layout.addWidget(button)
        self.setLayout(self.layout)


# Handles mouse events and sound
class Keyboard(QGraphicsRectItem):
    def __init__(self, x, y, width, height, color, name, staff, ypos):
        super().__init__()
        self.sound = QSoundEffect()
        self.color = color
        self.name = name
        self.staff = staff
        self.ypos = ypos
        self.label = QGraphicsTextItem(self.name, self)  # Creating a label for note names
        self.label.setFont(QFont('Times', 16))
        self.label.setPos(15 * 40, 100)
        self.label.hide()
        self.setRect(x, y, width, height)
        self.setBrush(QBrush(QColor(color)))
        self.setPen(QPen(Qt.GlobalColor.black, 1))
        self.note = None
        # Setting up the timer
        self.start_time = None
        self.timer = QTimer()
        self.timer.setSingleShot(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_time = QDateTime.currentDateTime()
            self.timer.start(1000)
            self.setBrush(QBrush(QColor('#306998')))  # Changing the color to blue
            self.label.show()
            self.note = Note(self.name, self.staff, self.ypos, 0)  # Creating a note with 0 duration
            self.play_note(self.name)
        event.accept()

    def play_note(self, name):
        filename = notes[name]
        self.sound.setSource(QUrl.fromLocalFile(f"C:/Users/heidi/PycharmProjects/y2_2023_11548_piano/notes/{filename}"))
        self.sound.play()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.timer.stop()
            if self.start_time is not None:
                end_time = QDateTime.currentDateTime()
                duration_ms = self.start_time.msecsTo(end_time)
                self.note.duration = duration_ms  # Updating the duration
            self.setBrush(QBrush(QColor(self.color)))  # Restoring the original color
            self.label.hide()
            self.sound.stop()  # Stops the sound
            self.staff.add_note_to_staff(self.note)
            event.accept()


class WhiteKey(Keyboard):
    def __init__(self, x, y, width, height, name, staff, ypos):
        super().__init__(x, y, width, height, "#FFFFFF", name, staff, ypos)


class BlackKey(Keyboard):
    def __init__(self, x, y, width, height, name, staff, ypos):
        super().__init__(x, y, width, height, "#000000", name, staff, ypos)


# Draws the keyboard
class Window(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.white_key_width = 40  # Setting values
        self.white_key_height = 200
        self.black_key_width = 20
        self.black_key_height = 120
        self.margin = 30
        self.x = self.margin
        self.y = self.margin
        self.staff = StaffWindow()

        for i, name in enumerate(white_note_names):  # Draws white keys
            ypos = 112 - i * 8  # note y positions range from 112 to 8
            white_key = WhiteKey(self.x, self.y, self.white_key_width, self.white_key_height, name, self.staff, ypos)
            self.scene.addItem(white_key)
            self.x += self.white_key_width

        self.x = 1.5 * self.white_key_width  # Setting a starting point for black keys

        for i, name in enumerate(black_note_names):  # Draws black keys
            if name != "":
                ypos = 112 - i * 8
                black_key = BlackKey(self.x, self.y, self.black_key_width, self.black_key_height,
                                     name, self.staff, ypos)
                self.scene.addItem(black_key)
                self.x += 2 * self.black_key_width
            else:
                self.x += 2 * self.black_key_width

        self.scene.setSceneRect(0, 0, self.x + self.margin, self.white_key_height + 2 * self.margin)
        self.setScene(self.scene)
        self.setGeometry(300, 200, int(self.x + self.margin), self.white_key_height + 2 * self.margin)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
