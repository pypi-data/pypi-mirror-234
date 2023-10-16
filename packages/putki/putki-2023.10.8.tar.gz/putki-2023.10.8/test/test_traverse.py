import os
import pathlib
from first import first

import putki.traverse as traverse


def test_is_path_ok():
    assert traverse.is_path('example/s/structures.yml')


def test_is_path_ok_too():
    assert traverse.is_path('')


def test_is_path_fail():
    assert not traverse.is_path(True)


def test_is_yaml_ok():
    assert traverse.is_yaml('example/s/structures.yml')


def test_is_yaml_ok_too():
    assert traverse.is_yaml('example/s/structures.yaml')


def test_is_yaml_fail():
    assert not traverse.is_yaml('example/s/structures.json')


def test_load_yaml_ok():
    assert traverse.load_yaml('example/s/structures.yml')


def test_load_yaml_fail_missing():
    assert not traverse.load_yaml('example/s/not-present.yml')


def test_load_yaml_fail_invalid():
    assert not traverse.load_yaml('example/s/invalid-misplaced.yml')


def test_meta_follow_include_ok_no_include():
    data = {'document': {}}
    assert traverse.meta_follow_include('', data)


def test_meta_follow_include_ok_has_include():
    data = {'document': {'import': '../../../meta-base.yml'}}
    assert traverse.meta_follow_include('example/s/c/x/d/meta.yml', data)


def test_validate_facet_ok():
    facet = {
        'f': {
            'approvals': 'approvals.yml',
            'bind': 'bind.txt',
            'changes': 'changes.yml',
            'meta': 'meta.yml',
            'render': True,
        }
    }
    assert traverse.validate_facet(facet, 'example/s/c/x/d/structure.yml') is None


def test_walk_binder_ok():
    assert traverse.walk_binder('example/s/c/x/d/bind.txt')


def test_walk_binder_fail_nothing_there():
    assert not traverse.walk_binder('example/s/c/x/d/not-existing.txt')


def test_walk_binder_fail_empty():
    assert not traverse.walk_binder('example/s/empty-misplaced-bind.txt')


def test_walk_binder_fail_misleading():
    v_map = traverse.walk_binder('example/s/misleading-misplaced-bind.txt')
    assert len(v_map) == 1
    assert not v_map[first(v_map)]


def test_follow_example_s_wrong_place():
    code, message, root, claims = traverse.follow('example/s/structures.yml')
    assert code == 0
    assert message == ''
    assert root
    assert claims

def test_follow_example_s_change_place():
    saved_path = pathlib.Path.cwd()
    os.chdir('example/s/')
    code, message, root, claims = traverse.follow('structures.yml')
    assert code == 0
    assert message == ''
    assert root
    assert claims
    os.chdir(saved_path)


def test_follow_example_s_fail_missing():
    code, message, root, claims = traverse.follow('example/s/not-present.yml')
    assert code == 1
    assert message == 'no structures found'
    assert root
    assert not claims


def test_walk_fs_example_s_missing_components():
    traverse.ROI = 'c'
    assert traverse.walk_fs({}, 'example/s/') == 1
