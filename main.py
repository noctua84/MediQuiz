from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager

from src.db import Db


class MainWindow(Screen):
    pass


class QuizWindow(Screen):
    pass


class AddQuestionWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


window_config = Builder.load_file("quiz.kv")
manager = WindowManager()
screens = [MainWindow(name="main"), QuizWindow(name="quiz"), AddQuestionWindow(name="add_question")]

for screen in screens:
    manager.add_widget(screen)

manager.current = "main"


class MediQuizApp(App):
    def build(self):
        return manager
    

if __name__ == "__main__":
    MediQuizApp().run()
