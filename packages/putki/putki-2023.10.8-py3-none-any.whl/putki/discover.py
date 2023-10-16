import pathlib
from typing import Union, no_type_check

import yaml
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from git.repo import Repo
from putki import ENCODING


@no_type_check
def root(within: Union[str, pathlib.Path] = '.') -> str:
    """Detect the root folder for tasks."""
    try:
        repo = Repo(within, search_parent_directories=True)
        try:
            repo_root = repo.git.rev_parse(show_toplevel=True)
            start_here = pathlib.Path(repo_root)
            for path in start_here.rglob('*'):
                if path.name == 'tasks' and path.is_dir():
                    return str(path)
            return ''
        except GitCommandError:
            return ''
    except (InvalidGitRepositoryError, NoSuchPathError):
        return ''


@no_type_check
def tasks(below: Union[str, pathlib.Path] = '.') -> dict[str, list[dict[str, str]]]:
    """Collect the tasks below by mapping the paths to lists of key value string maps."""
    jobs: dict[str, list[dict[str, str]]] = {}
    start_here = pathlib.Path(below)
    for path in start_here.rglob('**/*'):
        if path.is_file() and path.stat().st_size and path.suffix.lower() in ('.yaml', '.yml'):
            with open(path, 'rt', encoding=ENCODING) as handle:
                data = yaml.safe_load(handle)
            if data and data.get('tasks', None):
                jobs[str(path.parent)] = data['tasks']
    return jobs


@no_type_check
def combine(jobs: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    """Combine the tasks by mapping the local ids to path prefixed ids."""
    tasks_seq: list[dict[str, str]] = []
    common = min(sorted(jobs.keys()))
    for path, job_seq in jobs.items():
        prefix = path.replace(common, '', 1)
        for task in job_seq:
            local_id = task['id']
            task['id'] = f'{prefix}/{local_id}'
            tasks_seq.append(task)
    return tasks_seq


@no_type_check
def assemble_path(path_elements: dict[str, str]) -> str:
    """Assemble a connection string from /source/path_elements."""
    address_template = path_elements['address_template']
    user = path_elements.get('user')
    return (
        address_template.replace('{{protocol}}', path_elements['protocol'])
        .replace('{{user}}', user if user is not None else '')
        .replace('{{host}}', path_elements['host'])
        .replace('{{port}}', path_elements['port'])
        .replace('{{service_root}}', path_elements['service_root'])
    )


@no_type_check
def derive(
    tasks_seq: list[dict[str, Union[str, dict[str, str]]]]
) -> dict[str, dict[str, Union[str, int, dict[str, str]]]]:
    """Derive map with actionable names by mapping the path prefixed ids and assembling path elements."""
    actions: dict[str, dict[str, Union[str, int, dict[str, str]]]] = {}
    for slot, task in enumerate(tasks_seq):
        folder_slug = task['id'].replace('/', '_')

        action: dict[str, Union[str, int]] = {**task, 'rank': slot}
        source: dict[str, Union[str, dict[str, str]]] = task['source']
        action['url'] = source['path'] if source.get('path') else assemble_path(source['path_elements'])
        actions[folder_slug] = action

    return actions
