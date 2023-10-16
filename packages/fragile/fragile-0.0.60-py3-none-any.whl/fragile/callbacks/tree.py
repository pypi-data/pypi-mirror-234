"""Data structure to keep track of the graph that stores all the states visited by a Swarm."""
import copy
from typing import Any, Dict, Generator, List, Optional, Set, Tuple, Union

import judo
from judo.functions.random import random_state
from judo.judo_backend import Backend
import networkx as nx
import numpy
import numpy as np

from fragile.callbacks.data_tracking import TrackWalkersId
from fragile.core.state import SwarmState
from fragile.core.typing import InputDict, NamesData, NodeData, NodeDataGenerator, NodeId, Tensor


DEFAULT_ROOT_ID = ""


def to_node_id(x):
    return x
    if Backend.is_numpy():
        return str(x) if Backend.use_true_hash() else int(x)
    elif Backend.is_torch():
        return int(x)


class BaseTree:
    """Data structure in charge of storing the history of visited states of an algorithm run."""

    def __init__(self, root_id=DEFAULT_ROOT_ID):
        """
        Initialize a :class:`BaseTree`.

        Args:
            root_id: The node id of the root node.

        """
        self.root_id = root_id

    def __call__(self, *args, **kwargs) -> "BaseTree":
        """
        Return the current instance of :class:`BaseTree`.

        This is used to avoid defining a ``tree_callable `` as \
        ``lambda: tree_instance`` when initializing a :class:`Swarm`. If the \
        :class:`BaseTree` needs is passed to a remote process, you may need \
        to write custom serialization for it, or resort to creating an appropriate \
        ``tree_callable``.
        """
        return self

    def update(
        self,
        node_ids: List[NodeId],
        parent_ids: List[NodeId],
        n_iter: int = None,
        **kwargs,
    ) -> None:
        """
        Update the history of the tree adding the necessary data to recreate a \
        the trajectories sampled by the :class:`Swarm`.

        Args:
            node_ids: List of states hashes representing the node_ids of \
                the current states.
            parent_ids: List of states hashes representing the parent nodes of \
                        the current states.
            n_iter: Number of iteration of the algorithm when the data was sampled.
            kwargs: Keyword arguments representing different :class:`States` instances.

        Returns:
            None

        """
        pass

    def reset(self, *args, **kwargs) -> None:
        """
        Delete all the data currently stored and reset the internal state of \
        the tree.
        """
        pass

    def prune_tree(self, *args, **kwargs) -> None:
        """Remove branches of the tree."""
        pass


