import gspread
from google.oauth2 import service_account
import streamlit as st
from PIL import Image, ImageOps
import pandas as pd
import os
import time
import random
from datetime import datetime

# GOOGLE SHEETS SETUP
scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

creds = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=scope
)

client = gspread.authorize(creds)

sheet = client.open("AI experiment data").sheet1

st.set_page_config(page_title="AI-Supported Visual Tasks", layout="wide")

APP_TITLE = "How Do We Make Decisions in AI-Supported Visual Tasks?"
QUESTION_TIME_LIMIT = 30
AI_APPEAR_TIME = 10
IMAGE_MAX_WIDTH = 900

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

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

QUESTIONNAIRE_SCALE = {
    1: "not at all or very slightly",
    2: "a little",
    3: "somewhat",
    4: "quite a bit",
    5: "a lot",
}

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

PIS_SECTIONS = [
    ("The title of the research project", "How Do We Make Decisions in AI-Supported Visual Tasks?"),
    ("What is the purpose of the research?", "The research is organized by Namis Mansour, Postgraduate Student studying Clinical and Developmental Neuropsychology at the School of Psychology at Bournemouth University as part of the Psychology Project Unit. As a student dissertation project, this work is supervised by Dr. Ala Yankouskaya.\n\nIn this study, you will complete simple visual tasks where an AI tool, such as ChatGPT or Gemini, is involved. You will be asked to respond to visual questions and be shown suggestions produced by the AI during the task.\n\nThis helps us better understand how people work with AI tools in decision making."),
    ("Why have I been invited?", "We are looking to recruit 44 participants. You have been invited because you are a university student between the ages of 18 to 25 years old, are fluent in English, and you do not have diagnosed cognitive or neurological disorder(s)."),
    ("Do I have to take part?", "It is up to you to decide whether or not to take part. If you do decide to take part, you will have access to this information sheet to read. We want you to understand what participation involves, before you make a decision on whether to participate.\n\nIf you or any family member have an on-going relationship with BU or the research team, e.g. as a member of staff, as student or other service user, your decision on whether to take part (or continue to take part) will not affect this relationship and/or your studies at BU in any way.\n\nYou can withdraw from participation at any time and without giving a reason, simply by closing the browser page. Should you choose to withdraw your data after completing the experiment, you may do so by contacting the researcher.\n\nIf you withdraw after spending less than 15 minutes in the study, you will not be compensated. However, if you have spent more than 15 minutes, you will be compensated the full amount."),
    ("How long will the experiment take to complete?", "We anticipate that the experiment will take 30 minutes to complete. If you are a BU Psychology student, you will be compensated with 0.50 SONA credits for your time. If you are a non-BU student, your participation is still greatly appreciated, and you are more than welcome to contribute to this study."),
    ("What are the advantages and possible disadvantages or risks of taking part?", "This is simply a virtual task. It is not a test, we will not use it to judge your abilities or skills. While there are no personal benefits, taking part in this study helps us learn more about how people work with AI tools when it comes to decision making.\n\nThe task is safe and there are no expected risks, however, some people might feel a little challenged or pressed for time during the tasks. Don’t worry! The virtual tasks are designed to be simple and fair, with basic pattern recognition and skills that everyone can do."),
    ("What type of information will be sought from me and why is the collection of this information relevant for achieving the research project’s objectives?", "Your age and sex assigned at birth will be collected and will only be used to describe the group of participants. No other personal or identifiable information will be collected."),
    ("Use of my information", "The information collected from this task will be analyzed as part of the dissertation project. Your age and sex assigned at birth will only be used to describe the group of people taking part.\n\nYou can withdraw from participation at any point by closing your browser window. Once your response has been submitted, your identity and answers are anonymized, so withdrawal of data is impossible.\n\nThe information collected may be used to support other research projects in the future and access to it in this form will not be restricted, however, your identity will remain anonymous. It will not be possible for you to be identified from this data."),
    ("Sharing and further use of your personal information", "We will share your personal information only with BU staff and the BU student(s) working on the research project.\n\nResearch results will be included in a final year Psychology Dissertation that will not be made freely available.\n\nWhile anonymity is prioritized, the research team is committed to maintaining a respectful environment in line with research ethical guidelines and thus participants are also expected to engage in this study responsibly. Instances of misuse, harassment, or inappropriate behaviour, may exceptionally lead to revoking participants’ anonymity in order to uphold the integrity of the research process."),
    ("Contact for further information", "If you have any questions or would like further information, please contact Researcher Namis Mansour at s5822244@bournemouth.ac.uk, or Supervisor Ala Yankouskaya at ayankouskaya@bournemouth.ac.uk."),
    ("In case of complaints", "Any concerns about the study should be directed to Supervisor Ala Yankouskaya, ayankouskaya@bournemouth.ac.uk. If your concerns have not been answered by Dr. Ala, you should contact Professor Scott Wright, Associate Dean for Research, Innovation and Enterprise in the Faculty of Media, Science and Technology, Bournemouth University by email to researchgovernance@bournemouth.ac.uk."),
    ("Ethics ID", "68531"),
]

