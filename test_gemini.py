from google import genai
from dotenv import load_dotenv
from os import getenv
from config.settings.base import env_file_path

if env_file_path.is_file():
    load_dotenv(env_file_path)

client = genai.Client(api_key=getenv("GEMINI_API_KEY"))

response = client.models.generate_content(
    model=getenv("GEMINI_MODEL"),
    contents="Name me 5 animals",
)

print(response)