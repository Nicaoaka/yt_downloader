"""
### PROBLEM

You have several lists that each impose a *partial* ordering on some items
(an item can appear in more than one list). The lists disagree with each
other about relative order, and disagree about which items even exist in
common. You want ONE merged ordering that:

And you want one merged ordering that:
1.  Respects every "A comes before B" constraint that doesn't
    contradict a HIGHER priority list.

2.  Prefers the orderings of earlier (higher priority) lists over
    later (lower priority) ones whenever they conflict.

3.  For anything not pinned down by a constraint, breaks ties using
    priority (prefer inserting higher-priority items as early as
    their constraints allow).

### APPROACH (three main phases)

1.  Build a DAG. Each list becomes a chain of edges (item[i] -> item[i+1]),
    but only add an edge if it doesn't create a cycle with edges already
    added from higher-priority lists. This is where "higher priority
    wins on conflict" is enforced.

2.  Group nodes into "islands" (weakly-connected components) and give
    each island a priority equal to the priority of its most important
    member. This is what lets independent chunks of the graph be
    ordered relative to each other by importance, not by some arbitrary
    property of the algorithm.

3.  Topologically sort the DAG in reverse, using island-priority as the primary
    tie-break and node-priority as the secondary tie-break. Going in reverse
    puts low-priority parent nodes as close as possible to their
    higher-priority child nodes.
"""

__all__ = ['merge_ordered_lists']

import heapq
from collections import defaultdict
from typing import Hashable, Iterable


class DynamicTopoSort[T: Hashable]:
    """
    Maintains a topological order of a DAG *incrementally* as edges are
    added one at a time, rejecting any edge that would create a cycle.

    Why not just build the whole graph and run one topological sort at the end?
    Because for each added edge you need to know whether adding it keeps the
    graph acyclic. Maintaining topological information between runs is much
    cheaper than re-sorting the entire graph from scratch.

    Internal bookkeeping
    ---------------------
    Every node is kept in one canonical topological order at all times.

        _ord_to_node[pos]  -> the node currently sitting at position `pos`
        _node_to_ord[node] -> the position `node` currently sits at

    Invariant: for every edge parent -> child,
        _node_to_ord[parent] < _node_to_ord[child]
    i.e. parents always sit to the left of children:
    """

    def __init__(self, vertices: Iterable[T] = []) -> None:
        self._ord_to_node: list[T] = []
        self._node_to_ord: dict[T, int] = {}
        self._out_edges: dict[T, list[T]] = defaultdict(list)  # parent -> [children ...]
        self._in_edges:  dict[T, list[T]] = defaultdict(list)  #  child <- [parents ...]

        for v in vertices:
            self.add_vertex(v)

    def add_vertex(self, v: T):
        if v not in self._node_to_ord:
            pos = len(self._ord_to_node)  # append to the end of current ordering
            self._ord_to_node.append(v)
            self._node_to_ord[v] = pos
            self._out_edges[v]  # ensure entry exists
            self._in_edges[v]   # ensure entry exists

    def add_edge(self, parent: T, child: T) -> bool:
        """
        Adds edge `parent` -> `child` if it doesn't create a cycle.
        Returns `True` if the edge was added and `False` if it was not.

        3 cases:
          1. parent == child               -> self-loop, refuse.
          2. child already after parent    -> invariant already holds,
             just record the edge, no reordering needed.
          3. child currently before parent -> might be a cycle. Search
             the region between them; if no cycle, splice the two
             affected regions (parent + ancestors, child + descendants)
             back-to-back so the invariant holds again.
        """

        if parent == child:
            return False

        if child in self._out_edges[parent]:
            raise Warning("Edge already exists")

        # Case 2: already in the right relative order.
        #     ... parent ......... child ...
        #     add edge parent --> child, nothing to reorder.
        if self._node_to_ord[parent] < self._node_to_ord[child]:
            self._out_edges[parent].append(child)
            self._in_edges[child].append(parent)
            return True

        # Case 3: wrong relative order -- must check for a cycle.
        #     ... child ......... parent ...
        #  Only the region between them (inclusive) can possibly be
        #  involved in a cycle through this new edge, so we only search
        #  that bounded window.
        ancestors:   list[T] = []
        descendants: list[T] = []
        cycle = self._discover(parent, child, ancestors, descendants)
        if cycle:
            return False

        # Safe to add. Now fix the invariant: every node in
        # `descendants` (reachable from child, within the window) must
        # come before every node in `ancestors` (can reach parent,
        # within the window) once the new edge parent -> child exists.
        # We keep each group's own relative order, just interleave the
        # two groups back-to-back into the positions they collectively
        # occupied:
        #
        #     before:  [ ... descendants scattered among ancestors ... ]
        #     after:   [ ... all ancestors ..., all descendants ... ]
        current_pos     = sorted(self._node_to_ord[v] for v in descendants + ancestors)
        nodes_reordered = (sorted(ancestors, key=lambda n: self._node_to_ord[n]) +
                           sorted(descendants, key=lambda n: self._node_to_ord[n]))
        for pos, v in zip(current_pos, nodes_reordered):
            self._node_to_ord[v] = pos
            self._ord_to_node[pos] = v

        self._out_edges[parent].append(child)
        self._in_edges[child].append(parent)
        return True

    def _discover(self, parent: T, child: T, ancestors: list[T], descendants: list[T]) -> bool:
        """
        Given the *proposed* edge parent -> child (where child currently
        sits before parent), find:
          - `descendants`: child and everything reachable forward from
            it, but only as far as parent's current position (anything
            further right can't be relevant to a cycle back to parent).
          - `ancestors`: parent and everything that can reach it
            backward, but only as far as child's current position.

        Bounded search window:
            ...  child ................. parent  ...
                [c_ord .................  p_ord]

        If, while walking forward from child, we ever reach `parent`,
        adding parent -> child would close a cycle
        (parent -> ... -> parent), so we report that immediately.

        `ancestors` and `descendants` end up disjoint. A node can't be
        a descendant of child and an ancestor of parent without
        forming a cycle.
        """

        p_ord = self._node_to_ord[parent]
        c_ord = self._node_to_ord[child]

        # forward search: child -> ? -> ? (bounded to positions <= p_ord)
        visited: set[T] = set()
        stack = [child]
        while stack:
            curr = stack.pop()
            visited.add(curr)
            descendants.append(curr)
            for desc in self._out_edges[curr]:
                if desc == parent:
                    return True  # cycle: parent -> ... -> parent
                if self._node_to_ord[desc] <= p_ord and desc not in visited:
                    stack.append(desc)
                    visited.add(desc)

        # backward search: ? <- ? <- parent (bounded to c_ord <= positions)
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

