import contextlib


@contextlib.contextmanager
def soft_assert():
    errors = []

    def check(condition, message):
        if not condition:
            errors.append(message)

    yield check

    if errors:
        raise AssertionError("\n".join(errors))
