# AIA Game Library

A Python library for creating AI bots for AIA's game collection. This library allows you to programmatically create node-based AI logic that can be exported and used in Unity games.

## Installation

This library requires Python 3.7+. Simply place the `AIGameLibrary` folder in your project directory and import it:

```python
from AIGameLibrary import *
```

## Quick Start

Here's a simple example for Slime Volleyball:

```python
from AIGameLibrary import *

# Initialize the slime with name, color, country, and stats (speed, acceleration, jump)
InitializeSlime("AIA", "Yellow", "United States of America", 5, 3, 2)

# Calculate a position offset from the team spawn
positionSign = RelativePosition(Self.TeamSpawn, "Backward")

# Calculate where to move (ball position + offset)
moveTo = Ball.Position + positionSign * 0.4

# Calculate distance to ball and jump condition
distanceToBall = Distance(Ball.Position, Self.Position)
jumpCondition = distanceToBall < 2.25

# Control the slime (target position, jump condition)
SlimeController(moveTo, jumpCondition)

# Save the AI data to a file
SaveData("SlimeVolleyball/AIComp_Data/Saves/AIA python.txt", "grid")
```

## Core Concepts

### Nodes

The library uses a node-based system where operations return `Node` objects. Nodes can be combined using Python operators:

- **Arithmetic**: `+`, `-`, `*`, `/`, `//`, `%`, `**`
- **Comparison**: `<`, `<=`, `>`, `>=`, `==`, `!=`
- **Boolean**: `&` (and), `|` (or), `^` (xor), `~` (not)

Example:
```python
distance = Distance(Ball.Position, Self.Position)
shouldJump = distance < 2.5  # Returns a Node representing the comparison
```

### Vector Operations

Vector3 nodes support component access and operations:

```python
# Access vector components
ballPos = Ball.Position
x = ballPos.x  # X component
y = ballPos.y  # Y component
z = ballPos.z  # Z component

# Vector arithmetic
offset = Ball.Position - Self.Position
scaled = offset * 0.5
```

## Complete Node Reference

Node configurations determine which nodes are available in the Unity editor. Each configuration has a specific purpose. Expand the lists below to see nodes by configuration.

---

<details>
<summary><strong>Default</strong></summary>

**Description:** General purpose nodes for Slime Volleyball, AIALander Survival, and other games. Includes arithmetic, vectors, logic, variables, and debug tools.

<details>
<summary>Basic Types</summary>

- **`Float(value)`** - Represents a real number
  - Input: `value` (int, float, or str)
  - Output: Float

- **`Bool(value)`** - Represents a true/false or "boolean" value
  - Input: `value` (bool)
  - Output: Bool

- **`String(value)`** - Represents a text value
  - Input: `value` (str)
  - Output: String

- **`Color(value)`** - Outputs the color value selected in the dropdown
  - Output: Color

- **`Country(value)`** - Outputs the country value selected in the dropdown
  - Output: Country

</details>

<details>
<summary>Arithmetic Operations</summary>

- **`AddFloats(a, b)`** or `a + b` - Performs an addition operation between two numbers
  - Inputs: Float, Float
  - Output: Float

- **`SubtractFloats(a, b)`** or `a - b` - Performs a subtract operation between two numbers
  - Inputs: Float, Float
  - Output: Float

- **`MultiplyFloats(a, b)`** or `a * b` - Performs a multiplication operation between two numbers
  - Inputs: Float, Float
  - Output: Float

- **`DivideFloats(a, b)`** or `a / b` - Performs a divide operation between two numbers
  - Inputs: Float, Float
  - Output: Float

- **`Modulo(a, b)`** or `a % b` - Divides a number by another number and returns any remainder
  - Inputs: Float, Float
  - Output: Float

- **`ClampFloat(value, min, max)`** - Limits or "clamps" a number between a minimum and maximum value
  - Inputs: Float, Float, Float
  - Output: Float

- **`RandomFloat(min, max)`** - Returns a random number value between two values (changes every Update)
  - Inputs: Float, Float
  - Output: Float

</details>

<details>
<summary>Math Functions</summary>

- **`Abs(x)`** or `AbsFloat(x)` - Convert a number to its unsigned or absolute value
  - Input: Float
  - Output: Float

- **`Operation(x)`** - Performs the selected operation on the input number (Abs, Round, Floor, Ceil, Sin, Cos, Tan, Sqrt, etc.)
  - Input: Float
  - Output: Float

</details>

<details>
<summary>Vector Operations</summary>

- **`AddVector3(a, b)`** or `a + b` - Adds two three-dimensional vectors to each other
  - Inputs: Vector3, Vector3
  - Output: Vector3

- **`SubtractVector3(a, b)`** or `a - b` - Performs a subtract operation between two Vector3's
  - Inputs: Vector3, Vector3
  - Output: Vector3

