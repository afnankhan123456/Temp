import streamlit as st
import random
import requests
import json
import os
import re
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- CONFIG ---
FILENAME = "player_data.json"
IMAGE_URL_MAIN = "https://raw.githubusercontent.com/afnankhan123456/stremlit--game/main/images/main_backgrund.jpg"
IMAGE_URL_BG = "https://raw.githubusercontent.com/afnankhan123456/stremlit--game/main/2nd%20background.jpg"
SENDER_EMAIL = "afnank6789@gmail.com"
APP_PASSWORD = "uiqb avim axhz knzu"

# Show main image
st.image(IMAGE_URL_MAIN)

# --- FUNCTIONS ---
def get_base64_image(image_source):
    """Convert local file or URL to base64 string."""
    if image_source.startswith("http://") or image_source.startswith("https://"):
        response = requests.get(image_source)
        return base64.b64encode(response.content).decode()
    else:
        with open(image_source, "rb") as f:
            return base64.b64encode(f.read()).decode()

def is_valid_name(name):
    return re.match("^[A-Za-z]+$", name) is not None

def is_valid_email(email):
    return re.match(r"^[\w\.-]+@gmail\.com$", email) is not None

def save_player(name, guess):
    with open(FILENAME, "w") as f:
        json.dump({"name": name, "guess": guess}, f)

def load_player():
    with open(FILENAME, "r") as f:
        return json.load(f)

