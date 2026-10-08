from security import verify_password
from security import hash_password
from database import register_user
from database import login_user
from predict_persona import predict_cluster
from recommendation.recommendation import get_recommendations

current_persona = None

CLUSTER_TO_PERSONA = {
    0: "High-Value Customer",
    1: "Budget Customer",
    2: "Potential Customer",
    3: "Impulsive Spender"
}

try:
    import customtkinter as ctk
except ModuleNotFoundError:
    import tkinter as tk
    from tkinter import messagebox

    class _CustomTkinterUnavailable:
        def __getattr__(self, name):
            raise ModuleNotFoundError(
                "customtkinter is not installed. Install it with: pip install customtkinter"
            )

    ctk = _CustomTkinterUnavailable()
    # Keep the original tkinter messagebox available for the rest of the app.
else:
    from tkinter import messagebox

import re


from database import (
    register_user,
    login_user,
    save_prediction,
    get_prediction_history,
    update_user,
    delete_user
)

# =========================================================
# APP SETTINGS
# =========================================================

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Customer Persona Analytics")
app.geometry("1000x650")
app.resizable(False, False)


# =========================================================
# COLORS
# =========================================================

BG_COLOR = "#0B1120"
CARD_COLOR = "#111827"
INPUT_COLOR = "#1F2937"
WHITE = "#F8FAFC"
GRAY = "#94A3B8"
BLUE = "#3B82F6"
BLUE_HOVER = "#2563EB"
GREEN = "#22C55E"
YELLOW = "#F59E0B"
RED = "#EF4444"


# Store logged-in username
current_username = "User"


# =========================================================
# CLEAR SCREEN
# =========================================================

def clear_screen():
    for widget in app.winfo_children():
        widget.destroy()


# =========================================================
# BRAND PANEL
# =========================================================

def create_brand_panel(parent):

    panel = ctk.CTkFrame(
        parent,
        fg_color=BG_COLOR,
        corner_radius=0,
        width=480
    )

    panel.pack(
        side="left",
        fill="y"
    )

    logo = ctk.CTkLabel(
        panel,
        text="CP",
        width=75,
        height=75,
        corner_radius=18,
        fg_color=BLUE,
        text_color=WHITE,
        font=("Arial", 28, "bold")
    )

    logo.pack(pady=(120, 25))

    title = ctk.CTkLabel(
        panel,
        text="Customer\nPersona",
        text_color=WHITE,
        font=("Arial", 40, "bold"),
        justify="left"
    )

    title.pack(
        anchor="w",
        padx=65
    )

    subtitle = ctk.CTkLabel(
        panel,
        text="Understand your customers.\n"
             "Discover their behavior.\n"
             "Make smarter decisions.",
        text_color=GRAY,
        font=("Arial", 16),
        justify="left"
    )

    subtitle.pack(
        anchor="w",
        padx=68,
        pady=20
    )


# =========================================================
# WELCOME PAGE
# =========================================================

def welcome_page():

    clear_screen()

    main = ctk.CTkFrame(
        app,
        fg_color=BG_COLOR,
        corner_radius=0
    )

    main.pack(
        fill="both",
        expand=True
    )

    create_brand_panel(main)

    right = ctk.CTkFrame(
        main,
        fg_color=BG_COLOR,
        corner_radius=0
    )

    right.pack(
        side="right",
        fill="both",
        expand=True
    )

    card = ctk.CTkFrame(
        right,
        width=400,
        height=420,
        fg_color=CARD_COLOR,
        corner_radius=25
    )

    card.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    title = ctk.CTkLabel(
        card,
        text="Welcome",
        text_color=WHITE,
        font=("Arial", 32, "bold")
    )

    title.pack(pady=(65, 10))

    subtitle = ctk.CTkLabel(
        card,
        text="Customer analytics made simple.",
        text_color=GRAY,
        font=("Arial", 15)
    )

    subtitle.pack(pady=(0, 35))

    login_button = ctk.CTkButton(
        card,
        text="LOGIN",
        width=280,
        height=50,
        corner_radius=12,
        fg_color=BLUE,
        hover_color=BLUE_HOVER,
        font=("Arial", 16, "bold"),
        command=login_page
    )

    login_button.pack(pady=10)

    register_button = ctk.CTkButton(
        card,
        text="CREATE ACCOUNT",
        width=280,
        height=50,
        corner_radius=12,
        fg_color=INPUT_COLOR,
        hover_color="#374151",
        font=("Arial", 16, "bold"),
        command=register_page
    )

    register_button.pack(pady=10)

    footer = ctk.CTkLabel(
        card,
        text="Secure • Simple • Intelligent",
        text_color=GRAY,
        font=("Arial", 12)
    )

    footer.pack(pady=25)


