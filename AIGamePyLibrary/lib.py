import json
import math
import numbers
import random
from collections import deque
from typing import Literal

from .data import (
    outputs,
    ports,
    NODE_SIZES,
    DEFAULT_NODE_SIZE,
    DEFAULT_NODE_COLOR,
    SERIALIZE_SIZE_DELTA_NODES,
    SERIALIZE_COLOR_NODES,
    DROPDOWN_OPTIONS,
)

from .utils import Position2, Position3, generateId

data = {"serializableNodes": [], "serializableConnections": []}


def isNumber(value):
    return isinstance(value, numbers.Number) and not isinstance(value, bool)


class Node:
    def __init__(self, data: dict, outputIndex=1):
        self.data = data
        self.outputIndex = outputIndex
        self.type = outputs[data["id"]]
        self.inputPorts = {}
        self.outputPorts = {}
        for port in data["serializablePorts"]:
            if port["polarity"] == 0:
                self.inputPorts[port["id"]] = port
            else:
                self.outputPorts[port["id"]] = port

    @property
    def x(self):
        if self.type == "Vector3":
            from .nodes import Vector3Split

            return Vector3Split(self).x
        raise AttributeError("'Node' object has no attribute 'x'")

    @property
    def y(self):
        if self.type == "Vector3":
            from .nodes import Vector3Split

            return Vector3Split(self).y
        raise AttributeError("'Node' object has no attribute 'y'")

    @property
    def z(self):
        if self.type == "Vector3":
            from .nodes import Vector3Split

            return Vector3Split(self).z
        raise AttributeError("'Node' object has no attribute 'z'")

    def __repr__(self):
        return f"Node(type='{self.type}', id='{self.data['sID']}')"

    def __hash__(self):
        return int(self.data["sID"].replace("-", ""), 16) + self.outputIndex

    def __add__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == float and other.type == float:
                from .nodes import AddFloats

                return AddFloats(self, other)
            if self.type == "Vector3" and other.type == "Vector3":
                from .nodes import AddVector3

                return AddVector3(self, other)

        elif isNumber(other) and self.type == float:
            from .nodes import AddFloats

            return AddFloats(self, other)

        return NotImplemented

    def __radd__(self, other) -> "Node":
        return self.__add__(other)

    def __sub__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == float and other.type == float:
                from .nodes import SubtractFloats

                return SubtractFloats(self, other)
            if self.type == "Vector3" and other.type == "Vector3":
                from .nodes import SubtractVector3

                return SubtractVector3(self, other)

        elif isNumber(other) and self.type == float:
            from .nodes import SubtractFloats

            return SubtractFloats(self, other)

        return NotImplemented

    def __rsub__(self, other) -> "Node":
        if isNumber(other) and self.type == float:
            from .nodes import SubtractFloats

            return SubtractFloats(other, self)

        return NotImplemented

    def __mul__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == float and other.type == float:
                from .nodes import MultiplyFloats

                return MultiplyFloats(self, other)
            if self.type == "Vector3" and other.type == float:
                from .nodes import ScaleVector3

                return ScaleVector3(self, other)
            if self.type == float and other.type == "Vector3":
                from .nodes import ScaleVector3

                return ScaleVector3(other, self)

        elif isNumber(other):
            if self.type == float:
                from .nodes import MultiplyFloats

                return MultiplyFloats(self, other)
            if self.type == "Vector3":
                from .nodes import ScaleVector3

                return ScaleVector3(self, other)

        return NotImplemented

    def __rmul__(self, other) -> "Node":
        return self.__mul__(other)

    def __truediv__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == float and other.type == float:
                from .nodes import DivideFloats

                return DivideFloats(self, other)

        elif isNumber(other) and self.type == float:
            from .nodes import DivideFloats

            return DivideFloats(self, other)

        return NotImplemented

    def __rtruediv__(self, other) -> "Node":
        if isNumber(other) and self.type == float:
            from .nodes import DivideFloats

            return DivideFloats(other, self)

        return NotImplemented

    def __floordiv__(self, other) -> "Node":
        result = self.__truediv__(other)
        if result is NotImplemented:
            return result
        from .nodes import Operation

        return Operation(result, "floor")

    def __rfloordiv__(self, other) -> "Node":
        if isNumber(other) and self.type == float:
            from .nodes import DivideFloats

            div_result = DivideFloats(other, self)
            from .nodes import Operation

            return Operation(div_result, "floor")

        return NotImplemented

    def __mod__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == float and other.type == float:
                from .nodes import Modulo

                return Modulo(self, other)

        elif isNumber(other) and self.type == float:
            from .nodes import Modulo

            return Modulo(self, other)

        return NotImplemented

    def __rmod__(self, other) -> "Node":
        if isNumber(other) and self.type == float:
            from .nodes import Modulo

            return Modulo(other, self)

        return NotImplemented

    def __pow__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type in (float, "Any") and other.type in (float, "Any"):
                from .nodes import Power

                return Power(self, other)

        elif isNumber(other) and self.type in (float, "Any"):
            if other == 2 and self.type == float:
                from .nodes import MultiplyFloats

                return MultiplyFloats(self, self)

            from .nodes import Power

            return Power(self, other)

        return NotImplemented

    def __rpow__(self, other) -> "Node":
        if isNumber(other) and self.type in (float, "Any"):
            from .nodes import Power

            return Power(other, self)

        return NotImplemented

    def __neg__(self) -> "Node":
        if self.type == float:
            from .nodes import MultiplyFloats

            return MultiplyFloats(self, -1)

        return NotImplemented

    def __pos__(self) -> "Node":
        return self

    def __abs__(self) -> "Node":
        if self.type == float:
            from .nodes import Operation

            return Operation(self, "abs")

        return NotImplemented

    def __invert__(self) -> "Node":
        if self.type == bool:
            from .nodes import Not

            return Not(self)

        return NotImplemented

    def __eq__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == float and other.type == float:
                from .nodes import CompareFloats

                return CompareFloats(self, other)
            if self.type == bool and other.type == bool:
                from .nodes import CompareBool

                return CompareBool(self, other)

        elif isNumber(other) and self.type == float:
            from .nodes import CompareFloats

            return CompareFloats(self, other)

        elif isinstance(other, bool) and self.type == bool:
            from .nodes import CompareBool

            return CompareBool(self, other)

        return NotImplemented

    def __ne__(self, other) -> "Node":
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        from .nodes import Not

        return Not(result)

    def __lt__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == float and other.type == float:
                from .nodes import CompareFloats

                return CompareFloats(self, other, "<")

        elif isNumber(other) and self.type == float:
            from .nodes import CompareFloats

            return CompareFloats(self, other, "<")

        return NotImplemented

    def __le__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == float and other.type == float:
                from .nodes import CompareFloats

                return CompareFloats(self, other, "<=")

        elif isNumber(other) and self.type == float:
            from .nodes import CompareFloats

            return CompareFloats(self, other, "<=")

        return NotImplemented

    def __gt__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == float and other.type == float:
                from .nodes import CompareFloats

                return CompareFloats(self, other, ">")

        elif isNumber(other) and self.type == float:
            from .nodes import CompareFloats

            return CompareFloats(self, other, ">")

        return NotImplemented

    def __ge__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == float and other.type == float:
                from .nodes import CompareFloats

                return CompareFloats(self, other, ">=")

        elif isNumber(other) and self.type == float:
            from .nodes import CompareFloats

            return CompareFloats(self, other, ">=")

        return NotImplemented

    def __and__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == bool and other.type == bool:
                from .nodes import CompareBool

                return CompareBool(self, other, "and")

        elif isinstance(other, bool) and self.type == bool:
            from .nodes import CompareBool

            return CompareBool(self, other, "and")

        return NotImplemented

    def __rand__(self, other) -> "Node":
        if isinstance(other, bool) and self.type == bool:
            from .nodes import CompareBool

            return CompareBool(other, self, "and")

        return NotImplemented

    def __or__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == bool and other.type == bool:
                from .nodes import CompareBool

                return CompareBool(self, other, "or")

        elif isinstance(other, bool) and self.type == bool:
            from .nodes import CompareBool

            return CompareBool(self, other, "or")

        return NotImplemented

    def __ror__(self, other) -> "Node":
        if isinstance(other, bool) and self.type == bool:
            from .nodes import CompareBool

            return CompareBool(other, self, "or")

        return NotImplemented

    def __xor__(self, other) -> "Node":
        if isinstance(other, Node):
            from .nodes import CompareBool

            if self.type == bool and other.type == bool:
                return CompareBool(self, other, "xor")

        elif isinstance(other, bool) and self.type == bool:
            from .nodes import CompareBool

            return CompareBool(self, other, "xor")

        return NotImplemented

    def __rxor__(self, other) -> "Node":
        if isinstance(other, bool) and self.type == bool:
            from .nodes import CompareBool

            return CompareBool(other, self, "xor")

        return NotImplemented

    def __matmul__(self, other) -> "Node":
        if isinstance(other, Node):
            if self.type == "Vector3" and other.type == "Vector3":
                from .nodes import DotProduct

                return DotProduct(self, other)

        return NotImplemented

    def __rmatmul__(self, other) -> "Node":
        return self.__matmul__(other)


def _quantize_layout_coord(v, decimals=None):
    if v is None:
        return 0
    return v


