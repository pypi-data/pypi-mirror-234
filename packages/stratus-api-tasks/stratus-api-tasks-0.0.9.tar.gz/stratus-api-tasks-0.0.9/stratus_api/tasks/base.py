def create_celery_app(project_folder):
    """Creates a celery app based on the celery setting pulled from environment variables.
        DO NOT DELETE the `import tasks`

        :return: celery app
        """
    from stratus_api.core.settings import get_settings
    from stratus_api.core.logs import get_logger
    from celery import Celery
    celery_settings = get_settings(settings_type='celery')
    celery_app = Celery(__name__)
    celery_settings['imports'] = collect_app_tasks(project_folder=project_folder) + collect_root_modules(
        project_folder=project_folder)
    celery_app.config_from_object(celery_settings, force=True)
    import_tasks = collect_framework_tasks()
    for pkg, file in import_tasks:
        celery_app.autodiscover_tasks(packages=[pkg], related_name=file, force=True)
    get_logger()
    return celery_app


def collect_root_modules(project_folder):
    import pkgutil
    root_modules = []
    for finder, modname, ispkg in pkgutil.iter_modules([project_folder]):
        root_modules.append(modname)
    return root_modules


def collect_app_tasks(project_folder):
    import os
    tasks = set()
    for i in os.walk(os.path.join(project_folder, 'tasks')):
        base = i[0].replace(project_folder, '').replace('/', '.').strip('.')
        tasks.add(base)
        for f in [f.replace('.py', '') for f in i[-1] if
                  f.endswith('.py') and f not in {'__init__.py'} and "pycache" not in f]:
            tasks.add(base + '.' + f)
    return list(tasks)


def collect_framework_tasks():
    import os
    from stratus_api.core.common import get_subpackage_paths
    tasks = list()
    for package_path in get_subpackage_paths():
        tasks_file = os.path.join(package_path, 'tasks.py')
        tasks_folder = os.path.join(package_path, 'tasks/')
        if os.path.isfile(tasks_file):
            tasks.append(extract_task_path(root=package_path, file='tasks.py'))
        elif os.path.isdir(tasks_folder):
            for root, folders, files in os.walk(tasks_folder):
                for folder in folders:
                    tasks.append(extract_task_path(root=root, file=folder))
                for file in [i for i in files if 'pycache' not in i and '__init__' not in i and i.endswith('.py')]:
                    tasks.append(extract_task_path(root=root, file=file))

    return tasks


def extract_task_path(root, file):
    return ('stratus_api/' + root.split('/stratus_api/')[-1]).replace('/', '.'), file.replace('.py', '')


def start_task_signature(sig, **task_parameters):
    from stratus_api.core.settings import get_settings
    celery_settings = get_settings(settings_type='celery')
    if not celery_settings.get('broker_url'):
        return sig.apply()
    else:
        return sig.apply_async(**task_parameters)
