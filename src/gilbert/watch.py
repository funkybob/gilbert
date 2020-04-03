# Serve and watch files
import asyncio
import os

from aionotify import Flags, Watcher


class Watch:
    """
    Watch all the content dirs, and fire a render on change.
    """

    def __init__(self, site):
        self.site = site
        self.watcher = Watcher()

        for path in (site.templates_dir, site.pages_dir, site.content_dir):
            # Recursively add watches to all dirs
            self.add_watch(str(path))
            for subdir in self.find_dirs(path.resolve()):
                self.add_watch(subdir)

    def add_watch(self, path):
        self.watcher.watch(
            path,
            flags=(Flags.MODIFY | Flags.CREATE | Flags.DELETE | Flags.ATTRIB | Flags.DELETE_SELF | Flags.MOVE_SELF),
        )

    def remove_watch(self, path):
        self.watcher.unwatch(path)

    def find_dirs(self, path):
        with os.scandir(path) as itr:
            for entry in itr:
                if entry.is_dir():
                    yield entry.path
                    yield from self.find_dirs(entry.path)

    async def run(self, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        await self.watcher.setup(loop)

        self.site.templates.clear()
        self.site.render()

        while True:
            event = await self.watcher.get_event()

            if event.flags & Flags.ISDIR:
                full_name = os.path.join(event.alias, event.name)
                if event.flags & Flags.CREATE:
                    self.add_watch(full_name)

            self.site.templates.clear()
            self.site.render()