# =========================================================
# LOGIN PAGE
# =========================================================

def login_page():

    clear_screen()

    main = ctk.CTkFrame(
        app,
        fg_color=BG_COLOR,
        corner_radius=0
    )

    main.pack(
        fill="both",
        expand=True
    )

    create_brand_panel(main)

    card = ctk.CTkFrame(
        main,
        width=430,
        height=500,
        fg_color=CARD_COLOR,
        corner_radius=25
    )

    card.place(
        relx=0.74,
        rely=0.5,
        anchor="center"
    )

    title = ctk.CTkLabel(
        card,
        text="Welcome Back",
        text_color=WHITE,
        font=("Arial", 30, "bold")
    )

    title.pack(pady=(45, 8))

    subtitle = ctk.CTkLabel(
        card,
        text="Login to your account",
        text_color=GRAY,
        font=("Arial", 14)
    )

    subtitle.pack(pady=(0, 25))

    username_entry = ctk.CTkEntry(
        card,
        width=320,
        height=45,
        corner_radius=10,
        placeholder_text="Username or Email",
        fg_color=INPUT_COLOR,
        border_width=0
    )

    username_entry.pack(pady=3)

    password_entry = ctk.CTkEntry(
        card,
        width=320,
        height=45,
        corner_radius=10,
        placeholder_text="Password",
        show="*",
        fg_color=INPUT_COLOR,
        border_width=0
    )

    password_entry.pack(pady=3)

    show_password_var = ctk.BooleanVar(value=False)

    def toggle_password():

        if show_password_var.get():
            password_entry.configure(show="")
        else:
            password_entry.configure(show="*")

    show_password = ctk.CTkCheckBox(
        card,
        text="Show password",
        variable=show_password_var,
        command=toggle_password,
        text_color=GRAY
    )

    show_password.pack(
        anchor="w",
        padx=55,
        pady=5
    )

    def perform_login():


        username = username_entry.get().strip()
        password = password_entry.get()

        if username == "":
            messagebox.showerror(
                "Login Error",
                "Please enter your username or email."
            )
            return

        if password == "":
            messagebox.showerror(
                "Login Error",
                "Please enter your password."
            )
            return

        user = login_user(username, password)

        if user:
            global current_username
            current_username = username

            messagebox.showinfo(
                "Login Successful",
                "Login successful!"
            )

            dashboard_page()

        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid username or password."
            )


    login_button = ctk.CTkButton(
        card,
        text="LOGIN",
        width=320,
        height=48,
        corner_radius=10,
        fg_color=BLUE,
        hover_color=BLUE_HOVER,
        font=("Arial", 15, "bold"),
        command=perform_login
    )

    login_button.pack(pady=20)

    register_button = ctk.CTkButton(
        card,
        text="Don't have an account? Create one",
        width=300,
        fg_color="transparent",
        hover_color=INPUT_COLOR,
        text_color=BLUE,
        command=register_page
    )

    register_button.pack(pady=5)

    back_button = ctk.CTkButton(
        card,
        text="← Back",
        width=100,
        fg_color="transparent",
        hover_color=INPUT_COLOR,
        text_color=GRAY,
        command=welcome_page
    )

    back_button.pack(pady=10)


