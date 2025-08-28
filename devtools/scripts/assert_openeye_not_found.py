try:
    from openeye import oechem  # noqa

    raise Exception("OpenEye Toolkits ARE installed")
except ModuleNotFoundError:
    pass