def _rect_transform(local_pos, size, node_id, anchor_x=0, anchor_y=1):
    """Build serializableRectTransform. New minimal format: only position+anchoredPosition for layout.
    Region nodes include sizeDelta/anchors (SerializeSizeDelta per NodeTypeDataSO)."""
    x = _quantize_layout_coord(local_pos.get("x", 0))
    y = _quantize_layout_coord(local_pos.get("y", 0))
    z = _quantize_layout_coord(local_pos.get("z", 0))
    w, h = _quantize_layout_coord(size[0]), _quantize_layout_coord(size[1])
    rect = {
        "position": {"x": 0, "y": 0, "z": 0},
        "anchoredPosition": {"x": x, "y": y},
    }
    if node_id in SERIALIZE_SIZE_DELTA_NODES:
        rect["localPosition"] = {"x": x, "y": y, "z": z}
        rect["anchorMin"] = {"x": anchor_x, "y": anchor_y}
        rect["anchorMax"] = {"x": anchor_x, "y": anchor_y}
        rect["sizeDelta"] = {"x": w, "y": h}
    return rect


def _get_layout_position(transform):
    """Get (x, y) from transform. Prefers anchoredPosition, falls back to localPosition for old JSON."""
    ap = transform.get("anchoredPosition")
    if ap is not None:
        return (ap.get("x", 0), ap.get("y", 0))
    lp = transform.get("localPosition", {})
    return (lp.get("x", 0), lp.get("y", 0))


def _is_at_origin(transform):
    """True if node is at default (0,0) and should receive auto layout."""
    x, y = _get_layout_position(transform)
    return x == 0 and y == 0


def _set_layout_position(transform, x, y):
    """Set layout position. Uses anchoredPosition (Unity's preferred field for placement)."""
    x = _quantize_layout_coord(x)
    y = _quantize_layout_coord(y)
    transform["anchoredPosition"] = Position2(x, y)
    transform["localPosition"] = Position3(x, y, 0)
    transform["position"] = {"x": 0, "y": 0, "z": 0}


# Spatial compaction: refuse passthrough collapse when it would create a long
# wire through dense local structure; prefer collapsing isolated outliers.
_SPATIAL_LONG_SPAN = 500.0
_SPATIAL_BRIDGE_BAND = 120.0
_SPATIAL_CLOSE = 250.0
_LAYOUT_ANCHOR_NODES = frozenset({"Region", "CreateFunction"})


def _node_layout_xy(node) -> tuple[float, float] | None:
    transform = node.get("serializableRectTransform")
    if not transform:
        return None
    x, y = _get_layout_position(transform)
    return (float(x), float(y))


def _collect_node_positions() -> dict[str, tuple[float, float]]:
    positions: dict[str, tuple[float, float]] = {}
    for node in data["serializableNodes"]:
        xy = _node_layout_xy(node)
        if xy is not None:
            positions[node["sID"]] = xy
    return positions


def _layout_dist(a: tuple[float, float], b: tuple[float, float]) -> float:
    return math.hypot(a[0] - b[0], a[1] - b[1])


def _spatial_isolation(sid: str, positions: dict[str, tuple[float, float]], k: int = 3) -> float:
    if sid not in positions:
        return 0.0
    px = positions[sid]
    dists = sorted(_layout_dist(px, positions[o]) for o in positions if o != sid)
    if not dists:
        return 0.0
    take = dists[: min(k, len(dists))]
    return sum(take) / len(take)


def _isolation_quartile_threshold(positions: dict[str, tuple[float, float]]) -> float:
    if len(positions) < 4:
        return 0.0
    isolations = sorted(_spatial_isolation(sid, positions) for sid in positions)
    idx = int(0.75 * (len(isolations) - 1))
    return isolations[idx]


def _point_to_segment_dist(
    p: tuple[float, float],
    a: tuple[float, float],
    b: tuple[float, float],
) -> float:
    ax, ay = a
    bx, by = b
    px, py = p
    dx, dy = bx - ax, by - ay
    if dx == 0 and dy == 0:
        return _layout_dist(p, a)
    t = ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)
    t = max(0.0, min(1.0, t))
    proj = (ax + t * dx, ay + t * dy)
    return _layout_dist(p, proj)


def _is_spatial_bridge(
    node_xy: tuple[float, float],
    src_xy: tuple[float, float],
    dst_xy: tuple[float, float],
) -> bool:
    span = _layout_dist(src_xy, dst_xy)
    if span < _SPATIAL_LONG_SPAN:
        return False
    return _point_to_segment_dist(node_xy, src_xy, dst_xy) <= _SPATIAL_BRIDGE_BAND


def _spatial_collapse_allowed(
    *,
    spatial_structure: bool,
    candidate_sid: str,
    src_sid: str,
    dst_sids: set[str] | list[str],
    positions: dict[str, tuple[float, float]] | None = None,
    isolation_q75: float | None = None,
) -> bool:
    """True when a passthrough node may be collapsed without ruining local layout."""
    if not spatial_structure:
        return True
    if positions is None:
        positions = _collect_node_positions()
    if isolation_q75 is None:
        isolation_q75 = _isolation_quartile_threshold(positions)

    src_xy = positions.get(src_sid)
    cand_xy = positions.get(candidate_sid)
    if src_xy is None or cand_xy is None:
        return True

    dst_list = list(dst_sids)
    if not dst_list:
        return True

    max_span = 0.0
    for dst_sid in dst_list:
        dst_xy = positions.get(dst_sid)
        if dst_xy is None:
            continue
        span = _layout_dist(src_xy, dst_xy)
        if span < _SPATIAL_CLOSE:
            return True
        max_span = max(max_span, span)

    if max_span < _SPATIAL_CLOSE:
        return True

    if _spatial_isolation(candidate_sid, positions) >= isolation_q75:
        return True

    for dst_sid in dst_list:
        dst_xy = positions.get(dst_sid)
        if dst_xy is None:
            continue
        if _is_spatial_bridge(cand_xy, src_xy, dst_xy):
            return False

    return True


def _tighten_layout_to_neighbors(*, iterations: int = 2, blend: float = 0.35, max_step: float = 400.0) -> None:
    """Pull nodes toward wired neighbors to shrink leftover long wires after inlines."""
    for _ in range(iterations):
        positions = _collect_node_positions()
        if len(positions) < 2:
            return

        _, node_of, edges = _producer_consumer_edges()
        neighbors: dict[str, set[str]] = {}
        for prod_port, cons_port in edges:
            src = node_of.get(prod_port)
            dst = node_of.get(cons_port)
            if src and dst and src != dst:
                neighbors.setdefault(src, set()).add(dst)
                neighbors.setdefault(dst, set()).add(src)

        new_positions = dict(positions)
        for node in data["serializableNodes"]:
            sid = node["sID"]
            if node.get("id") in _LAYOUT_ANCHOR_NODES or sid not in positions:
                continue
            nbrs = neighbors.get(sid)
            if not nbrs:
                continue
            nbr_pos = [positions[n] for n in nbrs if n in positions]
            if not nbr_pos:
                continue
            cx = sum(p[0] for p in nbr_pos) / len(nbr_pos)
            cy = sum(p[1] for p in nbr_pos) / len(nbr_pos)
            ox, oy = positions[sid]
            nx = ox + blend * (cx - ox)
            ny = oy + blend * (cy - oy)
            dx, dy = nx - ox, ny - oy
            step = math.hypot(dx, dy)
            if step > max_step:
                scale = max_step / step
                nx = ox + dx * scale
                ny = oy + dy * scale
            new_positions[sid] = (nx, ny)

        for node in data["serializableNodes"]:
            sid = node["sID"]
            if sid not in new_positions:
                continue
            transform = node.get("serializableRectTransform")
            if not transform:
                continue
            x, y = new_positions[sid]
            _set_layout_position(transform, x, y)


def _normalize_modifier(node_name: str, node_value):
    """
    Normalize `modifier` for nodes whose modifier is a dropdown selection.

    - Accepts either an int index or a string label.
    - Validates against `DROPDOWN_OPTIONS` when available.
    - Converts to a stringified index, because Unity nodes store dropdown
      selections in the `modifier` field as a string.
    """
    options = DROPDOWN_OPTIONS.get(node_name)
    if not options:
        return node_value

    if isinstance(node_value, bool):
        # Avoid treating bool as int.
        return node_value

    if isinstance(node_value, int):
        if 0 <= node_value < len(options):
            return str(node_value)
        raise ValueError(
            f"{node_name} dropdown index out of range: {node_value}. "
            f"Valid range: 0..{len(options) - 1} ({', '.join(options)})"
        )

    if isinstance(node_value, str):
        value_str = node_value.strip()
        if value_str.isdigit():
            idx = int(value_str)
            if 0 <= idx < len(options):
                return str(idx)
            raise ValueError(
                f"{node_name} dropdown index out of range: {value_str}. "
                f"Valid range: 0..{len(options) - 1} ({', '.join(options)})"
            )

        lowered = value_str.casefold()
        for i, opt in enumerate(options):
            if opt.casefold() == lowered:
                return str(i)

        raise ValueError(
            f"{node_name} invalid selection: {node_value!r}. "
            f"Valid selections: {', '.join(options)}"
        )

    return node_value


