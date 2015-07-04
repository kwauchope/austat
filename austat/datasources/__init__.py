__all__ = ["dummy", "demographics"]

def getsources():
    sources = []
    for datasource in __all__:
        module = __import__("austat.datasources."+datasource, fromlist=[datasource])
        sources.append(getattr(module, datasource)())
    return sources

