import os
from pathlib import Path
from dotenv import load_dotenv

from django.core.wsgi import get_wsgi_application

dotenv_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agentflow.settings')

application = get_wsgi_application()
