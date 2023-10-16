import importlib_metadata


def _find_pex3_entrypoint():
    pex_dist = importlib_metadata.distribution("pex")
    for entrypoint in pex_dist.entry_points:
        if entrypoint.name == "pex3":
            return entrypoint
    msg = "Unable to find entrypoint for `pex3`"
    raise ValueError(msg)


if __name__ == "__main__":
    pex3 = _find_pex3_entrypoint()
    pex3.load()()
