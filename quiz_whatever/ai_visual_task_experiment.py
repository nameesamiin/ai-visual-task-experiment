import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk, ImageOps
import time
import csv
import os
from datetime import datetime

APP_TITLE = "How Do We Make Decisions in AI-Supported Visual Tasks?"
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 900
QUESTION_TIME_LIMIT = 30
AI_APPEAR_TIME = 10
IMAGE_MAX_WIDTH = 900
IMAGE_MAX_HEIGHT = 500
AI_FONT_SIZE = 16
BODY_FONT_SIZE = 14
SMALL_FONT_SIZE = 13
TITLE_FONT_SIZE = 26
SUBHEADER_FONT_SIZE = 16

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

QUESTIONNAIRE_ITEMS = [
    "I am easily influenced by other people’s opinions",
    "I can be influenced by a good commercial",
    "When someone coughs or sneezes, I usually feel the urge to do the same",
    "Imagining a refreshing drink can make me thirsty",
    "A good salesperson can really make me want their product",
    "I get a lot of good practical advice from magazines or TV",
    "If a product is nicely displayed, I usually want to buy it",
    "When I see someone shiver, I often feel a chill myself",
    "I get my style from certain celebrities",
    "When people tell me how they feel, I often notice that I feel the same way",
    "When making a decision, I often follow other people’s advice",
    "Reading descriptions of tasty dishes can make my mouth water",
    "I get many good ideas from others",
    "I frequently change my opinion after talking with others",
    "After I see a commercial for lotion, sometimes my skin feels dry",
    "I discovered many of my favorite things through my friends",
    "I follow current fashion trends",
    "Thinking about something scary can make my heart pound",
    "I have picked-up many habits from my friends",
    "If I am told I don’t look well, I start feeling ill",
    "It is important for me to fit in",
]

QUESTIONNAIRE_SCALE = [
    ("1", "not at all\nor very slightly"),
    ("2", "a little"),
    ("3", "somewhat"),
    ("4", "quite a bit"),
    ("5", "a lot"),
]

QUESTIONS = [
    {"id": 1,  "image": "1.png",  "options": ["A", "B", "C", "D"], "correct": "A"},
    {"id": 2,  "image": "2.png",  "options": ["A", "B", "C", "D"], "correct": "D"},
    {"id": 3,  "image": "3.png",  "options": ["A", "B", "C", "D"], "correct": "A"},
    {"id": 4,  "image": "4.png",  "options": ["A", "B", "C", "D"], "correct": "A"},
    {"id": 5,  "image": "5.png",  "options": ["A", "B", "C", "D"], "correct": "D"},
    {"id": 6,  "image": "6.png",  "options": ["A", "B", "C", "D"], "correct": "C"},
    {"id": 7,  "image": "7.png",  "options": ["A", "B", "C", "D"], "correct": "D"},
    {"id": 8,  "image": "8.png",  "options": ["A", "B", "C", "D"], "correct": "A"},
    {"id": 9,  "image": "9.png",  "options": ["A", "B", "C", "D"], "correct": "B"},
    {"id": 10, "image": "10.png", "options": ["A", "B", "C", "D"], "correct": "C"},
    {"id": 11, "image": "11.png", "options": ["A", "B", "C", "D"], "correct": "C"},
    {"id": 12, "image": "12.png", "options": ["A", "B", "C", "D"], "correct": "D"},
    {"id": 13, "image": "13.png", "options": ["A", "B", "C", "D"], "correct": "D"},
    {"id": 14, "image": "14.png", "options": ["A", "B", "C", "D"], "correct": "B"},
    {"id": 15, "image": "15.png", "options": ["A", "B", "C", "D"], "correct": "B"},
    {"id": 16, "image": "16.png", "options": ["A", "B", "C", "D"], "correct": "B"},
    {"id": 17, "image": "17.png", "options": ["A", "B", "C", "D"], "correct": "B"},
    {"id": 18, "image": "18.png", "options": ["A", "B", "C", "D"], "correct": "D"},
    {"id": 19, "image": "19.png", "options": ["A", "B", "C", "D"], "correct": "D"},
    {"id": 20, "image": "20.png", "options": ["A", "B", "C", "D"], "correct": "C"},
    {"id": 21, "image": "21.png", "options": ["A", "B", "C", "D"], "correct": "A"},
    {"id": 22, "image": "22.png", "options": ["A", "B", "C", "D"], "correct": "C"},
    {"id": 23, "image": "23.png", "options": ["A", "B", "C", "D"], "correct": "B"},
    {"id": 24, "image": "24.png", "options": ["A", "B", "C", "D"], "correct": "C"},
    {"id": 25, "image": "25.png", "options": ["A", "B", "C", "D"], "correct": "D"},
    {"id": 26, "image": "26.png", "options": ["A", "B", "C", "D"], "correct": "C"},
    {"id": 27, "image": "27.png", "options": ["A", "B", "C", "D"], "correct": "D"},
    {"id": 28, "image": "28.png", "options": ["A", "B", "C", "D"], "correct": "B"},
    {"id": 29, "image": "29.png", "options": ["A", "B", "C", "D"], "correct": "D"},
    {"id": 30, "image": "30.png", "options": ["A", "B", "C", "D"], "correct": "B"},
]