- **`ScaleVector3(vec, scalar)`** or `vec * scalar` - Multiplies a Vector3 by a number
  - Inputs: Vector3, Float
  - Output: Vector3

- **`DotProduct(a, b)`** or `a @ b` - Returns the dot product between two inputs. 1 = same direction, 0 = perpendicular, -1 = opposite direction
  - Inputs: Vector3, Vector3
  - Output: Float

- **`CrossProduct(a, b)`** - Calculates the cross product of two Vector3. Result is perpendicular to both inputs
  - Inputs: Vector3, Vector3
  - Output: Vector3

- **`Magnitude(vec)`** - Returns the length of the input Vector
  - Input: Vector3
  - Output: Float

- **`Normalize(vec)`** - Returns a vector with the same direction as the input but with a magnitude of 1
  - Input: Vector3
  - Output: Vector3

- **`Distance(pos1, pos2)`** - Calculates the distance between two points
  - Inputs: Vector3, Vector3
  - Output: Float

- **`Vector3Split(vec)`** - Splits a Vector3 into its three corresponding x, y, and z values
  - Input: Vector3
  - Output: Float (x), Float (y), Float (z)

- **`Vector3(x, y, z)`** or `ConstructVector3(x, y, z)` - Creates a Vector3 data type from three input numbers
  - Inputs: Float, Float, Float
  - Output: Vector3

</details>

<details>
<summary>Comparison & Logic Operations</summary>

- **`CompareFloats(a, b, operator)`** or `a < b`, `a > b`, etc. - Evaluates two float values against the operation selected in the dropdown
  - Inputs: Float, Float
  - Output: Bool

- **`CompareBool(a, b, operator)`** - Evaluates two boolean values against the operation selected in the dropdown
  - Inputs: Bool, Bool
  - Output: Bool

- **`Not(condition)`** or `~condition` - Toggles the value of the input boolean (TRUE↔FALSE)
  - Input: Bool
  - Output: Bool

- **`ConditionalSetFloat(condition, trueValue, falseValue)`** - Evaluates the input bool to toggle between two different number values
  - Inputs: Bool, Float, Float
  - Output: Float

- **`ConditionalSetVector3(condition, trueValue, falseValue)`** - Evaluates the input bool to toggle between two different Vector3 values
  - Inputs: Bool, Vector3, Vector3
  - Output: Vector3

- **`ConditionalSetBool(condition, trueValue, falseValue)`** - Evaluates the input bool to toggle between two different boolean values
  - Inputs: Bool, Bool, Bool
  - Output: Bool

</details>

<details>
<summary>Variables & Utilities</summary>

- **`SetVariable(value)`** - Saves the input value so that it can be used by any GetVariable nodes with a corresponding typed value
  - Input: Any
  - Output: None (destination node)

- **`GetVariable(name)`** - Outputs the value from the corresponding SetVariable node with the same typed value
  - Output: Any

- **`Relay(value)`** - Passes through data from input to output. Useful for organizing connections and keeping the graph readable
  - Input: Any
  - Output: Any

- **`IsNull(value)`** - Checks if the input is a null value
  - Input: Any
  - Output: Bool

- **`Keypress(key)`** - Indicates whether the selected key is currently pressed
  - Output: Bool

- **`RelativePosition(transform, direction)`** - Gets the world position relative to the input Transform and based on the selected option
  - Input: Transform
  - Output: Vector3

</details>

<details>
<summary>Debug & Visualization</summary>

- **`Debug(value)`** - Displays the real-time value of the output connection
  - Input: Any
  - Output: None (destination node)

- **`DebugDrawLine(start, end, width, color)`** - Draws a 2D line in worldspace. Useful for debugging and visualizing information
  - Inputs: Vector3, Vector3, Float, Color
  - Output: None (destination node)

- **`DebugDrawDisc(center, radius, height, color)`** - Draws a 2D disc in worldspace on the XY plane
  - Inputs: Vector3, Float, Float, Color
  - Output: None (destination node)

- **`TimePlot(name, color, iconUrl, value)`** - Adds a value to the time plot graph during a simulation (toggle with F1)
  - Inputs: String, Color, String, Float
  - Output: None (destination node)

</details>

<details>
<summary>Organization</summary>

- **`Region`** - Groups nodes visually for organization. Does not affect logic.
  - No inputs/outputs

</details>

</details>

---

<details>
<summary><strong>AIALander - Survival</strong></summary>

**Description:** Nodes for the AIALander Survival game mode. Control Aialander characters with pathfinding, states, emotes, and survival-specific data access.

<details>
<summary>Controller & Properties</summary>

- **`SurvivalController(targetPosition, state, sprint, emote)`** - Controls an Aialander's brain. Navigation uses pathfinding to find the nearest viable point to the input target position
  - Inputs: Vector3 (target), SurvivalState, Bool (sprint), SurvivalEmote (optional)
  - Output: None (destination node)

