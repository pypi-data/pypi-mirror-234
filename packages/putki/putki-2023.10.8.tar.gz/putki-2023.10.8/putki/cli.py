"""Command line interface for pipeline (Finnish: putki) - discovering and executing a specific task description."""
import logging
import pathlib
import sys

import typer

import putki.api as api
from putki import APP_NAME, DEFAULT_STRUCTURE_NAME, DEFAULT_STRUCTURES_NAME, QUIET, __version__ as APP_VERSION, log

app = typer.Typer(
    add_completion=False,
    context_settings={'help_option_names': ['-h', '--help']},
    no_args_is_help=True,
)

DocumentRoot = typer.Option(
    '',
    '-d',
    '--document-root',
    help='Root of the document tree to visit. Optional\n(default: positional tree root value)',
)

StructureName = typer.Option(
    DEFAULT_STRUCTURE_NAME,
    '-s',
    '--structure',
    help='structure mapping file (default: {DEFAULT_STRUCTURE_NAME})',
)

TargetName = typer.Option(
    '',
    '-t',
    '--target',
    help='target document key',
)

FacetName = typer.Option(
    '',
    '-f',
    '--facet',
    help='facet key of target document',
)

Verbosity = typer.Option(
    False,
    '-v',
    '--verbose',
    help='Verbose output (default is False)',
)

Strictness = typer.Option(
    False,
    '-s',
    '--strict',
    help='Ouput noisy warnings on console (default is False)',
)

OutputPath = typer.Option(
    '',
    '-o',
    '--output-path',
    help='Path to output unambiguous content to - like when ejecting a template',
)

StructuresName = typer.Option(
    DEFAULT_STRUCTURES_NAME,
    # '',
    '--structures',
    help='structures mapping file (default: {DEFAULT_STRUCTURES_NAME})',
)

ComponentFolderName = typer.Option(  # TODO: prepare later for additional intermediates
    'component',
    # '',
    '--component-folder-name',
    help='component folder name (default: component)',
)


@app.callback(invoke_without_command=True)
def callback(
    version: bool = typer.Option(
        False,
        '-V',
        '--version',
        help='Display the application version and exit',
        is_eager=True,
    )
) -> None:
    """
    Pipeline (Finnish: putki) - discovering and executing a specific task description.
    """
    if version:
        typer.echo(f'{APP_NAME} version {APP_VERSION}')
        raise typer.Exit()


def _verify_call_vector(
    doc_root: str, doc_root_pos: str, verbose: bool, strict: bool
) -> tuple[int, str, str, dict[str, bool]]:
    """DRY"""
    doc = doc_root.strip()
    if not doc and doc_root_pos:
        doc = doc_root_pos
    if not doc:
        print('Document tree root required', file=sys.stderr)
        return 2, 'Document tree root required', '', {}

    doc_root_path = pathlib.Path(doc)
    if doc_root_path.exists():
        if not doc_root_path.is_dir():
            print(f'requested tree root at ({doc}) is not a folder', file=sys.stderr)
            return 2, f'requested tree root at ({doc}) is not a folder', '', {}
    else:
        print(f'requested tree root at ({doc}) does not exist', file=sys.stderr)
        return 2, f'requested tree root at ({doc}) does not exist', '', {}

    options = {
        'quiet': QUIET and not verbose and not strict,
        'strict': strict,
        'verbose': verbose,
    }
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    return 0, '', doc, options


@app.command('tasks')
def verify_tasks(  # noqa
    doc_root_pos: str = typer.Argument(''),
    doc_root: str = DocumentRoot,
    structure: str = StructureName,
    target: str = TargetName,
    facet: str = FacetName,
    verbose: bool = Verbosity,
    strict: bool = Strictness,
) -> int:
    """
    Verify the structure definition against the file system.
    """
    code, message, doc, options = _verify_call_vector(doc_root, doc_root_pos, verbose, strict)
    if code:
        log.error(message)
        return code

    return sys.exit(
        api.verify_tasks(doc_root=doc, structure_name=structure, target_key=target, facet_key=facet, options=options)
    )


@app.command('structures')
def verify_structures(  # noqa
    doc_root_pos: str = typer.Argument(''),
    doc_root: str = DocumentRoot,
    structures: str = StructuresName,
    component: str = ComponentFolderName,
    verbose: bool = Verbosity,
    strict: bool = Strictness,
) -> int:
    """
    Verify the structure definition against the file system.
    """
    code, message, doc, options = _verify_call_vector(doc_root, doc_root_pos, verbose, strict)
    if code:
        log.error(message)
        return code

    return sys.exit(
        api.verify_structures(doc_root=doc, structures_name=structures, component=component, options=options)
    )


@app.command('version')
def app_version() -> None:
    """
    Display the application version and exit.
    """
    callback(True)