DEBRIEF_SECTIONS = [
    ("The title of the research project", "How Do We Make Decisions in AI-Supported Visual Tasks?"),
    ("Aims of the study", "The study aims to test how decisions are made while completing simple visual tasks that involve the usage of AI. Previous studies have investigated the effects of AI, but further research is needed to explore how AI can affect decision making."),
    ("Deception", "In this study, you answered a series of visual questions. For each question, you had 30 seconds to choose one answer from four options. You completed 30 questions in total. For some of the questions, an AI system showed a suggested answer on the screen. Sometimes this suggestion matched the correct answer, and sometimes it did not. You could choose whether or not to follow the AI’s suggestion when selecting your answer. We looked at how people responded to the questions when an AI suggestion was shown compared to when it was not.\n\nPlease note that this is not an intelligence test and was not designed to test your intellectual abilities. There were no right or wrong ways to approach it. All data will remain anonymous and confidential and will only be shared between the researcher and supervisor."),
    ("Withdrawal Process", "Please remember that all data is anonymous, so withdrawal after completion is not possible."),
    ("Contact for further information", "If you have any questions or would like further information, please contact the researcher at s5822244@bournemouth.ac.uk, or the supervisor at ayankouskaya@bournemouth.ac.uk."),
    ("In case of complaints", "Any concerns about the study should be directed to s5822244@bournemouth.ac.uk. If your queries have not been resolved, you are welcome to contact Prof Tiantian Zhang, Deputy Dean for Research & Professional Practice, Faculty of Science and Technology, Bournemouth University by email to researchgovernance@bournemouth.ac.uk."),
]


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
    return image