NO_AI = {3, 6, 9, 12, 15, 18, 21, 24, 27, 30}
AI_CORRECT = {1, 4, 7, 10, 13, 16, 19, 22, 25, 28}
AI_INCORRECT = {2, 5, 8, 11, 14, 17, 20, 23, 26, 29}

for q in QUESTIONS:
    if q["id"] in NO_AI:
        q["condition"] = "no_ai"
        q["ai_suggestion"] = ""
    elif q["id"] in AI_CORRECT:
        q["condition"] = "ai_correct"
        q["ai_suggestion"] = q["correct"]
    else:
        q["condition"] = "ai_incorrect"
        wrong_options = [x for x in q["options"] if x != q["correct"]]
        q["ai_suggestion"] = wrong_options[0]

WELCOME_TEXT = (
    "Welcome to the visual tasks experiment! This is a short 30 minute experiment in which you will complete "
    "30 simple visual tasks, then you will answer a short questionnaire. Please click the next button to read through "
    "the Participant Information Sheet."
)

PIS_SECTIONS = [
    ("The title of the research project", "How Do We Make Decisions in AI-Supported Visual Tasks?"),
    ("What is the purpose of the research?", '''The research is organized by Namis Mansour, Postgraduate Student studying Clinical and Developmental Neuropsychology at the School of Psychology at Bournemouth University as part of the Psychology Project Unit. As a student dissertation project, this work is supervised by Dr. Ala Yankouskaya.

In this study, you will complete simple visual tasks where an AI tool, such as ChatGPT or Gemini, is involved. You will be asked to respond to visual questions and be shown suggestions produced by the AI during the task.

This helps us better understand how people work with AI tools in decision making.'''),
    ("Why have I been invited?", "We are looking to recruit 44 participants. You have been invited because you are a university student between the ages of 18 to 25 years old, are fluent in English, and you do not have diagnosed cognitive or neurological disorder(s)."),
    ("Do I have to take part?", '''It is up to you to decide whether or not to take part. If you do decide to take part, you will have access to this information sheet to read. We want you to understand what participation involves, before you make a decision on whether to participate.

If you or any family member have an on-going relationship with BU or the research team, e.g. as a member of staff, as student or other service user, your decision on whether to take part (or continue to take part) will not affect this relationship and/or your studies at BU in any way.

You can withdraw from participation at any time and without giving a reason, simply by closing the browser page. Should you choose to withdraw your data after completing the experiment, you may do so by contacting the researcher.

If you withdraw after spending less than 15 minutes in the study, you will not be compensated. However, if you have spent more than 15 minutes, you will be compensated the full amount.'''),
    ("How long will the experiment take to complete?", "We anticipate that the experiment will take 30 minutes to complete. If you are a BU Psychology student, you will be compensated with 0.50 SONA credits for your time. If you are a non-BU student, your participation is still greatly appreciated, and you are more than welcome to contribute to this study."),
    ("What are the advantages and possible disadvantages or risks of taking part?", '''This is simply a virtual task. It is not a test, we will not use it to judge your abilities or skills. While there are no personal benefits, taking part in this study helps us learn more about how people work with AI tools when it comes to decision making.

The task is safe and there are no expected risks, however, some people might feel a little challenged or pressed for time during the tasks. Don’t worry! The virtual tasks are designed to be simple and fair, with basic pattern recognition and skills that everyone can do.'''),
    ("What type of information will be sought from me and why is the collection of this information relevant for achieving the research project’s objectives?", "Your age and sex assigned at birth will be collected and will only be used to describe the group of participants. No other personal or identifiable information will be collected."),
    ("Use of my information", '''The information collected from this task will be analyzed as part of the dissertation project. Your age and sex assigned at birth will only be used to describe the group of people taking part.

You can withdraw from participation at any point by closing your browser window. Once your response has been submitted, your identity and answers are anonymized, so withdrawal of data is impossible.

The information collected may be used to support other research projects in the future and access to it in this form will not be restricted, however, your identity will remain anonymous. It will not be possible for you to be identified from this data.'''),
    ("Sharing and further use of your personal information", '''We will share your personal information only with BU staff and the BU student(s) working on the research project.

Research results will be included in a final year Psychology Dissertation that will not be made freely available.

While anonymity is prioritized, the research team is committed to maintaining a respectful environment in line with research ethical guidelines and thus participants are also expected to engage in this study responsibly. Instances of misuse, harassment, or inappropriate behaviour, may exceptionally lead to revoking participants’ anonymity in order to uphold the integrity of the research process.'''),
    ("Contact for further information", "If you have any questions or would like further information, please contact Researcher Namis Mansour at s5822244@bournemouth.ac.uk, or Supervisor Ala Yankouskaya at ayankouskaya@bournemouth.ac.uk."),
    ("In case of complaints", "Any concerns about the study should be directed to Supervisor Ala Yankouskaya, ayankouskaya@bournemouth.ac.uk. If your concerns have not been answered by Dr. Ala, you should contact Professor Scott Wright, Associate Dean for Research, Innovation and Enterprise in the Faculty of Media, Science and Technology, Bournemouth University by email to researchgovernance@bournemouth.ac.uk."),
    ("Consent to Participate", "Please indicate that you have read and understood the Participant Information Sheet for this research project and that you consent to take part in this questionnaire before continuing."),
    ("Ethics ID", "68531"),
]

