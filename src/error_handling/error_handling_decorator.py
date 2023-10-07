import traceback


def handle_errors(method):
    """A decorator that will catch and handle any errors raised by method."""

    def wrapper(self, *args, **kwargs):  # Takes args and kwargs of original function
        try:
            return method(self, *args, **kwargs)  # Returns value of original function
        except Exception as err:
            self.controller.frames["ErrorScreen"].display_error_message(err)
            self.controller.frames["ErrorScreen"].display_full_traceback(
                traceback.format_exc()
            )
            self.controller.show_frame("ErrorScreen")

    return wrapper