# =========================================================
# PASSWORD STRENGTH
# =========================================================

def get_password_strength(password):

    score = 0

    if len(password) >= 8:
        score += 1

    if any(char.isupper() for char in password):
        score += 1

    if any(char.islower() for char in password):
        score += 1

    if any(char.isdigit() for char in password):
        score += 1

    special_characters = "!@#$%^&*()-_=+[]{};:,.<>?/|"

    if any(char in special_characters for char in password):
        score += 1

    return score


# =========================================================
# REGISTRATION PAGE
# =========================================================

def register_page():

    clear_screen()

    main = ctk.CTkFrame(
        app,
        fg_color=BG_COLOR,
        corner_radius=0
    )

    main.pack(
        fill="both",
        expand=True
    )

    card = ctk.CTkFrame(
        main,
        width=500,
        height=650,
        fg_color=CARD_COLOR,
        corner_radius=25
    )

    card.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    title = ctk.CTkLabel(
        card,
        text="Create Account",
        text_color=WHITE,
        font=("Arial", 30, "bold")
    )

    title.pack(pady=(30, 5))

    subtitle = ctk.CTkLabel(
        card,
        text="Join Customer Persona Analytics",
        text_color=GRAY,
        font=("Arial", 13)
    )

    subtitle.pack(pady=(0, 10))

    name_entry = ctk.CTkEntry(
        card,
        width=350,
        height=40,
        corner_radius=10,
        placeholder_text="Full Name",
        fg_color=INPUT_COLOR,
        border_width=0
    )

    name_entry.pack(pady=3)

    email_entry = ctk.CTkEntry(
        card,
        width=350,
        height=40,
        corner_radius=10,
        placeholder_text="Email Address",
        fg_color=INPUT_COLOR,
        border_width=0
    )

    email_entry.pack(pady=3)

    username_entry = ctk.CTkEntry(
        card,
        width=350,
        height=40,
        corner_radius=10,
        placeholder_text="Username",
        fg_color=INPUT_COLOR,
        border_width=0
    )

    username_entry.pack(pady=3)

    password_entry = ctk.CTkEntry(
        card,
        width=350,
        height=40,
        corner_radius=10,
        placeholder_text="Password",
        show="*",
        fg_color=INPUT_COLOR,
        border_width=0
    )

    password_entry.pack(pady=3)

    strength_label = ctk.CTkLabel(
        card,
        text="Password Strength: Not entered",
        text_color=GRAY,
        font=("Arial", 12)
    )

    strength_label.pack(pady=2)

    phone_entry = ctk.CTkEntry(
    card,
    width=350,
    height=40,
    corner_radius=10,
    placeholder_text="Phone Number",
    fg_color=INPUT_COLOR,
    border_width=0
)
    phone_entry.pack(pady=3)

    # Password strength update
    def update_password_strength(event=None):

        password = password_entry.get()

        score = get_password_strength(password)

        if password == "":
            strength_label.configure(
                text="Password Strength: Not entered",
                text_color=GRAY
            )

        elif score <= 2:
            strength_label.configure(
                text="Password Strength: Weak",
                text_color=RED
            )

        elif score <= 4:
            strength_label.configure(
                text="Password Strength: Medium",
                text_color=YELLOW
            )

        else:
            strength_label.configure(
                text="Password Strength: Strong",
                text_color=GREEN
            )

    password_entry.bind(
        "<KeyRelease>",
        update_password_strength
    )

    confirm_entry = ctk.CTkEntry(
        card,
        width=350,
        height=40,
        corner_radius=10,
        placeholder_text="Confirm Password",
        show="*",
        fg_color=INPUT_COLOR,
        border_width=0
    )

    confirm_entry.pack(pady=3)

    def perform_registration():
        print("HASH FUNCTION:", hash_password)
        print("TEST BCRYPT HASH:", hash_password("Test@1234"))
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        phone = phone_entry.get().strip()
        username = username_entry.get().strip()
        password = password_entry.get()
        confirm_password = confirm_entry.get()

        # Check name
        if name == "":
            messagebox.showerror(
                "Registration Error",
                "Please enter your full name."
            )
            return

        # Check email
        if email == "":
            messagebox.showerror(
                "Registration Error",
                "Please enter your email."
            )
            return

        email_pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

        if not re.match(email_pattern, email):
            messagebox.showerror(
                "Registration Error",
                "Please enter a valid email address."
            )
            return

        # Check phone
        if phone == "":
            messagebox.showerror(
                "Registration Error",
                "Please enter your phone number."
            )
            return

        # Check username
        if username == "":
            messagebox.showerror(
                "Registration Error",
                "Please create a username."
            )
            return

        # Check password
        if password == "":
            messagebox.showerror(
                "Registration Error",
                "Please create a password."
            )
            return

        if len(password) < 8:
            messagebox.showerror(
                "Registration Error",
                "Password must contain at least 8 characters."
            )
            return

        # Check password confirmation
        if password != confirm_password:
            messagebox.showerror(
                "Registration Error",
                "Passwords do not match."
            )
            return

        # Hash password before saving
        password_hash = hash_password(password)

        # Save user in database
        try:
            register_user(
                name,
                email,
                phone,
                username,
                password_hash
            )

            messagebox.showinfo(
                "Registration Successful",
                "Account created successfully!"
            )

            login_page()

        except Exception as e:
            messagebox.showerror(
                "Registration Error",
                f"Could not create account.\n\n{e}"
            )


    create_button = ctk.CTkButton(
        card,
        text="CREATE ACCOUNT",
        width=350,
        height=45,
        corner_radius=10,
        fg_color=BLUE,
        hover_color=BLUE_HOVER,
        font=("Arial", 15, "bold"),
        command=perform_registration
    )
    create_button.pack(pady=10)

    login_button = ctk.CTkButton(
        card,
        text="Already have an account? Login",
        width=300,
        fg_color="transparent",
        hover_color=INPUT_COLOR,
        text_color=BLUE,
        command=login_page
    )

    login_button.pack(pady=5)


