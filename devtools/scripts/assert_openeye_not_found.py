try:
    from openeye import oechem

    raise Exception("OpenEye Toolkits ARE installed")
except ModuleNotFoundError:
    pass
