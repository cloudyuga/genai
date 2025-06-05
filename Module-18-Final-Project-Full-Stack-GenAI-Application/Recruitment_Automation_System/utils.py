import os
from langchain_openai import ChatOpenAI
from PyPDF2 import PdfReader
import docx
from dotenv import load_dotenv
load_dotenv()

def get_llm() -> ChatOpenAI:
    """
    Lazily instantiates and returns a ChatOpenAI client using the API key
    provided in the OPENAI_API_KEY environment variable.
    Raises:
        ValueError: if the OPENAI_API_KEY is not set.
    """
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    return ChatOpenAI(model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY)

def extract_text(file_obj):
    if isinstance(file_obj, str):
        file_path = file_obj
    else:
        file_path = file_obj.name

    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".pdf":
        try:
            reader = PdfReader(file_path)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as e:
            return f"Error reading PDF: {e}"

    elif ext == ".docx":
        try:
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            return f"Error reading DOCX: {e}"

    elif ext == ".txt":
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Error reading TXT: {e}"

    else:
        return "Unsupported file format."
