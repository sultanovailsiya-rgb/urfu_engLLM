import os
from dotenv import load_dotenv

load_dotenv()  

is_stdio = os.getenv("IS_STDIO")
OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
