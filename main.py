from security import hash_password
from predict_persona import predict_persona
from recommendation.recommendation import get_offers, get_explanation

current_persona = None
current_user_id = None
last_result = None        # latest prediction (shown on the result page)

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
    create_tables,
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
            global current_username, current_user_id, current_persona, last_result
            current_user_id = user[0]
            current_username = user[4]
            current_persona = None
            last_result = None

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

        if not re.match(r"^\+?[0-9]{10,15}$", phone):
            messagebox.showerror(
                "Registration Error",
                "Please enter a valid phone number (10-15 digits)."
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
# SESSION / HISTORY / RECOMMENDATION HELPERS
# =========================================================

def logout():
    global current_username, current_user_id, current_persona, last_result
    current_username = "User"
    current_user_id = None
    current_persona = None
    last_result = None
    welcome_page()


PERSONA_STYLE = {
    "High-Value Customer": GREEN,
    "Budget Customer": BLUE,
    "Potential Customer": YELLOW,
    "Impulsive Spender": RED,
}

PERSONA_INFO = {
    "High-Value Customer": "High income and high spending",
    "Budget Customer": "Lower income and careful spending",
    "Potential Customer": "High income but low spending",
    "Impulsive Spender": "High spending for their income",
}


def create_topbar(parent):
    """Top bar shared by all inner pages."""
    topbar = ctk.CTkFrame(parent, height=70, fg_color=CARD_COLOR, corner_radius=0)
    topbar.pack(fill="x")

    ctk.CTkLabel(
        topbar, text="CP", width=45, height=45, corner_radius=12,
        fg_color=BLUE, font=("Arial", 18, "bold")
    ).pack(side="left", padx=20, pady=12)

    ctk.CTkLabel(
        topbar, text="Customer Persona Analytics",
        text_color=WHITE, font=("Arial", 20, "bold")
    ).pack(side="left")

    ctk.CTkButton(
        topbar, text="Logout", width=90,
        fg_color=INPUT_COLOR, hover_color="#374151", command=logout
    ).pack(side="right", padx=20)

    ctk.CTkButton(
        topbar, text="Dashboard", width=100,
        fg_color=INPUT_COLOR, hover_color="#374151", command=dashboard_page
    ).pack(side="right")


def new_page():
    clear_screen()
    main = ctk.CTkFrame(app, fg_color=BG_COLOR, corner_radius=0)
    main.pack(fill="both", expand=True)
    create_topbar(main)
    return main


def stat_bar(parent, label, text, value, color):
    """Label + value + progress bar (value between 0 and 1)."""
    row = ctk.CTkFrame(parent, fg_color="transparent")
    row.pack(fill="x", padx=25, pady=(10, 0))

    ctk.CTkLabel(row, text=label, text_color=GRAY,
                 font=("Arial", 12)).pack(side="left")
    ctk.CTkLabel(row, text=text, text_color=WHITE,
                 font=("Arial", 13, "bold")).pack(side="right")

    bar = ctk.CTkProgressBar(parent, height=10, progress_color=color,
                             fg_color=INPUT_COLOR)
    bar.pack(fill="x", padx=25, pady=(4, 0))
    bar.set(max(0, min(1, value)))


def recommendation_cards(parent, offers, color, columns=2):
    """Offer cards: title, short detail, coupon code and expiry date."""
    grid = ctk.CTkFrame(parent, fg_color="transparent")
    grid.pack(fill="x", padx=20, pady=5)

    for c in range(columns):
        grid.grid_columnconfigure(c, weight=1, uniform="offer")

    for i, offer in enumerate(offers):
        card = ctk.CTkFrame(grid, fg_color=INPUT_COLOR, corner_radius=12)
        card.grid(row=i // columns, column=i % columns,
                  padx=6, pady=6, sticky="nsew")

        ctk.CTkLabel(
            card, text=offer["title"], text_color=WHITE,
            font=("Arial", 14, "bold"), wraplength=215, justify="left",
            anchor="w"
        ).pack(anchor="w", padx=14, pady=(10, 2))

        ctk.CTkLabel(
            card, text=offer["detail"], text_color=GRAY,
            font=("Arial", 12), wraplength=215, justify="left",
            anchor="w"
        ).pack(anchor="w", padx=14)

        footer = ctk.CTkFrame(card, fg_color="transparent")
        footer.pack(fill="x", padx=14, pady=(6, 10))

        ctk.CTkLabel(
            footer, text="CODE: " + offer["code"], text_color=BG_COLOR,
            fg_color=color, corner_radius=6, height=22,
            font=("Arial", 11, "bold")
        ).pack(side="left")

        ctk.CTkLabel(
            footer, text="Valid till " + offer["valid_till"],
            text_color=GRAY, font=("Arial", 11)
        ).pack(side="right")


def result_page(result):
    """Shows the prediction result on a full page (no popup)."""
    persona = result["persona"]
    color = PERSONA_STYLE.get(persona, BLUE)
    offers = result["offers"]
    reason = get_explanation(
        persona, f"{result['income']:,.0f}K", f"{result['spending']:.0f}"
    )

    main = new_page()

    ctk.CTkLabel(main, text="Prediction Result", text_color=WHITE,
                 font=("Arial", 26, "bold")).pack(anchor="w", padx=35, pady=(15, 8))

    body = ctk.CTkFrame(main, fg_color="transparent")
    body.pack(fill="both", expand=True, padx=30)

    # ---------- left: persona + customer details
    left = ctk.CTkFrame(body, fg_color=CARD_COLOR, corner_radius=18, width=330)
    left.pack(side="left", fill="y", padx=(5, 10), pady=5)
    left.pack_propagate(False)

    ctk.CTkLabel(left, text="PREDICTED PERSONA", text_color=GRAY,
                 font=("Arial", 12, "bold")).pack(pady=(22, 8))

    ctk.CTkLabel(
        left, text=persona, text_color=BG_COLOR, fg_color=color,
        corner_radius=14, width=270, height=52, font=("Arial", 19, "bold")
    ).pack()

    ctk.CTkLabel(left, text=PERSONA_INFO.get(persona, ""), text_color=GRAY,
                 font=("Arial", 12)).pack(pady=(8, 0))

    ctk.CTkLabel(left, text=f"Cluster {result['cluster']}  •  "
                            f"{result['gender']}, age {result['age']}",
                 text_color=WHITE, font=("Arial", 13)).pack(pady=(4, 6))

    stat_bar(left, "Spending Score", f"{result['spending']:.0f} / 100",
             result["spending"] / 100, color)
    stat_bar(left, "Annual Income", f"Rs. {result['income']:,.0f}K",
             result["income"] / 1200, color)

    # ---------- right: reason + recommendations
    right = ctk.CTkFrame(body, fg_color=CARD_COLOR, corner_radius=18)
    right.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=5)

    ctk.CTkLabel(right, text="WHY THIS PERSONA?", text_color=GRAY,
                 font=("Arial", 12, "bold")).pack(anchor="w", padx=25, pady=(22, 6))

    ctk.CTkLabel(
        right, text=reason, text_color=WHITE, font=("Arial", 14),
        wraplength=470, justify="left"
    ).pack(anchor="w", padx=25)

    ctk.CTkLabel(right, text="RECOMMENDED OFFERS", text_color=GRAY,
                 font=("Arial", 12, "bold")).pack(anchor="w", padx=25, pady=(20, 4))

    recommendation_cards(right, offers, color)

    # ---------- bottom buttons
    status = ctk.CTkLabel(main, text="", text_color=GREEN, font=("Arial", 12))
    status.pack(pady=(4, 0))

    def download_report():
        try:
            from reports.report_generator import generate_report
            path = generate_report(
                current_username,
                result["income"] * 1000,
                result["spending"],
                persona,
                reason,
                [f"{o['title']} (code {o['code']}, valid till {o['valid_till']})"
                 for o in offers]
            )
            status.configure(text="PDF report saved: " + path, text_color=GREEN)
        except Exception as e:
            status.configure(text=f"Could not create report: {e}", text_color=RED)

    buttons = ctk.CTkFrame(main, fg_color="transparent")
    buttons.pack(pady=(4, 15))

    ctk.CTkButton(buttons, text="Predict Another", width=170, height=40,
                  command=customer_form_page).pack(side="left", padx=8)
    ctk.CTkButton(buttons, text="Download PDF Report", width=190, height=40,
                  fg_color=INPUT_COLOR, hover_color="#374151",
                  command=download_report).pack(side="left", padx=8)
    ctk.CTkButton(buttons, text="View History", width=150, height=40,
                  fg_color=INPUT_COLOR, hover_color="#374151",
                  command=history_page).pack(side="left", padx=8)


