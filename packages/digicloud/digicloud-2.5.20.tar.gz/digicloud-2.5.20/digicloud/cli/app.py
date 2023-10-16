from cliff.app import App


class BaseApp(App):
    """Overwrite ``cliff.app.App`` class.

    Make possibility to further extension and overwrite methods.
    """
    middlewares = []

    def prepare_to_run_command(self, cmd):
        for m in self.middlewares:
            m.before(cmd)

    def clean_up(self, cmd, result, err):
        for m in reversed(self.middlewares):
            m.after(cmd, result, err)