- **`ConstructSurvivalProperties(...)`** - Sets cosmetic options for this Aialander (name, country, skin color, body style, hair, etc.)
  - Inputs: String, Country, Color, Float, Float, Color, Float, String (outfit URL)
  - Output: None (destination node)

</details>

<details>
<summary>Data Access</summary>

- **`SurvivalGetTransform(value)`** - Selection of Transform options representing current locations in the simulation
  - Output: Transform

- **`SurvivalGetFloat(value)`** - Selection of global number-based options representing current parameters in the simulation
  - Output: Float

- **`SurvivalGetBool(value)`** - Selection of global True/False options representing current parameters in the simulation
  - Output: Bool

</details>

<details>
<summary>States & Emotes</summary>

- **`SurvivalState(value)`** - Selection of states Aialanders can be in. States determine what automatic behaviors Aialanders take
  - Output: SurvivalState

- **`SurvivalEmote(value)`** - Selection of emotes Aialanders can perform
  - Output: SurvivalEmote

- **`SurvivalAutoPosition(state)`** - Automatically decide where to move an Aialander based on predetermined rules for a given state
  - Input: SurvivalState
  - Output: Vector3

- **`ConditionalSetSurvivalState(condition, trueValue, falseValue)`** - Evaluates the input bool to toggle between two different state values
  - Inputs: Bool, SurvivalState, SurvivalState
  - Output: SurvivalState

- **`ConditionalSetSurvivalEmote(condition, trueValue, falseValue)`** - Evaluates the input bool to toggle between two different emote values
  - Inputs: Bool, SurvivalEmote, SurvivalEmote
  - Output: SurvivalEmote

</details>

</details>

---

### Slime Volleyball Specific Nodes

<details>
<summary><strong>Game Entity Access</strong></summary>

The library provides pre-defined game entities for Slime Volleyball:

- **`Self`** - Your player entity
  - `Self.Position` - Current position (Vector3)
  - `Self.Velocity` - Current velocity (Vector3)
  - `Self.CanJump` - Whether the player can jump (Bool)
  - `Self.TeamSpawn` - Team spawn transform
  - `Self.Score` - Team score (Float)

- **`Opponent`** - The opponent player entity
  - Same properties as `Self`

- **`Ball`** - The ball entity
  - `Ball.Position` - Current position (Vector3)
  - `Ball.Velocity` - Current velocity (Vector3)
  - `Ball.IsSelfSide` - Whether ball is on your side (Bool)
  - `Ball.TouchesRemaining` - Remaining touches (Float)

- **`Game`** - Game state information
  - `Game.DeltaTime` - Time since last frame (Float)
  - `Game.FixedDeltaTime` - Fixed timestep (Float)
  - `Game.Gravity` - Gravity value (Float)
  - `Game.Pi` - Pi constant (Float)
  - `Game.SimulationDuration` - Simulation duration (Float)

</details>

<details>
<summary><strong>Slime Volleyball Specific Functions</strong></summary>

- **`InitializeSlime(name, color, country, speed, acceleration, jump)`**
  - Initializes your slime bot with the specified properties
  - `name`: String name for the bot
  - `color`: Color name (see available colors below)
  - `country`: Country name (see available countries below)
  - `speed`, `acceleration`, `jump`: Numeric stat values
  - Output: None (side effect)

- **`SlimeController(targetPosition, jumpCondition)`**
  - Controls the slime's movement
  - `targetPosition`: Vector3 Node representing where to move
  - `jumpCondition`: Bool Node representing when to jump
  - Output: None (side effect)

- **`ConstructSlimeProperties(name, color, country, speedStat, accelerationStat, jumpStat)`**
  - Low-level function to construct slime properties
  - Inputs: String, Color, Country, Stat, Stat, Stat
  - Output: None (side effect)

- **`GetVector3(value)`** - Gets Vector3 data from the game
  - Available values: `"Self Position"`, `"Self Velocity"`, `"Ball Position"`, `"Ball Velocity"`, `"Opponent Position"`, `"Opponent Velocity"`
  - Output: Vector3

- **`GetBool(value)`** - Gets boolean data from the game
  - Available values: `"Self Can Jump"`, `"Opponent Can Jump"`, `"Ball Is Self Side"`
  - Output: Bool

- **`GetFloat(value)`** - Gets float data from the game
  - Available values: `"Delta time"`, `"Fixed delta time"`, `"Gravity"`, `"Pi"`, `"Simulation duration"`, `"Team score"`, `"Opponent score"`, `"Ball touches remaining"`
  - Output: Float

- **`GetTransform(value)`** - Gets transform data from the game
  - Available values: `"Self"`, `"Opponent"`, `"Ball"`, `"Self Team Spawn"`, `"Opponent Team Spawn"`
  - Output: Transform

