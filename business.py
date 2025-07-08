# business data
BUSINESS_INFO = {
    "name": "Untitled Company",
    "hours": {
        "monday": "9:00 - 18:00",
        "tuesday": "9:00 - 18:00",
        "wednesday": "9:00 - 18:00",
        "thursday": "9:00 - 18:00",
        "friday": "9:00 - 18:00",
        "saturday": "10:00 - 15:00",
        "sunday": "Closed"
    },
    "contact": {
        "phone": "+998 71 123 45 67",
        "email": "info@untitledcompany.com",
        "address": "123 Example Street, Uzbekistan, Tashkent"
    },
    "faq": [
        {
            "question": "How do I schedule a consultation?",
            "answer": "You can schedule a consultation by phone or through the form on our website."
        },
        {
            "question": "What payment methods do you accept?",
            "answer": "We accept cash, credit cards, and electronic payments."
        },
        {
            "question": "Do you offer delivery?",
            "answer": "Yes, we provide delivery services throughout the city."
        }
    ]
}

# func to search for answers
def get_answer(query):
    """Searches for an answer to a question in the business database"""
    if not query:
        return None
        
    query = query.lower()
    
    # check for keywords
    if any(word in query for word in ["hours", "schedule", "open", "working"]):
        hours_info = "\n".join([f"{day.capitalize()}: {hours}" for day, hours in BUSINESS_INFO["hours"].items()])
        return f"Our working hours:\n{hours_info}"
    
    elif any(word in query for word in ["address", "location", "where"]):
        return f"Our address: {BUSINESS_INFO['contact']['address']}"
    
    elif any(word in query for word in ["phone", "call", "contact", "number"]):
        return f"Our phone number: {BUSINESS_INFO['contact']['phone']}"
    
    elif any(word in query for word in ["mail", "email", "e-mail"]):
        return f"Our email: {BUSINESS_INFO['contact']['email']}"
    
    # search in FAQ
    for item in BUSINESS_INFO["faq"]:
        if any(word in item["question"].lower() for word in query.split()):
            return item["answer"]
    
    return None