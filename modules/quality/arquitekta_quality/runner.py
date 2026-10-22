from pathlib import Path
import time
from .browser import probe
from .core import Blocked, app_server, apply_edits, command, git, safe_source, sha256, validate_project, write_json


def run(project, folder, mode, ai, publish=None):
    """Bounded repair loop in a Git worktree. Never merges, pushes or deploys."""
    folder = Path(folder).resolve()
    folder.mkdir(parents=True, exist_ok=True)
    report = {'id': folder.name, 'project': project['id'], 'mode': mode, 'state': 'QUEUED',
              'events': [], 'attempts': [], 'started': time.time()}

    def update(state, detail):
        report['state'] = state
        report['events'].append({'at': time.time(), 'state': state, 'detail': detail})
        write_json(folder / 'report.json', report)
        if publish:
            publish(report)

    def evaluate(workspace, label):
        dest = folder / label
        dest.mkdir()
        with app_server(project, workspace, dest):
            result = probe(project, dest)
        code, log = command(project['verify'], workspace, project.get('verify_timeout', 180))
        (dest / 'verify.log').write_text(log)
        result['verification_exit_code'] = code
        if code:
            result['findings'].append({'check': 'verify', 'kind': 'project-check-failed', 'detail': log[-4000:]})
        write_json(dest / 'checks.json', result)
        return result

    try:
        update('PREPARING', 'Validando proyecto y creando copia aislada')
        repo = validate_project(project)
        if git(repo, 'status', '--porcelain'):
            raise Blocked('El repositorio tiene cambios locales. Guardarlos en Git antes de probar')
        report['base_commit'] = git(repo, 'rev-parse', 'HEAD')
        workspace = folder / 'worktree'
        branch = 'quality/' + folder.name
        git(repo, 'worktree', 'add', '-b', branch, str(workspace), report['base_commit'])
        report.update(branch=branch, workspace=str(workspace))
        update('TESTING', 'Probando recorridos en cuatro tamaños de pantalla')
        baseline = evaluate(workspace, 'before')
        report['before'] = baseline
        if not baseline['findings']:
            report['evidence'] = {p.relative_to(folder).as_posix(): sha256(p)
                                  for p in (folder / 'before').iterdir() if p.suffix in {'.png', '.zip', '.json'}}
            update('PASS_CONFIGURED_CHECKS', 'Pasaron las pruebas configuradas; revisar cobertura del informe')
            return report
        if mode == 'test':
            update('FAIL', 'Se encontraron fallos; evidencia disponible para reparar')
            return report
        if ai is None:
            raise Blocked('Falta configurar el modelo Ollama para reparar')
        allowed = project.get('editable_files', [])
        if not allowed:
            raise Blocked('Configurar editable_files para permitir reparaciones')
        current = baseline
        image_folder = folder / 'before'
        for attempt in range(1, min(3, max(1, int(project.get('max_attempts', 2)))) + 1):
            update('ANALYZING', f'Ollama analiza evidencia; intento {attempt}')
            sources = {name: safe_source(workspace, name, allowed).read_text() for name in allowed}
            if sum(len(v) for v in sources.values()) > 160000:
                raise Blocked('Contexto demasiado grande; dividir archivos por módulo')
            proposal = ai.propose(current, sources, image_folder.glob('*.png'))
            write_json(folder / f'proposal-{attempt}.json', proposal)
            report['attempts'].append({'number': attempt, 'summary': proposal['summary']})
            update('REPAIRING', proposal['summary'])
            apply_edits(workspace, proposal, allowed)
            update('VERIFYING', f'Repitiendo las mismas pruebas; intento {attempt}')
            current = evaluate(workspace, f'after-{attempt}')
            report['after'] = current
            image_folder = folder / f'after-{attempt}'
            if not current['findings']:
                # Model never controls acceptance criteria. Keep diff for human review.
                diff = git(workspace, 'diff', '--no-ext-diff', '--binary')
                if not diff:
                    raise Blocked('Sin cambios verificables; no declarar reparación')
                (folder / 'repair.patch').write_text(diff + '\n')
                git(workspace, 'add', '--', *allowed)
                git(workspace, '-c', 'user.name=ARQUITEKTA Quality', '-c',
                    'user.email=quality@localhost', 'commit', '-m', 'fix: verified quality repair')
                report['repair_commit'] = git(workspace, 'rev-parse', 'HEAD')
                report['evidence'] = {p.relative_to(folder).as_posix(): sha256(p)
                                      for p in folder.glob('*/*') if p.suffix in {'.png', '.zip', '.json'}
                                      and 'worktree' not in p.parts}
                update('REPAIRED_CONFIGURED_CHECKS', 'Corrección verificada en rama; lista para revisión, sin publicar')
                return report
        update('FAIL', 'Persisten fallos tras los intentos permitidos; copia y evidencia conservadas')
    except Exception as e:
        report['error'] = str(e)
        update('BLOCKED', str(e))
    finally:
        report['finished'] = time.time()
        write_json(folder / 'report.json', report)
    return report
