import random
import string
import re
import streamlit as st
from io import StringIO

# 🌈 Custom Styling
st.markdown(
    """
    <style>
    .main { background-color: #f0f2f6; }
    .stButton>button { background-color: #4CAF50; color: white; font-size: 18px; padding: 10px; border-radius: 10px; }
    .stTextInput>div>div>input { border: 2px solid #4CAF50; border-radius: 10px; }
    .stNumberInput>div>div>input { border: 2px solid #4CAF50; border-radius: 10px; }
    .stCheckbox>div { font-size: 18px; }
    </style>
    """,
    unsafe_allow_html=True
)

password_history = []
blacklist = ["password123", "12345678", "qwerty", "iloveyou", "admin"]


def generate_password(length, use_upper, use_lower, use_digits, use_symbols, min_upper, min_digits, min_symbols):
    if length < 8:
        st.error("🔴 Password length must be at least 8 characters.")
        return None

    characters = ""
    password = ""

    if use_upper:
        characters += string.ascii_uppercase
        password += ''.join(random.choice(string.ascii_uppercase) for _ in range(min_upper))
    if use_lower:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
        password += ''.join(random.choice(string.digits) for _ in range(min_digits))
    if use_symbols:
        characters += string.punctuation
        password += ''.join(random.choice(string.punctuation) for _ in range(min_symbols))

    if not characters:
        st.error("🔴 You must select at least one character set.")
        return None

    remaining_length = length - len(password)
    password += ''.join(random.choice(characters) for _ in range(remaining_length))
    password = ''.join(random.sample(password, len(password)))

    return password


def check_password_strength(password):
    score = 0
    strength_message = []

    if password in blacklist:
        st.error("🚫 This password is too common. Please choose a stronger one.")
        return

    if len(password) >= 8:
        strength_message.append("✅ Length is good (8+ characters).")
        score += 1
    else:
        strength_message.append("❌ Password should be at least 8 characters long.")

    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        strength_message.append("✅ Contains both uppercase and lowercase letters.")
        score += 1
    else:
        strength_message.append("❌ Include both uppercase and lowercase letters.")

    if re.search(r"\d", password):
        strength_message.append("✅ Contains numbers (0-9).")
        score += 1
    else:
        strength_message.append("❌ Add at least one number (0-9).")

    if re.search(r"[!@#$%^&*]", password):
        strength_message.append("✅ Contains special characters (!@#$%^&*).")
        score += 1
    else:
        strength_message.append("❌ Include at least one special character (!@#$%^&*).")

    strength_labels = ["Weak", "Moderate", "Strong"]
    strength_level = min(score, 3) - 1
    strength_level = max(strength_level, 0)

    st.progress(score / 4)
    st.subheader(f"Password Strength: {strength_labels[strength_level].upper()} 💪")

    for msg in strength_message:
        st.write(msg)


st.title("🔐 Random Password Generator + Strength Checker")
st.markdown("### 🛡️ Secure your accounts with strong passwords in seconds!")

num_passwords = st.number_input("How many passwords would you like to generate?", min_value=1, value=1)
length = st.number_input("Enter password length (minimum 8):", min_value=8, value=12)

use_upper = st.checkbox("Include uppercase letters")
use_lower = st.checkbox("Include lowercase letters")
use_digits = st.checkbox("Include numbers")
use_symbols = st.checkbox("Include symbols")

min_upper = st.number_input("Minimum uppercase letters", min_value=0, value=1)
min_digits = st.number_input("Minimum numbers", min_value=0, value=1)
min_symbols = st.number_input("Minimum symbols", min_value=0, value=1)

generate_button = st.button("🔑 Generate Password(s)")

if generate_button:
    for i in range(num_passwords):
        st.subheader(f"🔑 Generated Password {i + 1}")
        password = generate_password(length, use_upper, use_lower, use_digits, use_symbols, min_upper, min_digits, min_symbols)
        if password:
            st.code(password, language='plaintext')
            st.button("📋 Copy to Clipboard", key=f"copy_button_{i}")
            check_password_strength(password)
            password_history.append(password)
            st.markdown("---")

    if password_history:
        st.subheader("🔍 Password History")
        for i, pwd in enumerate(password_history[-5:]):
            st.write(f"{i+1}. {pwd}")

        buffer = "\n".join(password_history)
        st.download_button("📥 Download Passwords", buffer, file_name="passwords.txt")

# 📘 Footer
st.markdown("""
    ---
    👩‍💻 **Created by Syeda Farzana Shah**  
    💡 *Empowering security, one password at a time.*
    """)



