# ==========================================================
# RISK SCORE CONFIGURATION
# ==========================================================

RISK_SCORES = {

    "Email Addresses": 2,

    "Phone Numbers": 2,

    "Employee IDs": 3,

    "PAN Numbers": 8,

    "Aadhaar Numbers": 10,

    "Credit Card Numbers": 12,

    "Passwords": 15,

    "API Keys": 15

}


# ==========================================================
# RISK CLASSIFICATION FUNCTION
# ==========================================================

def classify_risk(results):

    total_score = 0

    score_details = {}

    sensitive_items = 0

    # Calculate Risk Score
    for category, items in results.items():

        count = len(items)

        sensitive_items += count

        category_score = count * RISK_SCORES.get(category, 0)

        score_details[category] = category_score

        total_score += category_score

    # Risk Level
    if total_score <= 5:

        risk = "🟢 LOW"

        risk_color = "green"

    elif total_score <= 20:

        risk = "🟡 MEDIUM"

        risk_color = "orange"

    else:

        risk = "🔴 HIGH"

        risk_color = "red"

    return (
        risk,
        total_score,
        score_details
    )


# ==========================================================
# OPTIONAL HELPER FUNCTION
# ==========================================================

def get_risk_message(risk):

    if "LOW" in risk:

        return "Minimal sensitive information detected."

    elif "MEDIUM" in risk:

        return "Moderate amount of sensitive information detected."

    else:

        return "Highly sensitive document. Immediate attention recommended."