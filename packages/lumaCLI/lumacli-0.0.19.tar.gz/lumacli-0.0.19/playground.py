import logging

from IPython.terminal.embed import InteractiveShellEmbed
from IPython.terminal.prompts import Prompts, Token
from pygments.token import Token

from lumaCLI import __version__
from lumaCLI.luma import *
from lumaCLI.tests import *
from lumaCLI.tests.utils import *
from lumaCLI.utils import *


logging.basicConfig(level=logging.ERROR)


class MyPrompt(Prompts):
    def __init__(self, shell):
        super().__init__(shell)

    def in_prompt_tokens(self, cli=None):
        return [(Token.Prompt, ">>> ")]

    def continuation_prompt_tokens(self, cli=None, width=None):
        return [(Token.Prompt, "... ")]

    def out_prompt_tokens(self):
        return [(Token.Prompt, "")]


if __name__ == "__main__":
    variables = {
        "name": "LumaCLI Playground",
        "version": __version__,
    }
    variables.update(globals())
    variables.update(locals())

    # Create an IPython shell instance
    shell = InteractiveShellEmbed(user_ns=variables)

    shell.banner1 = "\033[32m---------------- Luma CLI {version} Interactive Playground ----------------\033[0m\n\n".format(
        version=__version__
    )
    # Set custom prompts and autoreload
    shell.autoindent = True
    shell.prompts = MyPrompt(shell)
    shell.run_line_magic("load_ext", "autoreload")
    shell.run_line_magic("autoreload", "2")

    # Start the shell
    shell()