def init_state():
    defaults = {
        "page": "welcome",
        "participant_id": datetime.now().strftime("P%Y%m%d%H%M%S"),
        "age": "18",
        "sex_assigned_at_birth": "Female",
        "trial_results": [],
        "questionnaire_results": [],
        "questionnaire_total": 0,
        "current_question_index": 0,
        "question_start_time": None,
        "answer_history": [],
        "answer_change_log": [],
        "last_selected": "",
        "submitted_questions": set(),
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def save_all_results():
    pid = st.session_state["participant_id"]

    pd.DataFrame([{
        "participant_id": pid,
        "age": st.session_state["age"],
        "sex_assigned_at_birth": st.session_state["sex_assigned_at_birth"],
    }]).to_csv(os.path.join(DATA_DIR, f"{pid}_participant_info.csv"), index=False)

    if st.session_state["trial_results"]:
        pd.DataFrame(st.session_state["trial_results"]).to_csv(
            os.path.join(DATA_DIR, f"{pid}_trial_results.csv"), index=False
        )

    if st.session_state["questionnaire_results"]:
        pd.DataFrame(st.session_state["questionnaire_results"]).to_csv(
            os.path.join(DATA_DIR, f"{pid}_questionnaire.csv"), index=False
        )

    pd.DataFrame([{
        "participant_id": pid,
        "total_score": st.session_state["questionnaire_total"],
    }]).to_csv(os.path.join(DATA_DIR, f"{pid}_questionnaire_total.csv"), index=False)


def render_sections(sections):
    for header, body in sections:
        st.markdown(f"**{header}**")
        st.write(body)
        st.write("")


def move_to(page):
    st.session_state["page"] = page
    st.rerun()


def start_question(index):
    st.session_state["current_question_index"] = index
    st.session_state["question_start_time"] = time.time()
    st.session_state["answer_history"] = []
    st.session_state["answer_change_log"] = []
    st.session_state["last_selected"] = ""


def record_selection(choice, ai_shown, elapsed):
    last = st.session_state["last_selected"]
    if not last:
        st.session_state["answer_history"] = [{"choice": choice, "time": round(elapsed, 3)}]
        st.session_state["last_selected"] = choice
        return
    if choice != last:
        st.session_state["answer_change_log"].append({
            "from": last,
            "to": choice,
            "time": round(elapsed, 3),
            "after_ai_suggestion": "Yes" if ai_shown else "No",
        })
        st.session_state["answer_history"].append({"choice": choice, "time": round(elapsed, 3)})
        st.session_state["last_selected"] = choice


def submit_current_question(selected_answer, ai_shown, ai_show_time):
    q_index = st.session_state["current_question_index"]
    q = QUESTIONS[q_index]

    if q_index in st.session_state["submitted_questions"]:
        return

    total_time = round(time.time() - st.session_state["question_start_time"], 3)

    if not st.session_state["answer_history"] and selected_answer:
        st.session_state["answer_history"].append({"choice": selected_answer, "time": total_time})

    first_answer = st.session_state["answer_history"][0]["choice"] if st.session_state["answer_history"] else ""
    first_answer_time = st.session_state["answer_history"][0]["time"] if st.session_state["answer_history"] else ""
    change_count = len(st.session_state["answer_change_log"])
    changed_after_ai = "Yes" if any(x["after_ai_suggestion"] == "Yes" for x in st.session_state["answer_change_log"]) else "No"

    answer_after_ai = ""
    if ai_shown:
        post_ai = [entry["choice"] for entry in st.session_state["answer_history"] if entry["time"] >= ai_show_time]
        if post_ai:
            answer_after_ai = post_ai[-1]
        elif selected_answer:
            answer_after_ai = selected_answer

    matched_ai = ""
    if ai_shown and answer_after_ai:
        matched_ai = "Yes" if answer_after_ai == q["ai_suggestion"] else "No"

    st.session_state["trial_results"].append({
        "participant_id": st.session_state["participant_id"],
        "age": st.session_state["age"],
        "sex_assigned_at_birth": st.session_state["sex_assigned_at_birth"],
        "question_number": q["id"],
        "image_file": q["image"],
        "condition": q["condition"],
        "correct_answer": q["correct"],
        "ai_suggestion": q["ai_suggestion"],
        "ai_shown": "Yes" if ai_shown else "No",
        "ai_show_time_seconds": ai_show_time if ai_shown else "",
        "first_answer": first_answer,
        "first_answer_time_seconds": first_answer_time,
        "final_answer": selected_answer,
        "final_answer_time_seconds": total_time,
        "was_correct": "Yes" if selected_answer == q["correct"] else "No",
        "number_of_changes": change_count,
        "changed_after_ai_suggestion": changed_after_ai,
        "answer_after_ai_suggestion": answer_after_ai,
        "matched_ai_suggestion": matched_ai,
        "change_log": str(st.session_state["answer_change_log"]),
        "answer_history": str(st.session_state["answer_history"]),
    })

    st.session_state["submitted_questions"].add(q_index)

    if q_index + 1 < len(QUESTIONS):
        start_question(q_index + 1)
        st.rerun()
    else:
        move_to("tasks_done")


init_state()

st.title(APP_TITLE)
page = st.session_state["page"]

if page == "welcome":
    st.markdown("### Welcome to the visual tasks experiment!")
    st.write("This is a short 30 minute experiment in which you will complete 30 simple visual tasks, then you will answer a short questionnaire. Please click the next button to read through the Participant Information Sheet.")
    if st.button("Next"):
        move_to("pis")

elif page == "pis":
    st.header("Participant Information Sheet")
    render_sections(PIS_SECTIONS)

    consent_yes = st.checkbox("I have read and understood the Participant Information Sheet and consent to take part in this study")
    consent_no = st.checkbox("I do not consent to take part in this study [exit at this point]")
    data_access = st.checkbox("I give permission for members of the Research Team to have access to my anonymised responses. I understand that my anonymised responses may be reproduced in reports, academic publications and presentations but I will not be identified or identifiable.")

    if st.button("Next"):
        if consent_no:
            st.stop()
        if not consent_yes:
            st.warning("Please tick the consent box before continuing.")
        elif not data_access:
            st.warning("Please tick the anonymised data access box before continuing.")
        else:
            move_to("demographics")

elif page == "demographics":
    st.header("Please indicate your age and sex assigned at birth")
    st.session_state["age"] = st.selectbox("Age", [str(i) for i in range(18, 26)], index=0)
    st.session_state["sex_assigned_at_birth"] = st.selectbox("What sex were you assigned at birth?", ["Male", "Female"], index=1)
    if st.button("Next"):
        move_to("instructions")

elif page == "instructions":
    st.header("Instructions")
    st.write("This is a thirty minute task. You have thirty seconds to choose one answer from four options. Some tasks will include AI suggestions, and some will not. Once you have completed the tasks, you will answer a short questionnaire. Please remember this is not an intelligence test, this is simply a visual task. Click next to begin!")
    if st.button("Next"):
        start_question(0)
        move_to("questions")

elif page == "questions":
    q_index = st.session_state["current_question_index"]
    q = QUESTIONS[q_index]

    if st.session_state["question_start_time"] is None:
        start_question(q_index)

    elapsed = time.time() - st.session_state["question_start_time"]
    remaining = max(0, QUESTION_TIME_LIMIT - int(elapsed))
    ai_shown = q["condition"] != "no_ai" and elapsed >= AI_APPEAR_TIME
    ai_show_time = AI_APPEAR_TIME if ai_shown else None

    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"Question {q_index + 1} of {len(QUESTIONS)}")
    with col2:
        st.markdown(f"### Time left: {remaining}s")

    image_path = os.path.join(BASE_DIR, q["image"])
    if os.path.exists(image_path):
        img = load_clean_question_image(image_path)
        st.image(img, width=IMAGE_MAX_WIDTH)
    else:
        st.error(f"Missing image file: {q['image']}")

    selected = st.radio(
        "Choose one answer:",
        q["options"],
        format_func=lambda x: f"Choice {x}",
        key=f"question_{q_index}_choice"
    )

    record_selection(selected, ai_shown, elapsed)

    if ai_shown:
        st.markdown(f"<p style='font-size:21px; font-weight:bold;'>AI suggests: Choice ({q['ai_suggestion']})</p>", unsafe_allow_html=True)
    else:
        st.write("")

    c1, c2 = st.columns([1, 1])
    with c2:
        if st.button("Next"):
            submit_current_question(selected, ai_shown, ai_show_time)

    if remaining <= 0:
        submit_current_question(selected, ai_shown, ai_show_time)
    else:
        time.sleep(1)
        st.rerun()

