class StringMixin:
    def __str__(self):
        return str(self.value)

    def lower(self):
        return str(self.value.lower())
