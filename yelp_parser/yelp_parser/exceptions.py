class UnsupportedInputParameter(Exception):
    def __init__(self, msg, *args, **kwargs):
        self.msg = msg
        super().__init__(*args, **kwargs)
