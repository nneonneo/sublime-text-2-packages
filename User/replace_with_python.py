import sublime, sublime_plugin


class PromptReplaceWithPythonCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.settings = sublime.load_settings("with_python")
        prompt_text = self.settings.get("replace_lastcode") or ""
        self.window.show_input_panel("Enter Python command (using the 'text' variable)", prompt_text, self.on_done, None, None)
        pass

    def on_done(self, text):
        self.settings.set("replace_lastcode", text)
        try:
            if self.window.active_view():
                self.window.active_view().run_command("replace_with_python", {"code": text} )
        except ValueError:
            pass

class ReplaceWithPythonCommand(sublime_plugin.TextCommand):
    def run(self, edit, code):
        # Make some common modules available
        import re

        try:
            code = compile(code, "<string>", "exec")
        except Exception as e:
            sublime.error_message("Error while compiling your code: " + str(e))
            return

        sel = self.view.sel()
        for r in sel:
            text = self.view.substr(r)
            try:
                d = {"text": text, "re": re}
                exec code in d
                newtext = d['text']
            except Exception as e:
                sublime.error_message("Error while running your code: " + str(e))
                break

            self.view.replace(edit, r, newtext)