class NetworkxTree(BaseTree):
    """
    It is a tree data structure that stores the paths followed by the walkers \
    using a networkx DiGraph to keep track of the states relationships.
    """

    DEFAULT_ROOT_ID = DEFAULT_ROOT_ID
    DEFAULT_NEXT_PREFIX = "next_"
    DEFAULT_NODE_DATA = (
        "observs",
        "rewards",
        "oobs",
        "scores",
    )

    DEFAULT_EDGE_DATA = ("actions",)

    def __init__(
        self,
        names: NamesData = None,
        prune: bool = False,
        root_id: NodeId = DEFAULT_ROOT_ID,
        node_names: NamesData = DEFAULT_NODE_DATA,
        edge_names: NamesData = DEFAULT_EDGE_DATA,
        next_prefix: str = DEFAULT_NEXT_PREFIX,
    ):
        """
        Initialize a :class:`HistoryTree`.

        Args:
            names: Names of the data attributes that will be extracted stored \
                   in the graph data. The data generators will return the data
                   as a tuple of arrays, ordered according to ``names``.
            prune: If ``True`` the tree will be pruned after every iteration to \
                  remove the branches that have stopped its expansion process.
            root_id: The node id of the root node.
            next_prefix: Prefix used to refer to data extracted from the next \
                        node when parsing a data generator. For example: \
                        "next_observs" will reference the observation of the \
                        next node.
            node_names: Names of the data attributes of the :class:`States` that \
                       will be stored as node attributes in the internal graph.
            edge_names: Names of the data attributes of the :class:`States` that \
                       will be stored as edge attributes in the internal graph.
        """
        super(NetworkxTree, self).__init__(root_id=to_node_id(root_id))
        self.next_prefix = next_prefix
        self.names = names if names is not None else []
        self.data: nx.DiGraph = nx.DiGraph()
        self._node_count = 0
        self.leafs = set()
        self.last_added = set()
        # Node and edge names are parsed with no prefix
        self.prune = prune
        self.node_names = [
            name.lstrip(next_prefix)
            for name in self.names
            if name.lstrip(next_prefix) in node_names
        ]
        self.edge_names = [
            name.lstrip(next_prefix)
            for name in self.names
            if name.lstrip(next_prefix) in edge_names
        ]
        self._prune_sentinel = self.root_id

    def __len__(self) -> int:
        return self._node_count

    def __repr__(self) -> str:
        string = f"{self.__class__.__name__}: Nodes {self._node_count} Leafs {len(self.leafs)}"
        return string

    def reset(self, root_id: NodeId = None, state: Optional[SwarmState] = None) -> None:
        """
        Delete all the data currently stored and reset the internal state of the tree and \
        reset the root node with the provided data.
        """
        if state is not None:
            node_data = self._extract_data_from_states(index=0, only_node_data=True, state=state)
        else:
            node_data = {}
        self.reset_graph(root_id=to_node_id(root_id), node_data=node_data, epoch=-1)

    def update(
        self,
        node_ids: List[NodeId],
        parent_ids: List[NodeId],
        freeze_ids: List[NodeId],
        freeze_parents: List[NodeId],
        n_iter: int = None,
        **kwargs,
    ):
        """
        Update the history of the tree adding the necessary data to recreate a \
        the trajectories sampled by the :class:`Swarm`.

        Args:
            node_ids: List of states hashes representing the node_ids of \
                the current states.
            parent_ids: List of states hashes representing the parent nodes of \
                the current states.
            freeze_ids: List of the ids of walkers that are marked as inactive.
            freeze_parents: List of the parent ids of walkers that are marked as inactive.
            n_iter: Number of iteration of the algorithm when the data was sampled.
            kwargs: Keyword arguments representing different :class:`States` instances.

        Returns:
            None

        """
        leaf_ids, parent_ids = judo.to_numpy(node_ids), judo.to_numpy(parent_ids)
        freeze_ids = judo.to_numpy(freeze_ids)
        # Keep track of nodes that are active to make sure that they are not pruned

        self.last_added = set(freeze_ids) | set(freeze_parents)
        for i, (leaf, parent) in enumerate(zip(leaf_ids, parent_ids)):
            node_data, edge_data = self._extract_data_from_states(index=i, **kwargs)
            self.append_leaf(
                leaf_id=leaf,
                parent_id=parent,
                node_data=node_data,
                edge_data=edge_data,
                epoch=n_iter,
            )
        # if not hasher.uses_true_hash:
        #    id_states.update(ids=leaf_ids)

    def prune_tree(self, alive_leafs: Set[NodeId]):
        """
        Remove the branches that do not have a walker in their leaves.

        Args:
            alive_leafs: Contains the ids  of the leaf nodes that are being \
                         expanded by the walkers.

        Returns:
            None.

        """
        if self.prune:
            alive_leafs = set(alive_leafs)
            dead_leafs = self.leafs - alive_leafs
            self.prune_dead_branches(dead_leafs=dead_leafs, alive_leafs=alive_leafs)
        # self._update_prune_sentinel()

    def reset_graph(
        self,
        node_data: Dict[str, Any],
        root_id: NodeId = None,
        epoch: int = -1,
    ) -> None:
        """
        Delete all the data currently stored and reset the internal state of \
        the instance.

        Args:
            root_id: The node id of the root node.
            node_data: Dictionary containing the data that will be added to the \
                      new node created. The keys of the dictionary contain the \
                      names of the attributes and its values the corresponding \
                      value added to the node.
            epoch: Epoch of the :class:`Swarm` run when the current node was \
                    generated. Defaults to -1.

        Returns:
            None.

        """
        self.root_id = to_node_id(root_id) if root_id is not None else self.root_id
        self.data: nx.DiGraph = nx.DiGraph()
        self.data.add_node(self.root_id, epoch=epoch, **node_data)
        self._prune_sentinel = self.root_id
        self._node_count = 1
        self.leafs = {self.root_id}
        self.last_added = set()

    def append_leaf(
        self,
        leaf_id: NodeId,
        parent_id: NodeId,
        node_data: Dict[str, Any],
        edge_data: Dict[str, Any],
        epoch: int = -1,
    ) -> None:
        """
        Add a new state as a leaf node of the tree to keep track of the \
        trajectories of the swarm.

        Args:
            leaf_id: Node id that identifies the new node that will be added \
                    to the tree.
            parent_id: Node id that identifies the parent of the node that will \
                      be added to the tree.
            node_data: Dictionary containing the data that will be added to the \
                      new node created. The keys of the dictionary contain the \
                      names of the attributes and its values the corresponding \
                      value added to the node.
            edge_data: Dictionary containing the data that will be added to the \
                      new edge created from parent_id to leaf_id. The keys of \
                      the dictionary contain the names of the attributes and \
                      its values the corresponding value added to the edge.
            epoch: Epoch of the :class:`Swarm` run when the current node was \
                    generated. Defaults to -1.

        Returns:
            None.

        """
        # Don't add any leaf that creates a cycle in the graph
        if leaf_id not in self.data.nodes:
            if parent_id not in self.data.nodes:
                raise ValueError(
                    f"Parent {parent_id} of leaf {leaf_id} not in graph.",
                )
            import copy

            self.data.add_node(leaf_id, epoch=epoch, **copy.deepcopy(node_data))
            self.data.add_edge(parent_id, leaf_id, **copy.deepcopy(edge_data))
            # self.data.add_node(leaf_id, epoch=epoch, **node_data)
            # self.data.add_edge(parent_id, leaf_id, **edge_data)
            self.leafs.add(leaf_id)
            self._node_count += 1
            # If parent is no longer a leaf remove it from the list of leafs
            if parent_id in self.leafs:
                self.leafs.remove(parent_id)
        # TODO(guillemdb): Manage graphs that can have cycles
        # elif (
        #    parent_id in self.data.nodes
        #    and leaf_id in self.data.nodes
        #    and (parent_id, leaf_id) not in self.data.edges()
        # ):
        #    self.remove_cycle_and_store_closest_path(parent_id, leaf_id)

    def prune_dead_branches(self, dead_leafs: Set[NodeId], alive_leafs: Set[NodeId]) -> None:
        """
        Prune the orphan leaves that will no longer be used in order to save memory.

        Args:
            dead_leafs: Leaves of the branches that will be removed.
            alive_leafs: Leaves of the branches that will kept being expanded.

        Returns:
            None

        """
        alive_nodes = alive_leafs | self.last_added
        for leaf in set(dead_leafs):
            self.prune_branch(leaf, alive_nodes)
        return

    def prune_branch(self, leaf_id: NodeId, alive_nodes: Set[NodeId]) -> None:
        """
        Recursively prunes a branch that ends in an orphan leaf.

        Args:
            leaf_id: Value that identifies the leaf of the tree.
                If `leaf_id` is the hash of a walker state `from_hash`
                needs to be `True`. Otherwise it refers to a node id of
                the leaf node.
            alive_nodes: Nodes of the branches that can be still expanded.

        Returns:
            None

        """
        leaf_id = to_node_id(leaf_id)
        if (
            leaf_id == self._prune_sentinel
            or leaf_id in alive_nodes  # Remove only old nodes (inserted for 2+ epochs)
            or len(self.data.out_edges([leaf_id])) > 0  # Has children -> It's not a leaf
        ):
            return
        parent = self.get_parent(leaf_id)
        if parent in alive_nodes:
            return
        self.data.remove_node(leaf_id)
        self._node_count -= 1
        self.leafs.discard(leaf_id)
        if len(self.data.out_edges([parent])) == 0:  # Track if parent becomes a leaf
            self.leafs.add(parent)
        return self.prune_branch(parent, alive_nodes)

    def get_parent(self, node_id: NodeId) -> NodeId:
        """Get the node id of the parent of the target node."""
        try:
            return list(self.data.in_edges(to_node_id(node_id)))[0][0]
        except (KeyError, IndexError):
            raise KeyError("Node %s does not have a parent in the graph" % node_id)

    def get_branch(self, leaf_id: NodeId) -> List[NodeId]:
        """
        Return a list of the node ids of the path between root_node and leaf_id.

        Args:
            leaf_id: Node id of the end of the path that will be returned.

        Returns:
            List containing the nodes found between the root node and ``leaf_id``. \
            It starts with ``self.root_id`` and ends with ``leaf_id``.

        """
        leaf_id = to_node_id(leaf_id)
        nodes = [leaf_id]
        while leaf_id != self.root_id:
            node = self.get_parent(leaf_id)
            nodes.append(node)
            leaf_id = node
        return nodes[::-1]

    def get_path_node_ids(self, leaf_id: NodeId, root_id: NodeId = None) -> np.ndarray:
        """
        Get the data of the path between ``leaf_id`` and ``root_id``.

        Args:
            leaf_id: Id that identifies the leaf of the tree. \
                     If ``leaf_id`` is the hash of a walker state ``from_hash`` \
                     needs to be ``True``. Otherwise it refers to a node id of \
                     the leaf node.
            root_id: Node id of the root node of the tree.

        Returns:
            List of the node ids between ``root`` and ``leaf_id``.

        """
        leaf_id = to_node_id(leaf_id)
        root = root_id if root_id is not None else self.root_id
        nodes = nx.shortest_path(self.data, root, leaf_id)
        return numpy.array(nodes, dtype=judo.dtype.hash_type)

    def get_leaf_nodes(self) -> Tuple[NodeId]:
        """Return a list containing all the node ids of the leaves of the tree."""
        return tuple(node for node in self.data.nodes if len(self.data.out_edges([node])) == 0)

    def compose(self, other: Union["NetworkxTree", nx.Graph]) -> None:
        """
        Compose the graph of another :class:`BaseNetworkxTree` with the graph of \
        the current instance.

        Composition is the simple union of the node sets and edge sets.
        The node sets of ``self.data`` and ``other.data`` do not need to be \
        disjoint.

        The data in ``other`` takes precedence over the data in the current instance.

        Args:
            other: Instance of :class:`BaseNetworkxTree` that will be composed \
                  with the current instance.

        Returns:
            None

        """
        graph = other.data if isinstance(other, NetworkxTree) else other
        self.data = nx.compose(copy.deepcopy(self.data), copy.deepcopy(graph))

    def _update_prune_sentinel(self):
        children_edges = self.data.out_edges([self._prune_sentinel])
        while len(children_edges) == 1:
            self._prune_sentinel = tuple(children_edges)[0][1]  # Update to child node
            children_edges = self.data.out_edges([self._prune_sentinel])

    def _extract_data_from_states(
        self,
        index,
        state: SwarmState,
        only_node_data: bool = False,
    ):
        def get_name_from_states(name):
            try:
                value = state[name]
                is_scalar = (
                    not judo.is_tensor(value) and not isinstance(value, list) and index == 0
                )
                data = value if is_scalar else value[index]
            except Exception as e:
                raise ValueError(
                    "Unable to get %s from states with index %s state: %s" % (name, index, state),
                ) from e
            return copy.deepcopy(data)

        node_data = {name: get_name_from_states(name) for name in self.node_names}
        if only_node_data:
            return node_data
        edge_data = {name: get_name_from_states(name) for name in self.edge_names}
        return node_data, edge_data


