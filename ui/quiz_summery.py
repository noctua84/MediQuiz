import time

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from src.db import Db


class QuizSummery:
    def __init__(self, finished: list, correct: list, wrong: list):
        self.finished_questions = finished
        self.correct_answers = correct
        self.wrong_answers = wrong
        self.db = Db()
        
    def show_quiz_summery_popup(self):
        layout = BoxLayout(orientation="vertical")
        inner_layout = GridLayout(cols=2)
        fq_info_label = Label(text="Beantwortete Fragen: ")
        fq_label = Label(text=str(len(self.finished_questions)))
        ca_info_label = Label(text="Richtig Antwortn: ")
        ca_label = Label(text=str(len(self.correct_answers)))
        wa_info_label = Label(text="Falsche Antworten: ")
        wa_label = Label(text=str(len(self.wrong_answers)))
        
        inner_layout.add_widget(fq_info_label)
        inner_layout.add_widget(fq_label)
        inner_layout.add_widget(ca_info_label)
        inner_layout.add_widget(ca_label)
        inner_layout.add_widget(wa_info_label)
        inner_layout.add_widget(wa_label)
        
        footer_layout = BoxLayout(orientation="horizontal")
        # save_button = Button(text="Ergebnis speichern")
        # save_button.bind(on_press=self.save_stats)
        close_button = Button(text="Schließen", size_hint=(0.3, 0.3))
        
        # footer_layout.add_widget(save_button)
        footer_layout.add_widget(close_button)
        
        layout.add_widget(inner_layout)
        layout.add_widget(footer_layout)
        
        popup = Popup(title="Ergebnis", content=layout)
        popup.open()
        
        close_button.bind(on_press=popup.dismiss)
        
    def save_stats(self):
        if len(self.correct_answers) > 0:
            for question in self.correct_answers:
                self.db.save_stats(question, True, str(int(time.time())))
        
        if len(self.wrong_answers) > 0:
            for question in self.wrong_answers:
                self.db.save_stats(question, False, str(int(time.time())))
    