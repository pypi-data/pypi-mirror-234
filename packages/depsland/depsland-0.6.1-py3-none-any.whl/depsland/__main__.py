import os
import sys
import typing as t
from os.path import exists

from argsense import CommandLineInterface
from lk_utils import fs

from . import __path__
from . import __version__
from . import api
from . import paths
from . import system_info as sysinfo
from .manifest import T
from .manifest import get_last_installed_version

# fix sys.argv
if len(sys.argv) > 1 and sys.argv[1].endswith('.exe'):
    # e.g. ['E:\depsland_app\depsland\__main__.py',
    #       'E:\depsland_app\depsland.exe', ...]
    sys.argv.pop(1)

cli = CommandLineInterface('depsland')
print('depsland [red][dim]v[/]{}[/] [dim]({})[/]'.format(
    __version__, __path__[0]
), ':r')


@cli.cmd()
def version() -> None:
    """
    show basic information about depsland.
    """
    # ref: the rich text (with gradient color) effect is copied from
    #   likianta/lk-logger project.
    from lk_logger.control import _blend_text  # noqa
    from random import choice
    from . import __date__, __path__, __version__
    
    color_pairs_group = (
        ('#0a87ee', '#9294f0'),  # calm blue -> light blue
        ('#2d34f1', '#9294f0'),  # ocean blue -> light blue
        ('#ed3b3b', '#d08bf3'),  # rose red -> violet
        ('#f38cfd', '#d08bf3'),  # light magenta -> violet
        ('#f47fa4', '#f49364'),  # cold sandy -> camel tan
    )
    
    color_pair = choice(color_pairs_group)
    colorful_title = _blend_text(
        '♥ depsland v{} ♥'.format(__version__), color_pair
    )
    print(f'[b]{colorful_title}[/]', ':rs1')
    
    print(':rs1', '[cyan]released at [u]{}[/][/]'.format(__date__))
    print(':rs1', '[magenta]located at [u]{}[/][/]'.format(__path__[0]))


@cli.cmd()
def welcome(confirm_close=False) -> None:
    """
    show welcome message and exit.
    """
    from lk_logger.console import console
    from rich.markdown import Markdown
    from textwrap import dedent
    from . import __date__
    from . import __version__
    
    console.print(Markdown(dedent('''
        # Depsland

        Depsland is a python apps manager for non-developer users.
        
        - Version: {}
        - Release date: {}
        - Author: {}
        - Official website: {}
    ''').format(
        __version__,
        __date__,
        'Likianta <likianta@foxmail.com>',
        'https://github.com/likianta/depsland'
    )))
    
    if confirm_close:
        input('press enter to close window...')


@cli.cmd()
def launch_gui(_app_token: str = None, _run_at_once: bool = False) -> None:
    """
    launch depsland gui.
    
    kwargs:
        _app_token: an appid or a path to a manifest file.
            if given, the app will launch and instantly install it.
        _run_at_once:
            for `true` example, see `./api/dev_api/publish.py : main() : -
            \\[var] command`
            for `false` example, see `./api/dev_api/offline_build.py : -
            _create_updator()`
    """
    # import os
    # os.environ['QT_API'] = 'pyside6_lite'
    try:
        import qmlease
    except ModuleNotFoundError:
        print('launching GUI failed. you may forget to install qt for python '
              'library (suggest `pip install pyside6` etc.)', ':v4')
        return
    
    if sysinfo.platform.IS_WINDOWS:
        _toast_notification('Depsland is launching')
    
    if _app_token and os.path.isfile(_app_token):
        _app_token = fs.abspath(_app_token)
    # if _run_at_once is None:
    #     _run_at_once = bool(_app_token)
    
    from .ui import launch_app
    launch_app(_app_token, _run_at_once)


# -----------------------------------------------------------------------------
# ordered by lifecycle

@cli.cmd()
def init(manifest='.', app_name='', overwrite=False,
         auto_find_requirements=False) -> None:
    """
    create a "manifest.json" file in project directory.
    
    kwargs:
        manifest (-m): if directory of manifest not exists, it will be created.
        app_name (-n): if not given, will use directory name as app name.
        auto_find_requirements (-a):
        overwrite (-w):
    """
    api.init(_fix_manifest_param(manifest), app_name, overwrite,
             auto_find_requirements)


