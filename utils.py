import base64
import os
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import markdown
import io


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']

def get_gmail_service():
    """Authenticate and create Gmail service."""
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Create and return the Gmail service
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def convert_markdown_to_html(markdown_text):
    """Convert Markdown text to HTML."""
    html = markdown.markdown(markdown_text)
    return html

def create_draft_with_attachments(from_email, to_emails, subject, body, attachments=None):
    """
    Create a draft email with multiple recipients and optional attachments.

    :param from_email: Sender's email address
    :param to_emails: List of recipient email addresses
    :param subject: Email subject
    :param body: Email body content in Markdown
    :param attachments: List of file paths to attach
    :return: Draft object or None
    """
    service = get_gmail_service()
    if not service:
        return None

    try:
        # Convert Markdown to HTML
        html_body = convert_markdown_to_html(body)

        message = EmailMessage()
        message.set_content(html_body, subtype='html')  # Set content as HTML
        message["To"] = ", ".join(to_emails)
        message["From"] = from_email
        message["Subject"] = subject

        # Handle attachments
        if attachments:
            for file_path in attachments:
                with open(file_path, 'rb') as file:
                    file_data = file.read()
                    file_name = os.path.basename(file_path)
                    message.add_attachment(
                        file_data,
                        maintype='application',
                        subtype='octet-stream',
                        filename=file_name
                    )

        # Encode the message
        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"message": {"raw": encoded_message}}
        draft = (
            service.users()
            .drafts()
            .create(userId="me", body=create_message)
            .execute()
        )

        print(f'Draft created successfully. Draft ID: {draft["id"]}')
        return draft

    except Exception as error:
        print(f"An error occurred: {error}")
        return None

def get_contact_list(uploaded_file):
    """
    Retrieve a list of contacts or email addresses from an uploaded file.
    Each contact should be on a new line in the file.

    :param uploaded_file: A file-like object from Streamlit file uploader
    :return: List of contact email addresses
    """
    try:
        if uploaded_file is not None:
            # Read the file contents
            file_content = uploaded_file.getvalue().decode("utf-8")  # Decode bytes to string
            contacts = [line.strip() for line in file_content.split("\n") if line.strip()]
            return contacts
        else:
            return []
    except Exception as e:
        print(f"Error: {e}")
        return []



# Example usage in a Streamlit app:
# uploaded_file = st.file_uploader("Upload a contacts file", type=["txt"])
# if uploaded_file:
#     contacts = get_contact_list(uploaded_file)
#     st.write(contacts)



