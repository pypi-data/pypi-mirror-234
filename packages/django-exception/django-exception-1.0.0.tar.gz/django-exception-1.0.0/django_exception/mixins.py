from .utils import save_exception


class ExceptionMixin:
    def dispatch(self, *args, **kwargs):
        try:
            return super().dispatch(*args, **kwargs)
        except Exception as e:
            save_exception(e)
            raise e
