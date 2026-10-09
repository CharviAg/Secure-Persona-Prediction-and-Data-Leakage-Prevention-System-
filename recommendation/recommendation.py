from datetime import date, timedelta

# ---------------------------------------------------------
# Offer catalogue (edit these to match your real store offers)
# {item} is replaced by the customer's preferred category,
# or "products" if no category was entered.
# ---------------------------------------------------------
OFFER_CATALOG = {
    "High-Value Customer": {
        "valid_days": 30,
        "offers": [
            ("Gold Member: 20% off {item}", "Exclusive member price on every order this month.", "GOLD20"),
            ("Early access to new {item}", "Shop new arrivals 48 hours before everyone else.", "EARLY48"),
            ("Free express delivery", "No delivery charge on any order, no minimum.", "FREEFAST"),
            ("2x loyalty points", "Earn double reward points on all purchases.", "POINTS2X"),
        ],
    },
    "Budget Customer": {
        "valid_days": 14,
        "offers": [
            ("Flat 15% off {item}", "Everyday savings on your regular buys.", "SAVE15"),
            ("Buy 2 Get 1 Free", "Combo deal on selected {item}.", "B2G1"),
            ("Rs. 100 off above Rs. 999", "Instant discount on bigger baskets.", "SAVE100"),
            ("Seasonal sale: up to 40% off", "Clearance prices on {item}.", "SEASON40"),
        ],
    },
    "Potential Customer": {
        "valid_days": 21,
        "offers": [
            ("10% off your next order", "Welcome-back discount on {item}.", "WELCOME10"),
            ("Free product demo / trial", "Try selected {item} for 7 days before you commit.", "TRY7"),
            ("Rs. 250 off above Rs. 1,999", "Premium picks at a lower first price.", "FIRST250"),
            ("Extra 5% when you buy 2+", "Bundle {item} and save more.", "BUNDLE5"),
        ],
    },
    "Impulsive Spender": {
        "valid_days": 3,
        "offers": [
            ("24-hour flash sale: 25% off {item}", "Ends soon - limited stock.", "FLASH25"),
            ("Trending now: 2 for 1", "Most-viewed {item} this week.", "TREND2X"),
            ("Spend Rs. 1,500, get Rs. 300 voucher", "Voucher is added for your next visit.", "VOUCH300"),
            ("Free gift with your order", "On selected {item}, while stocks last.", "GIFTFREE"),
        ],
    },
}

FREQUENT_WORDS = ("daily", "weekly", "often", "every", "regular", "frequent")


def get_offers(persona, category=None, online_frequency=None, purchases_per_month=None):
    """
    Returns 4 concrete offers for the persona:
        [{"title", "detail", "code", "valid_till"}, ...]
    Personalised using the optional details when they are given.
    """
    plan = OFFER_CATALOG.get(persona)
    if plan is None:
        return [{
            "title": "General product recommendations",
            "detail": "Browse our latest products.",
            "code": "-",
            "valid_till": "-",
        }]

    item = (category or "").strip() or "products"
    expiry = (date.today() + timedelta(days=plan["valid_days"])).strftime("%d %b %Y")

    offers = [
        {
            "title": title.format(item=item),
            "detail": detail.format(item=item),
            "code": code,
            "valid_till": expiry,
        }
        for title, detail, code in plan["offers"]
    ]

    # Personalise the last slot from shopping habits
    online = (online_frequency or "").strip().lower()
    if online and any(word in online for word in FREQUENT_WORDS):
        offers[3] = {
            "title": "App & online exclusive: extra 5% off",
            "detail": "Because you shop online often - applies on top of other offers.",
            "code": "ONLINE5",
            "valid_till": expiry,
        }
    elif purchases_per_month is not None and purchases_per_month >= 5:
        offers[3] = {
            "title": "Loyalty cashback: Rs. 200 after your 5th order",
            "detail": "Reward for shopping with us regularly each month.",
            "code": "LOYAL200",
            "valid_till": expiry,
        }

    return offers


def get_recommendations(persona):
    """Short list of offer titles (used for history and the PDF report)."""
    return [offer["title"] for offer in get_offers(persona)]


def get_explanation(persona, income, spending_score):
    if persona == "High-Value Customer":
        return (
            f"The customer has an income of Rs.{income} "
            f"and a spending score of {spending_score}. "
            "High income and high spending behaviour indicate "
            "strong purchasing capacity."
        )
    elif persona == "Budget Customer":
        return (
            f"The customer has an income of Rs.{income} "
            f"and a spending score of {spending_score}. "
            "Lower income and spending behaviour indicate "
            "price-sensitive purchasing behaviour."
        )
    elif persona == "Potential Customer":
        return (
            f"The customer has an income of Rs.{income} "
            f"and a spending score of {spending_score}. "
            "The customer has good purchasing capacity but "
            "comparatively lower spending behaviour."
        )
    elif persona == "Impulsive Spender":
        return (
            f"The customer has an income of Rs.{income} "
            f"and a spending score of {spending_score}. "
            "High spending relative to income indicates "
            "strong spending behaviour."
        )
    return "General customer segment."
