import streamlit as st
import sys
import os
from pathlib import Path
from utils import create_draft_with_attachments, get_contact_list

# Add the src directory to the Python path
# sys.path.append(str(Path(__file__).parent))

# Import the YouTube blogger functions
from youtube_blogger.src.youtube_blogger.main import download_audio, split_audio, transcribe_audio
from youtube_blogger.src.youtube_blogger.crew import YoutubeBlogger
# Initialize session state for steps and other variables

if "attachments" not in st.session_state:
    st.session_state.attachments = []
if "email_body" not in st.session_state:
    st.session_state.email_body = ""
if "subject" not in st.session_state:
    st.session_state.subject = ""
if "contact_list" not in st.session_state:
    st.session_state.contact_list = []
if "to_emails" not in st.session_state:
    st.session_state.to_emails = []
if "blog_content" not in st.session_state:
    st.session_state.blog_content = []
# Set up page configuration
st.set_page_config(
    page_title="YouTube Blogger", 
    page_icon="📝", 
    layout="wide",
    initial_sidebar_state="expanded"
)


# Create output folders
os.makedirs("downloads", exist_ok=True)
os.makedirs("blogs", exist_ok=True)

# Custom styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #FF0000;
        text-align: center;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #555;
        margin-bottom: 1rem;
        text-align: center;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def step_2():
    st.title("Step 2: Select Recipients 📧")

    # Initialize session state variables if not already set
    if "uploaded_contacts" not in st.session_state:
        st.session_state.uploaded_contacts = False
    if "contact_list" not in st.session_state:
        st.session_state.contact_list = []
    if "to_emails" not in st.session_state:
        st.session_state.to_emails = []

    multi_mails = st.file_uploader("Upload txt file (containing email IDs)", type=["txt"], key="contact_file_uploader")

    # Only process file upload if a file is uploaded and contacts haven't been processed yet
    if multi_mails is not None and not st.session_state.uploaded_contacts:
        contact_list = get_contact_list(multi_mails)
        st.session_state.contact_list = contact_list
        st.session_state.uploaded_contacts = True
        st.rerun()  # Force a rerun to update the contact list

    # Only show multiselect if contacts are available
    if st.session_state.contact_list:
        to_emails = st.multiselect(
            "Select Recipients",
            options=st.session_state.contact_list,
            default=st.session_state.to_emails,  # Preserve previous selections
            help="You can select multiple recipients"
        )
    else:
        to_emails = []

    custom_email = st.text_input("Add Custom Email (optional)")
    
    # Add custom email if provided and not already in the list
    if custom_email and custom_email not in to_emails:
        to_emails.append(custom_email)

    # Update session state
    st.session_state.to_emails = to_emails


def main():
    st.markdown("""
    <div style="display: flex; align-items: center; justify-content: center;">
        <img src="https://img.icons8.com/color/96/000000/youtube-play.png" width="50" style="margin-right: 10px;">
        <h1 style="display: inline;">YouTube Blogger</h1>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Transform YouTube videos into blog posts with AI</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/youtube-play.png", width=100)
        st.header("About")
        st.write("This app converts YouTube videos to blog posts through:")
        st.write("1. Audio extraction")
        st.write("2. Speech transcription")
        st.write("3. AI content summarization")
        st.write("4. Blog post generation")
        
        # Optional settings
        st.header("Settings")
        chunk_size = st.slider("Audio chunk size (seconds)", 30, 120, 60)
    
    # Main content area
    youtube_url = st.text_input("Enter YouTube URL:")
    
    if st.button("Generate Blog Post"):
        if youtube_url:
            try:
                # Step 1: Download audio
                with st.status("Processing video...") as status:
                    status.update(label="Downloading audio from YouTube...")
                    audio_path = download_audio(youtube_url)

                    # Step 2: Split audio
                    status.update(label="Splitting audio into chunks...")
                    audio_chunks = split_audio(audio_path, chunk_length_ms=chunk_size * 1000)

                    # Step 3: Transcribe audio
                    status.update(label="Converting speech to text...")

                    # Create a placeholder for showing transcription progress
                    progress_text = st.empty()
                    progress_bar = st.progress(0)

                    # Override print to capture output during transcription
                    original_print = print

                    def progress_print(*args, **kwargs):
                        message = " ".join(map(str, args))
                        progress_text.text(message)
                        original_print(*args, **kwargs)

                    # Temporarily replace print function to capture output
                    import builtins
                    builtins.print = progress_print

                    # Run transcription
                    transcript = transcribe_audio(audio_chunks)

                    # Restore original print function
                    builtins.print = original_print

                    # Clear progress indicators
                    progress_text.empty()
                    progress_bar.empty()

                    # Step 4: Generate blog post
                    status.update(label="Generating blog post with AI...")
                    inputs = {"task_summarize": transcript}
                    YoutubeBlogger().crew().kickoff(inputs=inputs)
                    status.update(label="Done!", state="complete")

                # Display the generated blog
                if os.path.exists("report.md"):
                    with open("report.md", "r") as f:
                        blog_content = f.read()

                    st.success("Blog post generated successfully!")
                    st.session_state.blog_content = blog_content
                    # Show blog preview
                    st.markdown("## Generated Blog Post")
                    with st.expander("View Blog Content", expanded=True):
                        st.markdown(blog_content)

                    # Download button
                    st.download_button(
                        label="Download Blog Post",
                        data=blog_content,
                        file_name="youtube_blog.md",
                        mime="text/markdown"
                    )
                    if "report.md" not in st.session_state.attachments:
                        st.session_state.attachments.append("report.md")

                    st.session_state.email_body = f"Please open the blog summary that video that you watched, in attachment report.md file.\n\n{blog_content}"
                    st.session_state.subject = "Blog Of Youtube video"
                else:
                    st.error("Failed to generate blog post. Check the console for errors.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a YouTube URL")

    if st.button("Do you want Create Draft?"):
        st.session_state.step = "create_draft"

    if st.session_state.get("step") == "create_draft":
        step_2()
        if st.button("Create Draft"):
            body = st.session_state.email_body
            to_emails = st.session_state.get("to_emails", [])

            # Convert string to list if necessary
            if isinstance(to_emails, str):
                to_emails = [to_emails.strip()]

            from_email = "amarc8399@gmail.com"

            if not to_emails or to_emails == [""]:
                st.error("Please select at least one recipient")
                st.stop()

            if not st.session_state.subject:
                st.error("Please enter an email subject")
                st.stop()

            if not body:
                st.error("Please enter an email body")
                st.stop()

            st.write("Debugging: to_emails ->", to_emails)  # Debugging output

            try:
                drafts = []
                for email in to_emails:
                    draft = create_draft_with_attachments(
                        from_email,
                        [email],  # Pass a single email as a list
                        st.session_state.subject,
                        st.session_state.email_body,
                        st.session_state.attachments
                    )
                    if draft:
                        drafts.append(draft)

                if drafts:
                    st.success("Drafts created successfully!")
                    st.session_state.attachments = []
                else:
                    st.error("Failed to create drafts")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()