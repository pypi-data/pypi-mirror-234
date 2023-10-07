import importlib.metadata

__all__ = ("__version__",)

__version__ = importlib.metadata.version(__package__ or __name__)