# =========================================================
# DASHBOARD
# =========================================================

def dashboard_page():

    clear_screen()

    main = ctk.CTkFrame(
        app,
        fg_color=BG_COLOR,
        corner_radius=0
    )

    main.pack(
        fill="both",
        expand=True
    )

    # Top bar
    topbar = ctk.CTkFrame(
        main,
        height=70,
        fg_color=CARD_COLOR,
        corner_radius=0
    )

    topbar.pack(fill="x")

    logo = ctk.CTkLabel(
        topbar,
        text="CP",
        width=45,
        height=45,
        corner_radius=12,
        fg_color=BLUE,
        font=("Arial", 18, "bold")
    )

    logo.pack(
        side="left",
        padx=20,
        pady=12
    )

    title = ctk.CTkLabel(
        topbar,
        text="Customer Persona Analytics",
        text_color=WHITE,
        font=("Arial", 20, "bold")
    )

    title.pack(side="left")

    logout_button = ctk.CTkButton(
        topbar,
        text="Logout",
        width=90,
        fg_color=INPUT_COLOR,
        hover_color="#374151",
        command=welcome_page
    )

    logout_button.pack(
        side="right",
        padx=20
    )

    welcome = ctk.CTkLabel(
        main,
        text="Welcome, " + current_username + "!",
        text_color=WHITE,
        font=("Arial", 30, "bold")
    )

    welcome.pack(
        anchor="w",
        padx=45,
        pady=(40, 5)
    )

    subtitle = ctk.CTkLabel(
        main,
        text="Your customer analytics workspace",
        text_color=GRAY,
        font=("Arial", 15)
    )

    subtitle.pack(
        anchor="w",
        padx=47
    )

    # Cards
    cards = ctk.CTkFrame(
        main,
        fg_color="transparent"
    )

    cards.pack(
        fill="x",
        padx=35,
        pady=40
    )

    # Persona card
    persona_card = ctk.CTkFrame(
        cards,
        fg_color=CARD_COLOR,
        corner_radius=18,
        height=190
    )

    persona_card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=8
    )

    ctk.CTkLabel(
        persona_card,
        text="PERSONA",
        text_color=GRAY,
        font=("Arial", 12, "bold")
    ).pack(pady=(25, 8))

    ctk.CTkLabel(
        persona_card,
        text="Predict Customer",
        text_color=WHITE,
        font=("Arial", 19, "bold")
    ).pack(pady=5)

    ctk.CTkButton(
        persona_card,
        text="Start Prediction",
        width=170,
        command=customer_form_page
    ).pack(pady=15)

    # History card
    history_card = ctk.CTkFrame(
        cards,
        fg_color=CARD_COLOR,
        corner_radius=18,
        height=190
    )

    history_card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=8
    )

    ctk.CTkLabel(
        history_card,
        text="HISTORY",
        text_color=GRAY,
        font=("Arial", 12, "bold")
    ).pack(pady=(25, 8))

    ctk.CTkLabel(
        history_card,
        text="Prediction History",
        text_color=WHITE,
        font=("Arial", 19, "bold")
    ).pack(pady=5)

    ctk.CTkButton(
        history_card,
        text="View History",
        width=170,
        fg_color=INPUT_COLOR,
        command=lambda: messagebox.showinfo(
            "Prediction History",
            "Prediction history will be connected by Member 2."
        )
    ).pack(pady=15)

    # Recommendation card
    recommendation_card = ctk.CTkFrame(
        cards,
        fg_color=CARD_COLOR,
        corner_radius=18,
        height=190
    )

    recommendation_card.pack(
        side="left",
        fill="both",
        expand=True,
        padx=8
    )

    ctk.CTkLabel(
        recommendation_card,
        text="RECOMMENDATIONS",
        text_color=GRAY,
        font=("Arial", 12, "bold")
    ).pack(pady=(25, 8))

    ctk.CTkLabel(
        recommendation_card,
        text="Product Suggestions",
        text_color=WHITE,
        font=("Arial", 19, "bold")
    ).pack(pady=5)

    ctk.CTkButton(
        recommendation_card,
        text="View Recommendations",
        width=190,
        fg_color=INPUT_COLOR,
        command=lambda: messagebox.showinfo(
            "Recommendations",
            "Recommendations will be connected by Member 4."
        )
    ).pack(pady=15)


