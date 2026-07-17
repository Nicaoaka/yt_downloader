__all__ = ['merge_ordered_lists']

import heapq
from collections import defaultdict
from typing import Hashable, Iterable

class DynamicTopoSort[T: Hashable]:
    def __init__(self, nodes: Iterable[T] = []) -> None:
        self._ord_to_node: list[T] = [] 
        self._node_to_ord: dict[T, int] = {}
        self._out_edges: dict[T, list[T]] = defaultdict(list) # to find child descendents
        self._in_edges:  dict[T, list[T]] = defaultdict(list) # to find parent ancestors
        
        for n in nodes:
            self.add_node(n)

    def add_node(self, node: T):
        if node not in self._node_to_ord:
            pos = len(self._ord_to_node) # put at the end of current ordering
            self._ord_to_node.append(node)
            self._node_to_ord[node] = pos
            self._out_edges[node]  # ensure entry exists
            self._in_edges[node]   # ensure entry exists

    def add_edge(self, parent: T, child: T) -> bool:
        """
        Adds edge `parent` -> `child` if it doesn't create a cycle.
        Returns True if the edge was added and False if it was not.

        Overview:
        3 cases:
            1. Edge goes to self -> don't add edge
            2. Child is after parent in topo_order -> can add edge
            3. Child is before parent in topo_order -> 
                _discover() to check for cycle, check/update topo_order
        """

        # self loop
        if parent == child:
            return False
        
        # already exists
        if child in self._out_edges[parent]:
            raise Warning("Edge already exists")
        
        # matches order
        # ... parent ... child ...
        #     parent --> child
        if self._node_to_ord[parent] < self._node_to_ord[child]:
            self._out_edges[parent].append(child)
            self._in_edges[child].append(parent)
            return True
        
        # need to check for cycle
        # ... child ... parent ...
        #     child <-- parent
        ancestors:   list[T] = []
        descendants: list[T] = []
        cycle = self._discover(parent, child, ancestors, descendants)
        if cycle:
            return False
        
        # update order to support the edge
        BY_ORD = lambda node: self._node_to_ord[node]
        current_pos     = sorted(self._node_to_ord[node] for node in descendants + ancestors)
        nodes_reordered = sorted(ancestors, key=BY_ORD) + sorted(descendants, key=BY_ORD)
        for pos, node in zip(current_pos, nodes_reordered):
            self._node_to_ord[node] = pos
            self._ord_to_node[pos] = node

        # add edge
        self._out_edges[parent].append(child)
        self._in_edges[child].append(parent)
        return True
    
    def _discover(self, parent: T, child: T, ancestors: list[T], descendants: list[T]) -> bool:
        """
        Takes the edge as `parent` -> `child`.
        - `ancestors` is filled with parent and its ancestors up to child index
        - `descendants` is filled with child and its descendants up to parent index

        Bounded:
            ...  child ... parent  ...
            ... [c_ord ...  p_ord] ...
        
        DFS runs child only goes forward/right

        Forward:
             child -> ? -> ?
            [c_ord ... p_ord]
        
        Backward:
             ? <- ? <- parent
            [c_ord ...  p_ord]

        Note, ancestors and descendants will be disjoint.
        """
        
        p_ord = self._node_to_ord[parent]
        c_ord = self._node_to_ord[child]

        # forwards (child -> ? -> ?)
        visited: set[T] = set()
        stack = [child]
        while stack:
            curr = stack.pop()
            visited.add(curr)
            descendants.append(curr)
            for desc in self._out_edges[curr]:
                if desc == parent:
                    return True # found cycle
                if self._node_to_ord[desc] <= p_ord and desc not in visited:
                    stack.append(desc)
                    visited.add(desc)

        # backwards (? <- ? <- parent)
        visited = set()
        stack = [parent]
        while stack:
            curr = stack.pop()
            visited.add(curr)
            ancestors.append(curr)
            for anc in self._in_edges[curr]:
                if c_ord <= self._node_to_ord[anc] and anc not in visited:
                    stack.append(anc)
                    visited.add(anc)
    
        return False

type Node = int
type NodePriority = int
type IslandPriority = int