def AddNode(nodeName, nodeValue="", includePorts=True, position=None, ownerFunctionSID=""):
    node = {}

    if position is None:
        position = Position3(0, 0)

    nodeId = generateId()
    size = NODE_SIZES.get(nodeName, DEFAULT_NODE_SIZE)

    node["serializableRectTransform"] = _rect_transform(position, size, nodeName)
    node["id"] = nodeName
    node["sID"] = nodeId
    node["modifier"] = _normalize_modifier(nodeName, nodeValue)
    if ownerFunctionSID:
        node["ownerFunctionSID"] = ownerFunctionSID
    if nodeName in SERIALIZE_COLOR_NODES:
        node["serializeColor"] = True
        node["serializeSizeDelta"] = True
        node["serializableDefaultColor"] = DEFAULT_NODE_COLOR
    elif nodeName in SERIALIZE_SIZE_DELTA_NODES:
        node["serializeSizeDelta"] = True
    node["serializablePorts"] = []
    if includePorts:
        for portData in ports[nodeName]:
            node["serializablePorts"].append(
                {
                    "id": portData["id"],
                    "sID": generateId(),
                    "polarity": portData["polarity"],
                    "nodeSID": nodeId,
                }
            )

    data["serializableNodes"].append(node)

    return Node(node)


def ConnectPorts(portType: tuple | str, node0: Node, node1: Node):
    """Wire two ports. Emits Lean-minimal connection JSON only (no line/chrome)."""
    if isinstance(portType, tuple):
        port0 = node0.outputPorts[portType[0]]
        port1 = node1.inputPorts[portType[1]]
    else:
        port0 = node0.outputPorts[portType]
        port1 = node1.inputPorts[portType]
    connection = {
        "sID": generateId(),
        "port0InstanceID": 0,
        "port1InstanceID": 0,
        "port0SID": port0["sID"],
        "port1SID": port1["sID"],
    }
    data["serializableConnections"].append(connection)
    return connection


def findNodeByPortSID(portSID):
    for node in data["serializableNodes"]:
        for port in node["serializablePorts"]:
            if port["sID"] == portSID:
                return node
    return None


def gridLayout(offsetX=350, offsetY=-215):
    x = 1263
    y = -278
    nodesPerRow = max(1, int(math.sqrt(len(data["serializableNodes"]))))

    for i, node in enumerate(data["serializableNodes"]):
        transform = node["serializableRectTransform"]
        if not _is_at_origin(transform):
            continue
        _set_layout_position(transform, x, y)
        x += offsetX
        if (i + 1) % nodesPerRow == 0:
            x = 1263
            y += offsetY


def autoLayout(offsetX=350, offsetY=-215):
    adj = {}
    inDegree = {}

    for node in data["serializableNodes"]:
        adj[node["sID"]] = []
        inDegree[node["sID"]] = 0

    for conn in data["serializableConnections"]:
        sourceNode = findNodeByPortSID(conn["port0SID"])
        destNode = findNodeByPortSID(conn["port1SID"])

        if sourceNode and destNode and sourceNode["sID"] != destNode["sID"]:
            adj[sourceNode["sID"]].append(destNode["sID"])
            inDegree[destNode["sID"]] += 1

    queue = deque()
    for nodeSID, degree in inDegree.items():
        if degree == 0:
            queue.append(nodeSID)

    nodeRegistry = {node["sID"]: node for node in data["serializableNodes"]}

    nodeLevels = {nodeSID: 0 for nodeSID in nodeRegistry.keys()}
    visitedCount = 0

    while queue:
        u = queue.popleft()
        visitedCount += 1

        for v in adj[u]:
            nodeLevels[v] = max(nodeLevels[v], nodeLevels[u] + 1)
            inDegree[v] -= 1
            if inDegree[v] == 0:
                queue.append(v)

    if visitedCount < len(data["serializableNodes"]):
        gridLayout(offsetX, offsetY)
        return

    columns = {}
    for nodeSID, level in nodeLevels.items():
        if level not in columns:
            columns[level] = []
        columns[level].append(nodeRegistry[nodeSID])

    sortedColumns = sorted(columns.items())

    currentX = 1263
    for level, nodesInColumn in sortedColumns:
        totalHeight = (len(nodesInColumn) - 1) * offsetY
        currentY = -totalHeight / 2.0 - 278

        for node in nodesInColumn:
            transform = node["serializableRectTransform"]
            if not _is_at_origin(transform):
                continue
            _set_layout_position(transform, currentX, currentY)
            currentY += offsetY

        currentX += offsetX


def updateConnectionLinePoints():
    """No-op: minimal serialization format does not include connection line points."""
    pass


def _strip_relay_nodes(*, spatial_structure: bool = False):
    """Bypass and delete Relay nodes that are pure editor pass-throughs.

    Relays use a single polarity-2 ``Any1`` port. Rewrite every consumer that
    was fed through a Relay to the ultimate non-Relay producer, then drop the
    Relay nodes and the old edges.

    **Exception — memory latches:** if a node's output feeds a Relay that
    feeds back into the *same* node (Zudan ``ConditionalSet*`` pattern:
    out → Relay → false-branch), keep that Relay and its edges. Stripping
    those destroys tick-to-tick memory.
    """
    port_polarity: dict[str, int] = {}
    port_node_id: dict[str, str] = {}
    relay_ports: set[str] = set()
    for node in data["serializableNodes"]:
        for port in node.get("serializablePorts", []):
            sid = port.get("sID")
            if not sid:
                continue
            port_polarity[sid] = int(port.get("polarity", 0))
            port_node_id[sid] = node.get("id", "")
            if node.get("id") == "Relay":
                relay_ports.add(sid)

    if not relay_ports:
        return

    # relay_port -> producer port (may still be a relay; resolved below)
    source: dict[str, str] = {}
    relay_relay: list[tuple[str, str]] = []
    for conn in data["serializableConnections"]:
        a, b = conn.get("port0SID"), conn.get("port1SID")
        if not a or not b:
            continue
        pa, pb = port_polarity.get(a), port_polarity.get(b)
        if pa is None or pb is None:
            continue
        a_rel, b_rel = a in relay_ports, b in relay_ports
        # Out(1) → Relay(2)
        if pa == 1 and pb == 2 and b_rel:
            source[b] = a
        elif pb == 1 and pa == 2 and a_rel:
            source[a] = b
        # Relay(2) ↔ Relay(2)
        elif pa == 2 and pb == 2 and a_rel and b_rel:
            relay_relay.append((a, b))

    # Propagate along Relay↔Relay chains.
    changed = True
    while changed:
        changed = False
        for a, b in relay_relay:
            if a in source and b not in source:
                source[b] = source[a]
                changed = True
            if b in source and a not in source:
                source[a] = source[b]
                changed = True

    def ultimate(port: str) -> str | None:
        seen: set[str] = set()
        cur = port
        while cur in relay_ports:
            if cur in seen:
                return None
            seen.add(cur)
            nxt = source.get(cur)
            if not nxt:
                return None
            cur = nxt
        return cur

    port_to_node_sid: dict[str, str] = {}
    for node in data["serializableNodes"]:
        for port in node.get("serializablePorts", []):
            if port.get("sID"):
                port_to_node_sid[port["sID"]] = node["sID"]

    # Consumers of each relay port: polarity-0 (or other) ports fed by this relay.
    relay_consumers: dict[str, list[str]] = {rp: [] for rp in relay_ports}
    for conn in data["serializableConnections"]:
        a, b = conn.get("port0SID"), conn.get("port1SID")
        if not a or not b:
            continue
        pa, pb = port_polarity.get(a), port_polarity.get(b)
        if pa is None or pb is None:
            continue
        if a in relay_ports and pb == 0:
            relay_consumers[a].append(b)
        elif b in relay_ports and pa == 0:
            relay_consumers[b].append(a)
        # Relay ↔ Relay already in relay_relay; Relay fed by Out already in source.

    # Memory-cell Relays: output of node N feeds Relay, Relay feeds back into N
    # (Zudan ConditionalSet* latch). Also keep pure Relay↔Relay loops with no
    # external source (ultimate is None).
    cyclic_relay_ports: set[str] = set()
    for rp in relay_ports:
        if ultimate(rp) is None:
            cyclic_relay_ports.add(rp)
            continue
        prod = source.get(rp)
        if not prod:
            continue
        prod_node = port_to_node_sid.get(prod)
        if not prod_node:
            continue
        for cons in relay_consumers.get(rp, ()):
            if port_to_node_sid.get(cons) == prod_node:
                cyclic_relay_ports.add(rp)
                break

    blocked_relay_ports: set[str] = set()
    if spatial_structure:
        positions = _collect_node_positions()
        q75 = _isolation_quartile_threshold(positions)
        for rp in relay_ports:
            if rp in cyclic_relay_ports:
                continue
            src_port = ultimate(rp)
            if not src_port:
                continue
            relay_node = port_to_node_sid.get(rp)
            src_node = port_to_node_sid.get(src_port)
            if not relay_node or not src_node:
                continue
            dst_nodes = {
                port_to_node_sid[cons]
                for cons in relay_consumers.get(rp, ())
                if cons in port_to_node_sid
            }
            if not dst_nodes:
                continue
            if not _spatial_collapse_allowed(
                spatial_structure=True,
                candidate_sid=relay_node,
                src_sid=src_node,
                dst_sids=dst_nodes,
                positions=positions,
                isolation_q75=q75,
            ):
                blocked_relay_ports.add(rp)

    keep_relay_ports = cyclic_relay_ports | blocked_relay_ports

    new_conns: list[dict] = []
    seen_edges: set[tuple[str, str]] = set()

    def add_edge(p0: str, p1: str) -> None:
        key = (p0, p1)
        if key in seen_edges or p0 == p1:
            return
        seen_edges.add(key)
        new_conns.append(
            {
                "sID": generateId(),
                "port0SID": p0,
                "port1SID": p1,
                "port0InstanceID": 0,
                "port1InstanceID": 0,
            }
        )

    for conn in data["serializableConnections"]:
        a, b = conn.get("port0SID"), conn.get("port1SID")
        if not a or not b:
            continue
        a_rel, b_rel = a in relay_ports, b in relay_ports
        if a in keep_relay_ports or b in keep_relay_ports:
            # Preserve latch memory wiring and spatially blocked relays.
            key = (a, b)
            if key not in seen_edges:
                seen_edges.add(key)
                new_conns.append(conn)
            continue
        if not a_rel and not b_rel:
            key = (a, b)
            if key not in seen_edges:
                seen_edges.add(key)
                new_conns.append(conn)
            continue
        if a_rel and b_rel:
            continue  # relay↔relay absorbed
        relay_p, other = (a, b) if a_rel else (b, a)
        pol_other = port_polarity.get(other)
        if pol_other == 0:
            src = ultimate(relay_p)
            if src:
                add_edge(src, other)

    keep_relay_nodes = {
        port_to_node_sid[p] for p in keep_relay_ports if p in port_to_node_sid
    }

    data["serializableConnections"] = new_conns
    data["serializableNodes"] = [
        n
        for n in data["serializableNodes"]
        if n.get("id") != "Relay" or n["sID"] in keep_relay_nodes
    ]


