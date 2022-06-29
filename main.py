import random

from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import ListProperty, BooleanProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.screenmanager import Screen, ScreenManager, NoTransition

from src.db import Db
from src.model import init_orm, Question
from ui.check_answer import CheckAnswer
from ui.quiz_summery import QuizSummery

Config.set("graphics", "width", 800)
Config.set("graphics", "height", 600)

db = Db()
engine = db.engine
list_of_questions = []
question_count = 0


class MainWindow(BoxLayout):
    
    def btn_start(self):
        self.manager.current = "start"
        self.manager.transition = NoTransition()
    
    def btn_prepare_quiz(self):
        self.manager.current = "prepare_quiz"
        self.manager.transition = NoTransition()
    
    def btn_questions(self):
        self.manager.current = "questions"
        self.manager.transition = NoTransition()


class StartScreen(Screen):
    pass


class QuizWindow(Screen):
    global list_of_questions, question_count
    
    def __init__(self, **kwargs):
        super(QuizWindow, self).__init__(**kwargs)
        
        self.db = Db()
        self.finished_questions = []
        self.check = CheckAnswer()
        self.finish_count = 0
    
    def btn_quiz(self):
        global list_of_questions, question_count
        
        self.finished_questions = []
        self.finish_count = 0
        
        if len(list_of_questions) > 0:
            self.question.text = list_of_questions[0].question_text
        else:
            list_of_questions = db.get_questions()
            question_count = len(list_of_questions)
            self.question.text = list_of_questions[0].question_text
            self.answer.text = ""
    
    def btn_next_question(self):
        self.finish_count += 1
        print(self.question.text)
        print(self.answer.text)
        
        if len(list_of_questions) > 0:
            self.check.set_question(list_of_questions[0])
            self.check.show_check_answer_popup(self.answer.text)
            
        # store finished question, remove it from current active list and display next one.
        
            print(len(list_of_questions))
        
            self.finished_questions.append(list_of_questions[0])
            list_of_questions.pop(0)
        
        if len(list_of_questions) > 0:
            self.question.text = list_of_questions[0].question_text
            self.answer.text = ""
        
        if self.finish_count == question_count + 1:
            stats = QuizSummery(self.finished_questions, self.check.correct_answers, self.check.wrong_answers)
            stats.show_quiz_summery_popup()
            

class QuestionsWindow(Screen):
    global db
    
    def btn_save_question(self):
        cur_question = Question()
        cur_question.question_text = self.question.text
        cur_question.answer = self.answer.text
        cur_question.year = 1
        cur_question.section = 1
        
        db.save_question(cur_question)
        
        self.question.text = ""
        self.answer.text = ""
        
    def btn_show_question_list(self):
        global list_of_questions
        list_of_questions = db.get_questions()
        parent = self.parent
        parent.current = "question_list"
        

class QuestionListWindow(Screen):
    questions = ListProperty([])
    
    def btn_display_question_list(self):
        global list_of_questions
        self.questions = list_of_questions


class SelectableQuestionListItem(RecycleDataViewBehavior, GridLayout):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    cols = 3
    cur_question = None

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.question.text = data.get('raw').question_text
        self.answer.text = data.get('raw').answer
        
        return super(SelectableQuestionListItem, self).refresh_view_attrs(rv, index, data)
    
    def on_touch_down(self, touch):
        if super(SelectableQuestionListItem, self).on_touch_down(touch):
            return True
        
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)
        
    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected
            
    def btn_delete_question(self):
        global db
        cur_question = self.parent.parent.data[self.index]["raw"]
        self.parent.parent.data.pop(self.index)
        db.delete_question(cur_question.id)
        

class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass


class PrepareQuizWindow(Screen):
    
    def btn_start_quiz(self):
        global list_of_questions, db, question_count
        list_of_questions = db.get_questions()
        random.shuffle(list_of_questions)
        question_count = len(list_of_questions)
        parent = self.parent
        parent.current = "quiz"


class Manager(ScreenManager):
    pass


Builder.load_file("quiz.kv")


class MediQuizApp(App):
    def build(self):
        global engine
        init_orm(engine)
        
        app = MainWindow()
        return app
    

if __name__ == "__main__":
    MediQuizApp().run()
