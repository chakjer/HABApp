from pathlib import Path

from HABApp.config.logging import default_logfile
from HABApp.config.logging.config import _yaml_safe
from HABApp.config.platform_defaults import get_log_folder


def test_defaults() -> None:
    assert None is get_log_folder()
    assert Path('/log') == get_log_folder(Path('/log'))


def test_valid_yml(monkeypatch) -> None:
    """ensure we create valid yml files"""

    def ensure_key(key, obj) -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                ensure_key(k, v)
        else:
            assert obj != ''

    monkeypatch.setattr(default_logfile, 'is_openhabian', lambda: True)
    monkeypatch.setattr(default_logfile, 'get_log_folder', lambda: Path('/platfrom/log/folder'))

    default = default_logfile.get_default_logfile()
    ensure_key('root', _yaml_safe.load(default))

    monkeypatch.setattr(default_logfile, 'is_openhabian', lambda: False)
    default = default_logfile.get_default_logfile()
    ensure_key('root', _yaml_safe.load(default))

    monkeypatch.setattr(default_logfile, 'get_log_folder', lambda: None)
    default = default_logfile.get_default_logfile()
    ensure_key('root', _yaml_safe.load(default))
