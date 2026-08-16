from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QVariantAnimation, QEasingCurve
from PySide6.QtGui import QPainter, QPen, QColor

class LoadingWidget(QWidget):
    def __init__(self, size=25, outline_width=2.5, color="white", parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.color = QColor(color)
        self.outline_width = outline_width

        self.current_angle = 0
        self.span_angle = 0

        # Красивая нелинейная анимация длины дуги
        self.anim = QVariantAnimation(self)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.setDuration(1500)
        self.anim.setLoopCount(-1) # Бесконечно
        # Эффект плавного ускорения и замедления
        self.anim.setEasingCurve(QEasingCurve.Type.InOutQuad)
        # pylint: disable=no-member
        self.anim.valueChanged.connect(self.update_animation)
        self.anim.start()

    def update_animation(self, value):
        # Вращаем базовый угол
        self.current_angle = (value * 360 * 2) % 360

        # Динамически меняем длину дуги (эффект растяжения)
        if value < 0.5:
            self.span_angle = value * 2 * 270
        else:
            self.span_angle = (1 - value) * 2 * 270

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        w = int(self.outline_width)
        # Настройка кисти (закругленные края линии дают +10 к красоте)
        pen = QPen(self.color, w)
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(pen)

        # Отступаем от краев, чтобы линия не обрезалась
        rect = self.rect().adjusted(w, w, -w, -w)

        # Рисуем дугу (в Qt углы задаются в 1/16 градуса)
        start_angle = int(self.current_angle * 16)
        sweep_angle = int((self.span_angle + 20) * 16) # +20 чтобы дуга не исчезала в ноль

        painter.drawArc(rect, start_angle, sweep_angle)
