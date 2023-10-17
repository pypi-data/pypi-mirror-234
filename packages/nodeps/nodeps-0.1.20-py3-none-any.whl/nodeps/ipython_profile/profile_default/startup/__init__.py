# # coding=utf-8
# """
# Puntos Prompt Module
# """
# import os
# import subprocess
#
# from IPython.terminal.prompts import Prompts
# from IPython.terminal.prompts import Token
# import pathlib
# import platform
#
#
# def get_branch():
#     try:
#         return (
#             subprocess.check_output(
#                 "git branch --show-current", shell=True, stderr=subprocess.DEVNULL
#             )
#             .decode("utf-8")
#             .replace("\n", "")
#         )
#     except BaseException:
#         return ""
#
#
# class MyPrompt(Prompts):
#     def in_prompt_tokens(self, cli=None):
#         return [
#             (Token, ""),
#             (Token.OutPrompt, pathlib.Path().absolute().stem),
#             (Token, " "),
#             (Token.Generic.Subheading, "↪"),
#             (Token.Generic.Subheading, get_branch()),
#             *((Token, " "),
#               (Token.Prompt, "©")
#               if os.environ.get("VIRTUAL_ENV")
#               else (Token, "")),
#             (Token, " "),
#             (Token.Name.Class, "v" + platform.python_version()),
#             (Token, " "),
#             (Token.Name.Entity, "ipython"),
#             (Token, " "),
#             (Token.Prompt, "["),
#             (Token.PromptNum, str(self.shell.execution_count)),
#             (Token.Prompt, "]: "),
#             (
#                 Token.Prompt
#                 if self.shell.last_execution_succeeded
#                 else Token.Generic.Error,
#                 "❯ ",
#             ),
#         ]
#
#     def out_prompt_tokens(self, cli=None):
#         return [
#             (Token.OutPrompt, 'Out<'),
#             (Token.OutPromptNum, str(self.shell.execution_count)),
#             (Token.OutPrompt, '>: '),
#         ]
#
#
# IPYTHON = get_ipython()  # noqa
# IPYTHON.prompts = MyPrompt(IPYTHON)
