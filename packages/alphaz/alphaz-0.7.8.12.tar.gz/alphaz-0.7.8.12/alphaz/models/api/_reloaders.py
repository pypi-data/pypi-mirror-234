# MODULES
import os, configparser, datetime, copy, jwt, logging, re, itertools, sys, importlib, warnings, traceback, time

# WERKZEUG
from werkzeug._reloader import reloader_loops, ReloaderLoop
from ._reloader import _find_stat_paths

DEBUGGED_FOLDERS = set()
DEBUG = False


class AlphaStatReloaderLoop(ReloaderLoop):
    name = "AlphaStatDebug"
    start_time = None

    def __enter__(self) -> ReloaderLoop:
        self.mtimes: t.dict[str, float] = {}
        return super().__enter__()

    def run_step(self) -> None:
        global DEBUGGED_FOLDERS

        for name in _find_stat_paths(self.extra_files, self.exclude_patterns):
            if DEBUG:
                DEBUGGED_FOLDERS.add(name)
            try:
                mtime = os.stat(name).st_mtime
            except OSError:
                continue

            old_time = self.mtimes.get(name)

            if old_time is None:
                self.mtimes[name] = mtime
                continue

            if mtime > old_time:
                self.trigger_reload(name)

        if DEBUG and len(DEBUGGED_FOLDERS) == 0:
            with open("werkzeug_dirs.log", "w") as f:
                f.write("\n".join(DEBUGGED_FOLDERS))


class AlphaReloaderLoop(ReloaderLoop):
    name = "AlphaStat"

    def __enter__(self) -> ReloaderLoop:
        self.mtimes: dict[str, float] = {}
        self.sizes: dict[str, float] = {}
        self.stats: dict[str, object] = {}
        return super().__enter__()

    def run_step(self) -> None:
        for name in itertools.chain(
            _find_stat_paths(self.extra_files, self.exclude_patterns)
        ):
            try:
                stats = os.stat(name)
            except OSError:
                continue
            try:
                mtime = stats.st_mtime
            except OSError:
                continue
            try:
                size = stats.st_size
            except OSError:
                continue

            old_time = self.mtimes.get(name)
            old_size = self.sizes.get(name)
            old_stats = self.stats.get(name)

            if old_time is None:
                self.mtimes[name] = mtime
                continue
            if old_size is None:
                self.sizes[name] = size
                continue
            if old_stats is None:
                self.stats[name] = stats
                continue

            if size != old_size:
                print(
                    f"   > Reloading {name}: mtimes {mtime} > {old_time} sizes {size} / {old_size}"
                )
                self.trigger_reload(name)

            elif mtime > old_time:
                print(
                    f"   > File change {name} {mtime} > {old_time}:\n      {old_stats}\n      {stats}"
                )


class AlphaMTimeReloaderLoop(ReloaderLoop):
    name = "AlphaMTimeSimpleStat"

    def __enter__(self) -> ReloaderLoop:
        self.mtimes: t.dict[str, float] = {}
        return super().__enter__()

    def run_step(self) -> None:
        for name in itertools.chain(
            _find_stat_paths(self.extra_files, self.exclude_patterns)
        ):
            try:
                mtime = os.stat(name).st_mtime
            except OSError:
                continue

            old_time = self.mtimes.get(name)

            if old_time is None:
                self.mtimes[name] = mtime
                continue

            if mtime > old_time:
                print(
                    f"   REALOGIND {name=} {mtime=} {old_time=} {self.extra_files=} {self.exclude_patterns=}"
                )
                self.trigger_reload(name)


reloader_loops["alpham"] = AlphaMTimeReloaderLoop
reloader_loops["alpha"] = AlphaStatReloaderLoop