def _create_dag(lists: list[list[Node]], nodes: list[Node]):

    dts = DynamicTopoSort[Node](nodes=nodes)
    priority:  list[NodePriority] = [-len(lists) for _ in range(len(nodes))]

    for lst_priority, lst in enumerate(lists, start=1): # start is arbitrary
        parent: Node|None = None
        for child in lst:
            priority[child] = max(-lst_priority, priority[child])

            # first iter
            if parent is None:
                parent = child
                continue
            
            # edge already exists
            if child in dts._out_edges[parent]:
                parent = child
                continue
            
            # only add if it'd still be a DAG
            if not dts.add_edge(parent, child):
                continue
            
            # edges are stored in `dts`
            parent = child
    
    return dts, priority

def _get_islands_priorities(dts: DynamicTopoSort[Node], priority: list[NodePriority]) -> list[IslandPriority]:
    UNSET = 69420 # valid priorities are 0 or negative
    islands: list[IslandPriority] = [UNSET for _ in range(len(dts._ord_to_node))]
    for node in dts._ord_to_node:
        if islands[node] != UNSET: # node already visited
            continue

        p_island: IslandPriority = min(priority)
        curr_island: set[Node] = {node}
        stack: list[Node] = [node]
        while stack:
            curr = stack.pop()
            p_island = max(priority[curr], p_island)
            for next_ in dts._in_edges[curr] + dts._out_edges[curr]:
                if next_ not in curr_island:
                    curr_island.add(next_)
                    stack.append(next_)
        
        for node in curr_island:
            islands[node] = p_island
        
    return islands

def merge_ordered_lists[T: Hashable](_lists: Iterable[Iterable[T]]) -> list[T]:
    """
    Priority is highest to lowest from first to last element in `lists`.
    (eg. lists[0] is highest priority, lists[-1] is lowest priority).

    Higher priority lists will have their orderings favored
    over ALL conflicting orderings in lower priority lists.

    Overview:
    Preprocess items:
        Map every unique item in lists to a unique value (i.e. a hash)
        Will be used in postprocessing to create the return
        Create:
            `node_priorities` map from node to its priority

    Parse lists into a Directed Acyclic Graph:
        Iterate through `lists` from highest to lowest priority
            Init `parent` node as None
            For each element (`child`) in the list
                If `parent` is None or if the edge `parent` -> `child` exists,
                    Set `parent = child`
                    continue
                If creating an edge from `parent` to `child` would create a cycle,
                    (leave child as is; DO NOT set `parent = child`)
                    continue
                Create an edge from `parent` -> `child`
                Set `parent = child`
    
    Use topological sort (with highest priority node for tie breaking) to get result:
        Requires:
            `in_degrees` get during DAG creation or traversing DAG once
                (either should take negligible time)
        Create a minheap of all nodes with in_degree 0, with elements like (node_priority, node)
        Heappop through the minheap
            Add node to result
            Go through the node's edges (to `child` nodes)
                Update `in_degrees`
                If `in_degrees == 0` heappush the `child` to the minheap

    Postprocess and return the result
        Using the inverse of the preprocessing map, create the result
        Return the result
    """

    item_to_node: dict[T, Node] = {} # cache
    node_to_item: list[T] = []
    # behaves like dict[Node, T] since Node is an index

    lists: list[list[Node]] = []
    for _lst in _lists:
        lst: list[Node] = []
        for item in _lst:
            if item not in item_to_node:
                item_to_node[item] = len(node_to_item)
                node_to_item.append(item)
            lst.append(item_to_node[item])
        lists.append(lst)
    del item_to_node

    NODES: list[Node] = list(range(len(node_to_item)))
    if len(NODES) == 0: return []
    if len(NODES) == 1: return [node_to_item[0]]
    
    DTS, PRIORITY = _create_dag(lists, NODES)
    ISLANDS = _get_islands_priorities(DTS, PRIORITY)

    out_degree = [len(DTS._out_edges[node]) for node in NODES]
    rev_res: list[Node] = []
    minheap: list[tuple[IslandPriority, NodePriority, Node]] = []
    for node, deg in enumerate(out_degree):
        if deg == 0:
            heapq.heappush(minheap, (ISLANDS[node], PRIORITY[node], node))
    
    while minheap:
        _, _, curr = heapq.heappop(minheap)
        rev_res.append(curr)
        for parent in DTS._in_edges[curr]:
            out_degree[parent] -= 1
            if out_degree[parent] == 0:
                heapq.heappush(minheap, (ISLANDS[parent], PRIORITY[parent], parent))
    
    res = reversed(rev_res)
    return [node_to_item[node] for node in res]