def _inline_passthrough_variables(*, spatial_structure: bool = False):
    """Replace pure Set/Get alias variables with direct producer→consumer wires.

    Keeps a variable when it looks like memoization / bridging:
      - more than one ``SetVariable`` for the name
      - Set has no single wired producer
      - any ``GetVariable`` of the name is an ancestor of the Set (feedback)
      - Set and Get live in different ``ownerFunctionSID`` scopes (function
        bodies often use root variables as the intentional bridge)
    """
    port_polarity: dict[str, int] = {}
    port_node: dict[str, str] = {}
    for node in data["serializableNodes"]:
        for port in node.get("serializablePorts", []):
            sid = port.get("sID")
            if not sid:
                continue
            port_polarity[sid] = int(port.get("polarity", 0))
            port_node[sid] = node["sID"]

    # Directed node edges: producer node -> consumer node.
    forward: dict[str, set[str]] = {}
    reverse: dict[str, set[str]] = {}
    for conn in data["serializableConnections"]:
        a, b = conn.get("port0SID"), conn.get("port1SID")
        if not a or not b or a not in port_polarity or b not in port_polarity:
            continue
        pa, pb = port_polarity[a], port_polarity[b]
        if pa != 0 and pb == 0:
            src, dst = port_node[a], port_node[b]
        elif pb != 0 and pa == 0:
            src, dst = port_node[b], port_node[a]
        else:
            continue
        forward.setdefault(src, set()).add(dst)
        reverse.setdefault(dst, set()).add(src)

    sets: dict[str, list[dict]] = {}
    gets: dict[str, list[dict]] = {}
    for node in data["serializableNodes"]:
        name = node.get("modifier", "")
        if node.get("id") == "SetVariable":
            sets.setdefault(name, []).append(node)
        elif node.get("id") == "GetVariable":
            gets.setdefault(name, []).append(node)

    def ancestors(start: str) -> set[str]:
        seen: set[str] = set()
        stack = [start]
        while stack:
            u = stack.pop()
            if u in seen:
                continue
            seen.add(u)
            for p in reverse.get(u, ()):
                if p not in seen:
                    stack.append(p)
        return seen

    def producer_port_for_set(set_node: dict) -> str | None:
        in_ports = {
            p["sID"]
            for p in set_node.get("serializablePorts", [])
            if p.get("polarity") == 0 and p.get("sID")
        }
        found: list[str] = []
        for conn in data["serializableConnections"]:
            a, b = conn.get("port0SID"), conn.get("port1SID")
            if b in in_ports and a in port_polarity and port_polarity[a] != 0:
                found.append(a)
            elif a in in_ports and b in port_polarity and port_polarity[b] != 0:
                found.append(b)
        return found[0] if len(found) == 1 else None

    def get_out_port(get_node: dict) -> str | None:
        for p in get_node.get("serializablePorts", []):
            if p.get("polarity") == 1 and p.get("sID"):
                return p["sID"]
        return None

    inline_names: list[str] = []
    positions = _collect_node_positions() if spatial_structure else None
    isolation_q75 = _isolation_quartile_threshold(positions) if positions else 0.0
    for name, set_list in sets.items():
        get_list = gets.get(name, [])
        if len(set_list) != 1 or not get_list:
            continue
        set_node = set_list[0]
        prod = producer_port_for_set(set_node)
        if not prod:
            continue
        set_owner = set_node.get("ownerFunctionSID") or ""
        if any((g.get("ownerFunctionSID") or "") != set_owner for g in get_list):
            continue
        get_ids = {g["sID"] for g in get_list}
        if get_ids & ancestors(set_node["sID"]):
            continue  # feedback / memoization through this variable
        prod_node = port_node.get(prod)
        consumer_nodes: set[str] = set()
        for get_node in get_list:
            gout = get_out_port(get_node)
            if not gout:
                continue
            for conn in data["serializableConnections"]:
                a, b = conn.get("port0SID"), conn.get("port1SID")
                if a == gout and b in port_node:
                    consumer_nodes.add(port_node[b])
                elif b == gout and a in port_node:
                    consumer_nodes.add(port_node[a])
        if prod_node and not _spatial_collapse_allowed(
            spatial_structure=spatial_structure,
            candidate_sid=set_node["sID"],
            src_sid=prod_node,
            dst_sids=consumer_nodes or {g["sID"] for g in get_list},
            positions=positions,
            isolation_q75=isolation_q75,
        ):
            continue
        inline_names.append(name)

    if not inline_names:
        return

    remove_node_sids: set[str] = set()
    remove_ports: set[str] = set()
    rewires: list[tuple[str, str]] = []  # producer_port -> consumer_port

    for name in inline_names:
        set_node = sets[name][0]
        prod = producer_port_for_set(set_node)
        assert prod is not None
        remove_node_sids.add(set_node["sID"])
        for p in set_node.get("serializablePorts", []):
            if p.get("sID"):
                remove_ports.add(p["sID"])
        for get_node in gets[name]:
            gout = get_out_port(get_node)
            remove_node_sids.add(get_node["sID"])
            for p in get_node.get("serializablePorts", []):
                if p.get("sID"):
                    remove_ports.add(p["sID"])
            if not gout:
                continue
            for conn in data["serializableConnections"]:
                a, b = conn.get("port0SID"), conn.get("port1SID")
                if a == gout and b in port_polarity and port_polarity[b] == 0:
                    rewires.append((prod, b))
                elif b == gout and a in port_polarity and port_polarity[a] == 0:
                    rewires.append((prod, a))

    new_conns: list[dict] = []
    seen: set[tuple[str, str]] = set()
    for conn in data["serializableConnections"]:
        a, b = conn.get("port0SID"), conn.get("port1SID")
        if not a or not b:
            continue
        if a in remove_ports or b in remove_ports:
            continue
        key = (a, b)
        if key in seen:
            continue
        seen.add(key)
        new_conns.append(conn)
    for prod, cons in rewires:
        key = (prod, cons)
        if key in seen or prod == cons:
            continue
        seen.add(key)
        new_conns.append(
            {
                "sID": generateId(),
                "port0SID": prod,
                "port1SID": cons,
                "port0InstanceID": 0,
                "port1InstanceID": 0,
            }
        )

    data["serializableConnections"] = new_conns
    data["serializableNodes"] = [
        n for n in data["serializableNodes"] if n["sID"] not in remove_node_sids
    ]


def _norm_lit(mod) -> str:
    s = str(mod).replace(",", ".").strip()
    try:
        return f"{float(s):.6g}"
    except Exception:
        return s


def _producer_consumer_edges():
    polarity = {}
    node_of = {}
    for n in data["serializableNodes"]:
        for p in n.get("serializablePorts", []):
            if p.get("sID"):
                polarity[p["sID"]] = int(p.get("polarity", 0))
                node_of[p["sID"]] = n["sID"]
    edges = []
    for c in data["serializableConnections"]:
        a, b = c.get("port0SID"), c.get("port1SID")
        if not a or not b or a not in polarity or b not in polarity:
            continue
        pa, pb = polarity[a], polarity[b]
        if pa != 0 and pb == 0:
            edges.append((a, b))
        elif pb != 0 and pa == 0:
            edges.append((b, a))
    return polarity, node_of, edges


