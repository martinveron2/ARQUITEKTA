"""Portable connection registry. HTTP accepts IDs, never commands or source paths."""
from pathlib import Path
import json
from urllib.parse import urlencode, urlparse
from .core import Blocked, write_json


def metadata(project):
    return {key: project.get(key) for key in
            ('id', 'name', 'repository', 'technology', 'environment', 'test_data', 'permissions', 'base_url')}


def connect(registry, app_id, destination):
    project = registry.get(app_id)
    if not project:
        raise Blocked('Aplicación no preconfigurada por el operador')
    if project.get('environment') != 'test' or project.get('test_data') != 'synthetic':
        raise Blocked('El piloto requiere entorno test y datos synthetic explícitos')
    if project.get('permissions') != ['audit']:
        raise Blocked('El primer piloto sólo admite permiso audit')
    path = Path(destination)
    connections = json.loads(path.read_text()) if path.exists() else {}
    connections[app_id] = metadata(project)
    write_json(path, connections)
    return connections[app_id]


def dashboard_link(base_url, app_id):
    url = urlparse(base_url)
    if url.scheme not in {'http', 'https'} or not url.netloc or url.username or url.password or url.query or url.fragment:
        raise Blocked('URL del dashboard inválida')
    return base_url.rstrip('/') + '/?' + urlencode({'project': app_id})
