from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.metrics import dp

# Допустимый диапазон диаметра (в пикселях)
MIN_DIAMETER = 10
MAX_DIAMETER = 500

# Набор доступных цветов: (название, RGB)
COLORS = [
    ("Синий",    (0.1, 0.4, 0.9)),
    ("Красный",  (0.9, 0.15, 0.15)),
    ("Зелёный",  (0.15, 0.7, 0.2)),
    ("Жёлтый",   (0.95, 0.8, 0.1)),
    ("Фиолетовый", (0.6, 0.2, 0.8)),
    ("Чёрный",   (0.05, 0.05, 0.05)),
]


class CircleCanvas(Widget):
    """Виджет, на котором рисуется круг."""

    def draw_circle(self, diameter, color_rgb):
        self.canvas.clear()
        with self.canvas:
            Color(*color_rgb, 1)
            # Рисуем круг по центру виджета
            x = self.center_x - diameter / 2
            y = self.center_y - diameter / 2
            Ellipse(pos=(x, y), size=(diameter, diameter))


class CircleApp(App):
    def build(self):
        self.title = "Рисование круга"
        self.selected_color = COLORS[0][1]  # синий по умолчанию

        root = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Верхняя панель: поле ввода + кнопка "Нарисовать"
        controls = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(50), spacing=dp(10))

        self.diameter_input = TextInput(
            hint_text=f"Диаметр ({MIN_DIAMETER}-{MAX_DIAMETER})",
            multiline=False,
            input_filter='float',
        )
        controls.add_widget(self.diameter_input)

        draw_button = Button(text="Нарисовать", size_hint=(None, 1), width=dp(140))
        draw_button.bind(on_press=self.on_draw_pressed)
        controls.add_widget(draw_button)

        root.add_widget(controls)

        # Панель выбора цвета
        color_panel = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(50), spacing=dp(6))
        self.color_buttons = []
        for name, rgb in COLORS:
            btn = Button(text=name, background_color=(*rgb, 1))
            btn.bind(on_press=self.make_color_handler(rgb))
            color_panel.add_widget(btn)
            self.color_buttons.append(btn)
        root.add_widget(color_panel)

        # Метка для сообщений об ошибках / статуса
        self.status_label = Label(text="Выбран цвет: Синий", size_hint=(1, None), height=dp(30))
        root.add_widget(self.status_label)

        # Холст для рисования круга
        self.canvas_widget = CircleCanvas()
        root.add_widget(self.canvas_widget)

        return root

    def make_color_handler(self, rgb):
        """Возвращает функцию-обработчик нажатия для конкретного цвета."""
        def handler(instance):
            self.selected_color = rgb
            self.status_label.color = (1, 1, 1, 1)
            self.status_label.text = f"Выбран цвет: {instance.text}"
        return handler

    def on_draw_pressed(self, instance):
        text = self.diameter_input.text.strip()

        if not text:
            self.status_label.color = (1, 0, 0, 1)
            self.status_label.text = "Введите значение диаметра."
            return

        try:
            diameter = float(text)
        except ValueError:
            self.status_label.color = (1, 0, 0, 1)
            self.status_label.text = "Ошибка: нужно ввести число."
            return

        if diameter < MIN_DIAMETER or diameter > MAX_DIAMETER:
            self.status_label.color = (1, 0, 0, 1)
            self.status_label.text = f"Ошибка: диапазон {MIN_DIAMETER}-{MAX_DIAMETER}."
            return

        self.status_label.color = (1, 1, 1, 1)
        self.status_label.text = ""
        self.canvas_widget.draw_circle(diameter, self.selected_color)


if __name__ == "__main__":
    CircleApp().run()
