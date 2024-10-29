import os
from pathlib import Path


def get_project_root(search_file='.git'):
    current_path = Path(__file__).resolve()

    for parent in current_path.parents:
        if (parent / search_file).exists():
            return parent
    return None


ROOT_PATH = get_project_root()
DATA_PATH = os.path.join(ROOT_PATH, 'data', 'KDD19_data.json')

# --- openai ---
API_KEY = ''
API_BASE = 'https://api.openai.com/v1'

TEMPERATURE = 0.7
MODEL_NAME = 'gpt-4o-mini'
