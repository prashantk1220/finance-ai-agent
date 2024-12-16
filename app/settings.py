from dotenv import dotenv_values
from pathlib import Path

# Create a .env file in the project root folder with the required values
BASE_DIR = Path(__file__).resolve().parent.parent
env_vars = dotenv_values(BASE_DIR / ".env")

llm_model = env_vars.get('GROQ_MODEL', 'llama3-8b-8192')
db_user = env_vars.get('DB_USER')
db_name = env_vars.get('DB_NAME')
db_pass = env_vars.get('DB_PASSWORD')
db_host = env_vars.get('DB_HOST')
db_port = env_vars.get('DB_PORT')
db_table = env_vars.get('DB_TABLE', 'stock_data')

DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


# Otherwise Fall back to os.environ