- **`RelativePosition(transform, direction)`** - Gets a relative position vector
  - `transform`: Transform node
  - `direction`: One of `"Self"`, `"Self + Forward"`, `"Self + Backward"`, `"Self + Left"`, `"Self + Right"`, `"Self + Up"`, `"Self + Down"`, `"Forward"`, `"Backward"`, `"Left"`, `"Right"`, `"Up"`, `"Down"`
  - Output: Vector3

- **`Stat(value)`** - Creates a stat node (used for slime stats)
  - Input: `value` (int or str)
  - Output: Stat

- **`Color(value)`** - Creates a color node
  - Available colors: `"Black"`, `"Blue"`, `"Brown"`, `"Green"`, `"Hot Pink"`, `"Light Blue"`, `"Light Grey"`, `"Medium Grey"`, `"Orange"`, `"Pink"`, `"Purple"`, `"Red"`, `"White"`, `"Yellow"`
  - Output: Color

- **`Country(value)`** - Creates a country node
  - Available countries: `"Andorra"`, `"Argentina"`, `"Armenia"`, `"Australia"`, `"Austria"`, `"Bangladesh"`, `"Belarus"`, `"Belgium"`, `"Brazil"`, `"Canada"`, `"Chile"`, `"China"`, `"Colombia"`, `"Croatia"`, `"Cuba"`, `"Czechia"`, `"DR Congo"`, `"Denmark"`, `"Egypt"`, `"Ethiopia"`, `"Finland"`, `"France"`, `"Germany"`, `"Guatemala"`, `"India"`, `"Indonesia"`, `"Iran"`, `"Iraq"`, `"Ireland"`, `"Israel"`, `"Italy"`, `"Japan"`, `"Jordan"`, `"Kenya"`, `"Latvia"`, `"Malaysia"`, `"Mexico"`, `"Myanmar"`, `"Netherlands"`, `"New Zealand"`, `"Nigera"`, `"Norway"`, `"Oman"`, `"Pakistan"`, `"Palestine"`, `"Philippines"`, `"Poland"`, `"Portugal"`, `"Puerto Rico"`, `"Qatar"`, `"Romania"`, `"Russia"`, `"Slovakia"`, `"Slovenia"`, `"Somolia"`, `"South Africa"`, `"South Korea"`, `"Spain"`, `"Sweden"`, `"Switzerland"`, `"Syria"`, `"Tanzania"`, `"Thailand"`, `"Turkey"`, `"Ukraine"`, `"Unite Arab Emirates"`, `"United Kingdom"`, `"United States of America"`, `"Vietnam"`, `"Yemen"`
  - Output: Country

</details>

---

## Saving Your AI

<details>
<summary><strong>SaveData Function</strong></summary>

- **`SaveData(filePath, layout="auto", pruneUnusedNodes=True, keepPosition=True)`**
  - Saves the AI data to a JSON file that can be imported into Unity
  - `filePath`: Path to save the file
  - `layout`: Layout mode
    - `"auto"` - Topological layout (recommended)
    - `"grid"` - Grid-based layout
    - `"single"` - All nodes at origin
    - `"hidden"` - Nodes positioned off-screen
    - `None` - No layout changes
  - `pruneUnusedNodes`: Remove nodes that aren't connected (default: True)
  - `keepPosition`: Preserve manually set node positions (default: True)

</details>

## Example: Advanced Bot

```python
from AIGameLibrary import *

# Initialize bot
InitializeSlime("MyBot", "Blue", "Canada", 6, 4, 3)

# Calculate direction to ball
directionToBall = Ball.Position - Self.Position
distanceToBall = Magnitude(directionToBall)

# Normalize direction and add offset
normalizedDir = Normalize(directionToBall)
targetOffset = normalizedDir * 0.3
moveTo = Ball.Position + targetOffset

# Jump when close to ball and ball is above us
ballAbove = Ball.Position.y > Self.Position.y
closeToBall = distanceToBall < 2.0
jumpCondition = closeToBall & ballAbove

# Control the slime
SlimeController(moveTo, jumpCondition)

# Save with auto layout
SaveData("my_bot.txt", "auto")
```

## Tips

1. **Use Python operators**: Instead of calling `AddFloats(a, b)`, use `a + b` for cleaner code
2. **Node caching**: Functions automatically cache nodes with the same inputs for efficiency
3. **Layout options**: Use `"auto"` for clean topological layouts, `"grid"` for grid-based layouts
4. **Debugging**: Use `Debug(value)` to inspect node values during development
5. **Vector components**: Access vector components via `.x`, `.y`, `.z` properties on Vector3 nodes

## File Output

The `SaveData` function generates a JSON file that can be imported into Unity for use in AIA's games. The file contains all the node connections and logic you've defined in Python.
