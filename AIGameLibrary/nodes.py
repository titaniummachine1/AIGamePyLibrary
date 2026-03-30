import numbers
from typing import Literal

from .data import colorNames, countryNames
from .lib import AddNode, ConnectPorts, Node, SaveData, data
from .utils import Color, GetSurvivalSavePath, Position3


def parseLiteral(value):
    if isinstance(value, Node):
        return value

    elif isinstance(value, bool):
        return Bool(value)

    elif isinstance(value, numbers.Number):
        return Float(value)

    elif isinstance(value, str):
        if value in colorNames.__args__:
            return Color(value)
        elif value in countryNames.__args__:
            return Country(value)
        else:
            return String(value)

    return value


def cache(function):
    cachedNodes = {}

    def wrapper(*args, **kwargs):
        disableCache = kwargs.pop("disableCache", False)
        # Include both args and kwargs in cache key (kwargs sorted for determinism)
        cacheArgs = (
            tuple(hash(arg) for arg in args),
            tuple((k, hash(v)) for k, v in sorted(kwargs.items())),
        )

        if disableCache:
            return function(*args, **kwargs)

        if cacheArgs not in cachedNodes:
            cachedNodes[cacheArgs] = function(*args, **kwargs)

        return cachedNodes[cacheArgs]

    wrapper.cacheStore = cachedNodes
    return wrapper


class GameEntity:
    def __init__(self, entityType: str):
        self.entityType = entityType

    @property
    def Position(self) -> Node:
        return GetVector3(f"{self.entityType} Position")

    @property
    def Velocity(self) -> Node:
        return GetVector3(f"{self.entityType} Velocity")

    @property
    def Transform(self) -> Node:
        return GetTransform(self.entityType)


class PlayerEntity(GameEntity):
    @property
    def CanJump(self) -> Node:
        return GetBool(f"{self.entityType} Can Jump")

    @property
    def TeamSpawn(self) -> Node:
        return GetTransform(f"{self.entityType} Team Spawn")

    @property
    def Score(self) -> Node:
        if self.entityType == "Self":
            return GetFloat("Team score")
        if self.entityType == "Opponent":
            return GetFloat("Opponent score")


class BallClass(GameEntity):
    def __init__(self):
        super().__init__("Ball")

    @property
    def IsSelfSide(self) -> Node:
        return GetBool("Ball Is Self Side")

    @property
    def TouchesRemaining(self) -> Node:
        return GetFloat("Ball touches remaining")


class GameClass:
    @property
    def DeltaTime(self) -> Node:
        return GetFloat("Delta time")

    @property
    def FixedDeltaTime(self) -> Node:
        return GetFloat("Fixed delta time")

    @property
    def Gravity(self) -> Node:
        return GetFloat("Gravity")

    @property
    def Pi(self) -> Node:
        return GetFloat("Pi")

    @property
    def SimulationDuration(self) -> Node:
        return GetFloat("Simulation duration")


Self = PlayerEntity("Self")
Opponent = PlayerEntity("Opponent")
Ball = BallClass()
Game = GameClass()


def And(node0: Node, node1: Node) -> Node:
    return CompareBool(node0, node1, "and")


def Or(node0: Node, node1: Node) -> Node:
    return CompareBool(node0, node1, "or")


def Xor(node0: Node, node1: Node) -> Node:
    return CompareBool(node0, node1, "xor")


def Equal(node0: Node, node1: Node) -> Node:
    """Bool comparison"""
    return CompareBool(node0, node1, "equal to")


def Abs(node: Node) -> Node:
    return Operation(node, "abs")


def AbsFloat(node: Node) -> Node:
    """Alias for Abs - converts a number to its absolute value."""
    return Abs(node)


def Round(node: Node) -> Node:
    return Operation(node, "round")


def Floor(node: Node) -> Node:
    return Operation(node, "floor")


def Ceil(node: Node) -> Node:
    return Operation(node, "ceil")


