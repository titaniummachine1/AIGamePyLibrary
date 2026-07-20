from AIGamePyLibrary import *

InitializeSoccer(
    "AIA",
    "United States of America",
    Vector3(Float(0), Float(0), Float(0)),
    Vector3(Float(1), Float(0), Float(0)),
    Vector3(Float(2), Float(0), Float(0)),
    Vector3(Float(3), Float(0), Float(0)),
)

move = RelativePosition(SoccerGetTransform("Ball"), "Self")
sprint = Bool(False)
interact = Bool(False)

SoccerController1(sprint, move, interact)
SoccerController2(sprint, move, interact)
SoccerController3(sprint, move, interact)
SoccerController4(sprint, move, interact)

SaveData(GetSoccerSavePath("SoccerExample"), "auto")
