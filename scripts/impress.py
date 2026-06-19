from psychopy import visual


class Impressions:
    def __init__(self, win: visual.Window, left_name: str, right_name: str, y_pos: float):

        self.left = visual.TextStim(
            win,
            text= left_name,
            pos=(-0.7, y_pos)
        )
        self.right = visual.TextStim(
            win,
            text= right_name,
            pos=(0.7, y_pos)
        )
        self.rating_slider = visual.Slider(
            win,
            ticks=(1, 2, 3, 4, 5),
            labels=('1', '2', '3', '4', '5'),
            labelColor=win.color,
            style='radio',
            pos=(0, y_pos),
            size=(0.8, 0.1) 
        )
    

    def draw(self) -> None:
        self.left.draw()
        self.right.draw()
        self.rating_slider.draw()


    def get_slidervalue(self) -> any:
        value = self.rating_slider.getRating()
        return value