def _create_nodes[T](_lists: Iterable[Iterable[T]]) -> tuple[list[list[Node]], dict[T, Node], list[T]]:
    """
    Maps items in `_lists` iterables to ints (Nodes) ranging from `0` to `n-1`
    where `n` is the number of unique items in all iterables in `_lists`.

    Returns the translated `_lists` and mappings to and from Nodes to the original items.

    All nodes in `lists` can be generated with `range(len(node_to_item))`
    """

    item_to_node: dict[T, Node] = {}
    node_to_item: list[T] = []

    lists: list[list[Node]] = []
    for _lst in _lists:
        lst: list[Node] = []
        for item in _lst:
            if item not in item_to_node:
                item_to_node[item] = len(node_to_item)
                node_to_item.append(item)
            lst.append(item_to_node[item])
        lists.append(lst)
    return lists, item_to_node, node_to_item


def _create_dag(lists: list[list[Node]], nodes: list[Node]):
    """
    Turn each list into a chain of edges (consecutive items), adding
    them highest-priority-list first. `DynamicTopoSort.add_edge` is what
    enforces favoring higher-priority orderings.

    To keep a list connected to itself, if one of its edges are rejected,
    the current parent is kept and an edge to the next child is attempted
    until a valid edge is found.

    Also computes, per node:
      - `priority[node]`: how important the *most* important list that
        mentions this node is. Priorities are encoded as negative list
        index (-1 = appeared in the highest priority list, more
        negative = only in lower priority lists), so that "bigger
        (closer to 0) is more important" and a plain max-heap / sort
        works without extra sign-flipping later.
    """

    UNSET = 0
    dts = DynamicTopoSort[Node](vertices=nodes)
    priority:  list[NodePriority] = [UNSET for _ in range(len(nodes))]

    for lst_priority, lst in enumerate(lists, start=1):  # start is arbitrary
        parent: Node | None = None
        for child in lst:
            if priority[child] == UNSET:
                priority[child] = -lst_priority

            if parent is None:  # first item in this list
                parent = child
                continue

            if child in dts._out_edges[parent]:  # edge already exists
                parent = child
                continue

            if not dts.add_edge(parent, child):  # would create a cycle -> skip
                continue

            parent = child

    return dts, priority


