from random import seed
from random import choices
from itertools import product
from time import time
from sys import setrecursionlimit

seed(time()

     )
setrecursionlimit(10000)


class Vortex:
    def __init__(self, number: int):
        self.number = number
        self.next = None

    def __str__(self):
        return "Wierzchołek: " + str(self.number)

    def __repr__(self):
        return str(self.number)


def gen_graph(vortex_count: int, d: float) -> list:
    t = list(range(1, vortex_count + 1))
    return choices(list(product(t, t)), k=int(vortex_count ** 2 * d))


def gen_consequent_list(graph: list, n: int) -> list:
    csq_list = [Vortex(x) for x in range(1, n + 1)]
    for arc in graph:
        current = csq_list[arc[0] - 1]
        consequent = csq_list[arc[1] - 1]
        if current.next is None:
            current.next = Vortex(consequent.number)
        else:
            temp = current.next
            while True:
                if temp.next is None:
                    temp.next = Vortex(consequent.number)
                    break
                temp = temp.next
    return csq_list


def gen_adjacency_matrix(graph: list, n: int) -> list:
    matrix = [[0] * n for _ in range(n)]
    for arc in graph:
        matrix[arc[0] - 1][arc[1] - 1] = 1
    return matrix


def gen_arc_list(graph: list) -> list:
    return graph.copy()


def topological_sort_on_adjacency_matrix(matrix: list) -> (list, list, list, float):
    d = [-1] * len(matrix)
    f = [-1] * len(matrix)
    dfs = []
    i = [1]
    start_time = time()
    for x in range(1, len(matrix)):
        dfs_adjacency_matrix(matrix, dfs, x, i, d, f)
    return dfs, d, f, time() - start_time


def dfs_consequent_list(graph: list, visited: list, checked_no: int = 0, stack=None):
    if stack is None:
        stack = []
    if checked_no < len(graph):
        v = graph[checked_no]
        if v not in visited:
            visited.append(v)
            stack.append(v)
            if v.next is None:
                dfs_consequent_list(graph, visited, stack[-1].number - 1, stack)
            else:
                next_v = v.next
                while next_v is not None:
                    if graph[next_v.number - 1] not in visited:
                        dfs_consequent_list(graph, visited, next_v.number - 1, stack)
                    else:
                        next_v = next_v.next
                if len(stack):
                    dfs_consequent_list(graph, visited, stack[-1].number - 1, stack)
                else:
                    dfs_consequent_list(graph, visited, checked_no + 1, stack)
        if not len(stack):
            checked_no += 1
            dfs_consequent_list(graph, visited, checked_no, stack)


def dfs_adjacency_matrix(matrix: list, visited: list, checked_no: int, i: list, d: list, f: list):
    if checked_no not in visited:
        visited.append(checked_no)
        d[checked_no - 1] = i[0]
        i[0] += 1
        for next in range(len(matrix)):
            if matrix[checked_no - 1][next] == 1:
                dfs_adjacency_matrix(matrix, visited, next + 1, i, d, f)
        f[checked_no - 1] = i[0]
        i[0] += 1


def dfs_arcs_list(arcs: list, n: int, visited: list, checked: int):
    if checked not in visited:
        visited.append(checked)
        for arc in arcs:
            if arc[0] == checked:
                dfs_arcs_list(arcs, n, visited, arc[1])


def returns_adjacency(matrix: list, d: list, f: list) -> int:
    count = 0
    for x in range(len(d)):
        for y in range(len(f)):
            if matrix[x][y] == 1 and d[y] < d[x] < f[x] < f[y]:
                count += 1
    return count


def returns_arcs(arcs: list, d: list, f: list) -> int:
    count = 0
    for arc in arcs:
        if d[arc[1] - 1] < d[arc[0] - 1] < f[arc[0] - 1] < f[arc[1] - 1]:
            count += 1
    return count


def returns_consequent(graph: list, d: list, f: list) -> int:
    count = 0
    for v in graph:
        next_v = v.next
        while next_v is not None:
            if d[next_v.number - 1] < d[v.number - 1] < f[v.number - 1] < f[next_v.number - 1]:
                count += 1
            next_v = next_v.next
    return count


n = [200, 400, 600, 800, 1000, 1200, 1400, 1600, 1800, 2000]
d = [0.2, 0.4]

for density in d:
    print("Dla gestosci d = " + str(density))
    for vortexes in n:
        print("Dla n = " + str(vortexes))
        time_graph_generating = time()
        graph = gen_graph(vortexes, density)
        print("Czas generowania grafu (s): " + str(time() - time_graph_generating))

        adjacency_matrix = gen_adjacency_matrix(graph, vortexes)
        consequent_list = gen_consequent_list(graph, vortexes)
        arcs_list = gen_arc_list(graph)

        dfs_list, dlist, flist, time_mark = topological_sort_on_adjacency_matrix(adjacency_matrix)
        print("Czas zliczania etykiet (s): " + str(time_mark))

        start_time_adjacency = time()
        returns = returns_adjacency(adjacency_matrix, dlist, flist)
        print("Liczba lukow powrotnych: " + str(returns))
        print("Czas zliczania lukow powrotnych (macierz_sasiedztwa): " + str((time() - start_time_adjacency) * 1000))

        start_time_consequent = time()
        returns_consequent(consequent_list, dlist, flist)
        print("Czas zliczania lukow powrotnych (lista_nastepnikow): " + str((time() - start_time_consequent) * 1000))

        start_time_arcs = time()
        returns_arcs(arcs_list, dlist, flist)
        print("Czas zliczania lukow powrotnych (lista_lukow): " + str((time() - start_time_arcs) * 1000))
        print('\n')
    print('\n\n\n')
