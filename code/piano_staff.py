from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QBrush, QPixmap
from PyQt6.QtGui import QPainterPath, QPen
from PyQt6.QtCore import QPointF
from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsPathItem, \
    QGraphicsPixmapItem


# Handles the staff
class StaffWindow(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.width = 1000
        self.height = 200
        self.current_x = 60
        self.note_counter = 0
        self.bar_length = 140
        self.create_staff()

    def create_staff(self):
        # Creating the initial staff lines
        path = QPainterPath()
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor("black"))
        y = 38
        for i in range(5):
            path.moveTo(QPointF(0, y))
            path.lineTo(QPointF(self.width, y))
            y += 16
        self.scene.addPath(path, pen)
        self.add_clef()

        self.setGeometry(300, 70, self.width, self.height)
        self.setScene(self.scene)
        self.show()

    def add_note_to_staff(self, note):
        self.add_sharp(note)  # checks if sharp is needed
        if 600 <= note.duration < 1500:  # half note
            if self.note_counter % 4 == 3:  # checking if connecting line is needed
                self.add_quarter_note(note)
                self.add_connecting_line(note, 1)
                self.add_bar_line()
                if self.current_x + self.bar_length > self.width:
                    self.update_staff()  # Adding length to the staff if needed
                self.current_x += 20
                self.add_quarter_note(note)
            else:
                self.add_half_note(note)

        elif 1500 <= note.duration < 2300:  # 3/4 note
            if self.note_counter % 4 == 2:
                self.add_half_note(note)
                self.add_connecting_line(note, 2)
                self.add_bar_line()
                if self.current_x + self.bar_length > self.width:
                    self.update_staff()
                self.current_x += 20
                self.add_quarter_note(note)

            elif self.note_counter % 4 == 3:
                self.add_quarter_note(note)
                self.add_connecting_line(note, 1)
                self.add_bar_line()
                if self.current_x + self.bar_length > self.width:
                    self.update_staff()  # Adding length to the staff if needed
                self.current_x += 20
                self.add_half_note(note)
            else:
                self.add_three_quarter_note(note)

        elif 2300 <= note.duration:  # whole note
            # checking how note should be drawn based on the space left in the bar
            if self.note_counter % 4 == 1:
                self.add_three_quarter_note(note)
                self.add_connecting_line(note, 3)
                self.add_bar_line()
                if self.current_x + self.bar_length > self.width:
                    self.update_staff()  # Adding length to the staff if needed
                self.current_x += 20
                self.add_quarter_note(note)

            elif self.note_counter % 4 == 2:
                self.add_half_note(note)
                self.add_connecting_line(note, 2)
                self.add_bar_line()
                if self.current_x + self.bar_length > self.width:
                    self.update_staff()  # Adding length to the staff if needed
                self.current_x += 20
                self.add_half_note(note)

            elif self.note_counter % 4 == 3:
                self.add_quarter_note(note)
                self.add_connecting_line(note, 1)
                self.add_bar_line()
                if self.current_x + self.bar_length > self.width:
                    self.update_staff()  # Adding length to the staff if needed
                self.current_x += 20
                self.add_three_quarter_note(note)
            else:
                self.add_whole_note(note)
        else:
            self.add_quarter_note(note)

        if self.note_counter % 4 == 0:
            self.add_bar_line()  # Adding bar lines every 4 notes
            if self.current_x + self.bar_length > self.width:
                self.update_staff()
            self.current_x += 20

        self.horizontalScrollBar().setValue(self.current_x)  # Keeps the scrollbar on the right side

    def add_quarter_note(self, note):
        self.add_lines(note)
        note_pic = QGraphicsEllipseItem(0, 0, 12, 12)
        note_pic.setBrush(QBrush(Qt.GlobalColor.black))
        self.note_counter += 1
        note_width = 10
        note_x = self.current_x
        self.current_x += note_width + 20  # Updating x-position
        note_pic.setPos(note_x, note.y)
        self.scene.addItem(note_pic)

    def add_half_note(self, note):
        self.add_lines(note)
        note_pic = QGraphicsEllipseItem(0, 0, 12, 12)
        note_pic.setPen(QPen(Qt.GlobalColor.black))
        note_pic.setBrush(QBrush(Qt.GlobalColor.white))
        self.note_counter += 2
        note_width = 20
        note_x = self.current_x
        self.current_x += note_width + 40
        note_pic.setPos(note_x, note.y)
        self.scene.addItem(note_pic)

    def add_three_quarter_note(self, note):
        self.add_lines(note)
        note_pic = QGraphicsEllipseItem(0, 0, 12, 12)
        note_pic.setPen(QPen(Qt.GlobalColor.black))
        note_pic.setBrush(QBrush(Qt.GlobalColor.white))

        self.note_counter += 3
        note_width = 30
        note_x = self.current_x
        self.current_x += note_width + 60
        note_pic.setPos(note_x, note.y)
        dot = QGraphicsEllipseItem(self.current_x - 72, note.y + 7, 3, 3)  # dot for 3/4 note
        dot.setPen(QPen(Qt.GlobalColor.black))
        dot.setBrush(QBrush(Qt.GlobalColor.black))
        self.scene.addItem(dot)
        self.scene.addItem(note_pic)

    def add_whole_note(self, note):
        note_pic = QGraphicsEllipseItem(0, 0, 14, 12)
        note_pic.setPen(QPen(Qt.GlobalColor.black))
        note_pic.setBrush(QBrush(Qt.GlobalColor.white))
        if note.y == 112 or note.y == 16:  # Horizontal line for C, C#, A2 and A#2
            horizontal_line = QGraphicsLineItem(self.current_x - 3, note.y + 6, self.current_x + 17, note.y + 6)
            self.scene.addItem(horizontal_line)
        elif note.y == 8:  # horizontal line for B2
            horizontal_line = QGraphicsLineItem(self.current_x - 3, note.y + 12, self.current_x + 15, note.y + 12)
            self.scene.addItem(horizontal_line)
        self.note_counter += 4
        note_width = 40
        note_x = self.current_x
        self.current_x += note_width + 80
        note_pic.setPos(note_x, note.y)
        self.scene.addItem(note_pic)

    def add_lines(self, note):
        if note.y >= 72:   # Draws vertical line for notes below lower A
            vertical_line = QGraphicsLineItem(self.current_x + 12, note.y + 6, self.current_x + 12, note.y - 30)
            self.scene.addItem(vertical_line)
        else:  # Draws vertical line for notes above B
            vertical_line = QGraphicsLineItem(self.current_x, note.y + 6, self.current_x, note.y + 36)
            self.scene.addItem(vertical_line)
        if note.y == 112 or note.y == 16:  # Horizontal line for C, C#, A2 and A#2
            horizontal_line = QGraphicsLineItem(self.current_x - 3, note.y + 6, self.current_x + 15, note.y + 6)
            self.scene.addItem(horizontal_line)
        elif note.y == 8:  # horizontal line for B2
            horizontal_line = QGraphicsLineItem(self.current_x - 3, note.y + 12, self.current_x + 15, note.y + 12)
            self.scene.addItem(horizontal_line)

    def add_rest(self):
        image = QPixmap("C:/Users/heidi/PycharmProjects/y2_2023_11548_piano/images/rest.png").scaled(16, 45)
        pixmap_item = QGraphicsPixmapItem(image)
        self.note_counter += 1
        note_width = 10
        note_x = self.current_x
        self.current_x += note_width + 20
        pixmap_item.setPos(note_x, 45)
        self.scene.addItem(pixmap_item)
        if self.note_counter % 4 == 0:
            self.add_bar_line()  # Adding bar lines every 4 notes
            if self.current_x + self.bar_length > self.width:
                self.update_staff()  # Adding length to the staff if needed
            self.current_x += 20
        self.horizontalScrollBar().setValue(self.current_x)

    def add_bar_line(self):
        vertical_line = QGraphicsLineItem(self.note_counter / 4 * self.bar_length + 40,
                                          38, self.note_counter / 4 * self.bar_length + 40, 102)
        self.scene.addItem(vertical_line)

    def add_sharp(self, note):
        if note.name in ["C#", "D#", "F#", "G#", "A#", "C#2", "D#2", "F#2", "G#2", "A#2"]:
            image = QPixmap("C:/Users/heidi/PycharmProjects/y2_2023_11548_piano/images/sharp.png").scaled(8, 18)
            pixmap_item = QGraphicsPixmapItem(image)
            pixmap_item.setPos(self.current_x - 12, note.y-3)
            self.scene.addItem(pixmap_item)

    def add_clef(self):
        image = QPixmap("C:/Users/heidi/PycharmProjects/y2_2023_11548_piano/images/clef.png").scaled(55, 100)
        pixmap_item = QGraphicsPixmapItem(image)
        pixmap_item.setPos(0, 20)
        self.scene.addItem(pixmap_item)

    def add_connecting_line(self, note, flag):
        path = QPainterPath()
        if flag == 1:
            start = self.current_x - 20
            end = self.current_x + 20
        elif flag == 2:
            start = self.current_x - 50
            end = self.current_x + 20
        else:
            start = self.current_x - 80
            end = self.current_x + 20
        mid_point = start + (end - start) / 2
        path.moveTo(start, note.y + 14)
        path.quadTo(mid_point, note.y + 20, end, note.y + 14)
        path_item = QGraphicsPathItem(path)
        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(1)
        path_item.setPen(pen)
        self.scene.addItem(path_item)

    def update_staff(self):
        path = QPainterPath()
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor("black"))
        y = 38
        for i in range(5):
            path.moveTo(QPointF(self.current_x, y))
            path.lineTo(QPointF(self.current_x + self.bar_length, y))
            y += 16
        self.scene.addPath(path, pen)


class Note(QGraphicsEllipseItem):
    def __init__(self, name, staff, y, duration):
        super().__init__()
        self.name = name
        self.staff = staff
        self.y = y
        self.duration = duration