def _bypass_node(
    node_sid: str,
    in_port: str,
    out_port: str,
    *,
    spatial_structure: bool = False,
) -> bool:
    polarity, node_of, edges = _producer_consumer_edges()
    producers = [a for a, b in edges if b == in_port]
    consumers = [b for a, b in edges if a == out_port]
    if len(producers) != 1 or not consumers:
        return False
    prod = producers[0]
    if spatial_structure:
        positions = _collect_node_positions()
        q75 = _isolation_quartile_threshold(positions)
        prod_node = node_of.get(prod)
        dst_nodes = {node_of[c] for c in consumers if node_of.get(c)}
        if prod_node and dst_nodes and not _spatial_collapse_allowed(
            spatial_structure=True,
            candidate_sid=node_sid,
            src_sid=prod_node,
            dst_sids=dst_nodes,
            positions=positions,
            isolation_q75=q75,
        ):
            return False
    dead = set()
    for n in data["serializableNodes"]:
        if n["sID"] == node_sid:
            for p in n.get("serializablePorts", []):
                if p.get("sID"):
                    dead.add(p["sID"])
            break
    new_conns = []
    seen: set[tuple[str, str]] = set()
    for c in data["serializableConnections"]:
        a, b = c.get("port0SID"), c.get("port1SID")
        if a in dead or b in dead:
            continue
        key = (a, b)
        if key in seen:
            continue
        seen.add(key)
        new_conns.append(c)
    for cons in consumers:
        key = (prod, cons)
        if key in seen or prod == cons:
            continue
        seen.add(key)
        new_conns.append(
            {
                "sID": generateId(),
                "port0SID": prod,
                "port1SID": cons,
                "port0InstanceID": 0,
                "port1InstanceID": 0,
            }
        )
    data["serializableConnections"] = new_conns
    data["serializableNodes"] = [n for n in data["serializableNodes"] if n["sID"] != node_sid]
    return True


def _inline_double_not(*, spatial_structure: bool = False) -> int:
    """Not(Not(x)) path: wire x to outer consumers; drop the outer Not (and inner if unused)."""
    changed = 0
    while True:
        polarity, node_of, edges = _producer_consumer_edges()
        nodes = {n["sID"]: n for n in data["serializableNodes"]}
        did = False
        for n2 in list(data["serializableNodes"]):
            if n2.get("id") != "Not":
                continue
            in2 = next((p["sID"] for p in n2["serializablePorts"] if p.get("polarity") == 0), None)
            out2 = next((p["sID"] for p in n2["serializablePorts"] if p.get("polarity") == 1), None)
            if not in2 or not out2:
                continue
            prods = [a for a, b in edges if b == in2]
            if len(prods) != 1:
                continue
            n1 = nodes.get(node_of.get(prods[0]))
            if not n1 or n1.get("id") != "Not":
                continue
            out1 = prods[0]
            in1 = next((p["sID"] for p in n1["serializablePorts"] if p.get("polarity") == 0), None)
            if not in1:
                continue
            inner = [a for a, b in edges if b == in1]
            if len(inner) != 1:
                continue
            src = inner[0]
            consumers = [b for a, b in edges if a == out2]
            if not consumers:
                continue
            src_node = node_of.get(src)
            dst_nodes = {node_of[c] for c in consumers if node_of.get(c)}
            if src_node and dst_nodes and not _spatial_collapse_allowed(
                spatial_structure=spatial_structure,
                candidate_sid=n2["sID"],
                src_sid=src_node,
                dst_sids=dst_nodes,
            ):
                continue
            dead = {p["sID"] for p in n2["serializablePorts"] if p.get("sID")}
            new_conns = []
            seen: set[tuple[str, str]] = set()
            for c in data["serializableConnections"]:
                a, b = c.get("port0SID"), c.get("port1SID")
                if a in dead or b in dead:
                    continue
                key = (a, b)
                if key in seen:
                    continue
                seen.add(key)
                new_conns.append(c)
            for cons in consumers:
                key = (src, cons)
                if key in seen or src == cons:
                    continue
                seen.add(key)
                new_conns.append(
                    {
                        "sID": generateId(),
                        "port0SID": src,
                        "port1SID": cons,
                        "port0InstanceID": 0,
                        "port1InstanceID": 0,
                    }
                )
            data["serializableConnections"] = new_conns
            data["serializableNodes"] = [n for n in data["serializableNodes"] if n["sID"] != n2["sID"]]
            _, _, edges2 = _producer_consumer_edges()
            if not any(a == out1 for a, _ in edges2):
                dead1 = {p["sID"] for p in n1["serializablePorts"] if p.get("sID")}
                data["serializableConnections"] = [
                    c
                    for c in data["serializableConnections"]
                    if c.get("port0SID") not in dead1 and c.get("port1SID") not in dead1
                ]
                data["serializableNodes"] = [
                    n for n in data["serializableNodes"] if n["sID"] != n1["sID"]
                ]
            changed += 1
            did = True
            break
        if not did:
            break
    return changed


def _inline_identity_math(*, spatial_structure: bool = False) -> int:
    """Bypass ScaleVector3(*1), MultiplyFloats(*1), AddFloats(+0),
    SubtractFloats(x-0), DivideFloats(x/1). Not 0-x or 1/x."""
    changed = 0
    while True:
        polarity, node_of, edges = _producer_consumer_edges()
        float_val = {
            n["sID"]: _norm_lit(n.get("modifier"))
            for n in data["serializableNodes"]
            if n.get("id") == "Float"
        }

        def port_named(node, name, pol):
            for p in node.get("serializablePorts", []):
                if p.get("id") == name and int(p.get("polarity", -1)) == pol:
                    return p.get("sID")
            return None

        def producer_of(consumer_port):
            ps = [a for a, b in edges if b == consumer_port]
            return ps[0] if len(ps) == 1 else None

        did = False
        for n in list(data["serializableNodes"]):
            tid = n.get("id")
            target = None
            if tid == "ScaleVector3":
                f_in = port_named(n, "Float1", 0)
                v_in = port_named(n, "Vector31", 0)
                v_out = port_named(n, "Vector31", 1)
                if f_in and v_in and v_out:
                    fp = producer_of(f_in)
                    if fp and node_of.get(fp) in float_val and float_val[node_of[fp]] == "1":
                        target = (n["sID"], v_in, v_out)
            elif tid == "MultiplyFloats":
                a_in = port_named(n, "Float1", 0)
                b_in = port_named(n, "Float2", 0)
                out = port_named(n, "Float1", 1)
                if a_in and b_in and out:
                    pa, pb = producer_of(a_in), producer_of(b_in)
                    keep = None
                    if pa and node_of.get(pa) in float_val and float_val[node_of[pa]] == "1":
                        keep = b_in
                    elif pb and node_of.get(pb) in float_val and float_val[node_of[pb]] == "1":
                        keep = a_in
                    if keep:
                        target = (n["sID"], keep, out)
            elif tid == "AddFloats":
                a_in = port_named(n, "Float1", 0)
                b_in = port_named(n, "Float2", 0)
                out = port_named(n, "Float1", 1)
                if a_in and b_in and out:
                    pa, pb = producer_of(a_in), producer_of(b_in)
                    keep = None
                    if pa and node_of.get(pa) in float_val and float_val[node_of[pa]] == "0":
                        keep = b_in
                    elif pb and node_of.get(pb) in float_val and float_val[node_of[pb]] == "0":
                        keep = a_in
                    if keep:
                        target = (n["sID"], keep, out)
            elif tid == "SubtractFloats":
                # x - 0 only (Float2 == 0). 0 - x is negate, not identity.
                a_in = port_named(n, "Float1", 0)
                b_in = port_named(n, "Float2", 0)
                out = port_named(n, "Float1", 1)
                if a_in and b_in and out:
                    pb = producer_of(b_in)
                    if pb and node_of.get(pb) in float_val and float_val[node_of[pb]] == "0":
                        target = (n["sID"], a_in, out)
            elif tid == "DivideFloats":
                # x / 1 only (Float2 == 1). 1 / x is reciprocal, not identity.
                a_in = port_named(n, "Float1", 0)
                b_in = port_named(n, "Float2", 0)
                out = port_named(n, "Float1", 1)
                if a_in and b_in and out:
                    pb = producer_of(b_in)
                    if pb and node_of.get(pb) in float_val and float_val[node_of[pb]] == "1":
                        target = (n["sID"], a_in, out)
            if target and _bypass_node(*target, spatial_structure=spatial_structure):
                changed += 1
                did = True
                break
        if not did:
            break
    return changed


