__all__ = ['merge_ordered_lists']

from dataclasses import dataclass
import heapq
from collections import defaultdict
from typing import Iterable, Hashable
from enum import Enum

"""
Alogirthm made mostly with Claude
Lower = Higher priority (minheap)

Overview:
    Process input into graph and priorities
        `node_meta` - Nodes (each item) with list priority
        `edges` - Directed edges (from -> to)
        (store `in_degree` and `node_meta`)
    Turn graph into a DAG
        Use repeated DFS removing the lowest priority in the cycle
    
"""

@dataclass
class NodeMeta:
    own_priority: int          # never mutated after creation; used as tiebreaker
    effective_priority: int    # starts equal to own_priority, then propagated from successors

@dataclass
class Edge[T]:
    _from: T
    to: T
    priority: int

def merge_ordered_lists[T: Hashable](lists: Iterable[Iterable[T]]) -> list[T]:

    # --- Build graph ---

    graph: dict[T, set[T]] = defaultdict(set)
    in_degree: dict[T, int] = defaultdict(int)
    edges: list[Edge[T]] = []                   # all edges with metadata, for conflict resolution
    node_meta: dict[T, NodeMeta] = {}

    for priority, _lst in enumerate(lists):
        LIST = list(_lst)
        for i, curr in enumerate(LIST):

            if curr not in node_meta:
                node_meta[curr] = NodeMeta(own_priority=priority, effective_priority=priority)
            if curr not in graph:
                graph[curr] = set()

            if i > 0:
                parent = LIST[i - 1]
                if curr not in graph[parent]:
                    graph[parent].add(curr)
                    in_degree[curr] += 1
                    edges.append(Edge(parent, curr, priority))

        # print_graph(graph)

    resolve_cycles(graph, in_degree, edges)
    # print_graph(graph)

    propagate_priorities(graph, node_meta)

    # --- Topological sort (Kahn's algorithm with priority tiebreaker) ---

    # Tiebreak on (effective_priority, own_priority): effective_priority reflects
    # the best priority reachable through this node's chain; own_priority breaks
    # ties between roots whose chains happen to bottom out at the same value.
    available: list[tuple[int, int, T]] = []

    for node in node_meta:
        if in_degree[node] == 0:
            meta = node_meta[node]
            heapq.heappush(available, (meta.effective_priority, meta.own_priority, node))

    result: list[T] = []

    while available:
        # print(available)
        (_, _, node) = heapq.heappop(available)
        result.append(node)
        for child in graph[node]:
            in_degree[child] -= 1
            if in_degree[child] == 0:
                meta = node_meta[child]
                heapq.heappush(available, (meta.effective_priority, meta.own_priority, child))

    return result


def propagate_priorities[T](graph: dict[T, set[T]], node_meta: dict[T, NodeMeta]):
    """
    Propagate priority backwards through the DAG: a node's effective_priority
    becomes the best (lowest) priority of itself or anything reachable from it.
    Requires graph to already be acyclic (run after resolve_cycles).
    Processes nodes in reverse topological order so children are finalized
    before their parents are updated.
    """
    order = topological_order(graph)

    for node in reversed(order):
        for child in graph[node]:
            if node_meta[child].effective_priority < node_meta[node].effective_priority:
                node_meta[node].effective_priority = node_meta[child].effective_priority


def topological_order[T](graph: dict[T, set[T]]) -> list[T]:
    """Plain topological sort (no priority tiebreaking) used internally by propagation."""
    in_degree: dict[T, int] = defaultdict(int)
    for node in graph:
        in_degree[node]  # ensure entry exists
        for child in graph[node]:
            in_degree[child] += 1

    queue = [n for n in graph if in_degree[n] == 0]
    order: list[T] = []

    while queue:
        node = queue.pop()
        order.append(node)
        for child in graph[node]:
            in_degree[child] -= 1
            if in_degree[child] == 0:
                queue.append(child)

    return order


def resolve_cycles[T](
        graph: dict[T, set[T]],
        in_degree: dict[T, int],
        edges: list[Edge[T]]
):
    """
    Turn the graph into a DAG. Repeatedly runs a full DFS pass looking for
    cycles; whenever one is found, removes the single lowest-priority edge
    in that cycle, then restarts the DFS pass from scratch.
 
    A single DFS pass can only safely report the FIRST cycle it encounters:
    once a node goes black, later traversals trust that everything reachable
    from it is acyclic, but cutting an edge elsewhere can leave a different
    cycle through that same node undetected (it was already marked black
    before that cycle's defining back edge was reached). Restarting after
    each cut avoids this — every remaining cycle is guaranteed to be found
    by some future full pass, since black is only trustworthy when computed
    against the CURRENT graph, not a graph that's since been mutated.
    """

    edge_lookup: dict[tuple[T, T], Edge[T]] = {(e._from, e.to): e for e in edges}
    
    while True:
        weakest = find_weakest_cycle_edge(graph, edge_lookup)
        if weakest is None:
            return # one full pass found no cycles: graph is a DAG
 
        # print(f'Removed {weakest}')
        graph[weakest._from].discard(weakest.to)
        in_degree[weakest.to] -= 1
        edges.remove(weakest)
        del edge_lookup[(weakest._from, weakest.to)]
 