# =========================================================
# CUSTOMER DETAILS PAGE
# =========================================================

def customer_form_page():

    clear_screen()

    main = ctk.CTkFrame(
        app,
        fg_color=BG_COLOR,
        corner_radius=0
    )

    main.pack(
        fill="both",
        expand=True
    )

    title = ctk.CTkLabel(
        main,
        text="Customer Details",
        text_color=WHITE,
        font=("Arial", 30, "bold")
    )

    title.pack(pady=(35, 5))

    subtitle = ctk.CTkLabel(
        main,
        text="Enter customer information for persona prediction",
        text_color=GRAY,
        font=("Arial", 14)
    )

    subtitle.pack(pady=(0, 20))

    form = ctk.CTkFrame(
        main,
        width=650,
        height=400,
        fg_color=CARD_COLOR,
        corner_radius=20
    )

    form.place(
        relx=0.5,
        rely=0.58,
        anchor="center"
    )

    age_entry = ctk.CTkEntry(
        form,
        width=250,
        height=42,
        placeholder_text="Age",
        fg_color=INPUT_COLOR,
        border_width=0
    )

    age_entry.grid(
        row=0,
        column=0,
        padx=20,
        pady=15
    )

    income_entry = ctk.CTkEntry(
        form,
        width=250,
        height=42,
        placeholder_text="Annual Income",
        fg_color=INPUT_COLOR,
        border_width=0
    )

    income_entry.grid(
        row=0,
        column=1,
        padx=20,
        pady=15
    )

    spending_entry = ctk.CTkEntry(
        form,
        width=250,
        height=42,
        placeholder_text="Spending Score",
        fg_color=INPUT_COLOR,
        border_width=0
    )

    spending_entry.grid(
        row=1,
        column=0,
        padx=20,
        pady=15
    )

    purchases_entry = ctk.CTkEntry(
        form,
        width=250,
        height=42,
        placeholder_text="Purchases per Month",
        fg_color=INPUT_COLOR,
        border_width=0
    )

    purchases_entry.grid(
        row=1,
        column=1,
        padx=20,
        pady=15
    )

    online_entry = ctk.CTkEntry(
        form,
        width=250,
        height=42,
        placeholder_text="Online Shopping Frequency",
        fg_color=INPUT_COLOR,
        border_width=0
    )

    online_entry.grid(
        row=2,
        column=0,
        padx=20,
        pady=15
    )

    category_entry = ctk.CTkEntry(
        form,
        width=250,
        height=42,
        placeholder_text="Preferred Category",
        fg_color=INPUT_COLOR,
        border_width=0
    )

    category_entry.grid(
        row=2,
        column=1,
        padx=20,
        pady=15
    )

    def validate_customer():
        
        global current_persona

        age = age_entry.get().strip()
        income = income_entry.get().strip()
        spending = spending_entry.get().strip()

        if age == "" or income == "" or spending == "":
            messagebox.showerror(
                "Input Error",
                "Please enter Age, Annual Income and Spending Score."
            )
            return

        try:
            age_value = float(age)
            income_value = float(income)
            spending_value = float(spending)
        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Age, income and spending score must be numbers."
            )
            return

        if age_value <= 0:
            messagebox.showerror(
                "Input Error",
                "Age must be greater than zero."
            )
            return

        if income_value < 0:
            messagebox.showerror(
                "Input Error",
                "Income cannot be negative."
            )
            return

        if spending_value < 0:
            messagebox.showerror(
                "Input Error",
                "Spending score cannot be negative."
            )
            return

        messagebox.showinfo(
            "Success",
            "Customer information is valid!\n\n"
            "The ML model will be connected by Member 3."
        )
        
        try:

            # Member 3 - ML prediction
            cluster = predict_cluster(
                age_value,
                gender,
                income_value,
                spending_value
            )

            # Convert cluster to persona
            current_persona = CLUSTER_TO_PERSONA.get(
                cluster,
                "Unknown Persona"
            )

            # Member 4 - Recommendations
            recommendations = get_recommendations(
                current_persona
            )

            recommendation_text = "\n".join(
                "• " + item for item in recommendations
            )

            # Display result
            messagebox.showinfo(
                "Prediction Result",
                f"Cluster: {cluster}\n"
                f"Persona: {current_persona}\n\n"
                f"Recommendations:\n"
                f"{recommendation_text}"
            )

        except Exception as e:

            messagebox.showerror(
                "Prediction Error",
                f"Could not predict customer persona.\n\n{e}"
            )

    predict_button = ctk.CTkButton(
        form,
        text="PREDICT PERSONA",
        width=300,
        height=48,
        corner_radius=10,
        fg_color=BLUE,
        hover_color=BLUE_HOVER,
        font=("Arial", 15, "bold"),
        command=validate_customer
    )

    predict_button.grid(
        row=3,
        column=0,
        columnspan=2,
        pady=20
    )

    back_button = ctk.CTkButton(
        form,
        text="← Back to Dashboard",
        width=180,
        fg_color="transparent",
        hover_color=INPUT_COLOR,
        text_color=GRAY,
        command=dashboard_page
    )

    back_button.grid(
        row=4,
        column=0,
        columnspan=2,
        pady=5
    )


# =========================================================
# START PROGRAM
# =========================================================

welcome_page()

app.mainloop()
