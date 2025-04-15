import streamlit as st
import random
import string

# ---- CONFIG ----
st.set_page_config(page_title="🔐 Password Strength Meter", page_icon="🛡️", layout="centered")

# ---- CUSTOM MOBILE-FRIENDLY CSS ----
st.markdown("""
    <style>
        .stTextInput input {
            background-color: #f8f9fa;
            color: #333;
        }
        .css-1d391kg {
            padding: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ---- PASSWORD FUNCTIONS ----
def check_password_strength(password):
    length = len(password)
    has_lower = any(c.islower() for c in password)
    has_upper = any(c.isupper() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/" for c in password)
    score = sum([has_lower, has_upper, has_digit, has_special])

    if length < 6:
        return "❌ Weak", "red"
    elif length < 10 and score >= 2:
        return "🟠 Moderate", "orange"
    elif length >= 10 and score >= 3:
        return "🟢 Strong", "green"
    else:
        return "🔵 Very Strong", "blue"

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for _ in range(length))

def calculate_entropy(password):
    charset_size = 0
    if any(c.islower() for c in password): charset_size += 26
    if any(c.isupper() for c in password): charset_size += 26
    if any(c.isdigit() for c in password): charset_size += 10
    if any(c in string.punctuation for c in password): charset_size += len(string.punctuation)
    return len(password) * (charset_size.bit_length()) if charset_size else 0

def is_common_password(password):
    blacklist = {
        "123456", "password", "123456789", "qwerty", "abc123",
        "password1", "123123", "admin", "welcome", "iloveyou",
        "letmein", "football", "monkey", "password123"
    }
    return password.lower() in blacklist

def suggest_improvements(password):
    suggestions = []
    if len(password) < 12:
        suggestions.append("📏 Make your password longer.")
    if not any(c.islower() for c in password):
        suggestions.append("🔡 Add lowercase letters.")
    if not any(c.isupper() for c in password):
        suggestions.append("🔠 Add uppercase letters.")
    if not any(c.isdigit() for c in password):
        suggestions.append("🔢 Include some numbers.")
    if not any(c in string.punctuation for c in password):
        suggestions.append("💥 Add special characters.")
    return suggestions

# ---- MAIN UI ----
st.title("🛡️ Password Strength Meter")
st.caption("Secure your digital life with powerful passwords! 🔐💡")

password = st.text_input("🔍 Enter your password:", type="password")

if password:
    if is_common_password(password):
        st.error("🚫 This password is blacklisted because it's too common (like 'password123'). Please choose a more secure one!")
    else:
        strength, color = check_password_strength(password)
        entropy = calculate_entropy(password)

        st.markdown(f"**🔎 Strength:** <span style='color:{color}; font-weight:bold'>{strength}</span>", unsafe_allow_html=True)
        st.write(f"📊 **Entropy Score:** `{entropy:.2f}` bits")

        improvements = suggest_improvements(password)
        if improvements:
            st.warning("🛠️ Suggestions to Make Your Password Better:")
            for tip in improvements:
                st.write(f"- {tip}")

        if strength.startswith("❌"):
            st.warning("⚠️ Your password is weak. Try mixing upper/lowercase letters, numbers, and symbols.")
        elif strength.startswith("🟠"):
            st.info("🧩 Not bad! A few tweaks will make it much stronger.")
        elif strength.startswith("🟢"):
            st.success("✅ Great! Your password is strong and secure.")
        else:
            st.balloons()
            st.success("🎉 Fantastic! You've created a top-tier password!")

# ---- GENERATOR SECTION ----
st.markdown("---")
st.subheader("🔐 Need a Secure Password?")
password_length = st.slider("🔧 Choose your password length:", min_value=8, max_value=32, value=12)
if st.button("🎲 Generate Strong Password"):
    strong_password = generate_password(password_length)
    st.text(f"🧷 Your Secure Password: {strong_password}")
    st.info("🗝️ *Tip:* Save this password in a password manager to keep it safe and handy.")

# ---- FOOTER ----
st.markdown("<h5 style='text-align: center; margin-top: 50px;'>✨ Create by Dureshehwar Siddiqui</h5>", unsafe_allow_html=True)