def Sin(node: Node) -> Node:
    return Operation(node, "sin")


def Cos(node: Node) -> Node:
    return Operation(node, "cos")


def Tan(node: Node) -> Node:
    return Operation(node, "tan")


def Asin(node: Node) -> Node:
    return Operation(node, "asin")


def Acos(node: Node) -> Node:
    return Operation(node, "acos")


def Atan(node: Node) -> Node:
    return Operation(node, "atan")


def Sqrt(node: Node) -> Node:
    return Operation(node, "sqrt")


def Sign(node: Node) -> Node:
    return Operation(node, "sign")


def Ln(node: Node) -> Node:
    return Operation(node, "ln")


def Log10(node: Node) -> Node:
    return Operation(node, "log10")


def Exp(node: Node) -> Node:
    """e^x"""
    return Operation(node, "e^")


def Pow10(node: Node) -> Node:
    """10^x"""
    return Operation(node, "10^")


@cache
def InitializeSlime(
    name, color: colorNames, country: countryNames, speed, acceleration, jump
):
    speedNode = Stat(speed)
    accelerationNode = Stat(acceleration)
    jumpNode = Stat(jump)

    ConstructSlimeProperties(
        name, color, country, speedNode, accelerationNode, jumpNode
    )


@cache
def InitializeSurvival(
    name: str,
    country: countryNames,
    skin: colorNames,
    body_style: int | float,
    hair_style: int | float,
    hair_color: colorNames,
    facial_hair: int | float,
    custom_texture: str,
):
    """Initialize survival character with cosmetic properties. Sets up an Aialander for the Survival game. All parameters are required."""
    ConstructSurvivalProperties(
        String(name),
        Country(country),
        Color(skin),
        Float(body_style),
        Float(hair_style),
        Color(hair_color),
        Float(facial_hair),
        String(custom_texture),
    )


@cache
def InitializeParking(
    name: str,
    country: countryNames,
    skin_color: colorNames,
    body_style: int | float,
    hair_style: int | float,
    hair_color: colorNames,
    facial_hair_style: int | float,
    car_color: colorNames,
    custom_texture: str,
):
    """Initialize parking car and driver cosmetics for the Parking simulation."""
    ConstructModularUniformProperties(
        String(name),
        Country(country),
        Color(skin_color),
        Float(body_style),
        Float(hair_style),
        Color(hair_color),
        Float(facial_hair_style),
        Color(car_color),
        String(custom_texture),
    )