@cli.cmd()
def build(
    manifest: str = '.',
    offline: bool = False,
    gen_exe: bool = True
) -> None:
    """
    build your python application based on manifest file.
    the build result is stored in "dist" directory.
    [dim]if "dist" not exists, it will be auto created.[/]
    
    kwargs:
        manifest (-m): a path to the project directory (suggested) or to a -
            mainfest file.
            if project directory is given, will search 'manifest.json' file -
            under this dir.
            [red dim]╰─ if no such file found, will raise a FileNotFound -
            error.[/]
            if a file is given, it must be '.json' type. depsland will treat -
            its folder as the project directory.
            [blue dim]╰─ if a file is given, the file name could be custom. -
            (we suggest using 'manifest.json' as canondical.)[/]
    """
    if offline:
        api.build_offline(_fix_manifest_param(manifest))
    else:
        api.build(_fix_manifest_param(manifest), gen_exe)


@cli.cmd()
def publish(manifest='.', full_upload=False) -> None:
    """
    publish dist assets to oss.
    if you configured a local oss server, it will generate assets to -
    `~/oss/apps/<appid>/<version>` directory.
    
    kwargs:
        full_upload (-f): if true, will upload all assets, ignore the files -
            which may already exist in oss (they all will be overwritten).
            this option is useful if you found the oss server not work properly.
    """
    api.publish(_fix_manifest_param(manifest), full_upload)


@cli.cmd()
def install(appid: str, upgrade=True, reinstall=False) -> None:
    """
    install an app from oss by querying appid.
    
    kwargs:
        upgrade (-u):
        reinstall (-r):
    """
    api.install_by_appid(appid, upgrade, reinstall)


@cli.cmd()
def upgrade(appid: str) -> None:
    """
    upgrade an app from oss by querying appid.
    """
    api.install_by_appid(appid, upgrade=True, reinstall=False)


@cli.cmd()
def uninstall(appid: str, version: str = None) -> None:
    """
    uninstall an application.
    """
    if version is None:
        version = get_last_installed_version(appid)
    if version is None:
        print(f'{appid} is already uninstalled.')
        return
    api.uninstall(appid, version)


# @cli.cmd()
# def self_upgrade() -> None:
#     """
#     upgrade depsland itself.
#     """
#     api.self_upgrade()


# -----------------------------------------------------------------------------

@cli.cmd()
def show(appid: str, version: str = None) -> None:
    """
    show manifest of an app.
    """
    from .manifest import load_manifest
    if version is None:
        version = get_last_installed_version(appid)
    assert version is not None
    dir_ = '{}/{}/{}'.format(paths.project.apps, appid, version)
    manifest = load_manifest(f'{dir_}/manifest.pkl')
    print(manifest, ':l')


@cli.cmd()
def view_manifest(manifest: str = '.') -> None:
    from .manifest import load_manifest
    manifest = load_manifest(_fix_manifest_param(manifest))
    print(manifest, ':l')


