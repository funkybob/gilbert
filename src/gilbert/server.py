import asyncio

from bareasgi import Application
from bareasgi_static import add_static_file_provider
from watchfiles import awatch


class Watcher:
    def __init__(self, site):
        self.site = site

    async def run(self):
        async for changes in awatch(
            self.site.templates_dir,
            self.site.pages_dir,
            self.site.content_dir,
            stop_event=self.shutdown,
        ):
            print(f"-- Saw changes: {changes}")
            self.site.templates.clear()
            self.site.render()
            print("-- Rebuild complete")

    def start(self):
        print("STARTING WATCHER")
        self.site.templates.clear()
        self.site.render()
        print("RENDER COMPLETE")

        self.shutdown = asyncio.Event()
        self.task = asyncio.create_task(self.run())

    async def stop(self):
        self.shutdown.set()
        await self.task


def make_app(site):
    async def startup(request):
        request.info["watcher"] = Watcher(site)
        request.info["watcher"].start()

    async def shutdown(request):
        await request.info["watcher"].stop()

    app = Application(
        startup_handlers=[startup],
        shutdown_handlers=[shutdown],
    )
    add_static_file_provider(app, site.dest_dir, index_filename="index.html")

    return app
