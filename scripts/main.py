import csv
import datetime
import pathlib
from psychopy import visual, core, gui, event
from impress import Impressions
from each_images import EachQuestions

CSV_PATH = pathlib.Path(__file__ + "/../../data/result_K_impression.csv")
SETTINGS_ONNRYOU = pathlib.Path(__file__ + "/../../settings/ONNRYOU_images")


def start_settings(sub_info_list: list[any]) -> None:
    subj_info = {"被験者番号": ""}
    dialogue_box = gui.DlgFromDict(subj_info, order = ["被験者番号"])
    if dialogue_box.OK:
        subj_id:str = subj_info["被験者番号"]
    else:
        core.quit()
    
    now = datetime.datetime.now()
    sub_info_list.append(subj_id)
    sub_info_list.append(now.strftime("%Y%m%d %H:%M"))
    if not CSV_PATH.exists():
        CSV_PATH.parents[0].mkdir(parents=True, exist_ok=True)
        CSV_PATH.touch()


def question_all(win: visual.Window, ques_text: str, mouse: event.Mouse) -> list[any]:
    list_answer =[] 
    ques_text = visual.TextStim(
        win,
        text= ques_text,
        pos=(0, 0.7)
    )
    a_ques = Impressions(win, left_name="するどい", right_name="まるい",  y_pos=0.3)
    b_ques = Impressions(win, left_name="かたい", right_name="やわらかい", y_pos=0.1)
    c_ques = Impressions(win, left_name="ちかよりがたい", right_name="したしみやすい", y_pos=-0.1)
    d_ques = Impressions(win, left_name="こうげきてき", right_name="やさしい", y_pos=-0.3)
    e_ques = Impressions(win, left_name="ネガティブ", right_name="ポジティブ", y_pos=-0.5)
    next_button = visual.ButtonStim(
        win,
        text="次へ",
        pos=(0, -0.7),
        size=(0.2, 0.1),
        font="Meiryo"
    )

    while True:
        ques_text.draw()
        a_ques.draw()
        b_ques.draw()
        c_ques.draw()
        d_ques.draw()
        e_ques.draw()
        if(a_ques.get_slidervalue() is not None and b_ques.get_slidervalue() is not None 
           and c_ques.get_slidervalue() is not None and  d_ques.get_slidervalue() is not None 
           and e_ques.get_slidervalue() is not None):
            next_button.draw()
            if next_button.isClicked:
                while any(mouse.getPressed()):
                    win.flip()
                break
        if 'escape' in event.getKeys():
            core.quit()
        win.flip()
    
    list_answer.append(a_ques.get_slidervalue())
    list_answer.append(b_ques.get_slidervalue())
    list_answer.append(c_ques.get_slidervalue())
    list_answer.append(d_ques.get_slidervalue())
    list_answer.append(e_ques.get_slidervalue())
    return list_answer


def second_inst(win) -> None:
    inst_stim = visual.TextStim(
        win,
        text="今から，先ほどの物語を\n一文ずつ印象評定してください"
    )
    next_step_button = visual.ButtonStim(
        win,
        text="次へ",
        pos=(0, -0.7),
        size=(0.2, 0.1),
        font="Meiryo"
    )
    
    while True:
        inst_stim.draw()
        next_step_button.draw()
        if next_step_button.isClicked:
            break
        win.flip()
        if 'escape' in event.getKeys():
            core.quit()



def finished(win: visual.Window, list_sub_info: list[any]) -> None:
    inst_stim = visual.TextStim(win)
    inst_text = "これにて終了です。\nありがとうございました。"
    inst_stim.setText(inst_text)
    inst_stim.draw()
    win.flip()
    
    if CSV_PATH.exists() and CSV_PATH.stat().st_size > 0:
        with open(CSV_PATH, mode='r+b') as f:
            f.seek(-1, 2)          # ファイルの最後の1バイトに移動
            if f.read(1) != b'\n': # 最後が改行コードで終わっていない場合
                f.write(b'\n')
    
    with open(CSV_PATH, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(list_sub_info)
    core.wait(5)


def get_images()-> list[pathlib.Path]:
    images_path = [file for file in SETTINGS_ONNRYOU.iterdir() if file.name.startswith("K_")]
    return images_path


def main() -> None:
    sub_info_list = []
    start_settings(sub_info_list)
    win = visual.Window(fullscr=True, monitor="testMonitor", units="norm")
    mouse = event.Mouse()
    list_answer=question_all(win, "さきほどの物語の全体的な\n印象評価をしてください", mouse)
    sub_info_list.extend(list_answer)
    second_inst(win)

    setting_images = get_images()
    for image in setting_images:
        list_answer= []
        question = EachQuestions(win, image)
        list_answer = question.Update(win, mouse)
        sub_info_list.extend(list_answer)
    list_answer = []
    list_answer=question_all(win, "最後にもう一度物語の全体的な\n印象評価をしてください", mouse)
    sub_info_list.extend(list_answer)
    finished(win, list_sub_info=sub_info_list)
    win.close()


if __name__ == "__main__":
    main()