@cli.cmd(transport_help=True)
def run(appid: str, *args, _version: str = None, **kwargs) -> None:
    """
    a general launcher to start an installed app.
    """
    print(sys.argv, ':lv')
    
    version = _version or get_last_installed_version(appid)
    if not version:
        print(':v4', f'cannot find installed version of {appid}')
        return
    
    import lk_logger
    import subprocess
    from argsense import args_2_cargs
    from .manifest import load_manifest
    from .manifest import parse_script_info
    
    manifest = load_manifest('{}/{}/{}/manifest.pkl'.format(
        paths.project.apps, appid, version
    ))
    assert manifest['version'] == version
    command = parse_script_info(manifest)
    os.environ['DEPSLAND'] = paths.project.root
    os.environ['PYTHONPATH'] = '.;{app_dir};{pkg_dir}'.format(
        app_dir=manifest['start_directory'],
        pkg_dir=paths.apps.get_packages(appid, version)
    )
    
    if not manifest['launcher']['show_console']:
        if sysinfo.platform.IS_WINDOWS:
            _toast_notification(
                'Depsland is launching "{}"'.format(manifest['name'])
            )
    
    # print(':v', args, kwargs)
    lk_logger.unload()
    try:
        subprocess.run(
            (*command, *args_2_cargs(*args, **kwargs)),
            check=True,
            cwd=manifest['start_directory'],
            stderr=subprocess.PIPE,
            text=True,
        )
    except subprocess.CalledProcessError as e:
        lk_logger.enable()
        print(':v4f', '\n' + (e.stderr or '').replace('\r', ''))
        if manifest['launcher']['show_console']:
            # raise e
            input('press enter to close window... ')
        else:
            _toast_notification(
                'Exception occurred at "{}"!'.format(manifest['name'])
            )


# -----------------------------------------------------------------------------

@cli.cmd()
def rebuild_pypi_index(full: bool = False) -> None:
    """
    rebuild local pypi index. this may resolve some historical problems caused -
    by pip network issues.
    
    kwargs:
        full (-f): if a package is downloaded but not installed, will perform -
            a `pip install` action.
    """
    from .doctor import rebuild_pypi_index
    rebuild_pypi_index(perform_pip_install=full)


@cli.cmd()
def get_package_size(
        name: str,
        version: str = None,
        include_dependencies: bool = False
) -> None:
    """
    kwargs:
        include_dependencies (-d):
    """
    from .pypi import insight
    insight.measure_package_size(name, version, include_dependencies)


# -----------------------------------------------------------------------------

def _check_version(new: T.Manifest, old: T.Manifest) -> bool:
    from .utils import compare_version
    return compare_version(new['version'], '>', old['version'])


def _fix_manifest_param(manifest: str) -> str:  # return a file path to manifest
    if os.path.isdir(manifest):
        out = fs.normpath(f'{manifest}/manifest.json', True)
    else:
        out = fs.normpath(manifest, True)
        assert exists(out), f'path not exists: {out}'
    # print(':v', out)
    return out


def _get_dir_to_last_installed_version(appid: str) -> t.Optional[str]:
    if last_ver := get_last_installed_version(appid):
        dir_ = '{}/{}/{}'.format(paths.project.apps, appid, last_ver)
        assert exists(dir_), dir_
        return dir_
    return None


def _get_manifests(appid: str) -> t.Tuple[t.Optional[T.Manifest], T.Manifest]:
    from .manifest import change_start_directory
    from .manifest import init_target_tree
    from .manifest import load_manifest
    from .oss import get_oss_client
    from .utils import make_temp_dir
    
    temp_dir = make_temp_dir()
    
    oss = get_oss_client(appid)
    oss.download(oss.path.manifest, x := f'{temp_dir}/manifest.pkl')
    manifest_new = load_manifest(x)
    change_start_directory(manifest_new, '{}/{}/{}'.format(
        paths.project.apps,
        manifest_new['appid'],
        manifest_new['version']
    ))
    init_target_tree(manifest_new)
    fs.move(x, manifest_new['start_directory'] + '/manifest.pkl')
    
    if x := _get_dir_to_last_installed_version(appid):
        manifest_old = load_manifest(f'{x}/manifest.pkl')
    else:
        print('no previous version found, it may be your first time to install '
              f'{appid}')
        print('[dim]be noted the first-time installation may consume a long '
              'time. depsland will try to reduce the consumption in the '
              'succeeding upgrades/installations.[/]', ':r')
        manifest_old = None
    
    return manifest_old, manifest_new


def _run_cli() -> None:
    """ this function is for poetry to generate script entry point. """
    cli.run()


# windows only
def _toast_notification(text: str) -> None:
    from windows_toasts import Toast
    from windows_toasts import WindowsToaster
    toaster = WindowsToaster('Depsland Launcher')
    toast = Toast()
    toast.text_fields = [text]
    toaster.show_toast(toast)


if __name__ == '__main__':
    cli.run()
