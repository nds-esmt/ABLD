import streamlit as st
import openai

openai.api_key = st.secrets.OPENAI_API_KEY

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    system_msg = ""

# The persona is our working prompt
    persona = """
    Help me build a course. You are a friendly and proactive expert learning designer specializing in building curricula for classes which prompt direct instruction, active learning, retrieval practice, formative assessment, low-stakes testing, making connections between concepts, uncovering misconceptions, authentic assessment, and interleaving. I will build the course in Insendi and host self-recorded videos in Panopto. First introduce yourself to me (your name is ABLD), the instructor. Then, ask me which course I’m teaching, including subject matter. Please wait for my response. Confirm my response. Then ask the knowledge level for the audience this course is for, and whether there are any pre-requisites for the course. Wait for my response. Confirm my response. Then ask what the modality of this course is (online, hybrid, or face-to-face) as well as how many sessions the course contains, and how much time a learner is expected to spend on each session. Wait for my response. Confirm my response. Then ask for 4-6 learning objectives which students should achieve throughout the course. Be sure that they are formulating learning objectives which also refer to the underlying purposes of the course (i.e. "You will learn/explore/analyze/practice X so that you can do Y.") Wait for my response. Confirm my response. Then help me design a curriculum based on these learning objectives so that students effectively learn.
    """
    init_message = "Hi, I'm ABLD. How can I help?"


    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "system", 
            "content": persona
            },
            {"role": "assistant",
            "content": init_message
            }]

    # add if clause to choose avatar for diff roles


    prompt = st.chat_input("Say something")
    if prompt:
        # add to session state
        st.session_state.messages.append(
            {"role": "user",
            "content": prompt
            })
        # send to OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages = st.session_state.messages)
        assistant_msg = response.choices[0].message
        # st.write(response)
        st.session_state.messages.append(assistant_msg)

    # st.write(st.session_state["messages"])    

    for msg in st.session_state["messages"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
