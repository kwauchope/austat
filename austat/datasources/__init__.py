__all__ = ["dummy", "demographics", "todo", "economic", "social"]

_SOURCES = []

def _import(path, name, ds_lst):
    return __import__(path + name, fromlist=ds_lst)

def getsources():
    if not _SOURCES:
        for datasource in __all__:
            try:
                module = _import("austat.datasources.", datasource, [datasource])
            except ImportError:
                module = _import("datasources.", datasource, [datasource])
            source = getattr(module, datasource)()
            if len(source.getdatasets()) > 0:
                _SOURCES.append(source)
    return _SOURCES


def available_sources():
    srcs = getsources()

    return list({'id': x[0], 'name': x[1].name, "answers" : x[1].answers} for x in enumerate(srcs))