def _inline_split_construct(*, spatial_structure: bool = False) -> int:
    """ConstructVector3(split.xyz) from one Vector3Split -> use the split's input vector."""
    changed = 0
    while True:
        polarity, node_of, edges = _producer_consumer_edges()
        nodes = {n["sID"]: n for n in data["serializableNodes"]}
        did = False
        for n in list(data["serializableNodes"]):
            if n.get("id") != "ConstructVector3":
                continue
            feeds = {}
            for p in n.get("serializablePorts", []):
                if int(p.get("polarity", -1)) != 0:
                    continue
                ps = [a for a, b in edges if b == p["sID"]]
                if len(ps) == 1:
                    feeds[p.get("id")] = ps[0]
            if not {"Float1", "Float2", "Float3"} <= set(feeds):
                continue
            split_ids = []
            ok = True
            for pname, prod in feeds.items():
                sn = nodes.get(node_of.get(prod))
                if not sn or sn.get("id") != "Vector3Split":
                    ok = False
                    break
                pr = next((pp for pp in sn["serializablePorts"] if pp.get("sID") == prod), None)
                if not pr or pr.get("id") != pname:
                    ok = False
                    break
                split_ids.append(sn["sID"])
            if not ok or len(set(split_ids)) != 1:
                continue
            split = nodes[split_ids[0]]
            vin = next(
                (
                    p["sID"]
                    for p in split["serializablePorts"]
                    if p.get("id") == "Vector31" and int(p.get("polarity", -1)) == 0
                ),
                None,
            )
            vout_c = next(
                (
                    p["sID"]
                    for p in n["serializablePorts"]
                    if p.get("id") == "Vector31" and int(p.get("polarity", -1)) == 1
                ),
                None,
            )
            if not vin or not vout_c:
                continue
            sprods = [a for a, b in edges if b == vin]
            if len(sprods) != 1:
                continue
            src = sprods[0]
            consumers = [b for a, b in edges if a == vout_c]
            if not consumers:
                continue
            src_node = node_of.get(src)
            dst_nodes = {node_of[c] for c in consumers if node_of.get(c)}
            if src_node and dst_nodes and not _spatial_collapse_allowed(
                spatial_structure=spatial_structure,
                candidate_sid=n["sID"],
                src_sid=src_node,
                dst_sids=dst_nodes,
            ):
                continue
            dead = {p["sID"] for p in n["serializablePorts"] if p.get("sID")}
            new_conns = []
            seen: set[tuple[str, str]] = set()
            for c in data["serializableConnections"]:
                a, b = c.get("port0SID"), c.get("port1SID")
                if a in dead or b in dead:
                    continue
                key = (a, b)
                if key in seen:
                    continue
                seen.add(key)
                new_conns.append(c)
            for cons in consumers:
                key = (src, cons)
                if key in seen or src == cons:
                    continue
                seen.add(key)
                new_conns.append(
                    {
                        "sID": generateId(),
                        "port0SID": src,
                        "port1SID": cons,
                        "port0InstanceID": 0,
                        "port1InstanceID": 0,
                    }
                )
            data["serializableConnections"] = new_conns
            data["serializableNodes"] = [x for x in data["serializableNodes"] if x["sID"] != n["sID"]]
            _, _, edges2 = _producer_consumer_edges()
            split_outs = {
                p["sID"]
                for p in split["serializablePorts"]
                if p.get("sID") and int(p.get("polarity", -1)) == 1
            }
            if not any(a in split_outs for a, _ in edges2):
                dead_s = {p["sID"] for p in split["serializablePorts"] if p.get("sID")}
                data["serializableConnections"] = [
                    c
                    for c in data["serializableConnections"]
                    if c.get("port0SID") not in dead_s and c.get("port1SID") not in dead_s
                ]
                data["serializableNodes"] = [
                    x for x in data["serializableNodes"] if x["sID"] != split["sID"]
                ]
            changed += 1
            did = True
            break
        if not did:
            break
    return changed


# Pure producers / constants safe to drop when nothing consumes their outputs.
# Never include Function/CreateFunction, Set/Get, ConditionalSet*, Debug/TimePlot,
# or action sinks — those can affect play without a used output edge.
_ORPHAN_DCE_ALLOW = frozenset(
    {
        "String",
        "Float",
        "Bool",
        "Color",
        "Vector3",
        "Vector3Constant",
        "AddFloats",
        "SubtractFloats",
        "MultiplyFloats",
        "DivideFloats",
        "AddVector3",
        "SubtractVector3",
        "ScaleVector3",
        "Normalize",
        "ConstructVector3",
        "Vector3Split",
        "CompareBool",
        "CompareFloats",
        "Not",
        "And",
        "Or",
        "Xor",
        "IsNull",
        "DotProduct",
        "Distance",
        "ClampFloat",
        "Operation",
        "RelativePosition",
        "Magnitude",
        "Cross",
        "Lerp",
        "SoccerGetBool",
        "SoccerGetFloat",
        "SoccerGetVector3",
        "SoccerGetTransform",
        "SoccerPlayerSensors1",
        "SoccerPlayerSensors2",
        "SoccerPlayerSensors3",
        "SoccerPlayerSensors4",
    }
)


def _orphan_dce_allowed(node_id: str) -> bool:
    if not node_id:
        return False
    if node_id in _ORPHAN_DCE_ALLOW:
        return True
    return node_id.startswith("SoccerPlayerSensors")


def _dce_orphan_producers() -> int:
    """Drop allowlisted nodes whose outputs feed nobody (and fully disconnected ones).

    Existing ``removeUnusedNodes`` keeps every String forever; this cleans those
    leftover label constants and other pure dead producers after leaner inlines.
    Fixpoint: removing a consumer can orphan its producers.
    """
    total = 0
    for _ in range(32):
        _, _, edges = _producer_consumer_edges()
        used_out = {a for a, _ in edges}
        used_any = used_out | {b for _, b in edges}
        doomed: set[str] = set()
        for n in data["serializableNodes"]:
            nid = n.get("id")
            if not _orphan_dce_allowed(nid):
                continue
            ports = [p for p in n.get("serializablePorts", []) if p.get("sID")]
            outs = [p["sID"] for p in ports if int(p.get("polarity", -1)) == 1]
            if outs:
                if any(o in used_out for o in outs):
                    continue
                doomed.add(n["sID"])
                continue
            # No output ports: drop only if nothing touches the node at all.
            if ports and not any(p["sID"] in used_any for p in ports):
                doomed.add(n["sID"])
            elif not ports:
                doomed.add(n["sID"])
        if not doomed:
            break
        dead_ports = {
            p["sID"]
            for n in data["serializableNodes"]
            if n["sID"] in doomed
            for p in n.get("serializablePorts", [])
            if p.get("sID")
        }
        data["serializableConnections"] = [
            c
            for c in data["serializableConnections"]
            if c.get("port0SID") not in dead_ports and c.get("port1SID") not in dead_ports
        ]
        data["serializableNodes"] = [
            n for n in data["serializableNodes"] if n["sID"] not in doomed
        ]
        total += len(doomed)
    return total


def _strip_leaner_fields(
    *,
    strip_regions: bool = False,
    strip_layout: bool = False,
    spatial_structure: bool = False,
):
    """Extra size trim beyond Lean — decision-irrelevant chrome only.

    Keeps node serializableRectTransform (quantized anchoredPosition from
    _prepare_for_unity_format) so Unity editor graphs stay readable unless
    ``strip_layout`` (core). Still strips port rects and other chrome.
    Region nodes are kept for editor readability unless ``strip_regions``
    (core). Region / CreateFunction visual fields (colors, serializeSizeDelta)
    are preserved.

    When ``spatial_structure`` is True (layout kept), passthrough inlines are
    gated to avoid long cross-graph wires through dense local structure, then
    node positions are tightened toward wired neighbors.

    Parity-checked ladder (AIA / AIA3 / Titanium):
      PASS: Region, Relay rewire, Set/Get alias inline, double-Not, identity
            math (*1/+0/x-0/x/1), split→construct noop, orphan DCE (allowlist),
            UUID remap / field chrome
      FAIL: stripDebugSinks on AIA/AIA3 (debug nodes feed decisions)
    """
    if strip_regions:
        data["serializableNodes"] = [
            n for n in data["serializableNodes"] if n.get("id") != "Region"
        ]
    _strip_relay_nodes(spatial_structure=spatial_structure)
    _inline_passthrough_variables(spatial_structure=spatial_structure)
    _inline_double_not(spatial_structure=spatial_structure)
    _inline_identity_math(spatial_structure=spatial_structure)
    _inline_split_construct(spatial_structure=spatial_structure)
    _dce_orphan_producers()
    for node in data["serializableNodes"]:
        node_id = node.get("id", "")
        if not node.get("ownerFunctionSID"):
            node.pop("ownerFunctionSID", None)
        mod = node.get("modifier", None)
        if mod in ("", None) or (isinstance(mod, str) and not str(mod).strip()):
            node.pop("modifier", None)
        if node_id not in SERIALIZE_SIZE_DELTA_NODES:
            node.pop("serializeSizeDelta", None)
        if node_id not in SERIALIZE_COLOR_NODES:
            node.pop("serializeColor", None)
            node.pop("defaultColor", None)
            node.pop("serializableDefaultColor", None)
        if strip_layout:
            node.pop("serializableRectTransform", None)
        for port in node.get("serializablePorts", []):
            port.pop("nodeSID", None)
            port.pop("serializableRectTransform", None)
            port.pop("controlPointSerializableRectTransform", None)
    for conn in data["serializableConnections"]:
        conn.pop("sID", None)
        conn.pop("port0InstanceID", None)
        conn.pop("port1InstanceID", None)


_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def _short_id(index: int) -> str:
    """Dense base62 id; length grows only when needed."""
    if index < 0:
        raise ValueError("index must be >= 0")
    if index == 0:
        return _ALPHABET[0]
    digits = []
    n = index
    base = len(_ALPHABET)
    while n:
        n, rem = divmod(n, base)
        digits.append(_ALPHABET[rem])
    return "".join(reversed(digits))


def remapSids(verbose=False):
    """Rewrite every node/port/connection SID to a short dense id.

    Preserves graph topology and modifiers; only opaque identity strings change.
    Call after Lean/leaner chrome stripping. Returns ``(unique_old, unique_new)``.
    """
    mapping: dict[str, str] = {}
    next_i = 0

    def map_one(old):
        nonlocal next_i
        if not old:
            return old
        if old in mapping:
            return mapping[old]
        new = _short_id(next_i)
        next_i += 1
        mapping[old] = new
        return new

    # Nodes first so ownerFunctionSID targets exist in the map before ports.
    for node in data["serializableNodes"]:
        if "sID" in node:
            node["sID"] = map_one(node["sID"])
        owner = node.get("ownerFunctionSID")
        if owner:
            node["ownerFunctionSID"] = map_one(owner)
        for port in node.get("serializablePorts", []):
            if "sID" in port:
                port["sID"] = map_one(port["sID"])
            if "nodeSID" in port:
                port["nodeSID"] = map_one(port["nodeSID"])
    for conn in data["serializableConnections"]:
        if "sID" in conn:
            conn["sID"] = map_one(conn["sID"])
        if "port0SID" in conn:
            conn["port0SID"] = map_one(conn["port0SID"])
        if "port1SID" in conn:
            conn["port1SID"] = map_one(conn["port1SID"])

    if verbose:
        print(f"  remapSids: {len(mapping)} ids -> base62 (max len {max((len(v) for v in mapping.values()), default=0)})")
    return len(mapping), next_i