INSTRUCTION_TEXT = (
    "This is a thirty minute task. You have thirty seconds to choose one answer from four options. "
    "Some tasks will include AI suggestions, and some will not. Once you have completed the tasks, you will answer a short questionnaire. "
    "Please remember this is not an intelligence test, this is simply a visual task. Click next to begin!"
)

TASKS_DONE_TEXT = "Tasks completed, well done! Please fill up the questionnaire on the next screen."

DEBRIEF_SECTIONS = [
    ("The title of the research project", "How Do We Make Decisions in AI-Supported Visual Tasks?"),
    ("Aims of the study", "The study aims to test how decisions are made while completing simple visual tasks that involve the usage of AI. Previous studies have investigated the effects of AI, but further research is needed to explore how AI can affect decision making."),
    ("Deception", '''In this study, you answered a series of visual questions. For each question, you had 30 seconds to choose one answer from four options. You completed 30 questions in total. For some of the questions, an AI system showed a suggested answer on the screen. Sometimes this suggestion matched the correct answer, and sometimes it did not. You could choose whether or not to follow the AI’s suggestion when selecting your answer. We looked at how people responded to the questions when an AI suggestion was shown compared to when it was not.

Please note that this is not an intelligence test and was not designed to test your intellectual abilities. There were no right or wrong ways to approach it. All data will remain anonymous and confidential and will only be shared between the researcher and supervisor.'''),
    ("Withdrawal Process", "Please remember that all data is anonymous, so withdrawal after completion is not possible."),
    ("Contact for further information", "If you have any questions or would like further information, please contact the researcher at s5822244@bournemouth.ac.uk, or the supervisor at ayankouskaya@bournemouth.ac.uk."),
    ("In case of complaints", "Any concerns about the study should be directed to s5822244@bournemouth.ac.uk. If your queries have not been resolved, you are welcome to contact Prof Tiantian Zhang, Deputy Dean for Research & Professional Practice, Faculty of Science and Technology, Bournemouth University by email to researchgovernance@bournemouth.ac.uk."),
]