elif page == "tasks_done":
    st.success("Tasks completed, well done! Please fill up the questionnaire on the next screen.")
    if st.button("Next"):
        move_to("questionnaire")

elif page == "questionnaire":
    st.header("Questionnaire")
    st.markdown("### Instructions")
    st.write(
        "Please indicate to what extent the following statements apply to you. "
        "Use the following scale to record your answers:"
    )

    scale_df = pd.DataFrame([
        {
            "1": QUESTIONNAIRE_SCALE[1],
            "2": QUESTIONNAIRE_SCALE[2],
            "3": QUESTIONNAIRE_SCALE[3],
            "4": QUESTIONNAIRE_SCALE[4],
            "5": QUESTIONNAIRE_SCALE[5],
        }
    ])
    st.table(scale_df)

    responses = []
    for i, item in enumerate(QUESTIONNAIRE_ITEMS, start=1):
        response = st.radio(
            f"{i}. {item}",
            [1, 2, 3, 4, 5],
            horizontal=True,
            key=f"qnr_{i}"
        )
        responses.append((i, item, response))

   if st.button("Next"):
    total = 0

    for i, item, response in responses:
        total += int(response)

        # SAVE EACH RESPONSE TO GOOGLE SHEET
        sheet.append_row([
            st.session_state["participant_id"],
            i,
            item,
            response,
            int(response)
        ])

    # SAVE TOTAL SCORE
    sheet.append_row([
        st.session_state["participant_id"],
        "TOTAL",
        "",
        "",
        total
    ])

    st.session_state["questionnaire_total"] = total
    move_to("debrief")
        
elif page == "debrief":
    st.header("Participant Debrief")
    render_sections(DEBRIEF_SECTIONS)
    if st.button("Next"):
        save_all_results()
        move_to("end")

elif page == "end":
    st.success("Thank you so much for your participation! Your credits will be transferred as soon as possible!")
    if st.button("End quiz"):
        st.balloons()