def _prepare_for_unity_format(
    *,
    leaner: bool = False,
    remap_sids: bool = False,
    strip_regions: bool = False,
    strip_layout: bool = False,
):
    """Ensure graph data matches new minimal format (NodeTypeDataSO).
    - Standard nodes: rect = position (0,0,0) + anchoredPosition only; no color/size (prefab provides)
    - Region: full rect + color (SerializeSizeDelta, SerializeColor)
    - Ports: id, sID, polarity, nodeSID only (position from prefab)
    - Connections: wire SIDs only — drop editor line/curve/color chrome (Lean format)

    ``strip_regions=True`` / ``strip_layout=True`` are the ``core`` chrome kill
    switch (Regions + node serializableRectTransform). ``leaner=True``
    additionally drops fields the headless sim does not need for decisions.
    ``remap_sids=True`` rewrites UUIDs to short base62 ids.
    """
    for node in data["serializableNodes"]:
        node_id = node.get("id", "")
        transform = node.get("serializableRectTransform", {})
        if transform and strip_layout:
            ap = transform.get("anchoredPosition")
            lp = transform.get("localPosition", {})
            if ap is None and lp:
                ap = {"x": lp.get("x", 0), "y": lp.get("y", 0)}
            if ap is not None:
                transform["anchoredPosition"] = {
                    "x": _quantize_layout_coord(ap.get("x", 0)),
                    "y": _quantize_layout_coord(ap.get("y", 0)),
                }
            transform["position"] = {"x": 0, "y": 0, "z": 0}
            if node_id not in SERIALIZE_SIZE_DELTA_NODES:
                for key in ("localPosition", "anchorMin", "anchorMax", "sizeDelta"):
                    transform.pop(key, None)
            else:
                if lp:
                    transform["localPosition"] = {
                        "x": _quantize_layout_coord(lp.get("x", 0)),
                        "y": _quantize_layout_coord(lp.get("y", 0)),
                        "z": _quantize_layout_coord(lp.get("z", 0)),
                    }
                sd = transform.get("sizeDelta")
                if sd is not None:
                    transform["sizeDelta"] = {
                        "x": _quantize_layout_coord(sd.get("x", 0)),
                        "y": _quantize_layout_coord(sd.get("y", 0)),
                    }
            transform.pop("scale", None)
        if node_id not in SERIALIZE_COLOR_NODES:
            node.pop("defaultColor", None)
            node.pop("serializableDefaultColor", None)
        if node_id not in SERIALIZE_SIZE_DELTA_NODES:
            node.pop("serializeSizeDelta", None)
            node.pop("serializeColor", None)
        for port in node.get("serializablePorts", []):
            port.pop("serializableRectTransform", None)
            port.pop("controlPointSerializableRectTransform", None)

    # Match TitaniumLean / minimal Unity load: connections are pure port links.
    _CONN_KEEP = ("sID", "port0SID", "port1SID", "port0InstanceID", "port1InstanceID")
    slim = []
    for conn in data["serializableConnections"]:
        slim.append({k: conn[k] for k in _CONN_KEEP if k in conn})
    data["serializableConnections"] = slim

    if strip_regions:
        data["serializableNodes"] = [
            n for n in data["serializableNodes"] if n.get("id") != "Region"
        ]
    if leaner:
        # Regions already handled above when strip_regions=True.
        _strip_leaner_fields(
            strip_regions=False,
            strip_layout=strip_layout,
            spatial_structure=not strip_layout,
        )
    elif strip_layout:
        for node in data["serializableNodes"]:
            node.pop("serializableRectTransform", None)
    if remap_sids:
        remapSids(verbose=False)


def removeUnreadVariables(verbose=False):
    """Delete SetVariable writes no GetVariable reads, and GetVariable reads
    whose output feeds nothing.

    `removeUnusedNodes` cannot do this: a SetVariable is a SINK, so it always
    looks used and its whole producing subgraph is kept alive with it. One
    real graph carried a 405-node service this way -- 29 of 31 variables were
    written and never read, and everything computing them came along.

    Runs to a fixpoint: dropping a write can orphan a read, and dropping a
    read can orphan a write. Bounded, since each round strictly removes nodes.

    A variable pair is a data edge with NO wire between the two nodes, so this
    is the one thing an optimiser can silently sever -- delete the write and
    the read still looks connected while reading nothing. Callers should check
    `assertVariablesIntact()` afterwards.
    """
    total_w = total_r = 0
    for _ in range(10):
        nodes = data["serializableNodes"]
        read = {n["modifier"] for n in nodes if n["id"] == "GetVariable"}
        doomed = {n["sID"] for n in nodes
                  if n["id"] == "SetVariable" and n["modifier"] not in read}
        wired = set()
        for c in data["serializableConnections"]:
            wired.add(c["port0SID"])
            wired.add(c["port1SID"])
        doomed |= {
            n["sID"] for n in nodes if n["id"] == "GetVariable"
            and not any(p["sID"] in wired for p in n.get("serializablePorts", []))
        }
        if not doomed:
            break
        dead_ports = {p["sID"] for n in nodes if n["sID"] in doomed
                      for p in n.get("serializablePorts", [])}
        data["serializableConnections"] = [
            c for c in data["serializableConnections"]
            if c["port0SID"] not in dead_ports and c["port1SID"] not in dead_ports
        ]
        data["serializableNodes"] = [n for n in nodes if n["sID"] not in doomed]
        total_w += len(doomed)
    if verbose and total_w:
        print(f"  removeUnreadVariables: dropped {total_w} unread variable node(s)")
    return total_w


def assertVariablesIntact():
    """Fail if any GetVariable lost the SetVariable that fed it.

    Variables link by NAME, not by wire, so no wire-based pruner can see the
    dependency. Severing one leaves a read that looks perfectly connected and
    silently returns nothing -- this turns that into a hard error instead.
    """
    nodes = data["serializableNodes"]
    written = {n["modifier"] for n in nodes if n["id"] == "SetVariable"}
    read = {n["modifier"] for n in nodes if n["id"] == "GetVariable"}
    orphaned = read - written
    if orphaned:
        raise RuntimeError(
            "GetVariable with no SetVariable feeding it: " + ", ".join(sorted(orphaned))
        )


def stripDebugSinks(verbose=False):
    """Delete Debug*/TimePlot sinks so the pruner can collect everything that
    existed only to feed them.

    Typically ~29% of a graph. Competition builds do not render debug output,
    and the save format costs ~2.4 KB per node. Safe only if drawing code
    never feeds a decision -- verify that, do not assume it.
    """
    nodes = data["serializableNodes"]
    sinks = {"DebugDrawLine", "DebugDrawDisc", "TimePlot", "Debug"}
    doomed = {n["sID"] for n in nodes if n["id"] in sinks}
    if not doomed:
        return 0
    dead_ports = {p["sID"] for n in nodes if n["sID"] in doomed
                  for p in n.get("serializablePorts", [])}
    data["serializableConnections"] = [
        c for c in data["serializableConnections"]
        if c["port0SID"] not in dead_ports and c["port1SID"] not in dead_ports
    ]
    data["serializableNodes"] = [n for n in nodes if n["sID"] not in doomed]
    if verbose:
        print(f"  stripDebugSinks: removed {len(doomed)} debug sink(s)")
    return len(doomed)


