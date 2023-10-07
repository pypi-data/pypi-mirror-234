class Context:
    context: dict = {}

    @staticmethod
    def set(key, value):
        Context.context[key] = value

    @staticmethod
    def get(key):
        Context.context.setdefault(key)
        return Context.context.get(key)

    @staticmethod
    def clear():
        Context.context.clear()
