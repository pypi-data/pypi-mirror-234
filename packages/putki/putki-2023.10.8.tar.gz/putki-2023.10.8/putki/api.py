import os
import pathlib
from typing import no_type_check

import yaml
import putki.discover as discover
import putki.traverse as traverse
from putki import log


@no_type_check
def verify_tasks(doc_root, structure_name, target_key, facet_key, options) -> int:
    """Yes."""
    tasks_root = discover.root()
    log.info(f'Identified tasks default root at {tasks_root}')
    tasks_map = discover.tasks(doc_root)
    if not tasks_map:
        log.error('No tasks files found')
        return 1
    log.info(f'Mapped tasks below specified root at {doc_root}')
    files_count = len(tasks_map.keys())
    log.info(f'The {files_count} tasks files collected below specified root at {doc_root} are:')
    for path in tasks_map:
        log.info(f'- {path}')
    task_count = sum(len(section) for section in tasks_map.values())
    tasks = discover.combine(tasks_map)
    log.info(f'Collected the following {task_count} tasks from {files_count} tasks files:')
    show_me = yaml.safe_dump_all(tasks)
    for path in show_me.split('\n'):
        log.info(path)
    log.info('OK')
    return 0


@no_type_check
def verify_structures(doc_root, structures_name, component, options) -> int:
    """Maybe later."""
    traverse.ROI = component
    saved_path = pathlib.Path.cwd()
    os.chdir(doc_root)
    log.info(f'Verifying structures below {doc_root}')
    code, message, root, claims = traverse.follow(structures_name)
    traverse.walk_fs(claims, root)
    os.chdir(saved_path)
    return 0
