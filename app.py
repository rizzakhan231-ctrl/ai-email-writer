import streamlit as st
from openai import OpenAI
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

st.set_page_config(page_title="AI Email Writer", page_icon="📧")

st.title("📧 AI Email / Letter Writer")

# Use secret API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_email(purpose, tone, recipient, sender, key_points):

    prompt = f"""
    Write a complete professional email.

    Purpose: {purpose}
    Tone: {tone}
    Recipient: {recipient}
    Sender: {sender}
    Key Points: {key_points}

    Include subject line.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    return response.choices[0].message.content


def save_as_pdf(content):
    filename = "Generated_Email.pdf"
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    elements = []

    for line in content.split("\n"):
        elements.append(Paragraph(line, styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)
    return filename


purpose = st.text_input("Purpose")
tone = st.selectbox("Tone", ["Professional", "Friendly", "Formal", "Apology"])
recipient = st.text_input("Recipient Name")
sender = st.text_input("Your Name")
key_points = st.text_area("Key Points")

if st.button("Generate Email"):
    email = generate_email(purpose, tone, recipient, sender, key_points)
    st.text_area("Generated Email", email, height=300)

    pdf_file = save_as_pdf(email)
    with open(pdf_file, "rb") as file:
        st.download_button("Download PDF", file, file_name="Generated_Email.pdf")