@cache
def AddVector3(node0: Node, node1: Node):
    baseNode = AddNode("AddVector3")
    inputTypes = ["Vector3", "Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def AddFloats(node0: Node, node1: Node):
    baseNode = AddNode("AddFloats")
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def Bool(value: bool):
    return AddNode("Bool", "0" if value else "1")


@cache
def ClampFloat(node0: Node, node1: Node, node2: Node):
    baseNode = AddNode("ClampFloat")
    inputTypes = ["Float", "Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2])
    return baseNode


@cache
def Color(value: colorNames):
    return AddNode("Color", value)


@cache
def Vector3(node0: Node, node1: Node, node2: Node):
    baseNode = AddNode("ConstructVector3")
    inputTypes = ["Float", "Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2])
    return baseNode


@cache
def CompareBool(
    node0: Node,
    node1: Node,
    value: Literal["and", "or", "equal to", "xor", "nor", "nand", "xnor"] = "and",
):
    value = ["and", "or", "equal to", "xor", "nor", "nand", "xnor"].index(value)
    baseNode = AddNode("CompareBool", value)
    inputTypes = ["Bool", "Bool"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def CompareFloats(
    node0: Node, node1: Node, value: Literal["==", "<", ">", "<=", ">="] = "=="
):
    value = ["==", "<", ">", "<=", ">="].index(value)
    baseNode = AddNode("CompareFloats", value)
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def ConditionalSetBool(node0: Node, node1: Node, node2: Node, value: bool = True):
    baseNode = AddNode("ConditionalSetBool", "0" if value else "1")
    inputTypes = ["Bool", "Bool", "Bool"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2])
    return baseNode


@cache
def ConditionalSetFloat(node0: Node, node1: Node, node2: Node, value: bool = True):
    baseNode = AddNode("ConditionalSetFloatV2", "0" if value else "1")
    inputTypes = ["Bool", "Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2])
    return baseNode


@cache
def ConditionalSetSurvivalEmote(node0: Node, node1: Node, node2: Node, value: bool = True):
    baseNode = AddNode("ConditionalSetSurvivalEmote", "0" if value else "1")
    inputTypes = ["Bool", "SurvivalEmote", "SurvivalEmote"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2])
    return baseNode


@cache
def ConditionalSetSurvivalState(node0: Node, node1: Node, node2: Node, value: bool = True):
    baseNode = AddNode("ConditionalSetSurvivalState", "0" if value else "1")
    inputTypes = ["Bool", "SurvivalState", "SurvivalState"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2])
    return baseNode


@cache
def ConditionalSetVector3(node0: Node, node1: Node, node2: Node, value: bool = True):
    baseNode = AddNode("ConditionalSetVector3", "0" if value else "1")
    inputTypes = ["Bool", "Vector3", "Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2])
    return baseNode


@cache
def ConstructSlimeProperties(
    node0: Node,
    node1: colorNames,
    node2: countryNames,
    node3: Node,
    node4: Node,
    node5: Node,
):
    baseNode = AddNode("ConstructSlimeProperties")
    inputTypes = ["String", "Color", "Country", "Stat", "Stat", "Stat"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2, node3, node4, node5])
    return baseNode


@cache
def ConstructSurvivalProperties(
    node0: Node,
    node1: countryNames,
    node2: colorNames,
    node3: Node,
    node4: Node,
    node5: colorNames,
    node6: Node,
    node7: Node,
):
    """Sets cosmetic options for an Aialander. Inputs: name, country, skin color, body style, hair style, hair color, facial hair, outfit URL."""
    baseNode = AddNode("ConstructSurvivalProperties")
    inputTypes = ["String", "Country", "Color", "Float", "Float", "Color", "Float", "String"]
    connectInputNodes(
        baseNode,
        inputTypes,
        [node0, node1, node2, node3, node4, node5, node6, node7],
    )
    return baseNode


@cache
def SlimeController(node0: Node, node1: Node):
    baseNode = AddNode("SlimeController")
    inputTypes = ["Vector3", "Bool"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def Country(value: countryNames):
    return AddNode("Country", value)


@cache
def CrossProduct(node0: Node, node1: Node):
    baseNode = AddNode("CrossProduct")
    inputTypes = ["Vector3", "Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


debugCounter = 0


def Debug(inputData, string: str = None, changePosition=True):
    global debugCounter

    if changePosition:
        # magic numbers for position gotten via
        # snappedX = (20 + x) * 64 - 17
        # snappedY = -(4 + y) * 64 - 22
        xPos = 1263 - 64 * 6
        yPos = -278 - 64 * 4 * debugCounter
        baseNode = AddNode("Debug", position=Position3(xPos, yPos - 55))
        data["serializableNodes"][-1]["serializablePorts"][0][
            "serializableRectTransform"
        ]["scale"] = Position3(0, 0)
        if string is not None:
            AddNode(
                "String", string, includePorts=False, position=Position3(xPos, yPos)
            )

    else:
        baseNode = AddNode("Debug")
        if string is not None:
            AddNode("String", string, includePorts=False)

    debugCounter += 1

    if isinstance(inputData, tuple):
        inputNode = parseLiteral(inputData[0])
        num = inputData[1]
    else:
        inputNode = parseLiteral(inputData)
        num = inputNode.outputIndex

    ports = [
        port["id"]
        for port in inputNode.data["serializablePorts"]
        if port["polarity"] != 0
    ]
    portName = ports[num - 1]
    ConnectPorts((portName, "Any1"), inputNode, baseNode)
    data["serializableConnections"][-1]["line"]["startWidth"] = 0  # invisible line

    return baseNode


def DebugDrawLine(node0: Node, node1: Node, node2: Node, node3: colorNames):
    baseNode = AddNode("DebugDrawLine")
    inputTypes = ["Vector3", "Vector3", "Float", "Color"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2, node3])
    return baseNode


def DebugDrawDisc(node0: Node, node1: Node, node2: Node, node3: colorNames):
    baseNode = AddNode("DebugDrawDisc")
    inputTypes = ["Vector3", "Float", "Float", "Color"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2, node3])
    return baseNode


def TimePlot(
    node0: Node,
    node1: colorNames,
    node2: Node,
    node3: Node,
):
    """Adds a value to the time plot graph during a simulation (toggle with F1). Inputs: name, color, iconUrl, value."""
    baseNode = AddNode("TimePlot")
    inputTypes = ["String", "Color", "String", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2, node3])
    return baseNode


@cache
def Distance(node0: Node, node1: Node):
    baseNode = AddNode("Distance")
    inputTypes = ["Vector3", "Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def DivideFloats(node0: Node, node1: Node):
    baseNode = AddNode("DivideFloats")
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def DotProduct(node0: Node, node1: Node):
    baseNode = AddNode("DotProduct")
    inputTypes = ["Vector3", "Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def Float(value: int | float | str):
    return AddNode("Float", str(value))


@cache
def GetVariable(name: str):
    """Outputs the value from the corresponding SetVariable node with the same variable name."""
    return AddNode("GetVariable", name)


@cache
def IsNull(node0: Node):
    """Checks if the input is a null value."""
    baseNode = AddNode("IsNull")
    inputTypes = ["Any"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


@cache
def Keypress(value: int):
    """Indicates whether the selected key is currently pressed. Pass key index (0-based)."""
    return AddNode("Keypress", str(value))


@cache
def GetBool(value: Literal["Self Can Jump", "Opponent Can Jump", "Ball Is Self Side"]):
    value = ["Self Can Jump", "Opponent Can Jump", "Ball Is Self Side"].index(value)
    return AddNode("VolleyballGetBool", value)


@cache
def GetFloat(
    value: Literal[
        "Delta time",
        "Fixed delta time",
        "Gravity",
        "Pi",
        "Simulation duration",
        "Team score",
        "Opponent score",
        "Ball touches remaining",
    ],
):
    value = [
        "Delta time",
        "Fixed delta time",
        "Gravity",
        "Pi",
        "Simulation duration",
        "Team score",
        "Opponent score",
        "Ball touches remaining",
    ].index(value)
    return AddNode("VolleyballGetFloat", value)


@cache
def GetTransform(
    value: Literal[
        "Self", "Opponent", "Ball", "Self Team Spawn", "Opponent Team Spawn"
    ],
):
    value = [
        "Self",
        "Opponent",
        "Ball",
        "Self Team Spawn",
        "Opponent Team Spawn",
    ].index(value)
    return AddNode("VolleyballGetTransform", value)


@cache
def GetVector3(
    value: Literal[
        "Self Position",
        "Self Velocity",
        "Ball Position",
        "Ball Velocity",
        "Opponent Position",
        "Opponent Velocity",
    ],
):
    value = [
        "Self Position",
        "Self Velocity",
        "Ball Position",
        "Ball Velocity",
        "Opponent Position",
        "Opponent Velocity",
    ].index(value)
    return AddNode("SlimeGetVector3", value)


@cache
def Magnitude(node0: Node):
    baseNode = AddNode("Magnitude")
    inputTypes = ["Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


@cache
def Modulo(node0: Node, node1: Node):
    baseNode = AddNode("Modulo")
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def MultiplyFloats(node0: Node, node1: Node):
    baseNode = AddNode("MultiplyFloats")
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def Not(node0: Node):
    baseNode = AddNode("Not")
    inputTypes = ["Bool"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


@cache
def Normalize(node0: Node):
    baseNode = AddNode("Normalize")
    inputTypes = ["Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


@cache
def Operation(
    node0: Node,
    value: Literal[
        "abs",
        "round",
        "floor",
        "ceil",
        "sin",
        "cos",
        "tan",
        "asin",
        "acos",
        "atan",
        "sqrt",
        "sign",
        "ln",
        "log10",
        "e^",
        "10^",
    ],
):
    value = [
        "abs",
        "round",
        "floor",
        "ceil",
        "sin",
        "cos",
        "tan",
        "asin",
        "acos",
        "atan",
        "sqrt",
        "sign",
        "ln",
        "log10",
        "e^",
        "10^",
    ].index(value)
    baseNode = AddNode("Operation", value)
    inputTypes = ["Float"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


@cache
def RelativePosition(
    node0: Node,
    value: Literal[
        "Self",
        "Self + Forward",
        "Self + Backward",
        "Self + Left",
        "Self + Right",
        "Self + Up",
        "Self + Down",
        "Forward",
        "Backward",
        "Left",
        "Right",
        "Up",
        "Down",
    ],
):
    value = [
        "Self",
        "Self + Forward",
        "Self + Backward",
        "Self + Left",
        "Self + Right",
        "Self + Up",
        "Self + Down",
        "Forward",
        "Backward",
        "Left",
        "Right",
        "Up",
        "Down",
    ].index(value)
    baseNode = AddNode("RelativePosition", value)
    inputTypes = ["Transform"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


def RandomFloat(node0: Node, node1: Node):
    baseNode = AddNode("RandomFloat")
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


def Region():
    """Groups nodes visually for organization. Does not affect logic."""
    return AddNode("Region", includePorts=True)


@cache
def Relay(node0: Node):
    """Passes through data from input to output. Useful for organizing connections."""
    baseNode = AddNode("Relay")
    inputTypes = ["Any"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


@cache
def ScaleVector3(node0: Node, node1: Node):
    baseNode = AddNode("ScaleVector3")
    inputTypes = ["Vector3", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


class Vector3Components:
    def __init__(self, x: Node, y: Node, z: Node):
        self.x = x
        self.y = y
        self.z = z

    def __getitem__(self, index):
        return [self.x, self.y, self.z][index]


@cache
def Vector3Split(node0: Node):
    baseNode = AddNode("Vector3Split")
    inputTypes = ["Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return Vector3Components(baseNode, Node(baseNode.data, 2), Node(baseNode.data, 3))


@cache
def SetVariable(name: str, value: Node):
    """Saves the input value so that it can be used by GetVariable nodes with the same variable name."""
    baseNode = AddNode("SetVariable", name)
    inputTypes = ["Any"]
    connectInputNodes(baseNode, inputTypes, [value])
    return baseNode


@cache
def Stat(value: int | str):
    return AddNode("Stat", str(value))


@cache
def String(value: str):
    return AddNode("String", value)


@cache
def SubtractFloats(node0: Node, node1: Node):
    baseNode = AddNode("SubtractFloats")
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def SubtractVector3(node0: Node, node1: Node):
    baseNode = AddNode("SubtractVector3")
    inputTypes = ["Vector3", "Vector3"]
    connectInputNodes(baseNode, inputTypes, [node0, node1])
    return baseNode


@cache
def SurvivalAutoPosition(node0: Node):
    """Automatically decide where to move an Aialander based on predetermined rules for a given state."""
    baseNode = AddNode("SurvivalAutoPosition")
    inputTypes = ["SurvivalState"]
    connectInputNodes(baseNode, inputTypes, [node0])
    return baseNode


@cache
def SurvivalController(node0: Node, node1: Node, node2: Node, node3: Node):
    """Controls an Aialander's brain. Inputs: targetPosition, state, sprint, emote. Use SurvivalEmote(0) for no emote."""
    baseNode = AddNode("SurvivalController")
    inputTypes = ["Vector3", "SurvivalState", "Bool", "SurvivalEmote"]
    connectInputNodes(baseNode, inputTypes, [node0, node1, node2, node3])
    return baseNode


@cache
def SurvivalEmote(value: int):
    """Selection of emotes. 0=None, 1=Hi, 2=Talk, 3=Bored, 4=Wave."""
    return AddNode("SurvivalEmote", str(value))


@cache
def SurvivalGetBool(value: int):
    """Selection of bool options. 0=Is Carrying Resource, 1=Container has Health, 2=Container Was Attacked, 3=Container Was Stolen From, 4=Self Was Attacked."""
    return AddNode("SurvivalGetBool", str(value))


@cache
def SurvivalGetFloat(value: int):
    """Selection of float options (Health %, Hunger %, Stamina %, etc.). See README for full list."""
    return AddNode("SurvivalGetFloat", str(value))


@cache
def SurvivalGetTransform(value: int):
    """Selection of Transform options (Self, Player Nearest, etc.). See README for full list."""
    return AddNode("SurvivalGetTransform", str(value))


@cache
def SurvivalState(value: str):
    """Selection of states. Use enum name: 'Passive', 'Gather', 'Eat', 'Attack', 'Steal', 'Dead'."""
    return AddNode("SurvivalState", value)


class RaycastHitComponents:
    """Multi-output helper for `CarRaycasts` (RaycastHit1..RaycastHit8)."""

    def __init__(self, baseNode: Node):
        self._baseNode = baseNode

    @property
    def RaycastHit1(self) -> Node:
        return Node(self._baseNode.data, 1)

    @property
    def RaycastHit2(self) -> Node:
        return Node(self._baseNode.data, 2)

    @property
    def RaycastHit3(self) -> Node:
        return Node(self._baseNode.data, 3)

    @property
    def RaycastHit4(self) -> Node:
        return Node(self._baseNode.data, 4)

    @property
    def RaycastHit5(self) -> Node:
        return Node(self._baseNode.data, 5)

    @property
    def RaycastHit6(self) -> Node:
        return Node(self._baseNode.data, 6)

    @property
    def RaycastHit7(self) -> Node:
        return Node(self._baseNode.data, 7)

    @property
    def RaycastHit8(self) -> Node:
        return Node(self._baseNode.data, 8)

    def __iter__(self):
        """Allow tuple unpacking: ray1, ..., ray8 = CarRaycasts(sensor)."""
        yield self.RaycastHit1
        yield self.RaycastHit2
        yield self.RaycastHit3
        yield self.RaycastHit4
        yield self.RaycastHit5
        yield self.RaycastHit6
        yield self.RaycastHit7
        yield self.RaycastHit8

    def __len__(self):
        return 8

    def __getitem__(self, index):
        return [
            self.RaycastHit1,
            self.RaycastHit2,
            self.RaycastHit3,
            self.RaycastHit4,
            self.RaycastHit5,
            self.RaycastHit6,
            self.RaycastHit7,
            self.RaycastHit8,
        ][index]


class HitInfoComponents:
    """Multi-output helper for `HitInfo` (WasHit, Distance)."""

    def __init__(self, baseNode: Node):
        # We override `type` so Python operators work (==, <, arithmetic, etc.).
        self._wasHit = Node(baseNode.data, 1)
        self._wasHit.type = bool

        self._distance = Node(baseNode.data, 1)
        self._distance.type = float

    @property
    def WasHit(self) -> Node:
        return self._wasHit

    @property
    def Distance(self) -> Node:
        return self._distance

    def __iter__(self):
        """Allow tuple unpacking: was_hit, distance = HitInfo(raycast_hit)."""
        yield self.WasHit
        yield self.Distance

    def __len__(self):
        return 2

    def __getitem__(self, index):
        return [self.WasHit, self.Distance][index]


@cache
def ModularUniformController(throttle: Node, steering: Node, brake: Node):
    """Destination node: sends throttle/steering/brake to the parking car."""
    baseNode = AddNode("ModularCarController")
    inputTypes = ["Float", "Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [throttle, steering, brake])
    return baseNode


@cache
def ConstructModularUniformProperties(
    name: str,
    country: countryNames,
    skinColor: colorNames,
    bodyStyle: int | float,
    hairStyle: int | float,
    hairColor: colorNames,
    facialHairStyle: int | float,
    carColor: colorNames,
    outfitUrl: str,
):
    """Destination node: sets cosmetic options for the parking car."""
    baseNode = AddNode("UniformModularCarProperties")
    inputTypes = ["String", "Country", "Color", "Float", "Float", "Color", "Float", "Color", "String"]
    connectInputNodes(
        baseNode,
        inputTypes,
        [name, country, skinColor, bodyStyle, hairStyle, hairColor, facialHairStyle, carColor, outfitUrl],
    )
    return baseNode


@cache
def Spherecast(radius: Node, distance: Node):
    """Defines the Spherecast radius/distance used for `CarRaycasts` sensors."""
    baseNode = AddNode("Spherecast")
    inputTypes = ["Float", "Float"]
    connectInputNodes(baseNode, inputTypes, [radius, distance])
    return baseNode


@cache
def CarRaycasts(spherecast: Node) -> RaycastHitComponents:
    """Sends sensors out around the parking car and returns `RaycastHit1..8`."""
    baseNode = AddNode("CarRaycasts")
    inputTypes = ["Spherecast"]
    connectInputNodes(baseNode, inputTypes, [spherecast])
    return RaycastHitComponents(baseNode)


@cache
def HitInfo(raycastHit: Node) -> HitInfoComponents:
    """Extracts bool+distance from a selected `RaycastHit` output."""
    baseNode = AddNode("HitInfo")
    inputTypes = ["RaycastHit"]
    connectInputNodes(baseNode, inputTypes, [raycastHit])
    return HitInfoComponents(baseNode)


@cache
def ParkingGetTransform(value: int):
    """Selection of Transform options for the parking simulation."""
    return AddNode("ParkingGetTransform", str(value))


@cache
def ParkingGetFloat(value: int):
    """Selection of Float options for the parking simulation."""
    return AddNode("ParkingGetFloat", str(value))


@cache
def ParkingGetBool(value: int):
    """Selection of Bool options for the parking simulation."""
    return AddNode("ParkingGetBool", str(value))


def connectInputNodes(baseNode, inputTypes, inputs):
    counters = {}

    for inputType, inputData in zip(inputTypes, inputs):
        num1 = 1

        if isinstance(inputData, Node):
            num1 = inputData.outputIndex

        if isinstance(inputData, tuple):
            inputNode = inputData[0]
            num1 = inputData[1]
        else:
            inputNode = inputData

        inputNode = parseLiteral(inputNode)

        if inputType not in counters:
            counters[inputType] = 1
        num2 = counters[inputType]
        counters[inputType] += 1

        if inputType == "Any":
            # Get actual output port from input node (Float1, Vector31, Bool1, etc.)
            outputPorts = [
                p["id"]
                for p in inputNode.data["serializablePorts"]
                if p["polarity"] != 0
            ]
            portName1 = outputPorts[num1 - 1]
            portName2 = "Any1"
        else:
            portName1 = f"{inputType}{num1}"
            portName2 = f"{inputType}{num2}"
            if isinstance(inputType, tuple):
                portName1 = f"{inputType[0]}{num1}"
                portName2 = f"{inputType[1]}{num2}"

        if inputData is not None:
            ConnectPorts((portName1, portName2), inputNode, baseNode)