def recommendations_page():
    """Latest prediction's recommendations, or an overview of every persona."""
    if last_result is not None:
        result_page(last_result)
        return

    main = new_page()

    ctk.CTkLabel(main, text="Offers & Recommendations", text_color=WHITE,
                 font=("Arial", 26, "bold")).pack(anchor="w", padx=35, pady=(15, 2))
    ctk.CTkLabel(main, text="No prediction yet - here are the offers we use for each persona.",
                 text_color=GRAY, font=("Arial", 13)).pack(anchor="w", padx=37, pady=(0, 8))

    grid = ctk.CTkFrame(main, fg_color="transparent")
    grid.pack(fill="both", expand=True, padx=30)
    grid.grid_columnconfigure((0, 1), weight=1)

    for i, (persona, color) in enumerate(PERSONA_STYLE.items()):
        card = ctk.CTkFrame(grid, fg_color=CARD_COLOR, corner_radius=16)
        card.grid(row=i // 2, column=i % 2, padx=8, pady=8, sticky="nsew")

        ctk.CTkLabel(card, text=persona, text_color=BG_COLOR, fg_color=color,
                     corner_radius=10, height=34, width=220,
                     font=("Arial", 15, "bold")).pack(pady=(14, 4))
        ctk.CTkLabel(card, text=PERSONA_INFO[persona], text_color=GRAY,
                     font=("Arial", 12)).pack(pady=(0, 6))

        for offer in get_offers(persona):
            ctk.CTkLabel(card, text="●  " + offer["title"] + "   [" + offer["code"] + "]",
                         text_color=WHITE, font=("Arial", 13),
                         anchor="w").pack(anchor="w", padx=30, pady=1)

        ctk.CTkLabel(card, text="").pack(pady=2)

    ctk.CTkButton(main, text="Start Prediction", width=200, height=40,
                  command=customer_form_page).pack(pady=12)


def history_page():
    """Prediction history shown as a table on its own page (no popup)."""
    main = new_page()

    ctk.CTkLabel(main, text="Prediction History", text_color=WHITE,
                 font=("Arial", 26, "bold")).pack(anchor="w", padx=35, pady=(15, 8))

    history = get_prediction_history(current_user_id)

    if not history:
        empty = ctk.CTkFrame(main, fg_color=CARD_COLOR, corner_radius=18)
        empty.pack(fill="x", padx=35, pady=20)
        ctk.CTkLabel(empty, text="No predictions yet", text_color=WHITE,
                     font=("Arial", 20, "bold")).pack(pady=(35, 5))
        ctk.CTkLabel(empty, text="Your predictions will appear here.",
                     text_color=GRAY, font=("Arial", 13)).pack()
        ctk.CTkButton(empty, text="Start Prediction", width=190, height=40,
                      command=customer_form_page).pack(pady=25)
        return

    table = ctk.CTkScrollableFrame(main, fg_color=CARD_COLOR, corner_radius=16)
    table.pack(fill="both", expand=True, padx=35, pady=(0, 20))

    headers = ["#", "Age", "Gender", "Income (K)", "Score", "Cluster", "Persona"]
    widths = [50, 60, 80, 110, 70, 80, 200]

    for col, (h, w) in enumerate(zip(headers, widths)):
        ctk.CTkLabel(table, text=h, text_color=GRAY, width=w, anchor="w",
                     font=("Arial", 12, "bold")).grid(row=0, column=col, padx=6, pady=8)

    for r, (pid, age, gender, income, score, cluster, persona, _rec) in enumerate(history, start=1):
        color = PERSONA_STYLE.get(persona, WHITE)
        values = [pid, age, gender, f"{income:,.0f}", f"{score:.0f}", cluster, persona]
        for col, (v, w) in enumerate(zip(values, widths)):
            ctk.CTkLabel(table, text=str(v), width=w, anchor="w",
                         text_color=color if col == 6 else WHITE,
                         font=("Arial", 13, "bold" if col == 6 else "normal")
                         ).grid(row=r, column=col, padx=6, pady=5)


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
        command=logout
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
        command=history_page
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
        text="OFFERS",
        text_color=GRAY,
        font=("Arial", 12, "bold")
    ).pack(pady=(25, 8))

    ctk.CTkLabel(
        recommendation_card,
        text="Personalised Offers",
        text_color=WHITE,
        font=("Arial", 19, "bold")
    ).pack(pady=5)

    ctk.CTkButton(
        recommendation_card,
        text="View Offers",
        width=190,
        fg_color=INPUT_COLOR,
        command=recommendations_page
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

    title.pack(pady=(18, 2))

    subtitle = ctk.CTkLabel(
        main,
        text="Fill in the customer's details below.  Fields marked * are required.",
        text_color=GRAY,
        font=("Arial", 14)
    )

    subtitle.pack(pady=(0, 8))

    form = ctk.CTkFrame(
        main,
        width=650,
        height=400,
        fg_color=CARD_COLOR,
        corner_radius=20
    )

    form.place(
        relx=0.5,
        rely=1.0,
        y=-12,
        anchor="s"
    )

    def make_field(row, col, label, hint, placeholder, required=False):
        """Label above the box, example inside it, short explanation below it."""
        cell = ctk.CTkFrame(form, fg_color="transparent")
        cell.grid(row=row, column=col, padx=22, pady=(8, 2), sticky="w")

        ctk.CTkLabel(
            cell,
            text=label + (" *" if required else ""),
            text_color=WHITE,
            font=("Arial", 13, "bold")
        ).pack(anchor="w")

        entry = ctk.CTkEntry(
            cell,
            width=270,
            height=36,
            placeholder_text=placeholder,
            fg_color=INPUT_COLOR,
            border_width=0
        )
        entry.pack(pady=(3, 2))

        ctk.CTkLabel(
            cell,
            text=hint,
            text_color=GRAY,
            font=("Arial", 11)
        ).pack(anchor="w")

        return entry

    age_entry = make_field(
        0, 0, "Age (in years)",
        "How old the customer is",
        "e.g. 28", required=True)

    income_entry = make_field(
        0, 1, "Annual Income (Rs. thousands)",
        "Yearly income in thousands: 650 = Rs. 650,000",
        "e.g. 650", required=True)

    spending_entry = make_field(
        1, 0, "Spending Score (1-100)",
        "How much they spend: 1 = very low, 100 = very high",
        "e.g. 60", required=True)

    purchases_entry = make_field(
        1, 1, "Purchases per Month",
        "Optional - number of purchases made each month",
        "e.g. 4")

    online_entry = make_field(
        2, 0, "Online Shopping Frequency",
        "Optional - how often they shop online",
        "e.g. Weekly")

    category_entry = make_field(
        2, 1, "Preferred Category",
        "Optional - the product type they like most",
        "e.g. Fashion")

    gender_cell = ctk.CTkFrame(form, fg_color="transparent")
    gender_cell.grid(row=3, column=0, padx=22, pady=(8, 2), sticky="w")

    ctk.CTkLabel(
        gender_cell,
        text="Gender *",
        text_color=WHITE,
        font=("Arial", 13, "bold")
    ).pack(anchor="w")

    gender_menu = ctk.CTkOptionMenu(
        gender_cell,
        values=["Male", "Female"],
        width=270,
        height=36
    )

    gender_menu.set("Male")
    gender_menu.pack(pady=(3, 2))

    ctk.CTkLabel(
        gender_cell,
        text="Choose the customer's gender",
        text_color=GRAY,
        font=("Arial", 11)
    ).pack(anchor="w")

    error_label = ctk.CTkLabel(
        form,
        text="",
        text_color=RED,
        font=("Arial", 12)
    )

    error_label.grid(row=4, column=0, columnspan=2, pady=(4, 0))

    def show_error(message):
        error_label.configure(text=message)

    def validate_customer():

        global current_persona, last_result

        show_error("")

        age = age_entry.get().strip()
        income = income_entry.get().strip()
        spending = spending_entry.get().strip()

        if age == "" or income == "" or spending == "":
            show_error("Please enter Age, Annual Income and Spending Score.")
            return

        try:
            age_value = float(age)
            income_value = float(income)
            spending_value = float(spending)
        except ValueError:
            show_error("Age, income and spending score must be numbers.")
            return

        if age_value <= 0:
            show_error("Age must be greater than zero.")
            return

        if income_value < 0:
            show_error("Income cannot be negative.")
            return

        if spending_value < 0:
            show_error("Spending score cannot be negative.")
            return

        if spending_value > 100:
            show_error("Spending score must be between 0 and 100.")
            return

        gender = gender_menu.get()

        category = category_entry.get().strip()
        online_frequency = online_entry.get().strip()
        purchases_text = purchases_entry.get().strip()
        purchases_value = None

        if purchases_text != "":
            try:
                purchases_value = float(purchases_text)
            except ValueError:
                show_error("Purchases per month must be a number.")
                return

            if purchases_value < 0:
                show_error("Purchases per month cannot be negative.")
                return

        try:

            # ML prediction (cluster + persona)
            cluster, persona = predict_persona(
                age_value,
                gender,
                income_value,
                spending_value
            )

            current_persona = persona

            # Recommendations
            offers = get_offers(
                current_persona,
                category,
                online_frequency,
                purchases_value
            )

            recommendations = [offer["title"] for offer in offers]

            # Save to prediction history
            save_prediction(
                current_user_id,
                int(age_value),
                gender,
                income_value,
                spending_value,
                cluster,
                current_persona,
                "; ".join(recommendations)
            )

            # Show the result on its own page
            last_result = {
                "age": int(age_value),
                "gender": gender,
                "income": income_value,
                "spending": spending_value,
                "cluster": cluster,
                "persona": current_persona,
                "recommendations": recommendations,
                "offers": offers
            }

            result_page(last_result)

        except Exception as e:

            show_error(f"Could not predict customer persona: {e}")

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
        row=5,
        column=0,
        columnspan=2,
        pady=(6, 4)
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
        row=6,
        column=0,
        columnspan=2,
        pady=(0, 8)
    )


# =========================================================
# START PROGRAM
# =========================================================

create_tables()

welcome_page()

app.mainloop()
