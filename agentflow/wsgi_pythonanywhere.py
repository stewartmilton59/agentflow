import os
import sys
from pathlib import Path
from dotenv import load_dotenv

project_home = '/home/agentflow/agentflow'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

dotenv_path = Path(project_home) / '.env'
load_dotenv(dotenv_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'agentflow.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
