class RAGError(Exception):
    """An error whose message is safe to show to an end user (never contains secrets)."""