class _S(Enum):
    UNVISITED = 0
    ON_PATH = 1
    DONE = 2

def find_weakest_cycle_edge[T](
        graph: dict[T, set[T]],
        edge_lookup: dict[tuple[T, T], Edge[T]],
) -> Edge[T] | None:
    """
    Run one full iterative DFS over the graph (does not mutate it).
    Returns the lowest-priority edge belonging to the FIRST cycle found,
    or None if the graph is currently a DAG.
    """
    status: dict[T, _S] = defaultdict(lambda: _S.UNVISITED)
 
    for start in graph.keys():
        if status[start] != _S.UNVISITED:
            continue
 
        # Each frame is [node, iterator over remaining neighbors]. The
        # sequence of first elements across `stack` IS the current root-to-
        # leaf path (gray nodes, in order), so no separate `path` list is needed.
        stack: list[list] = [[start, iter(graph[start])]]
        status[start] = _S.ON_PATH
 
        while stack:
            node, neighbor_iter = stack[-1]
            neighbor = next(neighbor_iter, None)
 
            if neighbor is None:
                status[node] = _S.DONE
                stack.pop()
                continue
 
            if status[neighbor] == _S.UNVISITED:
                status[neighbor] = _S.ON_PATH
                stack.append([neighbor, iter(graph[neighbor])])
 
            elif status[neighbor] == _S.ON_PATH:
                # Back edge: `neighbor` is an ancestor on the current path.
                # Find its position in `stack` to recover the full cycle.
                cycle_start = next(i for i, frame in enumerate(stack) if frame[0] == neighbor)
                cycle_nodes = [frame[0] for frame in stack[cycle_start:]] + [neighbor]
                weakest: Edge[T] | None = None
                for a, b in reversed(list(zip(cycle_nodes, cycle_nodes[1:]))):
                    edge = edge_lookup[(a, b)]
                    if weakest is None or edge.priority > weakest.priority:
                        weakest = edge
 
                return weakest

            elif status[neighbor] == _S.DONE:
                # already fully explored, nothing to do.
                pass
 
    return None  # full pass completed, no cycles found


def print_graph[T](graph: dict[T, set[T]]):
    for k, v in graph.items():
        print(f'{k:>4}: {v}')
    print()


def tests():
    test_cases = [
        # ('W AB BC CD ZY YX XW'.split(), 'ZYXWABCD'),
        # ('A Z AB'.split(), 'AZB'),
        # ('AFG BC BCEF CDEF'.split(), 'ABCDEFG'),
        # ('A B C'.split(), 'ABC'),
        # ('AC BC CA'.split(), 'ABC'),
        # ('CA BC AB'.split(), 'BCA'),
        # ('BC CA AB CDA'.split(), 'BCDA'),
        # ('BC CA CDA AB'.split(), 'BCDA'),
        # ('1234567890 0987654321'.split(), '1234567890'),
        # ('AB 12B34A56'.split(), 'A12B3456'),
        # ('AB BCA'.split(), 'ABC'),
        
        # set iteration leads to different results based on inputs
        # ('AB B_-A'.split(), 'AB_-'),
        # ('AB B_A-'.split(), 'AB-_'),

        # ('AB BCDA'.split(), 'ABCD'),
        # ('AB BCAD'.split(), 'ABCD'),

        ([
            '1256890ABDE',
            '3456890ABDE',
            '7890ABCDEFG',
        ], '1234567890ABCDEFG'),
    ]

    for lists, expected in test_cases:
        result = merge_ordered_lists(lists)
        joined = ''.join(result)
        if joined != expected:
            print(f'Result: {joined}  Expected: {expected}  Match: {joined == expected}')

def main():
    tests()
    # import random
    # import json

    # m, M = 1, 25
    # SIZES = [17,14,12,10]
    # WRITE = True

    # nums = list(range(m, M+1))
    # lists = [random.sample(nums, s) for s in SIZES]
    # for l in lists: random.shuffle(l)

    # if WRITE:
    #     with open(f'test/mereger-{len(SIZES)}.in.json', 'w') as f:
    #         json.dump(lists, f)
    
    # out = merge_ordered_lists(lists)

    # if WRITE:
    #     with open(f'test/mereger-{len(SIZES)}.out.json', 'w') as f:
    #         json.dump(out, f)

if __name__ == "__main__":
    main()