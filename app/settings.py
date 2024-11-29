from dotenv import dotenv_values
from pathlib import Path

# Create a .env file in the project root folder with the required values
BASE_DIR = Path(__file__).resolve().parent.parent
env_vars = dotenv_values(BASE_DIR / ".env")

db_user = env_vars.get('DB_USER')
db_name = env_vars['DB_NAME']
db_pass = env_vars['DB_PASSWORD']
db_host = env_vars['DB_HOST']
db_port = int(env_vars['DB_PORT'])
db_table = env_vars.get('DB_TABLE', 'stock_data')

DATABASE_URL = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
# DATABASE_URL = "postgresql://prash:password@localhost:5432/finance_db"

# Otherwise Fall back to os.environ