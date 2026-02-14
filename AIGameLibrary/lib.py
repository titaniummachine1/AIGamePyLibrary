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
    DEFAULT_CONNECTION_COLOR,
    CAP_COLOR,
)
from .utils import Position3, generateId

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
            if self.type == float and other.type == float:
                from .customNodes import Power

                return Power(self, other)

        elif isNumber(other) and self.type == float:
            if other == 2:
                from .nodes import MultiplyFloats

                return MultiplyFloats(self, self)

            from .customNodes import Power

            return Power(self, other)

        return NotImplemented

    def __rpow__(self, other) -> "Node":
        if isNumber(other) and self.type == float:
            from .customNodes import Power

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


def _rect_transform(local_pos, size, anchor_x=0, anchor_y=1):
    """Build serializableRectTransform matching Unity format."""
    x, y, z = local_pos.get("x", 0), local_pos.get("y", 0), local_pos.get("z", 0)
    w, h = size
    return {
        "position": {"x": x, "y": y, "z": z},
        "localPosition": local_pos,
        "anchorMin": {"x": anchor_x, "y": anchor_y},
        "anchorMax": {"x": anchor_x, "y": anchor_y},
        "sizeDelta": {"x": w, "y": h},
    }


def _default_line():
    """Line structure matching Unity - points filled by UpdateLine at runtime."""
    return {
        "capStart": {
            "active": False,
            "shape": 3,
            "size": 5,
            "color": CAP_COLOR,
            "angleOffset": 0,
        },
        "capEnd": {
            "active": False,
            "shape": 3,
            "size": 5,
            "color": CAP_COLOR,
            "angleOffset": 0,
        },
        "ID": "",
        "startWidth": 3,
        "endWidth": 3,
        "dashDistance": 5,
        "color": DEFAULT_CONNECTION_COLOR,
        "points": [],
        "lineStyle": 0,
        "length": 0,
        "animation": {
            "isActive": False,
            "pointsDistance": 90,
            "size": 10,
            "color": {"r": 0.3, "g": 0.89, "b": 0.3, "a": 1},
            "shape": 1,
            "speed": 0,
        },
    }


def AddNode(nodeName, nodeValue="", includePorts=True, position=None):
    node = {}

    if position is None:
        position = Position3(0, 0)

    nodeId = generateId()
    size = NODE_SIZES.get(nodeName, DEFAULT_NODE_SIZE)

    node["serializableRectTransform"] = _rect_transform(position, size)
    node["id"] = nodeName
    node["sID"] = nodeId
    node["modifier"] = nodeValue
    node["defaultColor"] = DEFAULT_NODE_COLOR
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
    if isinstance(portType, tuple):
        port0 = node0.outputPorts[portType[0]]
        port1 = node1.inputPorts[portType[1]]
    else:
        port0 = node0.outputPorts[portType]
        port1 = node1.inputPorts[portType]
    conn_id = generateId()
    connection = {
        "id": f"Connection ({node0.data['id']} - {node1.data['id']})",
        "sID": conn_id,
        "port0InstanceID": 0,
        "port1InstanceID": 0,
        "port0SID": port0["sID"],
        "port1SID": port1["sID"],
        "selectedColor": {"r": 1, "g": 0.58, "b": 0.04, "a": 1},
        "hoverColor": CAP_COLOR,
        "defaultColor": DEFAULT_CONNECTION_COLOR,
        "curveStyle": 3,
        "label": "",
        "line": _default_line(),
        "enableDrag": True,
        "enableHover": True,
        "enableSelect": True,
        "disableClick": False,
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
        if transform["localPosition"] != Position3(0, 0):
            continue
        transform["localPosition"] = Position3(x, y)
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
            if transform["localPosition"] != Position3(0, 0):
                continue
            transform["localPosition"] = Position3(currentX, currentY)
            currentY += offsetY

        currentX += offsetX


def updateConnectionLinePoints():
    """No-op: minimal serialization format does not include connection line points."""
    pass


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


def SaveData(
    filePath,
    layout: Literal["auto", "grid", "single", "hidden", None] = "auto",
    pruneUnusedNodes=True,
    keepPosition=True,
):
    if pruneUnusedNodes:
        removeUnusedNodes()

    match layout:
        case "auto":
            autoLayout()
        case "grid":
            gridLayout()
        case "single":
            for node in data["serializableNodes"]:
                transform = node["serializableRectTransform"]
                if transform["localPosition"] != Position3(0, 0) and keepPosition:
                    continue
                transform["localPosition"] = Position3(0, 0)
        case "hidden":
            for node in data["serializableNodes"]:
                transform = node["serializableRectTransform"]
                if transform["localPosition"] != Position3(0, 0) and keepPosition:
                    continue
                transform["localPosition"] = Position3(9999, 9999)
                transform["scale"] = Position3(0, 0)

    updateConnectionLinePoints()

    with open(filePath, "w") as f:
        json.dump(data, f, separators=(",", ":"))
