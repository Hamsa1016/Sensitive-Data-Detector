import re

# ==========================================================
# REGEX PATTERNS
# ==========================================================

patterns = {

    "Email Addresses":
        r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b",


    "Phone Numbers":
        r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",


    "PAN Numbers":
        r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",


    "Aadhaar Numbers":
        r"(?i)(?:aadhaar|aadhaar number)\s*[:=-]?\s*(\d{4}\s\d{4}\s\d{4}|\d{12})",


    "Credit Card Numbers":
        r"\b(?:\d{4}[- ]?){3}\d{4}\b",


    "Employee IDs":
        r"\b(?:EMP|Emp|emp)[-_]?\d+\b",


    "Passwords":
        r"(?i)password\s*[:=]\s*.+",


    "API Keys":
        r"(?i)AP[I1L][_\s-]?KEY\s*[:=-]?\s*(sk[_A-Za-z0-9]+)",

    "Account Numbers":
        r"(?i)(?:account\s*number|account\s*no|a/c)\s*[:=-]?\s*(\d{9,18})",

    "IFSC Codes":
        r"(?i)ifsc\s*[:=-]?\s*([A-Z]{4}0[A-Z0-9]{6})"

    # "Phone Numbers":
    #     r"(?i)(?:phone)?\s*[:=-]?\s*(\+91[- ]?[6-9]\d{9}|[6-9]\d{9})",

    # "PAN Numbers":
    #     r"(?i)(?:pan)?\s*[:=-]?\s*([A-Z]{5}[0-9]{4}[A-Z])",

    # "Aadhaar Numbers":
    #     r"(?i)(?:aadhaar|aadhaar number)\s*[:=-]?\s*(\d{4}\s\d{4}\s\d{4}|\d{12})",

    # "Employee IDs":
    #     r"(?i)(?:employee\s*id|emp\s*id)\s*[:=-]?\s*(EMP\d+)",

    # "API Keys":
    #     r"(?i)(?:api[_\s-]?key)\s*[:=-]?\s*(sk_[A-Za-z0-9_]+)",

    # "Account Numbers":
    #     r"(?i)(?:account\s*number|account\s*no|a/c)\s*[:=-]?\s*(\d{9,18})",

    # "IFSC Codes":
    #     r"(?i)(?:ifsc)\s*[:=-]?\s*([A-Z]{4}0[A-Z0-9]{6})"

}
# ==========================================================
# DETECT SENSITIVE DATA
# ==========================================================

def detect_sensitive_data(text):

    results = {}
    print("OCR Text:", text)
    # OCR corrections
    text = text.replace("!", "1")
    text = text.replace("|", "1")
    text = re.sub(r"EMP[I!]", "EMP1", text)
    for category, pattern in patterns.items():

        matches = re.findall(pattern, text, re.IGNORECASE)

        cleaned = []
    

        for item in matches:

            if isinstance(item, tuple):
                item = "".join(item)

            item = str(item).strip()

            if item and item not in cleaned:
                cleaned.append(item)

        results[category] = cleaned

    return results
    # ==========================================================
# CONFIDENTIAL BUSINESS INFORMATION
# ==========================================================

# def detect_confidential_information(text):

#     keywords = [

#         "confidential",
#         "internal use only",
#         "trade secret",
#         "restricted",
#         "private",
#         "company confidential",
#         "do not share",
#         "proprietary",
#         "classified"

#     ]

#     found = []

#     lower_text = text.lower()

#     for word in keywords:

#         if word in lower_text:

#             found.append(word.title())

#     return found
def detect_confidential_information(text):

    keywords = [
        "confidential",
        "internal use only",
        "trade secret",
        "restricted",
        "private",
        "company confidential",
        "do not share",
        "proprietary",
        "classified"
    ]

    found = []

    lower_text = text.lower()

    # OCR corrections
    lower_text = lower_text.replace("0", "o")
    lower_text = lower_text.replace("1", "l")
    lower_text = lower_text.replace("c0nfidential", "confidential")
    lower_text = lower_text.replace("0nly", "only")

    for word in keywords:

        if word in lower_text:
            found.append(word.title())

    return found


# ==========================================================
# TOTAL SENSITIVE ITEMS
# ==========================================================

def total_sensitive_items(results):

    total = 0

    for values in results.values():
        total += len(values)

    return total


# ==========================================================
# MASK SENSITIVE VALUES (ADVANCED)
# ==========================================================

def mask_value(value):

    value = str(value).strip()
    # ----------------------------
    # Password
    # ----------------------------

    if value.lower().startswith("password"):

        return "Password = ********"

    # ----------------------------
    # Password / API Key
    # ----------------------------

    if (
    value.startswith("sk_")
    or value.startswith("AIza")
    or value.startswith("ghp_")
    or value.startswith("AKIA")
):

        return value[:3] + "********" + value[-4:]

    # ----------------------------
    # Email
    # ----------------------------

    if "@" in value:

        username, domain = value.split("@")

        if len(username) > 1:

            masked_user = username[0] + "*" * (len(username)-1)

        else:

            masked_user = "*"

        return masked_user + "@" + domain



    # ----------------------------
    # Phone Number
    # ----------------------------

    phone = value.replace("+91","").replace("-","").replace(" ","")

    if phone.isdigit() and len(phone) == 10:

        return "******" + phone[-4:]



    # ----------------------------
    # Aadhaar
    # ----------------------------

    aadhaar = value.replace(" ","")

    if aadhaar.isdigit() and len(aadhaar)==12:

        return "********" + aadhaar[-4:]



    # ----------------------------
    # PAN
    # ----------------------------

    if re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", value):

        return "*****" + value[5:]



    # ----------------------------
    # Credit Card
    # ----------------------------

    card = value.replace(" ","").replace("-","")

    if card.isdigit() and len(card)==16:

        return "**** **** **** " + card[-4:]



    # ----------------------------
    # Employee ID
    # ----------------------------

    if re.match(r"(?i)emp[-_]?\d+", value):

        return value[:3] + "****"


    # ----------------------------
    # Bank details
    # ----------------------------

    if re.fullmatch(r"[A-Z]{4}0[A-Z0-9]{6}", value):
        return value[:4] + "******" + value[-2:]





    return value