class DataTree(NetworkxTree):
    """
    Tree data structure that keeps track of the visited states.

    It allows to save the :class:`Swarm` data after every iteration and methods to \
    recover the sampled data after the algorithm run.

    The data that will be stored in the graph it's defined in the ``names`` parameter.
    For example:

     - If names is ``["observs", "actions"]``, the observations of every visited \
       state will be stored as node attributes, and actions will be stored as edge attributes.

     - If names if ``["observs", "actions", "next_observs"]`` the same data will be stored,
       but when the data generator methods are called the observation corresponding \
       to the next state will also be returned.

     The attribute ``names`` also defines the order of the data returned by the generator.

     As long as the data is stored in the graph (passing a valid ``names`` list at \
     initialization, the order of the data can be redefined passing the ``names`` \
     parameter to the generator method.

     For example, if the ``names`` passed at initialization is ``["states", "rewards"]``, \
     you can call the generator methods with ``names=["rewards", "states", "next_states"]`` \
     and the returned data will be a tuple containing (rewards, states, next_states).

    """

    def __init__(
        self,
        names: NamesData = None,
        prune: bool = False,
        root_id: NodeId = DEFAULT_ROOT_ID,
        node_names: NamesData = NetworkxTree.DEFAULT_NODE_DATA,
        edge_names: NamesData = NetworkxTree.DEFAULT_EDGE_DATA,
        next_prefix: str = NetworkxTree.DEFAULT_NEXT_PREFIX,
    ):
        """
        Initialize a :class:`HistoryTree`.

        Args:
            names: Names of the data attributes that will be extracted stored \
                   in the graph data. The data generators will return the data
                   as a tuple of arrays, ordered according to ``names``.
            prune: If ``True`` the tree will be pruned after every iteration to \
                  remove the branches that have stopped its expansion process.
            root_id: The node id of the root node.
            next_prefix: Prefix used to refer to data extracted from the next \
                        node when parsing a data generator. For example: \
                        "next_observs" will reference the observation of the \
                        next node.
            node_names: Names of the data attributes of the :class:`States` that \
                       will be stored as node attributes in the internal graph.
            edge_names: Names of the data attributes of the :class:`States` that \
                       will be stored as edge attributes in the internal graph.
        """
        super(DataTree, self).__init__(
            names=names,
            prune=prune,
            root_id=root_id,
            next_prefix=next_prefix,
            node_names=node_names,
            edge_names=edge_names,
        )

    def _one_node_tuples(self, node, next_node, return_children) -> NodeData:
        node_data, edge_data = self.data.nodes[node], self.data.edges[(node, next_node)]
        if return_children:
            return node_data, edge_data, self.data.nodes[next_node]
        else:
            return node_data, edge_data

    def _extract_one_node_data(self, data: NodeData, names: NamesData) -> Tuple:
        """
        Transform the one tuple of dictionaries returned by the data generators \
        into a tuple of data values where each value corresponds to a name in names.
        """

        def get_item(data, name):
            node_data, edge_data, *next_node_data = data
            if name.startswith(self.next_prefix):
                true_name = name.replace(self.next_prefix, "")
                return next_node_data[0][true_name]
            elif name in node_data:
                return node_data[name]
            elif name in edge_data:
                return edge_data[name]
            raise KeyError("%s not found in data: %s" % (name, data))

        return tuple(get_item(data, name) for name in names)

    def _process_batch(self, batch_data: List[tuple]) -> Tuple[Tensor, ...]:
        """
        Preprocess the list of tuples representing a batched group of elements \
        and return a tuple of arrays representing the batched values for every \
        data attribute.
        """
        unpacked = zip(*batch_data)
        return tuple(judo.as_tensor(val) for val in unpacked)

    def _generate_batches(
        self,
        generator: NodeDataGenerator,
        names: NamesData,
        batch_size: int = None,
    ) -> Generator[Tuple, None, None]:
        """Return batches of processed data represented as tuples of arrays."""
        returned = []
        batch_counter = 0
        for i, data in enumerate(generator):
            batch_counter += 1
            extracted_data = self._extract_one_node_data(data, names)
            if batch_size is None:  # Do not batch data
                yield extracted_data
                continue
            returned.append(extracted_data)
            if batch_counter == batch_size:
                batch_counter = 0
                yield self._process_batch(returned)
                returned = []
            elif batch_size > 0 and i == len(self) - batch_size:
                break
        # If a batch size less than 1 is provided return all the data as a single batch
        if batch_size is not None and batch_size <= 1:
            yield self._process_batch(returned)

    def _validate_names(self, names):
        if names is None:
            return self.names
        for name in names:
            name = (
                name[len(self.next_prefix) :]  # noqa: E203
                if name.startswith(self.next_prefix)
                else name
            )
            if name not in self.names:
                raise KeyError(
                    "Data corresponding to name %s "
                    "not present in self.names: %s for element %s"
                    % (name, self.names, name[len(self.next_prefix) :]),  # noqa: E203
                )
        return names

    def path_data_generator(
        self,
        node_ids: Union[Tuple[NodeId], Set[NodeId], List[NodeId]],
        return_children: bool = False,
    ) -> NodeDataGenerator:
        """
        Return a generator that returns the data corresponding to a path.

        Each value yielded corresponds to one element of the path. The edge data \
        will be assigned to the parent node of the  edge. This means the edge \
        data contains the data associated with the transition to a child.

        The data corresponding to the last node of the path will not be returned.

        Args:
            node_ids: Node ids of a path ordered. The first node of the path \
                     corresponds to the first element of ``node_ids``.
            return_children: If ``True`` the data corresponding to the child of \
                            each node in the path will also be returned.

        Yields:
            tuple of dictionaries containing the data of each node and edge of \
            the path, following the order of ``node_ids``.

            If ``return_children`` is ``False`` it will yield (node_data, \
            edge_data).
            If ``return_children`` is ``True`` it will yield (node_data, \
            edge_data, next_node_data).

        """
        for (i, node) in enumerate(node_ids[:-1]):
            next_node = node_ids[i + 1]
            yield self._one_node_tuples(node, next_node, return_children)

    def random_nodes_generator(self, return_children: bool = False) -> NodeDataGenerator:
        """
        Return a generator that yields the data of all the nodes sampling them at random.

        Each value yielded corresponds to the data associated with one node and the \
        edge connecting to one of its children. The edge data will be assigned \
        to the parent node of the edge. This means the edge data of each node \
        contains the data associated with the transition to a child.

        Args:
            return_children: If ``True`` the data corresponding to the child of \
                            each node in the path will also be returned.

        Yields:
            tuple of dictionaries containing the data for each node and edge \
            sampled at random.

            If ``return_children`` is ``False`` it will yield (node_data, \
            edge_data).
            If ``return_children`` is ``True`` it will yield (node_data, \
            edge_data, next_node_data).

        """
        with Backend.use_backend("numpy"):
            permutation = random_state.permutation(list(self.data.nodes))
        for next_node in permutation:
            if next_node == self.root_id:
                continue
            node = self.get_parent(next_node)
            yield self._one_node_tuples(node, next_node, return_children)

    def iterate_path_data(
        self,
        node_ids: Union[Tuple[NodeId], List[NodeId]],
        batch_size: int = None,
        names: NamesData = None,
    ) -> NodeDataGenerator:
        """
        Return a generator that yields the data of the nodes contained in the provided path.

        Args:
            node_ids: Ids of the nodes of the path that will be sampled. The \
                     nodes must be provided in order, starting with the first \
                     node of the path.
            batch_size: If it is not None, the generator will return batches of \
                        data with the target batch size. If Batch size is less than 1 \
                        it will return a single batch containing all the data.
            names: Names of the data attributes that will be yielded by the generator.

        Returns:
            Generator providing the data corresponding to a path in the internal tree.

        """
        names = self._validate_names(names)
        return_children = any(name.startswith(self.next_prefix) for name in names)
        path_generator = self.path_data_generator(
            node_ids=judo.to_numpy(node_ids),
            return_children=return_children,
        )
        return self._generate_batches(path_generator, names=names, batch_size=batch_size)

    def iterate_nodes_at_random(
        self,
        batch_size: int = None,
        names: NamesData = None,
    ) -> NodeDataGenerator:
        """
        Return a generator that yields the data of the nodes contained in the provided path.

        Args:
            batch_size: If it is not None, the generator will return batches of \
                        data with the target batch size. If Batch size is less than 1 \
                        it will return a single batch containing all the data.
            names: Names of the data attributes that will be yielded by the generator.

        Returns:
            Generator providing the data corresponding to all the nodes of \
            the tree sampled at random.

        """
        names = self._validate_names(names)
        return_children = any(name.startswith(self.next_prefix) for name in names)
        node_generator = self.random_nodes_generator(return_children=return_children)
        return self._generate_batches(node_generator, names=names, batch_size=batch_size)

    def iterate_branch(
        self,
        node_id: NodeId,
        batch_size: int = None,
        names: NamesData = None,
    ) -> NodeDataGenerator:
        """
        Return a generator that yields the data of the nodes contained in the provided path.

        Args:
            node_id: Ids of the last node of the branch that will be sampled. \
                    The first node will be the root node of the tree, and the last \
                    one will be the one with the provided ``node_id``.
            batch_size: If it is not None, the generator will return batches of \
                        data with the target batch size. If Batch size is less than 1 \
                        it will return a single batch containing all the data.
            names: Names of the data attributes that will be yielded by the generator.

        Returns:
            Generator providing the data corresponding to a branch of the internal tree.

        """
        node_id = to_node_id(node_id)
        branch_path = self.get_path_node_ids(leaf_id=node_id)
        return self.iterate_path_data(branch_path, batch_size=batch_size, names=names)


