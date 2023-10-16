"""Ensure all components have render folders with pipe harness."""
import pathlib
from typing import Any, Union

import yaml
from putki import ENCODING, log

Path = Union[str, pathlib.Path]

ROI = 'component'
STRUCTURES = 'structures.yml'
UNDERSCORE = '_'


def is_path(value: Union[bool, str]) -> bool:
    """Convention rules."""
    return bool(value) != value


def is_yaml(path: Path) -> bool:
    """Convention rules again."""
    return pathlib.Path(path).suffix.lower() in ('.yaml', '.yml')


def walk_binder(binder_path: Path) -> dict[Path, bool]:
    """Visit all entries of the binder assuming the paths lead to files."""
    binder_path = pathlib.Path(binder_path)
    try:
        with binder_path.open('rt', encoding=ENCODING) as handle:
            binder = [binder_path.parent / x.strip() for x in handle.readlines()]
    except FileNotFoundError:  # noqa
        log.error(f'missing {binder_path} binder file')
        return {}
    v_map: dict[Path, bool] = {source: source.is_file() for source in binder}
    for k, v in v_map.items():
        if not v:
            log.error(f'declared missing {k} file')
    return v_map


def load_yaml(path: Path) -> Union[Any, dict[str, Any]]:
    """Eventually load a YAML resource."""
    path = pathlib.Path(path)
    if not path.is_file():
        log.error(f'declared missing {path} file')
        return {}
    try:
        return yaml.safe_load(path.open('rt', encoding=ENCODING))
    except:  # noqa
        log.error(f'invalid YAML {path} file')
        return {}


def meta_follow_include(path: Path, data: dict[str, dict[str, Any]]) -> bool:
    """Visit any import assuming the path leads to a file."""
    include = data['document'].get('import', '')
    if include:
        incl_path = pathlib.Path(path).parent / include
        return bool(load_yaml(incl_path))
    return True


def validate_facet(facet: dict[str, Any], ssp: Path) -> None:
    """Validate the surface of a facet."""
    for facet_code, data in facet.items():
        log.info(f'    * {facet_code}:')
        path_likes = {}
        for k in sorted(data.keys()):
            v = data[k]
            log.info(f'      {k :9s} -> {v}')
            if is_path(v):
                pl_try = pathlib.Path(ssp).parent / v
                path_likes[k] = pl_try
                d = load_yaml(pl_try)
                if k == 'bind':
                    _ = walk_binder(pl_try)
                elif k == 'meta' and is_yaml(pl_try):
                    _ = meta_follow_include(pl_try, d)


def follow(structures_path: Path) -> tuple[int, str, pathlib.Path, dict[str, Any]]:
    """Execute the traversal."""
    sp = pathlib.Path(structures_path)
    root_path = sp.parent

    log.info(f'Structures from {STRUCTURES}(root):')
    s_info = load_yaml(sp)
    if not s_info:
        return 1, 'no structures found', root_path, {}

    claims = s_info['structures']
    for part, sub_path in claims.items():
        log.info(f'- {part}:')
        sub_p = pathlib.Path(sub_path)
        sub_info = load_yaml(sub_p)
        for target, structure_path_str in sub_info.get('structures', {}).items():
            comp_cand, perspective = target.rsplit(UNDERSCORE, 1)
            log.info(f'  + {perspective}:')
            ssp = sub_p.parent / structure_path_str
            structure_info = load_yaml(ssp)
            if structure_info:
              for facet in structure_info[target]:
                  validate_facet(facet, ssp)
    return 0, '', root_path, claims


def walk_fs(claims: dict[str, Any], root_path: Path) -> int:
    """Yes."""
    root_path = pathlib.Path(root_path)
    roi_path = root_path / ROI
    cp_declared = [claim for claim in claims]
    component_paths = [p for p in sorted(roi_path.iterdir()) if p.is_dir()]
    components = [f'{p.name}' for p in component_paths]

    log.info('Components (from folders):')
    for c in components:
        log.info(f'- {c}')

    log.info(f'Verifying any component structures not declared in root level {STRUCTURES}')
    missing = 0
    for cp in component_paths:
        if cp.name not in cp_declared:
            missing += 1
            log.error(f'missing component ({cp.name}):')
            sp = cp / STRUCTURES
            sx_info = load_yaml(sp)
            if sx_info:
                log.info(sx_info)

    if missing:
        log.error(f'missing declarations (badness = {missing})')
        return 1
    else:
        log.info('OK - no missing declarations')
        return 0