def removeUnusedNodes():
    portToNode = {}
    nodeToPorts = {}
    nodeIsString = {}

    for node in data["serializableNodes"]:
        node_sid = node["sID"]
        nodeIsString[node_sid] = node["id"] == "String"
        nodeToPorts[node_sid] = {"input": [], "output": []}

        for port in node["serializablePorts"]:
            portToNode[port["sID"]] = node_sid
            if port["polarity"] == 0:
                nodeToPorts[node_sid]["input"].append(port["sID"])
            else:
                nodeToPorts[node_sid]["output"].append(port["sID"])

    connectionGraph = {}
    portConnections = {}

    for node in data["serializableNodes"]:
        connectionGraph[node["sID"]] = {"inputs": set(), "outputs": set()}

    for connection in data["serializableConnections"]:
        sourceNode = portToNode.get(connection["port0SID"])
        destinationNode = portToNode.get(connection["port1SID"])

        if sourceNode and destinationNode and sourceNode != destinationNode:
            connectionGraph[sourceNode]["outputs"].add(destinationNode)
            connectionGraph[destinationNode]["inputs"].add(sourceNode)

            portConnections[connection["port0SID"]] = (
                portConnections.get(connection["port0SID"], 0) + 1
            )
            portConnections[connection["port1SID"]] = (
                portConnections.get(connection["port1SID"], 0) + 1
            )

    # nodesToRemove are the BFS starting points
    nodesToRemove = set()
    queue = deque()

    for node in data["serializableNodes"]:
        node_sid = node["sID"]

        if nodeIsString[node_sid]:
            continue

        hasInputPorts = len(nodeToPorts[node_sid]["input"]) > 0
        hasOutputPorts = len(nodeToPorts[node_sid]["output"]) > 0

        inputConnected = any(
            portConnections.get(pid, 0) > 0 for pid in nodeToPorts[node_sid]["input"]
        )

        outputConnected = any(
            portConnections.get(pid, 0) > 0 for pid in nodeToPorts[node_sid]["output"]
        )

        if (hasInputPorts and not inputConnected) or (
            hasOutputPorts and not outputConnected
        ):
            nodesToRemove.add(node_sid)
            queue.append(node_sid)

    # BFS to find all nodes that become disconnected
    while queue:
        currentNode = queue.popleft()

        for dependentNode in connectionGraph[currentNode]["outputs"]:
            if dependentNode in nodesToRemove or nodeIsString[dependentNode]:
                continue

            if all(
                src in nodesToRemove for src in connectionGraph[dependentNode]["inputs"]
            ):
                nodesToRemove.add(dependentNode)
                queue.append(dependentNode)

        for sourceNode in connectionGraph[currentNode]["inputs"]:
            if sourceNode in nodesToRemove or nodeIsString[sourceNode]:
                continue

            if all(
                dst in nodesToRemove for dst in connectionGraph[sourceNode]["outputs"]
            ):
                nodesToRemove.add(sourceNode)
                queue.append(sourceNode)

    activeConnections = []
    for connection in data["serializableConnections"]:
        sourceNode = portToNode.get(connection["port0SID"])
        destinationNode = portToNode.get(connection["port1SID"])

        if sourceNode not in nodesToRemove and destinationNode not in nodesToRemove:
            activeConnections.append(connection)
    data["serializableConnections"] = activeConnections

    activeNodes = []
    for node in data["serializableNodes"]:
        node_sid = node["sID"]
        if node_sid not in nodesToRemove or nodeIsString[node_sid]:
            activeNodes.append(node)
    data["serializableNodes"] = activeNodes


def _optimize_to_fixpoint(verbose=False, *, strip_debug=False, prune=True):
    """Interleave strip, variable prune and DCE until a full round is a no-op.

    One pass feeds the next: stripping a TimePlot can orphan the SetVariable
    that only fed it, dropping that write can orphan the subgraph behind it,
    and so on. A single pass of each leaves most of that on the table."""
    max_rounds = max(len(data["serializableNodes"]), 1)
    for round_idx in range(max_rounds):
        changed = 0
        if strip_debug:
            changed += stripDebugSinks(verbose and round_idx == 0)
        if prune:
            changed += removeUnreadVariables(verbose and round_idx == 0)
            before = len(data["serializableNodes"])
            removeUnusedNodes()
            changed += before - len(data["serializableNodes"])
            assertVariablesIntact()
        if changed == 0:
            break


def ClearData():
    """Empty the in-memory graph (keeps the shared `data` dict identity)."""
    data["serializableNodes"].clear()
    data["serializableConnections"].clear()


def LoadData(filePath):
    """Replace the in-memory graph with an existing Unity save JSON.

    Mutates the shared `data` dict in place so imports of `data` keep working.
    No Python decompile — this loads the graph as-is for further editing or
    `SaveData` / `OptimizeFile`. Returns ``(node_count, connection_count)``.
    """
    with open(filePath, encoding="utf-8") as f:
        loaded = json.load(f)
    if not isinstance(loaded, dict):
        raise ValueError(f"{filePath}: expected a JSON object graph")
    nodes = loaded.get("serializableNodes")
    conns = loaded.get("serializableConnections")
    if not isinstance(nodes, list) or not isinstance(conns, list):
        raise ValueError(
            f"{filePath}: missing serializableNodes / serializableConnections"
        )
    # Replace list contents in place — some callers may hold the list refs.
    data["serializableNodes"][:] = nodes
    data["serializableConnections"][:] = conns
    return len(data["serializableNodes"]), len(data["serializableConnections"])


def OptimizeFile(
    inputPath,
    outputPath=None,
    *,
    optimize: Literal["normal", "release", "core"] = "release",
    layout: Literal["auto", "grid", "single", "hidden", None] = None,
    pruneUnusedNodes=True,
    keepPosition=True,
    leaner=False,
    remap_sids=False,
    verbose=False,
):
    """Compact an existing Unity bot JSON without a Python rebuild.

    Editor-made (or already-exported) graphs are the same JSON format Python
    writes, so there is no need to reverse them into Python source. This loads
    the file, runs the same optimiser as ``SaveData(optimize=...)``, and writes
    the result.

    ``optimize="normal"``: prune dead nodes only, preserve all visual data.
    ``optimize="release"`` (default here): also strip debug sinks and re-prune.
    Still preserves all visual data.
    ``optimize="core"``: strip ALL visual chrome (Regions, layout rects,
    colors, port rects). Nodes at 0,0. Leaves only logic for headless use.
    ``leaner=True``: run graph inlines + strip chrome, keep layout/Regions.
    ``remap_sids=True``: rewrite UUIDs to short base62 ids.

    Pass ``outputPath=None`` to overwrite ``inputPath`` in place.
    Returns the path written.
    """
    before_n, before_c = LoadData(inputPath)
    if verbose:
        print(f"  loaded {inputPath}: {before_n} nodes, {before_c} connections")
    out = inputPath if outputPath is None else outputPath
    SaveData(
        out,
        layout=layout,
        pruneUnusedNodes=pruneUnusedNodes,
        keepPosition=keepPosition,
        optimize=optimize,
        leaner=leaner,
        remap_sids=remap_sids,
        verbose=verbose,
    )
    after_n = len(data["serializableNodes"])
    after_c = len(data["serializableConnections"])
    if verbose:
        print(
            f"  wrote {out}: {after_n} nodes, {after_c} connections "
            f"({before_n - after_n} nodes / {before_c - after_c} connections removed)"
        )
    return out


def _slim_connections():
    """Strip connection metadata down to just port0SID + port1SID.

    The game engine only needs to know which two ports are wired. Fields like
    sID, port0InstanceID, port1InstanceID, line points, colors, etc. are
    editor chrome that has no effect on in-game visuals or logic.
    """
    data["serializableConnections"] = [
        {"port0SID": c["port0SID"], "port1SID": c["port1SID"]}
        for c in data["serializableConnections"]
        if c.get("port0SID") and c.get("port1SID")
    ]


def SaveData(
    filePath,
    layout: Literal["auto", "grid", "single", "hidden", None] = "auto",
    pruneUnusedNodes=True,
    keepPosition=True,
    optimize: Literal["normal", "release", "core"] = "normal",
    leaner=False,
    remap_sids=False,
    verbose=False,
):
    """Write the in-memory graph to a Unity save JSON file.

    Three independent optimization modes via ``optimize``:

    **"normal"** (default):
        Prune dead nodes and unread variables only. All visual data
        (layout, Regions, positions, scale, colors, port rects) preserved
        exactly as-is. Safe on a friend's Unity-exported graph — looks
        identical in the editor, just smaller.

    **"release"**:
        Same as normal, plus strip every Debug*/TimePlot sink and re-prune
        to a fixpoint so anything that ONLY fed debug output goes with it.
        Visual data still preserved exactly.

    **"core"**:
        Same as release, plus strip ALL visual chrome: Regions removed,
        node layout rects removed (nodes at 0,0), no coordinate quantizing,
        port rects and connection chrome stripped. Leaves only logic.
        Smallest possible output for headless / competition use.

    ``leaner=True`` runs graph-level inlines (relay bypass, passthrough
    variable collapse, identity-math fold, split→construct noop) and strips
    decision-irrelevant JSON chrome, but keeps layout/Regions. Spatial-aware
    (won't create long wires through dense local structure).

    ``remap_sids=True`` rewrites node/port/connection UUIDs to short base62.

    Every node evaluates every tick in-engine, so removing nodes removes real
    per-tick work, not just file size.

    To compact a bot that was *not* built in Python (Unity editor export, or
    any existing .txt graph), use ``OptimizeFile`` / ``LoadData`` instead of
    trying to reverse it into Python — there is no general decompiler.
    """
    if optimize == "core":
        _optimize_to_fixpoint(verbose, strip_debug=True, prune=pruneUnusedNodes)
        updateConnectionLinePoints()
        _prepare_for_unity_format(
            leaner=True,
            remap_sids=remap_sids,
            strip_regions=True,
            strip_layout=True,
        )
    elif optimize == "release":
        _optimize_to_fixpoint(verbose, strip_debug=True, prune=pruneUnusedNodes)
        updateConnectionLinePoints()
        if leaner:
            _prepare_for_unity_format(
                leaner=True,
                remap_sids=remap_sids,
                strip_regions=False,
                strip_layout=False,
            )
        elif remap_sids:
            remapSids(verbose=False)
    else:  # "normal"
        if pruneUnusedNodes:
            removeUnreadVariables(verbose)
            removeUnusedNodes()
            assertVariablesIntact()
        updateConnectionLinePoints()
        if leaner:
            _prepare_for_unity_format(
                leaner=True,
                remap_sids=remap_sids,
                strip_regions=False,
                strip_layout=False,
            )
        elif remap_sids:
            remapSids(verbose=False)

    _slim_connections()

    with open(filePath, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"), ensure_ascii=False)
