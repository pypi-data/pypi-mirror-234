import os

def perform_dfs(graph, i, v, cv, result_order, cyclic_flag):
    cv[i] = 1
    for x in graph[i]:
        if x in v:
            continue
        if x in cv:
            cyclic_flag[0] = True
            return
        perform_dfs(graph, x, v, cv, result_order, cyclic_flag)
    result_order.append(i)
    del cv[i]
    v[i] = 1

def top_sort(graph):
    result_order = []
    cyclic_flag = {0: False}
    v = {}
    cv = {}
    for i in range(0, len(graph)):
        if i not in v:
            perform_dfs(graph, i, v, cv, result_order, cyclic_flag)
        if cyclic_flag[0]:
            error_msgs = [
                f'module contains cyclic imports',
                f'cycle beginning from module: {module_names[i]}',
            ]
            raise Exception( '\n'.join(error_msgs) )
    return result_order[::-1]

def bfs_files(base_dir, target_exts):
    target_exts_map = { x : 1 for x in target_exts }
    q = [base_dir]
    result = []
    while len(q) > 0:
        fspath = q.pop()
        if os.path.isdir(fspath):
            for file in os.listdir(fspath):
                q.append( f'{fspath}/{file}' )
            continue
        i1 = fspath.rfind('.', 0)
        ext = fspath[i1+1 : len(fspath) ]
        if ext in target_exts_map or len(target_exts) == 0:
            result.append(fspath)
    return result
