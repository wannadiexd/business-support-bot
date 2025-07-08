import streamlit as st
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
from business import BUSINESS_INFO, get_answer

load_dotenv()

st.set_page_config(
    page_title=BUSINESS_INFO["name"],
    page_icon="🏢",
    layout="wide"
)

# func to check if email is valid (basic check)
def is_valid_email(email):
    """Simple function to check if email contains @ symbol"""
    return "@" in email

# func to create a GitHub Issue
def create_github_issue(title, body, labels=None):
    """
    Creates a new issue in the GitHub repository
    Returns (success, result) where:
    - success: True if issue was created, False otherwise
    - result: Issue URL if successful, error message if not
    """
    token = os.getenv("GITHUB_TOKEN")
    repo_owner = os.getenv("GITHUB_OWNER")
    repo_name = os.getenv("GITHUB_REPO")
    
    if not all([token, repo_owner, repo_name]):
        return False, "GitHub configuration error. Please contact the administrator."
    
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/issues"
    
    # headers
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "title": title,
        "body": body
    }
    
    if labels:
        data["labels"] = labels
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        if response.status_code == 201:
            issue_data = response.json()
            return True, issue_data["html_url"]
        else:
            error_message = f"Error: {response.status_code} - {response.json().get('message', 'Unknown error')}"
            return False, error_message
            
    except Exception as e:
        return False, f"Error creating ticket: {str(e)}"

if 'ticket_created' not in st.session_state:
    st.session_state.ticket_created = False

# CSS для центрирования и выделения заголовка
st.markdown("""
<style>
.centered-title {
    text-align: center;
    font-size: 3.5em;
    font-weight: 800;
    margin-bottom: 30px;
    color: white;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    padding: 10px;
}

.title-container {
    display: flex;
    justify-content: center;
    width: 100%;
    margin-bottom: 20px;
}

.centered-subheader {
    text-align: center;
    font-size: 1.5em;
}

.user-info {
    text-align: right;
    font-size: 0.8em;
    color: #666;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

# Добавляем информацию о дате и логине
st.markdown("<div class='user-info'>Current Date and Time (UTC - YYYY-MM-DD HH:MM:SS formatted): 2025-07-08 13:22:42<br>Current User's Login: wannadiexd</div>", unsafe_allow_html=True)

# центрированный и выделенный заголовок (белый, без подчеркивания)
st.markdown(f"<div class='title-container'><div class='centered-title'>{BUSINESS_INFO['name']}</div></div>", unsafe_allow_html=True)

st.markdown("---")

# центрированный заголовок для вопросов
st.markdown("<div class='centered-subheader'>Ask a question about our business</div>", unsafe_allow_html=True)

# центрирование поля ввода
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    user_question = st.text_input("", placeholder="Example: When are you open?", label_visibility="collapsed")

# if the user has typed a question
if user_question:
    # get the answer from database
    answer = get_answer(user_question)
    
    # if found an answer
    if answer:
        st.success(answer)
    # if didn't find an answer
    else:
        st.warning("Sorry, I don't have an answer to your question.")
        
        # support ticket creation option
        st.header("Create a Support Ticket")
        st.info("If you didn't find an answer to your question, you can create a support ticket on GitHub.")
        
        # additional information for the support ticket
        issue_description = st.text_area(
            "Additional information:", 
            value=f"Original question: {user_question}\n\nAdditional details:"
        )
        
        # email for feedback
        user_email = st.text_input("Your email for feedback:", placeholder="example@email.com")
        
        # button to create the ticket
        if st.button("Create Ticket"):
            if not st.session_state.ticket_created:
                if not user_email:
                    st.error("Please enter your email for feedback.")
                elif not is_valid_email(user_email):
                    st.error("Please enter a valid email address.")
                else:
                    with st.spinner("Creating support ticket..."):
                        # prepare issue title and description
                        issue_title = f"Question: {user_question[:50]}..." if len(user_question) > 50 else f"Question: {user_question}"
                        
                        # get current date for the ticket
                        current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # combine all information for the ticket
                        full_description = f"{issue_description}\n\nContact email: {user_email}\nSubmitted on: {current_date}"
                        
                        # create the issue on github
                        success, result = create_github_issue(issue_title, full_description, ["support", "question"])
                        
                        # show appropriate message based on result
                        if success:
                            st.session_state.ticket_created = True
                            st.success(f"Ticket successfully created! You can track its status at: {result}")
                        else:
                            st.error(result)

# frequently asked questions section
st.header("Frequently Asked Questions")

for item in BUSINESS_INFO["faq"]:
    with st.expander(item["question"]):
        st.write(item["answer"])

# contact info moved to bottom
st.markdown("---")
st.header("Contact Information")
col1, col2 = st.columns(2)
with col1:
    st.write(f"📞 Phone: {BUSINESS_INFO['contact']['phone']}")
    st.write(f"✉️ Email: {BUSINESS_INFO['contact']['email']}")
with col2:
    st.write(f"🏠 Address: {BUSINESS_INFO['contact']['address']}")
    
    # Working days info (moved to contact section)
    work_days = [day.capitalize() for day, hours in BUSINESS_INFO["hours"].items() if hours != "Closed"]
    st.write(f"🗓️ Working days: {', '.join(work_days)}")

st.markdown("---")
st.markdown("© 2025 " + BUSINESS_INFO["name"] + ". All rights reserved.")