END_TEXT = "Thank you so much for your participation! Your credits will be transferred as soon as possible!"


def ensure_folders():
    os.makedirs(DATA_DIR, exist_ok=True)


def clean_colored_highlights(image):
    image = image.convert("RGB")
    pixels = image.load()
    width, height = image.size
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            max_c = max(r, g, b)
            min_c = min(r, g, b)
            if (max_c - min_c) > 18 and max_c > 80:
                pixels[x, y] = (255, 255, 255)
    return image


def load_clean_question_image(path):
    image = Image.open(path)
    image = clean_colored_highlights(image)
    image = image.convert("L")
    image = ImageOps.autocontrast(image)
    image.thumbnail((IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT))
    return ImageTk.PhotoImage(image)


def render_sectioned_text(parent, sections):
    for header, body in sections:
        tk.Label(parent, text=header, font=("Arial", SUBHEADER_FONT_SIZE, "bold"), bg="white", fg="black", anchor="w", justify="left").pack(anchor="w", pady=(0, 4))
        tk.Label(parent, text=body, wraplength=1080, justify="left", font=("Arial", BODY_FONT_SIZE), bg="white", fg="black").pack(anchor="w", pady=(0, 14))


class ScrollableFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        canvas = tk.Canvas(self, highlightthickness=0, bg="white")
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.inner = tk.Frame(canvas, bg="white")
        self.inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        self.canvas = canvas


class ExperimentApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight()
        window_w = max(1150, min(screen_w - 80, 1400))
        window_h = max(760, min(screen_h - 120, 950))
        self.geometry(f"{window_w}x{window_h}+40+40")
        self.minsize(1150, 760)
        self.configure(bg="white")

        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("TFrame", background="white")
        style.configure("TLabel", background="white", foreground="black", font=("Arial", BODY_FONT_SIZE))
        style.configure("TButton", font=("Arial", BODY_FONT_SIZE))
        style.configure("TRadiobutton", background="white", foreground="black", font=("Arial", BODY_FONT_SIZE))
        style.configure("TCheckbutton", background="white", foreground="black", font=("Arial", BODY_FONT_SIZE))
        style.configure("TCombobox", font=("Arial", BODY_FONT_SIZE))

        self.current_frame = None
        self.timer_job = None
        self.image_ref = None

        self.participant_info = {
            "participant_id": datetime.now().strftime("P%Y%m%d%H%M%S"),
            "age": "",
            "sex_assigned_at_birth": ""
        }

        self.trial_results = []
        self.questionnaire_results = []
        self.question_index = 0

        self.selected_answer = tk.StringVar(value="")
        self.question_start_time = None
        self.time_remaining = QUESTION_TIME_LIMIT
        self.ai_shown = False
        self.ai_show_time = None
        self.answer_history = []
        self.answer_change_log = []
        self.finished_question = False
        self.questionnaire_vars = []

        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.after(100, self.finish_window_setup)

    def finish_window_setup(self):
        self.lift()
        self.focus_force()
        self.update_idletasks()
        self.show_welcome()

    def clear_frame(self):
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None
        if self.current_frame is not None:
            self.current_frame.destroy()

    def bottom_right_button(self, parent, text, command):
        row = ttk.Frame(parent)
        row.pack(side="bottom", fill="x", padx=20, pady=20)
        ttk.Button(row, text=text, command=command).pack(side="right")

    def show_welcome(self):
        self.clear_frame()
        frame = ttk.Frame(self, padding=40)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        center = ttk.Frame(frame)
        center.place(relx=0.5, rely=0.45, anchor="center")
        ttk.Label(center, text=APP_TITLE, font=("Arial", TITLE_FONT_SIZE, "bold"), justify="center").pack(pady=(0, 25))
        ttk.Label(center, text=WELCOME_TEXT, wraplength=900, justify="center", font=("Arial", BODY_FONT_SIZE)).pack()

        self.bottom_right_button(frame, "Next", self.show_pis)

    def show_pis(self):
        self.clear_frame()
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        ttk.Label(frame, text="Participant Information Sheet", font=("Arial", 22, "bold")).pack(pady=(0, 10))
        scroll = ScrollableFrame(frame)
        scroll.pack(fill="both", expand=True)
        render_sectioned_text(scroll.inner, PIS_SECTIONS)

        self.consent_yes = tk.BooleanVar(value=False)
        self.consent_no = tk.BooleanVar(value=False)
        self.data_access = tk.BooleanVar(value=False)

        ttk.Checkbutton(scroll.inner, text="I have read and understood the Participant Information Sheet and consent to take part in this study", variable=self.consent_yes).pack(anchor="w", pady=6)
        ttk.Checkbutton(scroll.inner, text="I do not consent to take part in this study [exit at this point]", variable=self.consent_no).pack(anchor="w", pady=6)
        ttk.Checkbutton(scroll.inner, text="I give permission for members of the Research Team to have access to my anonymised responses. I understand that my anonymised responses may be reproduced in reports, academic publications and presentations but I will not be identified or identifiable.", variable=self.data_access).pack(anchor="w", pady=8)

        self.bottom_right_button(frame, "Next", self.validate_pis)

    def validate_pis(self):
        if self.consent_no.get():
            self.destroy()
            return
        if not self.consent_yes.get():
            messagebox.showwarning("Consent required", "Please tick the consent box before continuing.")
            return
        if not self.data_access.get():
            messagebox.showwarning("Permission required", "Please tick the anonymised data access box before continuing.")
            return
        self.show_demographics()

    def show_demographics(self):
        self.clear_frame()
        frame = ttk.Frame(self, padding=40)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        center = ttk.Frame(frame)
        center.place(relx=0.5, rely=0.42, anchor="center")
        ttk.Label(center, text="Please indicate your age and sex assigned at birth", font=("Arial", 22, "bold"), justify="center").pack(pady=(0, 30))

        age_row = ttk.Frame(center)
        age_row.pack(pady=10)
        ttk.Label(age_row, text="Age:", font=("Arial", BODY_FONT_SIZE)).pack(side="left", padx=(0, 10))
        self.age_var = tk.StringVar(value="18")
        ttk.Combobox(age_row, textvariable=self.age_var, values=[str(i) for i in range(18, 26)], state="readonly", width=10).pack(side="left")

        sex_row = ttk.Frame(center)
        sex_row.pack(pady=10)
        ttk.Label(sex_row, text="What sex were you assigned at birth?", font=("Arial", BODY_FONT_SIZE)).pack(side="left", padx=(0, 10))
        self.sex_var = tk.StringVar(value="Female")
        ttk.Combobox(sex_row, textvariable=self.sex_var, values=["Male", "Female"], state="readonly", width=12).pack(side="left")

        self.bottom_right_button(frame, "Next", self.save_demographics)

    def save_demographics(self):
        self.participant_info["age"] = self.age_var.get()
        self.participant_info["sex_assigned_at_birth"] = self.sex_var.get()
        self.show_instructions()

    def show_instructions(self):
        self.clear_frame()
        frame = ttk.Frame(self, padding=40)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        center = ttk.Frame(frame)
        center.place(relx=0.5, rely=0.45, anchor="center")
        ttk.Label(center, text="Instructions", font=("Arial", TITLE_FONT_SIZE, "bold")).pack(pady=(0, 25))
        ttk.Label(center, text=INSTRUCTION_TEXT, wraplength=900, justify="center", font=("Arial", BODY_FONT_SIZE)).pack()

        self.bottom_right_button(frame, "Next", self.start_questions)

    def start_questions(self):
        self.question_index = 0
        self.show_question()

    def show_question(self):
        self.clear_frame()
        if self.question_index >= len(QUESTIONS):
            self.show_tasks_done()
            return

        self.current_question = QUESTIONS[self.question_index]
        self.selected_answer.set("")
        self.question_start_time = time.time()
        self.time_remaining = QUESTION_TIME_LIMIT
        self.ai_shown = False
        self.ai_show_time = None
        self.answer_history = []
        self.answer_change_log = []
        self.finished_question = False

        frame = ttk.Frame(self, padding=16)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        top = ttk.Frame(frame)
        top.pack(fill="x")
        ttk.Label(top, text=f"Question {self.question_index + 1} of {len(QUESTIONS)}", font=("Arial", 16, "bold")).pack(side="left")
        self.timer_label = ttk.Label(top, text=f"Time left: {self.time_remaining}s", font=("Arial", 16, "bold"))
        self.timer_label.pack(side="right")

        image_frame = ttk.Frame(frame)
        image_frame.pack(fill="both", expand=True, pady=(10, 5))
        image_path = os.path.join(BASE_DIR, self.current_question["image"])
        if not os.path.exists(image_path):
            ttk.Label(image_frame, text=f"Missing image file: {self.current_question['image']}\nPut it in the same folder as this Python script.", font=("Arial", 16)).pack(expand=True)
        else:
            self.image_ref = load_clean_question_image(image_path)
            tk.Label(image_frame, image=self.image_ref, bg="white").pack(expand=True)

        answers_frame = ttk.Frame(frame)
        answers_frame.pack(pady=4)

        for idx, option in enumerate(self.current_question["options"]):
            r = idx // 2
            c = idx % 2
            rb = ttk.Radiobutton(
                answers_frame,
                text=f"Choice {option}",
                value=option,
                variable=self.selected_answer,
                command=self.record_answer_selection
            )
            rb.grid(row=r, column=c, padx=24, pady=10, sticky="w")

        bottom = ttk.Frame(frame)
        bottom.pack(side="bottom", fill="x", pady=(4, 4))
        self.ai_label = ttk.Label(bottom, text="", font=("Arial", AI_FONT_SIZE, "bold"))
        self.ai_label.pack(side="left")
        ttk.Button(bottom, text="Next", command=self.finish_question).pack(side="right")

        self.update_timer()

    def record_answer_selection(self):
        choice = self.selected_answer.get()
        elapsed = round(time.time() - self.question_start_time, 3)

        if not self.answer_history:
            self.answer_history.append({"choice": choice, "time": elapsed})
            return

        previous = self.answer_history[-1]["choice"]
        if choice != previous:
            self.answer_change_log.append({
                "from": previous,
                "to": choice,
                "time": elapsed,
                "after_ai_suggestion": "Yes" if self.ai_shown else "No"
            })
            self.answer_history.append({"choice": choice, "time": elapsed})

    def update_timer(self):
        self.timer_label.config(text=f"Time left: {self.time_remaining}s")
        elapsed = time.time() - self.question_start_time

        if (not self.ai_shown) and self.current_question["condition"] != "no_ai" and elapsed >= AI_APPEAR_TIME:
            self.ai_shown = True
            self.ai_show_time = round(elapsed, 3)
            self.ai_label.config(text=f"AI suggests: Choice ({self.current_question['ai_suggestion']})")

        if self.time_remaining <= 0:
            self.finish_question()
            return

        self.time_remaining -= 1
        self.timer_job = self.after(1000, self.update_timer)

    def finish_question(self):
        if self.finished_question:
            return
        self.finished_question = True

        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None

        final_answer = self.selected_answer.get().strip()
        total_time = round(time.time() - self.question_start_time, 3)

        if not self.answer_history and final_answer:
            self.answer_history.append({"choice": final_answer, "time": total_time})

        first_answer = self.answer_history[0]["choice"] if self.answer_history else ""
        first_answer_time = self.answer_history[0]["time"] if self.answer_history else ""
        change_count = len(self.answer_change_log)
        changed_after_ai = "Yes" if any(x["after_ai_suggestion"] == "Yes" for x in self.answer_change_log) else "No"

        answer_after_ai = ""
        if self.ai_shown:
            post_ai = [entry["choice"] for entry in self.answer_history if entry["time"] >= self.ai_show_time]
            if post_ai:
                answer_after_ai = post_ai[-1]
            elif final_answer:
                answer_after_ai = final_answer

        matched_ai = ""
        if self.ai_shown and answer_after_ai:
            matched_ai = "Yes" if answer_after_ai == self.current_question["ai_suggestion"] else "No"

        self.trial_results.append({
            "participant_id": self.participant_info["participant_id"],
            "age": self.participant_info["age"],
            "sex_assigned_at_birth": self.participant_info["sex_assigned_at_birth"],
            "question_number": self.current_question["id"],
            "image_file": self.current_question["image"],
            "condition": self.current_question["condition"],
            "correct_answer": self.current_question["correct"],
            "ai_suggestion": self.current_question["ai_suggestion"],
            "ai_shown": "Yes" if self.ai_shown else "No",
            "ai_show_time_seconds": self.ai_show_time if self.ai_show_time is not None else "",
            "first_answer": first_answer,
            "first_answer_time_seconds": first_answer_time,
            "final_answer": final_answer,
            "final_answer_time_seconds": total_time,
            "was_correct": "Yes" if final_answer == self.current_question["correct"] else "No",
            "number_of_changes": change_count,
            "changed_after_ai_suggestion": changed_after_ai,
            "answer_after_ai_suggestion": answer_after_ai,
            "matched_ai_suggestion": matched_ai,
            "change_log": str(self.answer_change_log),
            "answer_history": str(self.answer_history)
        })

        self.question_index += 1
        self.show_question()

    def show_tasks_done(self):
        self.clear_frame()
        frame = ttk.Frame(self, padding=40)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        center = ttk.Frame(frame)
        center.place(relx=0.5, rely=0.45, anchor="center")
        ttk.Label(center, text=TASKS_DONE_TEXT, wraplength=820, justify="center", font=("Arial", 22, "bold")).pack()
        self.bottom_right_button(frame, "Next", self.show_questionnaire)

    def show_questionnaire(self):
        self.clear_frame()
        frame = ttk.Frame(self, padding=18)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        ttk.Label(frame, text="Questionnaire", font=("Arial", 22, "bold")).pack(pady=(0, 8))
        scroll = ScrollableFrame(frame)
        scroll.pack(fill="both", expand=True)

        tk.Label(
            scroll.inner,
            text="Instructions",
            font=("Times New Roman", 22, "bold"),
            bg="white", fg="black", anchor="w", justify="left"
        ).grid(row=0, column=0, columnspan=7, sticky="w", padx=10, pady=(10, 20))

        tk.Label(
            scroll.inner,
            text="Please indicate to what extent the following statements apply to you. Use the following scale to record your answers:",
            font=("Times New Roman", 20, "bold"),
            bg="white", fg="black", wraplength=1100, justify="left"
        ).grid(row=1, column=0, columnspan=7, sticky="w", padx=10, pady=(0, 20))

        tk.Label(scroll.inner, text="", bg="white").grid(row=2, column=0, padx=10)
        for idx, (num, label) in enumerate(QUESTIONNAIRE_SCALE, start=1):
            tk.Label(scroll.inner, text=num, font=("Times New Roman", 20), bg="white", fg="black").grid(row=2, column=idx, pady=(0, 4))
            tk.Label(scroll.inner, text=label, font=("Times New Roman", 13), bg="white", fg="black", justify="center", wraplength=150).grid(row=3, column=idx, padx=8, pady=(0, 14))

        self.questionnaire_vars = []
        start_row = 4
        for i, item in enumerate(QUESTIONNAIRE_ITEMS, start=1):
            row_index = start_row + i
            tk.Label(
                scroll.inner,
                text=f"{i}. {item}",
                font=("Arial", BODY_FONT_SIZE),
                bg="white", fg="black", anchor="w", justify="left", wraplength=650
            ).grid(row=row_index, column=0, sticky="w", padx=10, pady=8)

            var = tk.StringVar(value="")
            self.questionnaire_vars.append((item, var))
            for col_idx, (num, _) in enumerate(QUESTIONNAIRE_SCALE, start=1):
                tk.Radiobutton(
                    scroll.inner,
                    variable=var,
                    value=num,
                    bg="white",
                    activebackground="white",
                    highlightthickness=0
                ).grid(row=row_index, column=col_idx, padx=18, pady=8)

        self.bottom_right_button(frame, "Next", self.save_questionnaire)

    def save_questionnaire(self):
        self.questionnaire_results = []
        total_score = 0

        for i, (prompt, var) in enumerate(self.questionnaire_vars, start=1):
            response = var.get()
            numeric = int(response) if response.isdigit() else 0
            total_score += numeric

            self.questionnaire_results.append({
                "participant_id": self.participant_info["participant_id"],
                "item_number": i,
                "questionnaire_item": prompt,
                "response": response,
                "numeric_score": numeric
            })

        self.total_questionnaire_score = total_score
        self.show_debrief()

    def show_debrief(self):
        self.clear_frame()
        frame = ttk.Frame(self, padding=20)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        ttk.Label(frame, text="Participant Debrief", font=("Arial", 22, "bold")).pack(pady=(0, 10))
        scroll = ScrollableFrame(frame)
        scroll.pack(fill="both", expand=True)
        render_sectioned_text(scroll.inner, DEBRIEF_SECTIONS)

        self.bottom_right_button(frame, "Next", self.show_end)

    def show_end(self):
        self.save_results()
        self.clear_frame()
        frame = ttk.Frame(self, padding=40)
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

        center = ttk.Frame(frame)
        center.place(relx=0.5, rely=0.45, anchor="center")
        ttk.Label(center, text=END_TEXT, wraplength=900, justify="center", font=("Arial", 22, "bold")).pack()
        self.bottom_right_button(frame, "End quiz", self.destroy)

    def save_results(self):
        ensure_folders()
        pid = self.participant_info["participant_id"]

        with open(os.path.join(DATA_DIR, f"{pid}_participant_info.csv"), "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(self.participant_info.keys()))
            writer.writeheader()
            writer.writerow(self.participant_info)

        if self.trial_results:
            with open(os.path.join(DATA_DIR, f"{pid}_trial_results.csv"), "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(self.trial_results[0].keys()))
                writer.writeheader()
                writer.writerows(self.trial_results)

        if self.questionnaire_results:
            with open(os.path.join(DATA_DIR, f"{pid}_questionnaire.csv"), "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=list(self.questionnaire_results[0].keys()))
                writer.writeheader()
                writer.writerows(self.questionnaire_results)

        if hasattr(self, "total_questionnaire_score"):
            with open(os.path.join(DATA_DIR, f"{pid}_questionnaire_total.csv"), "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["participant_id", "total_score"])
                writer.writeheader()
                writer.writerow({
                    "participant_id": pid,
                    "total_score": self.total_questionnaire_score
                })


if __name__ == "__main__":
    ensure_folders()
    app = ExperimentApp()
    app.mainloop()
