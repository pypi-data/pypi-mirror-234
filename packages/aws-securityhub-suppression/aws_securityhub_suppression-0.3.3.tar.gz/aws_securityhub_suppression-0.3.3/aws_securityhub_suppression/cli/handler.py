import os
import click


class CliHandler(click.MultiCommand):
    __plugin_folder = os.path.join(os.path.dirname(__file__), "commands")

    def list_commands(self, ctx):
        """Dynamically get the list of cli."""
        rv = []
        for filename in os.listdir(self.__plugin_folder):
            if filename.endswith(".py") and not filename.startswith("__init__"):
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        """Dynamically get the command."""
        ns = {}
        fn = os.path.join(self.__plugin_folder, name + ".py")
        with open(fn) as f:
            code = compile(f.read(), fn, "exec")
            eval(code, ns, ns)
        return ns["cli"]