def _get_islands_priorities(dts: DynamicTopoSort[Node], priority: list[NodePriority]) -> list[IslandPriority]:
    """
    Splits the DAG into weakly-connected components ("islands" -- ignore
    edge direction, just look at what's connected to what) and gives
    every node in an island the priority of that island's *most*
    important member.

    Islands matter because two nodes with no path between them (in either
    direction) have no constraint telling us their relative order at
    all. Left purely to per-node priority, a low-priority node sitting
    in an otherwise-unconstrained corner of the graph could end up
    interleaved oddly with a high-priority chain it has nothing to do
    with. Tagging every node with its island's priority means an entire
    unrelated cluster of nodes is treated as a single unit of importance
    when the final sort is deciding what to schedule, rather
    than every node globally competing at the same time.

    Example:
        1. `ab`
        2. `xyz`
        3. `bc`
        Result: `abcxyz`
        
    Explanation:
        island from `ab` and `bc` (priority -1):    a -- b -- c
        island from `xyz`         (priority -2):    x -- y -- z

        Even though the node `c` has priority -3, its island priority
        of -1 (from `a` or `b`) causes `c` to appear before `xyz`.
    """
    UNSET = 0 # valid priorities are negative
    islands: list[IslandPriority] = [UNSET for _ in range(len(dts._ord_to_node))]

    for node in dts._ord_to_node: # starting order of traversal isn't important
        if islands[node] != UNSET: # already assigned to an island
            continue

        p_island: IslandPriority = min(priority)
        curr_island: set[Node] = {node}
        stack: list[Node] = [node]
        while stack:
            curr = stack.pop()
            p_island = max(priority[curr], p_island)
            for next_ in dts._in_edges[curr] + dts._out_edges[curr]: # ignore direction
                if next_ not in curr_island:
                    curr_island.add(next_)
                    stack.append(next_)

        for member in curr_island:
            islands[member] = p_island

    return islands

def _reversed_kahns(dts: DynamicTopoSort[Node], priority: list[NodePriority], islands: list[IslandPriority]) -> list[Node]:
    r"""
    Kahn's algorithm but you focus on nodes with no children,
    (and in this case) while always choosing the lowest priority node.
    Internally, nodes accumulate in reverse (since we walk backward from
    sinks), it is corrected (reversed again to undo that) before returning.

    Why reversed Kahn's?

    Regular Kahn's gives unintuitive results when a low priority node
    blocks a high priority node while there are other medium priority nodes available.
    
    Example:

        list[0] (highest): `a` b  c d e
        list[1]:           `1` d  2
        list[2] (lowest):  `3` b  4

        3   4            3   4           [3]  4                4    
         \ /              \ /              \ /                /     
      [a]=b=c=d=e   ->    (b)=c=d=e  ->    (b)=c=d=e   ->     b=c=d=e
             ∕ ∖               ∕ ∖                ∖                ∖ 
            1   2            [1]  2                2                2

        Result:  a`1`3bc   de24
        Expect:  a   3bc`1`de24

    `a`, `1`, and `3` all have an `in_degree` of 0, so regular Kahn's
    considers them "ready". After `a`, `b` has a dependency so it
    isn't ready. So, then its `1` or `3`. Since `1` has higher priority
    it is chosen and causing it to be emitted early. This is why
    it looks like `1` is dragged up to the front of the output.

    To fix this, we can go bottom-up. Instead of picking nodes as soon
    as they are available, we can always pick the one which is last.
    This favors cleaning up descendants as soon as possible.
    This means medium priority nodes like `1` are handled before
    continuing with higher priority nodes.

    Example (cont.):

        3   [4]                 3                3             3                3           [3]
         \ /                     \                \             \                \
        a=b=c=d=e   -> ... ->   a=b=c=[d]   ->   a=b=c   ->    a=b=[c]   ->    a=[b]   ->    a   ->   [a]
             ∕ ∖                      ∕
            1   2                    1              [1]
        
        (42ed1cb3a) -> a3bc1de24 which is expected

    Note:
    There are may be edge cases where even this setup doesn't
    give intuitive results. In most cases, this algorithm will suffice.
    """
    out_degree = [len(dts._out_edges[node]) for node in range(len(dts._ord_to_node))]

    res_rev: list[Node] = []
    minheap: list[tuple[IslandPriority, NodePriority, Node]] = []
    for node, deg in enumerate(out_degree):
        if deg == 0:
            heapq.heappush(minheap, (islands[node], priority[node], node))

    remaining_out_degree = out_degree[:]
    while minheap:
        _, _, curr = heapq.heappop(minheap)
        res_rev.append(curr)
        for parent in dts._in_edges[curr]:
            remaining_out_degree[parent] -= 1
            if remaining_out_degree[parent] == 0:
                heapq.heappush(minheap, (islands[parent], priority[parent], parent))

    return list(reversed(res_rev))

def merge_ordered_lists[T: Hashable](_lists: Iterable[Iterable[T]]) -> list[T]:
    """
    Priority is highest to lowest from first to last element in `lists`.
    (eg. lists[0] has the highest priority, lists[-1] has the lowest priority).

    Higher priority lists have their orderings favored over ALL
    conflicting orderings in lower priority lists.

    Phases:
    1.  (Preprocess items into ints)
    2.  Build DAG
    3.  Tag islands with priority
    4.  Topologically sort the DAG to get ordering
    5.  (Map ints back to original items)
    """

    lists, item_to_node, node_to_item = _create_nodes(_lists)
    if len(node_to_item) == 0:
        return []
    if len(node_to_item) == 1:
        return [node_to_item[0]]
    dts, priority = _create_dag(lists, list(range(len(node_to_item))))
    islands = _get_islands_priorities(dts, priority)
    ordering = _reversed_kahns(dts, priority, islands)

    return [node_to_item[node] for node in ordering]