class HistoryTree(TrackWalkersId):
    """
    Tree data structure that keeps track of the visited states.

    It allows to save the :class:`Swarm` data after every iteration and methods to \
    recover the sampled data after the algorithm run.

    The data that will be stored in the graph it's defined in the ``names`` parameter.
    For example:

     - If names is ``["observs", "actions"]``, the observations of every visited \
       state will be stored as node attributes, and actions will be stored as edge attributes.

     - If names if ``["observs", "actions", "next_observs"]`` the same data will be stored,
       but when the data generator methods are called the observation corresponding \
       to the next state will also be returned.

     The attribute ``names`` also defines the order of the data returned by the generator.

     As long as the data is stored in the graph (passing a valid ``names`` list at \
     initialization, the order of the data can be redefined passing the ``names`` \
     parameter to the generator method.

     For example, if the ``names`` passed at initialization is ``["states", "rewards"]``, \
     you can call the generator methods with ``names=["rewards", "states", "next_states"]`` \
     and the returned data will be a tuple containing (rewards, states, next_states).

    """

    name = "tree"

    def __init__(
        self,
        names: NamesData = None,
        prune: bool = False,
        root_id: NodeId = DEFAULT_ROOT_ID,
        node_names: NamesData = None,
        edge_names: NamesData = ("actions", "dt"),
        next_prefix: str = NetworkxTree.DEFAULT_NEXT_PREFIX,
        **kwargs,
    ):
        self.names = names
        self.prune = prune
        self.root_id = root_id
        self.node_names = node_names
        self.edge_names = edge_names
        self.next_prefix = next_prefix
        self._tree = None
        super(HistoryTree, self).__init__(**kwargs)

    @property
    def graph(self) -> nx.Graph:
        return self._tree.data

    @property
    def data_tree(self):
        return self._tree

    @property
    def inputs(self) -> InputDict:
        inputs = super(HistoryTree, self).inputs
        if self.names is None:
            return inputs
        clones = {n: {"clone": True} for n in self.names}
        return {**inputs, **clones}

    def __getattr__(self, item):
        try:
            getattr(self._tree, item)
        except AttributeError:
            return super(HistoryTree, self).__getattribute__(item)

    def __repr__(self):
        return (
            f"<strong>{self.__class__.__name__}</strong>: "
            f"Nodes {len(self._tree)} Leafs {len(self._tree.leafs)}"
        )

    def to_html(self):
        tree = self._tree
        string = (
            f"<strong>{self.__class__.__name__}</strong>: "
            f"Nodes {len(tree)} Leafs {len(tree.leafs)}"
        )
        return string

    def setup(self, swarm):
        super(HistoryTree, self).setup(swarm)
        self.names = self.names if self.names is not None else self.swarm.state.names
        self._tree = DataTree(
            names=self.names,
            prune=self.prune,
            root_id=self.root_id,
            node_names=self.node_names if self.node_names is not None else self.swarm.state.names,
            edge_names=self.edge_names,
            next_prefix=self.next_prefix,
        )

    def reset(self, root_id=None, state=None, **kwargs):
        if root_id is None:
            root_id = 0
        self._tree.reset(root_id=root_id, state=state)
        if root_id is not None:
            parent_ids = judo.copy(self.get("parent_ids"))
            parent_ids[:] = root_id
            self.update(parent_ids=parent_ids)

    def update_tree(self):
        id_walkers = self.get("id_walkers", inactives=True)
        parent_ids = self.get("parent_ids", inactives=True)
        self._tree.update(
            parent_ids=parent_ids,
            node_ids=id_walkers,
            n_iter=self.swarm.epoch,
            freeze_ids=id_walkers,
            freeze_parents=parent_ids,
            state=self.swarm.state,
        )

    def before_walkers(self):
        self.update_tree()

    def after_evolve(self):
        self._tree.prune_tree(alive_leafs=self.get("id_walkers"))

    def after_reset(self):
        if hasattr(self.swarm, "root"):
            best_id = self.swarm.root.id_walker
            state = self.swarm.root.data
        else:
            best_id = self.get("id_walkers")[0]
            state = self.swarm.state.export_walker(index=0, names=self._tree.node_names)
        self.reset(root_id=best_id, state=state)

    def iterate_root_path(
        self,
        batch_size: int = None,
        names: NamesData = None,
    ) -> NodeDataGenerator:
        """
        Return a generator that yields the data of the nodes contained in the provided path.

        Args:
            batch_size: If it is not None, the generator will return batches of \
                        data with the target batch size. If Batch size is less than 1 \
                        it will return a single batch containing all the data.
            names: Names of the data attributes that will be yielded by the generator.

        Returns:
            Generator providing the data corresponding to a branch of the internal tree.

        """

        return self._tree.iterate_branch(
            node_id=self.swarm.root.id_walker,
            batch_size=batch_size,
            names=names,
        )

    def get_root_graph(self):
        root_path_nodes = self.data_tree.get_path_node_ids(self.swarm.root.id_walkers)
        return copy.deepcopy(self.graph.subgraph(root_path_nodes))
