import coiled


def setup_failure(reason: str, backend: str):
    coiled.add_interaction("setup-failure", error_message=reason, success=False, backend=backend)
