import re

def get_case_summary(text):
    case_type = "an unknown"
    court_name = "an unspecified court"
    judgement_date = "not mentioned"

    # Court name
    court_match = re.search(r'(HIGH COURT OF [A-Z ]+|SUPREME COURT OF INDIA)', text, re.IGNORECASE)
    if court_match:
        court_name = court_match.group(0).title()

    # Judgment date
    date_match = re.search(
        r'\b(?:\d{1,2}(?:st|nd|rd|th)?[ ,/-]*)?(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[ ,/-]*\d{2,4}',
        text, re.IGNORECASE
    )
    if date_match:
        judgement_date = date_match.group(0)

    # Case type
    lowered = text.lower()
    if "writ petition" in lowered:
        case_type = "a writ petition"
    elif "civil appeal" in lowered:
        case_type = "a civil appeal"
    elif "criminal appeal" in lowered:
        case_type = "a criminal appeal"

    return f"The legal document is related to {case_type} case, the date of judgment is {judgement_date}, and the court is {court_name}."
