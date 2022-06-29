from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup

from src.model import Question


class CheckAnswer:
    def __init__(self):
        self.question = None
        self.correct_answers = []
        self.wrong_answers = []
    
    def set_question(self, question: Question):
        self.question = question
        
    def show_check_answer_popup(self, answer: str):
        layout = BoxLayout(orientation="vertical")
        inner_layout = GridLayout(cols=2)
        q_info_label = Label(text="Frage: ")
        q_label = Label(text=self.question.question_text)
        a_info_label = Label(text="Erwartete Antwort: ")
        a_label = Label(text=self.question.answer)
        ga_info_label = Label(text="Gegebene Antwort: ")
        ga_label = Label(text=answer)
        
        footer_layout = BoxLayout(orientation="horizontal")
        y_button = Button(text="Richtig", size_hint=(0.3, 0.3))
        n_button = Button(text="Falsch", size_hint=(0.3, 0.3))
        c_button = Button(text="Schließen", size_hint=(0.3, 0.3))
        
        y_button.bind(on_press=self.correct)
        n_button.bind(on_press=self.wrong)
        
        footer_layout.add_widget(y_button)
        footer_layout.add_widget(n_button)
        footer_layout.add_widget(c_button)
        
        inner_layout.add_widget(q_info_label)
        inner_layout.add_widget(q_label)
        inner_layout.add_widget(a_info_label)
        inner_layout.add_widget(a_label)
        inner_layout.add_widget(ga_info_label)
        inner_layout.add_widget(ga_label)
        
        layout.add_widget(inner_layout)
        layout.add_widget(footer_layout)
        
        popup = Popup(title="Überprüfen", content=layout)
        popup.open()
        
        c_button.bind(on_press=popup.dismiss)
    
    def correct(self, kwargs):
        self.correct_answers.append(self.question)
    
    def wrong(self, kwargs):
        self.wrong_answers.append(self.question)
        