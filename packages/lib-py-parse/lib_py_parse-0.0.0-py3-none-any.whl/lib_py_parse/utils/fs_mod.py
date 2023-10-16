import lib_py_parse.utils.graph_alg as graph_alg

def fmt_mod_py( module_name, base_dir='' ):
    C1 = module_name.replace('.', '/')
    if len(base_dir) > 0:
        return f'{base_dir}/{C1}.py'
    return f'{C1}.py'

# return list[ mod_name ] in [pkg_base].[pkg_ns]
def iter_py_mod( pkg_ns, pkg_base ):
    L1 = graph_alg.bfs_files( f'{pkg_base}/{pkg_ns}', ['py'] )
    result = [
        [
            fspath[len(pkg_base)+1:].replace('/', '.')[:-3],
            fspath,
        ]
        for fspath in L1
    ]
    return result
