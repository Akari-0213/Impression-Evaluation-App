import pathlib
from psychopy import visual, core, event
from impress import Impressions

class EachQuestions:
    def __init__(self, win: visual.Window, image: pathlib.Path):
        self.image_stim = visual.ImageStim(
            win, 
            image=image,
            size=(2, 2 * 125/1115),
            pos=(0, 0.65) #上限1.0に合わせる
        )
        self.a_ques = Impressions(win, left_name="するどい", right_name="まるい",  y_pos=0.3)
        self.b_ques = Impressions(win, left_name="かたい", right_name="やわらかい", y_pos=0.1)
        self.c_ques = Impressions(win, left_name="ちかよりがたい", right_name="したしみやすい", y_pos=-0.1)
        self.d_ques = Impressions(win, left_name="こうげきてき", right_name="やさしい", y_pos=-0.3)
        self.e_ques = Impressions(win, left_name="ネガティブ", right_name="ポジティブ", y_pos=-0.5)
        self.next_button = visual.ButtonStim(
            win,
            text="次へ",
            pos=(0, -0.7),
            size=(0.2, 0.1),
            font="Meiryo"
        )
    
    def Update(self, win: visual.Window, mouse: event.Mouse):
        list_answer =[] 
        while True:
            self.image_stim.draw()
            self.a_ques.draw()
            self.b_ques.draw()
            self.c_ques.draw()
            self.d_ques.draw()
            self.e_ques.draw()
            if(self.a_ques.get_slidervalue() is not None and self.b_ques.get_slidervalue() is not None 
            and self.c_ques.get_slidervalue() is not None and  self.d_ques.get_slidervalue() is not None 
            and self.e_ques.get_slidervalue() is not None):
                self.next_button.draw()
                if self.next_button.isClicked:
                    while any(mouse.getPressed()):
                        win.flip()
                    break
            win.flip()
            if 'escape' in event.getKeys():
                core.quit()
        list_answer.append(self.a_ques.get_slidervalue())
        list_answer.append(self.b_ques.get_slidervalue())
        list_answer.append(self.c_ques.get_slidervalue())
        list_answer.append(self.d_ques.get_slidervalue())
        list_answer.append(self.e_ques.get_slidervalue())
        return list_answer
