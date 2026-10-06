def get_recommendations(persona, income=None, spending_score=None):
    recommendations = []

    # High-Value Customer
    if persona == "High-Value Customer":
        recommendations = [
            "Premium products",
            "Exclusive loyalty rewards",
            "Early access to new products",
            "Personalized premium offers"
        ]

        if spending_score is not None and spending_score >= 80:
            recommendations.append("VIP membership benefits")

        if spending_score is not None and spending_score >= 70:
            recommendations.append("High-value customer exclusive deals")

    # Budget Customer
    elif persona == "Budget Customer":
        recommendations = [
            "Budget-friendly products",
            "Discount coupons",
            "Combo offers",
            "Seasonal sale products"
        ]

        if spending_score is not None and spending_score < 40:
            recommendations.append("Extra savings and discount offers")

        if spending_score is not None and spending_score >= 40:
            recommendations.append("Value-for-money product bundles")

    # Potential Customer
    elif persona == "Potential Customer":
        recommendations = [
            "Premium trial offers",
            "Personalized promotions",
            "First-purchase discounts",
            "Product demonstrations"
        ]

        if spending_score is not None and spending_score < 50:
            recommendations.append("Low-risk introductory offers")

        if spending_score is not None and spending_score >= 50:
            recommendations.append("Upgrade offers for premium products")

    # Impulsive Spender
    elif persona == "Impulsive Spender":
        recommendations = [
            "Limited-time offers",
            "Flash sales",
            "Trending products",
            "Personalized deals"
        ]

        if spending_score is not None and spending_score >= 80:
            recommendations.append("Exclusive limited-time deals")

        if spending_score is not None and spending_score >= 70:
            recommendations.append("Trending product recommendations")

    else:
        recommendations = [
            "General product recommendations",
            "Popular products",
            "Seasonal offers"
        ]

    return recommendations


def get_explanation(persona, income, spending_score):

    if persona == "High-Value Customer":
        return (
            f"The customer has an income of Rs.{income} "
            f"and a spending score of {spending_score}. "
            "High spending behaviour indicates strong purchasing "
            "capacity and suitability for premium offers."
        )

    elif persona == "Budget Customer":
        return (
            f"The customer has an income of Rs.{income} "
            f"and a spending score of {spending_score}. "
            "The customer shows price-sensitive purchasing behaviour, "
            "so discounts and value-for-money offers are recommended."
        )

    elif persona == "Potential Customer":
        return (
            f"The customer has an income of Rs.{income} "
            f"and a spending score of {spending_score}. "
            "The customer has potential for higher engagement, "
            "so introductory and personalized offers are recommended."
        )

    elif persona == "Impulsive Spender":
        return (
            f"The customer has an income of Rs.{income} "
            f"and a spending score of {spending_score}. "
            "High spending behaviour indicates that limited-time "
            "offers and trending products may be effective."
        )

    return "General customer segment."


def get_customer_insight(persona, income, spending_score):

    if spending_score >= 80:
        spending_level = "very high"
    elif spending_score >= 60:
        spending_level = "high"
    elif spending_score >= 40:
        spending_level = "moderate"
    else:
        spending_level = "low"

    return (
        f"The customer belongs to the {persona} segment "
        f"with a {spending_level} spending level. "
        "Recommendations are personalized according to "
        "the customer's persona and spending behaviour."
    )