def send_otp_email(to_email, otp):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = "Your OTP for Game Login"
    msg.attach(MIMEText(f"Your OTP is: {otp}", "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f" Failed to send OTP: {e}")
        return False

# --- INITIAL STATES ---
for key in ["name_submitted", "email_submitted", "otp_verified"]:
    if key not in st.session_state:
        st.session_state[key] = False

if "player_name" not in st.session_state:
    st.session_state.player_name = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "sent_otp" not in st.session_state:
    st.session_state.sent_otp = ""

# --- BACKGROUND SETUP BEFORE OTP ---
if not st.session_state.otp_verified:
    base64_image = get_base64_image(IMAGE_URL_BG)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{base64_image}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# --- FUNCTIONS ---
def get_base64_image(url):
    """Fetch image from URL and return as base64."""
    response = requests.get(url)
    return base64.b64encode(response.content).decode()

# --- UI ---

# Logo image URL
image_url = "https://raw.githubusercontent.com/afnankhan123456/stremlit--game/main/1st%20logo.jpg"

# Chhota logo as base64 for inline HTML
img_base64 = get_base64_image(image_url)

st.markdown(f"""
    <div style='display: flex; align-items: center; justify-content: center; margin-bottom: 20px;'>
        <img src="data:image/jpeg;base64,{img_base64}" width="100" style="margin-right: 20px; border-radius: 10px;">
        <h1 style="color: #007BFF; font-family: Arial, sans-serif;">WELCOME TO THE BATTLEZONE ⚔️🔥</h1>
    </div>
""", unsafe_allow_html=True)

# Reward image
REWARD_IMAGE_URL = "https://raw.githubusercontent.com/afnankhan123456/stremlit--game/main/2nd%20logo.jpg"
reward_img_base64 = get_base64_image(REWARD_IMAGE_URL)

st.markdown(f"""
    <div style="background-color: green; padding: 15px; border-radius: 12px; border: 2px solid #ddd;
                box-shadow: 0px 0px 6px rgba(0,0,0,0.1); max-width: 600px; margin: auto; margin-bottom: 10px;">
        <div style='display: flex; align-items: center;'>
            <img src="data:image/jpeg;base64,{reward_img_base64}" width="100" 
                 style="margin-right: 15px; border-radius: 10px;">
            <p style="font-size: 16px; color: white; font-weight: bold; margin: 0;">
                🏆 Winning player gets <span style="color: #FFEB3B;">2x Prize</span> on winning 💰💵
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)



# --- MAIN INTERFACE ---
with st.container():
    # Step 1: Name input
    if not st.session_state.get("name_submitted", False):
        with st.form("name_form"):
            name = st.text_input("👤 Enter your name:")
            name_submit = st.form_submit_button("Next ➡️")
            
            if name_submit:
                if not is_valid_name(name):
                    st.error("❌ Invalid name. Only alphabets allowed.")
                else:
                    st.session_state.name_submitted = True
                    st.session_state.player_name = name
                    st.success(f"✅ Hello {name}, now enter your Gmail.")                 

    # Step 2: Email
    elif not st.session_state.get("email_submitted", False):
        with st.form("email_form"):
            email = st.text_input("📧 Enter your Gmail:")
            email_submit = st.form_submit_button("Send OTP")
            if email_submit:
                if not is_valid_email(email):
                    st.error("❌ Please enter a valid Gmail address.")
                else:
                    otp = str(random.randint(100000, 999999))
                    if send_otp_email(email, otp):
                        st.session_state.sent_otp = otp
                        st.session_state.user_email = email
                        st.session_state.email_submitted = True
                        st.success("📩 OTP sent to your email.")

    # Step 3: OTP
    elif not st.session_state.get("otp_verified", False):
        with st.form("otp_form", clear_on_submit=True):
            user_otp = st.text_input("🔐 Enter the OTP sent to your email:", type="password")
            otp_submit = st.form_submit_button("Verify OTP")

            if otp_submit:
                if "sent_otp" in st.session_state and user_otp.strip() == st.session_state.sent_otp:
                    st.session_state.otp_verified = True
                    st.success("✅ OTP Verified! Now you can play.")
                    st.rerun()  # Force page reload only once after verification
                else:
                    st.error("❌ Incorrect OTP. Try again.")


# --- Step 4: Full background update after OTP verified ---
if st.session_state.otp_verified:
    IMAGE_URL2 = "https://raw.githubusercontent.com/afnankhan123456/stremlit--game/main/2nd%20background.jpg"
    next_img_base64 = get_base64_image(IMAGE_URL2)

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{next_img_base64}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<h2 style='color:white; text-align:center; margin-top: 200px;'>", unsafe_allow_html=True)

# --- File path where login data is stored ---
file_path = "/tmp/login_data.json"  # Temporary storage for deployment

# Load existing data if file exists
if os.path.exists(file_path):
    with open(file_path, "r") as f:
        login_data = json.load(f)
else:
    login_data = {}

# This block runs only after OTP verification
if st.session_state.get("otp_verified", False):
    email = st.session_state.user_email

    # Increase login count
    login_data[email] = login_data.get(email, 0) + 1

    # Save updated login count
    with open(file_path, "w") as f:
        json.dump(login_data, f)

    # --- Store users data in memory ---
    if "users" not in st.session_state:
        st.session_state.users = {}

    users = st.session_state.users

    import streamlit as st
import random

# --- User Data Storage ---
if "users" not in st.session_state:
    st.session_state.users = {}

users = st.session_state.users

# --- Game Logic Functions ---
def get_winning_rounds(base=0):
    return [base + i for i in [4, 9, 15, 20]]

def count_correct(user_guess, system_answer):
    return sum([user_guess[i] == system_answer[i] for i in range(3)])

def get_min_bet(email, upto_round):
    prev_bets = [g['amount'] for g in users[email]['games'] if g['round'] < upto_round]
    return min(prev_bets) if prev_bets else 0

def play_game(email, user_guess, user_bet):
    if email not in users:
        users[email] = {"games": []}

    round_no = len(users[email]['games']) + 1
    total_games = len(users[email]['games'])

    base = (total_games // 20) * 20
    winning_rounds = get_winning_rounds(base)

    if round_no in winning_rounds:
        min_bet = get_min_bet(email, round_no)
        user_bet = min_bet

    # Random answer generation
    if round_no in winning_rounds:
        system_answer = user_guess.copy()
    else:
        while True:
            system_answer = random.sample([1, 2, 3], 3)
            if count_correct(user_guess, system_answer) < 3:
                break

    correct = count_correct(user_guess, system_answer)

    # Reward calculation
    if correct == 1:
        reward = round(user_bet * 0.25, 2)
    elif correct == 2:
        reward = round(user_bet * 0.50, 2)
    elif correct == 3:
        reward = round(user_bet * 2, 2)
        st.success("🎉 All 3 guesses are correct! You win double the bet!")
        st.balloons()

        explosion_html = """
        <div class="explosion"></div>
        <style>
        .explosion {
          position: relative;
          width: 100px;
          height: 100px;
          margin: 50px auto;
        }
        .explosion::before {
          content: '';
          position: absolute;
          width: 200px;
          height: 200px;
          background: radial-gradient(circle, red, orange, yellow, white);
          border-radius: 50%;
          animation: boom 0.7s ease-out forwards;
          transform: scale(0);
          opacity: 0.8;
          left: -50px;
          top: -50px;
          z-index: 999;
        }
        @keyframes boom {
          to {
            transform: scale(2);
            opacity: 0;
          }
        }
        </style>
        """
        st.markdown(explosion_html, unsafe_allow_html=True)
    else:
        reward = 0

    # Store result
    result = {
        "round": round_no,
        "guess": user_guess,
        "answer": system_answer,
        "correct": correct,
        "amount": user_bet,
        "reward": reward
    }
    users[email]['games'].append(result)

    return result

# --- UI ---
if st.session_state.get("otp_verified"):

    st.header("🎮 Play the Game")

    bet = st.number_input("Enter Bet Amount", min_value=1, key="bet_input")

    if bet > 0:

        guess1 = horizontal_buttons("🎯 Select 1st Number", "guess1")
        guess2 = horizontal_buttons("🎯 Select 2nd Number", "guess2")
        guess3 = horizontal_buttons("🎯 Select 3rd Number", "guess3")

        if st.button("Submit Guess", key="submit_guess"):
            user_guess = [guess1, guess2, guess3]
            result = play_game(st.session_state.get("email", "guest"), user_guess, bet)

            st.success(f"Answer: {result['answer']}")
            st.info(f"Correct Guesses: {result['correct']}")
            st.success(f"Reward Earned: ₹{result['reward']}")

