# Aialander PyLib

A Python library for creating AI bots for AIA's game collection. This library allows you to programmatically create node-based AI logic that can be exported and used in Unity games.

> If you are an LLM writing a bot from this README, jump to **[Notes for LLM Authors](#notes-for-llm-authors)** at the bottom first. It explains the mental model, lists the mistakes we keep seeing, and shows a correct minimal script.

## Installation

This library requires Python 3.7+. Place the `AIGameLibrary` folder in your project directory and import it:

```python
from AIGameLibrary import *
```

The GitHub repo is named **`AIGamePyLibrary`** but the importable Python **package** is **`AIGameLibrary`** (no "Py"). A tiny `AIGamePyLibrary` shim package is also installed that re-exports everything, so `from AIGamePyLibrary import *` works too.

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

## Marking your bot as LLM-driven

The car / kart Properties node carries an **`isLLM`** flag that is **not exposed in the Unity inspector** — it can only be set by the PyLib compiler. At runtime Unity reads it from the node's **`modifier`** field during `Initialize()`, writes it onto the resulting properties (`KartProperties` / modular car properties), and applies it to the spawned `Player` (`Player.IsLLM = true`).

To set it, **capture the Properties node** returned by any of the helpers and assign its `modifier` after construction. Accepted values: **`"True"` / `"False"`** or **`"1"` / `"0"`** (anything else falls back to `False`).

```python
from AIGameLibrary import *

# Works for InitializeDemoDerby, InitializeParking, and ConstructModularUniformProperties —
# they all return the same UniformModularCarProperties node.
props = InitializeDemoDerby(
    "MyBot", "United States of America", "Tan",
    0, 0, "Brown", 0, "Red", "",
)
props.data["modifier"] = "True"   # mark this car as LLM-driven
```

`isLLM` is persisted in the saved JSON through the standard `modifier` field, so the graph round-trips through Unity without losing the flag. Equivalent behavior is wired up on the C# side for `ConstructKartProperties` (Kart-style simulations) — same `modifier` accepted values.

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
<summary><strong>Default Nodes</strong></summary>

**Description:** General purpose nodes for all simulations. Includes arithmetic, vectors, logic, variables, and debug tools.

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
  - Options: `"Auburn"`, `"Black"`, `"Blonde"`, `"Blue"`, `"Brown"`, `"Dark Brown"`, `"Dark Green"`, `"Green"`, `"Hot Pink"`, `"Light Blue"`, `"Light Grey"`, `"Medium Grey"`, `"Orange"`, `"Pink"`, `"Purple"`, `"Red"`, `"Tan"`, `"White"`, `"Yellow"`
  - Output: Color

- **`Country(value)`** - Outputs the country value selected in the dropdown
  - Options: `"Unknown"`, `"Afghanistan"`, `"Albania"`, `"Algeria"`, `"Andorra"`, `"Angola"`, `"Argentina"`, `"Armenia"`, `"Australia"`, `"Austria"`, `"Azerbaijan"`, `"Bahamas"`, `"Bahrain"`, `"Bangladesh"`, `"Barbados"`, `"Belarus"`, `"Belgium"`, `"Bermuda"`, `"Bohemia"`, `"Botswana"`, `"Brazil"`, `"Bulgaria"`, `"Burkina Faso"`, `"Burundi"`, `"Cameroon"`, `"Canada"`, `"Chile"`, `"China"`, `"Colombia"`, `"Costa Rica"`, `"Croatia"`, `"Cuba"`, `"Cyprus"`, `"Czechia"`, `"Côte d'Ivoire"`, `"Denmark"`, `"Djibouti"`, `"Dominican Republic"`, `"DR Congo"`, `"Ecuador"`, `"Egypt"`, `"Eritrea"`, `"Estonia"`, `"Ethiopia"`, `"Fiji"`, `"Finland"`, `"France"`, `"Gabon"`, `"Georgia"`, `"Germany"`, `"Ghana"`, `"Greece"`, `"Grenada"`, `"Guatemala"`, `"Guyana"`, `"Haiti"`, `"Hong Kong"`, `"Hungary"`, `"Iceland"`, `"India"`, `"Indonesia"`, `"Iran"`, `"Iraq"`, `"Ireland"`, `"Israel"`, `"Italy"`, `"Jamaica"`, `"Japan"`, `"Jordan"`, `"Kazakhstan"`, `"Kenya"`, `"Kosovo"`, `"Kuwait"`, `"Kyrgyzstan"`, `"Latvia"`, `"Lebanon"`, `"Lithuania"`, `"Luxembourg"`, `"Malaysia"`, `"Mauritius"`, `"Mexico"`, `"Moldova"`, `"Mongolia"`, `"Montenegro"`, `"Morocco"`, `"Mozambique"`, `"Myanmar"`, `"Namibia"`, `"Netherlands"`, `"New Zealand"`, `"Niger"`, `"Nigeria"`, `"North Korea"`, `"North Macedonia"`, `"Norway"`, `"Oman"`, `"Pakistan"`, `"Palestine"`, `"Panama"`, `"Paraguay"`, `"Peru"`, `"Philippines"`, `"Poland"`, `"Portugal"`, `"Puerto Rico"`, `"Qatar"`, `"Romania"`, `"Russia"`, `"Samoa"`, `"San Marino"`, `"Saudi Arabia"`, `"Scotland"`, `"Senegal"`, `"Serbia"`, `"Singapore"`, `"Slovakia"`, `"Slovenia"`, `"Somolia"`, `"South Africa"`, `"South Korea"`, `"Spain"`, `"Sri Lanka"`, `"Sudan"`, `"Suriname"`, `"Sweden"`, `"Switzerland"`, `"Syria"`, `"Taiwan"`, `"Tajikistan"`, `"Tanzania"`, `"Thailand"`, `"Togo"`, `"Tonga"`, `"Trinidad and Tobago"`, `"Tunisia"`, `"Turkey"`, `"Turkmenistan"`, `"Uganda"`, `"Ukraine"`, `"United Arab Emirates"`, `"United Kingdom"`, `"United States of America"`, `"Uruguay"`, `"Uzbekistan"`, `"Venezuela"`, `"Vietnam"`, `"Virgin Islands"`, `"Yemen"`, `"Zambia"`, `"Zimbabwe"`, `"ChatGPT"`, `"Claude"`, `"Deepseek"`, `"Gemini"`, `"Grok"`, `"Llama"`, `"Mistral"`, `"Perplexity"`, `"Qwen"`
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

- **`Operation(x)`** - Performs the selected operation on the input number
  - Options: `abs`, `round`, `floor`, `ceil`, `sin`, `cos`, `tan`, `asin`, `acos`, `atan`, `sqrt`, `sign`, `ln`, `log10`, `e^`, `10^`
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
  - Options: `==`, `<`, `>`, `<=`, `>=`
  - Inputs: Float, Float
  - Output: Bool

- **`CompareBool(a, b, operator)`** - Evaluates two boolean values against the operation selected in the dropdown
  - Options: `AND`, `OR`, `EQUAL TO`, `XOR`, `NOR`, `NAND`, `XNOR`
  - Inputs: Bool, Bool
  - Output: Bool

- **`Not(condition)`** or `~condition` - Toggles the value of the input boolean (TRUE↔FALSE)
  - Input: Bool
  - Output: Bool

- **`ConditionalSetFloat(condition, trueValue, falseValue)`** - Evaluates the input bool to toggle between two different number values
  - Options: `True` (use trueValue when condition is true), `False` (use trueValue when condition is false)
  - Inputs: Bool, Float, Float
  - Output: Float

- **`ConditionalSetVector3(condition, trueValue, falseValue)`** - Evaluates the input bool to toggle between two different Vector3 values
  - Options: `True`, `False` (same as ConditionalSetFloat)
  - Inputs: Bool, Vector3, Vector3
  - Output: Vector3

- **`ConditionalSetBool(condition, trueValue, falseValue)`** - Evaluates the input bool to toggle between two different boolean values
  - Options: `True`, `False` (same as ConditionalSetFloat)
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
  - Options: `Self`, `Self + Forward`, `Self + Backward`, `Self + Left`, `Self + Right`, `Self + Up`, `Self + Down`, `Forward`, `Backward`, `Left`, `Right`, `Up`, `Down`
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
<summary><strong>Survival Simulation</strong></summary>

**Requirements:** The SurvivalController is the required destination to control a single 3d character. ConstructSurvivalProperties sets that character's aesthetic.

**Overview:** Aialanders are trapped on a deserted island with apple trees and other inhabitants. Each Aialander has a storage container they can put food. Tree count and location can vary per simulation. The number of competitors and their stategies will vary per simulation.  The maximum number of total players is 7.

**Objective:** To survive on the island given the available food. Other inhabitants may be friendly or aggressive, you can choose any personality you want. Ending with the highest rank will give you the most clout but it's your decision if that's important to you or not.

<details>
<summary>Customization</summary>

**Body Type**
- `0` Pants and shorts
- `1` Dress
- `2` Robot

**Beard Styles**
- `0` None
- `1` Full trimmed beard

**Hair Styles**
- `0` Curtains
- `1` Caesar
- `2` Bob
- `3` Faux hawk
- `4` Long polytail
- `5` Pebbles
- `6` Side pony
- `7` Samurai side bun
- `8` Undercut
- `9` Medium polytail
- `10` Bowl
- `11` Space buns
- `12` Samurai bun
- `13` Bald

**Custom Outfit**
The properties node has a custom outfit at the bottom that can take a URL string to an image. You can upload the image to something like imgur and then copy the image URL.

If you want, here's the PSD to make a custom outfit texture for your character:
https://github.com/theaia/AIGamePyLibrary/blob/main/CustomOutfit.psd

</details>

<details>
<summary>Container Information</summary>

**Health**
- Each player starts with a designated container with 250 health.
- Containers do not regenerate health.
- When a container's health reaches 0 it will be destroyed along with any food stored in it.

**Terrain**
- Terrain has an approximate diameter of 160.
- For the competition the seed will be random—you may be the closest one to a tree, or the furthest.
- I'll be running the sim with both abundant and scarce resources. Adjust your strategy appropriately.
- After being harvested, fruit respawn after 190 seconds. Each tree starts with and has a maximum of 3 fruit.

</details>

<details>
<summary>Ranking</summary>

Players are sorted by Survival Time, then Most Health, then Hunger, then stored apple count. When a player dies, their survival time stops at the time they die.

</details>

<details>
<summary>Player Information</summary>

**Abilities**
- Standard move speed is 5.
- Sprinting increases player speed 9. Players must have available stamina to sprint.
- Attacking deals 10 damage per hit and consumes 5 stamina. Players must have enough stamina to attack. Attack range is 2. Attack radius is 1 in the forward direction of the player. Attacking while holding food will drop the food.
- Players will drop food they are holding when they die.
- Emoting will stop all movement and cause the player to perform a looping animation until their emote state is set to "None".

**Health**
- Players all start with 100 health.
- Players will regenerate 1 health per Tick after they've not taken damage for 5 seconds.
- After a player has started regenerating health, their "last attacked by" player is reset.

**Hunger**
- Players start with 100 Hunger points.
- Every 5 seconds players lose 10 points. The 5 second timer is reset whenever a player eats.
- If the player does not have 10 hunger to be consumed, they will instead take 10 damage.
- Consuming food restores 25 points.

**Stamina**
- Players all start with 100 stamina.
- Sprinting consumes stamina at .15 per tick and Attacking consumes stamina at 5 per attack.
- After not consuming stamina for 3 seconds players will regenerate 2 stamina per Tick.

**Aggression**
- Players have an aggression level.
- Attacking a player with the same or lower aggression level will increase a player's aggression by 1.
- Attacking a player's container with the same or lower aggression level will increase a player's aggression by .5.
- Players can reference players based on aggression using the Get Transform and Get Float nodes.
- Stealing from an alive player's container will increase aggression by .25.
- Stealing from a dead player's inventory does not affect a player's aggression level.

</details>

<details>
<summary>Player States</summary>

- **Passive** - The player will not perform any actions during this state.

- **Gathering** - If not carrying any food a player will search for nearby food to gather and automatically pick it from trees or off the ground. When carrying food the player will automatically deposit it into its own storage container if nearby.

- **Eating** - If not carrying any food a player will search for nearby food to gather and automatically pick it from trees, off of the ground, or from its own container. When carrying food the player will automatically consume it.

- **Attack** - If not carrying any food a player will search for nearby players and containers and will automatically attack them when in range. When carrying food the player will automatically drop it.

- **Steal** - If not carrying any food a player will search for nearby containers they do not own to steal from. When carrying food the player will automatically deposit it into its own storage container if nearby.

- **Dead** - The player will not perform any actions during this state.

</details>

<details>
<summary>Nodes</summary>

<details>
<summary>Controller & Properties</summary>

- **`SurvivalController(targetPosition, state, sprint, emote)`** - Controls an Aialander's brain. Navigation uses pathfinding to find the nearest viable point to the input target position
  - Inputs: Vector3 (target), SurvivalState, Bool (sprint), SurvivalEmote (optional)
  - Output: None (destination node)

- **`ConstructSurvivalProperties(...)`** - Sets cosmetic options for this Aialander (name, country, skin color, body type, hair style, etc.)
  - Inputs: String, Country, Color, Float (body type), Float (hair style), Color, Float, String (outfit URL)
  - Output: None (destination node)
  - See Customization section for body type and hair style option numbers

</details>

<details>
<summary>Data Access</summary>

- **`SurvivalGetTransform(value)`** - Selection of Transform options representing current locations in the simulation
  - Options:
    - `0` Self
    - `1` Player Last Damaged By
    - `2` Player Last Attacking (Global)
    - `3` Player Nearest
    - `4` Player 2nd Nearest
    - `5` Player Farthest
    - `6` Player with Highest Health
    - `7` Player with Lowest Health
    - `8` Player with Highest Hunger
    - `9` Player with Lowest Hunger
    - `10` Player with Highest Stamina
    - `11` Player with Lowest Stamina
    - `12` Player Last Stolen From Self Container
    - `13` Player Last Stealing (Global)
    - `14` Player with Highest Score
    - `15` Player with Lowest Score
    - `16` Player of Closest Score
    - `17` Player with Most Aggression
    - `18` Player with Lowest Aggression
    - `19` Player Nearest with Aggression
    - `20` Player Nearest with No Aggression
    - `21` Player with Most Stored Fruit
    - `22` Player with Least Stored Fruit
    - `23` Container Self
    - `24` Container Closest (excluding self)
    - `25` Container Farthest (excluding self)
    - `26` Container of Last Attacker
    - `27` Container of Last Global Attacker
    - `28` Container of Most Stored Fruit
    - `29` Container of Nearest Dead Player
    - `30` Container of Nearest Dead Player (with Food)
    - `31` Container of Highest Aggression Player
    - `32` Container of Lowest Aggression Player
    - `33` Container of Player with Closest Rank
    - `34` Fruit Nearest
    - `35` Fruit Farthest
    - `36` Fruit Nearest Self Container
    - `37` Fruit (Random)
    - `38` Tree Nearest
  - Output: Transform

- **`SurvivalGetFloat(value)`** - Selection of global number-based options representing current parameters in the simulation
  - Options:
    - `0` Health Percentage
    - `1` Hunger Percentage
    - `2` Stamina Percentage
    - `3` Current Rank
    - `4` Stored Food Count
    - `5` Distance to Nearest Player
    - `6` Distance to Nearest Aggressive Player
    - `7` Distance to Last Attacker
    - `8` Distance to Nearest Container
    - `9` Distance to Nearest Fruit Tree
    - `10` Player Count Remaining
    - `11` Current Simulation Time
    - `12` Max Simulation Time
    - `13` Simulation Time Remaining
    - `14` Delta time
    - `15` Fixed delta time
    - `16` Pi
    - `17` Self Gathers
    - `18` Self Food Consumed
    - `19` Self Steals
    - `20` Self Damage Dealt
    - `21` Self Kills
    - `22` Self Aggression Level
    - `23` Available Fruit Count
    - `24` Player Count Without Stored Food
    - `25` Average Player Health
    - `26` Average Player Hunger
    - `27` Average Player Stamina
    - `28` Average Player Aggression Level
    - `29` Total Possible Fruit
    - `30` Distance Traveled
  - Output: Float

- **`SurvivalGetBool(value)`** - Selection of global True/False options representing current parameters in the simulation
  - Options:
    - `0` Is Carrying Resource
    - `1` Container has Health
    - `2` Container Was Attacked
    - `3` Container Was Stolen From
    - `4` Self Was Attacked
  - Output: Bool

</details>

<details>
<summary>States & Emotes</summary>

- **`SurvivalState(value)`** - Selection of states Aialanders can be in. States determine what automatic behaviors Aialanders take
  - Options: `Passive`, `Gather`, `Eat`, `Attack`, `Steal`, `Dead`
  - Output: SurvivalState

- **`SurvivalEmote(value)`** - Selection of emotes Aialanders can perform
  - Options: `None`, `Hi`, `Talk`, `Bored`, `Wave`
  - Output: SurvivalEmote

- **`SurvivalAutoPosition(state)`** - Automatically decide where to move an Aialander based on predetermined rules for a given state
  - Input: SurvivalState
  - Output: Vector3

- **`ConditionalSetSurvivalState(condition, trueValue, falseValue)`** - Evaluates the input bool to toggle between two different state values
  - Options: `True`, `False` (same as ConditionalSetFloat)
  - Inputs: Bool, SurvivalState, SurvivalState
  - Output: SurvivalState

- **`ConditionalSetSurvivalEmote(condition, trueValue, falseValue)`** - Evaluates the input bool to toggle between two different emote values
  - Options: `True`, `False` (same as ConditionalSetFloat)
  - Inputs: Bool, SurvivalEmote, SurvivalEmote
  - Output: SurvivalEmote

</details>

</details>

</details>

---

<details>
<summary><strong>Parking Simulation</strong></summary>

**Requirements:** The ModularUniformController is the required destination to control a single car. ConstructModularUniformProperties sets that car's aesthetic. CarRaycasts casts rays out in 8 directions and returns HitInfo.

**Overview:** The goal of the simulation is to navigate the car to a target parking stall and have it sit inside the stall for 3 seconds. After that, the player progresses to a new level with the same goal but from a different local position and with a different target parking stall.

Alignment to the stall is encouraged but not required. Colliding with any objects will reset the player to the starting position.

**Tips**

- Raycasts all extend from the **center** of the car. The car width is roughly **6**; the car length is roughly **10.8**.
- Stepping on the **brake** while setting **throttle** to **`-1`** will almost instantly stop the car—worth using when an obstacle is very close.

<details>
<summary>Controller & Properties</summary>

- **`ModularUniformController(throttle, steering, brake)`** - Sends inputs to the car to control it
  - Inputs:
    - Float (throttle: `1` is forward, `-1` is reverse)
    - Float (steering: `-1` is left, `1` is right)
    - Float (brake: any value over `0` applies brake)
  - Output: None (destination node)

- **`InitializeParking(name, country, skinColor, bodyStyle, hairStyle, hairColor, facialHairStyle, carColor, outfitUrl)`** - Convenience helper to set all parking car cosmetic options in one call
  - Inputs:
    - String (name tag)
    - Country (country this character is representing)
    - Color (skin color)
    - Float (body style: `0` = male, `1` = female; value wraps to prevent errors)
    - Float (hair style; value wraps to prevent errors)
    - Color (hair color)
    - Float (facial hair style; value wraps to prevent errors)
    - Color (car color)
    - String (optional image URL to download and apply to the outfit)
  - Output: None (side effect)

- **`ConstructModularUniformProperties(name, country, skinColor, bodyStyle, hairStyle, hairColor, facialHairStyle, carColor, outfitUrl)`** - Sets cosmetic options for this car
  - Inputs:
    - String (name tag)
    - Country (country this character is representing)
    - Color (skin color)
    - Float (body style: `0` = male, `1` = female; value wraps to prevent errors)
    - Float (hair style; value wraps to prevent errors)
    - Color (hair color)
    - Float (facial hair style; value wraps to prevent errors)
    - Color (car color)
    - String (optional image URL to download and apply to the outfit)
  - Output: None (destination node)

</details>

<details>
<summary>Marking the bot as LLM-driven</summary>

See the top-level [Marking your bot as LLM-driven](#marking-your-bot-as-llm-driven) section. The same `props.data["modifier"] = "True"` recipe applies to `InitializeParking`, `InitializeDemoDerby`, and `ConstructModularUniformProperties` — they all return the same `UniformModularCarProperties` node.

</details>

<details>
<summary>Sensors & Raycast Results</summary>

- **`Spherecast(radius, distance)`** - Defines the radius/size and travel distance used for spherecast sensors
  - Inputs:
    - Float (radius)
    - Float (distance)
  - Output: Spherecast

- **`CarRaycasts(spherecast)`** - Sends sensors out into the world around the car to detect information about the world
  - Inputs:
    - Spherecast (length/size of spherecasts to send out as sensors)
  - Outputs:
    - `RaycastHit1` forward left
    - `RaycastHit2` forward
    - `RaycastHit3` forward right
    - `RaycastHit4` left
    - `RaycastHit5` right
    - `RaycastHit6` rear left
    - `RaycastHit7` rear
    - `RaycastHit8` rear right

- **`HitInfo(raycastHit)`** - Extracts collision info from a `RaycastHit`
  - Inputs: RaycastHit (connect one of `RaycastHit1`..`RaycastHit8`)
  - Outputs:
    - Bool (was a collision detected?)
    - Float (distance to the collision; returns infinity if no collision)

</details>

<details>
<summary>Game State Access</summary>

- **`ParkingGetTransform(value)`** - Selection of Transform options that represent a current location in the simulation
  - Options: `Self`, `Target Parking Stall`
  - Output: Transform

- **`ParkingGetFloat(value)`** - Selection of global number-based options that represent a current parameter in the simulation
  - Options: `Speed`, `Target Stall Width`, `Target Stall Depth`, `Current Level`, `Fail Count`, `Current Simulation Time`, `Max Simulation Time`, `Delta Time`, `Fixed Delta Time`, `Pi`
  - Output: Float

- **`ParkingGetBool(value)`** - Selection of global True/False based options that represent a current parameter in the simulation
  - Options: `Is Partially in Target Parking Stall`, `Is Fully in Target Parking Stall`
  - Output: Bool

</details>

</details>

---

<details>
<summary><strong>Demo Derby Simulation</strong></summary>

**Requirements:** Same modular car stack as Parking: `ModularUniformController` drives your car; `ConstructModularUniformProperties` (or `InitializeParking` / `InitializeDemoDerby`) sets cosmetics. `Spherecast`, `CarRaycasts`, and `HitInfo` behave as in Parking.

**Overview:** Maximize damage to other cars. Collisions deal damage; vulnerable parts change handling (front wheels steering; rear wheels, engine, driveshaft acceleration). At **0** engine health a car **explodes** and damages nearby cars.

**Tips:** Raycasts originate at the car **center** (rough width **6**, length **10.8**, same as Parking). JSON node id for auto throttle is **`Autothrottle`** (not `AutoThrottle`).

<details>
<summary>Initialization</summary>

- **`InitializeDemoDerby(name, country, skinColor, bodyStyle, hairStyle, hairColor, facialHairStyle, carColor, outfitUrl)`** - Convenience helper to set all derby car cosmetic options in one call. Same nine **positional** arguments as `InitializeParking`; delegates to it.
  - Inputs:
    - String (name tag)
    - Country (country this character is representing — bot personas like `"ChatGPT"`, `"Claude"`, `"Deepseek"`, `"Gemini"`, `"Grok"`, `"Llama"`, `"Mistral"`, `"Perplexity"`, `"Qwen"` are valid Country values too)
    - Color (skin color)
    - Float (body style: `0` = male, `1` = female; value wraps to prevent errors)
    - Float (hair style; value wraps to prevent errors)
    - Color (hair color)
    - Float (facial hair style; value wraps to prevent errors)
    - Color (car color)
    - String (optional image URL to download and apply to the outfit; pass `""` for none)
  - **Returns** the `UniformModularCarProperties` node — capture it so you can set `props.data["modifier"] = "True"` to mark the bot as LLM-driven (see [Marking your bot as LLM-driven](#marking-your-bot-as-llm-driven)).

</details>

<details>
<summary>Controller, cosmetics, sensors</summary>

Use the same helpers as Parking: `ModularUniformController`, `ConstructModularUniformProperties`, `InitializeParking`, `Spherecast`, `CarRaycasts`, `HitInfo` (see **Parking Simulation**).

</details>

<details>
<summary>Car queries and automation</summary>

- **Guardrails (common LLM pitfalls)**:
  - **Transform vs Vector3**: Many helpers output a **Transform** (type `Transform`) which is *not* a Vector3 position. In this library, transforms are represented as `Node` objects and **do not** have Unity-style fields like `.Position` / `.position`.
  - **How to get a position Vector3 from a Transform**: use **`RelativePosition(transform_node, "Self")`** (returns a `Vector3`).
  - **Bad (will error)**:
    - `goal = CarGetPart(0, car).PartTransform.Position`
  - **Good (same intent)**:
    - `part = CarGetPart(0, car)`
    - `goal = RelativePosition(part.PartTransform, "Self")`

- **`DemoDerbyGetTransform(value)`** - `0` self body/controller, `1` fixed reference (inspector), `2` random pathable waypoint.

- **`DemoDerbyGetCar(mode, index_float=None)`** - Returns a **Car** reference. Pass **`index_float`** when `mode` is **`0`** (by index, wrapped to vehicle count) or **`1`** (by rank, wrapped to ranked-vehicle count; ranking = `DamageDealt` desc, then `HealthNormalized` desc). Modes **`0`–`26`** (match `DemoDerbyGetCarGate.cs`):
    - **`0`** by index · **`1`** by rank · **`2`** self
    - **`3`** nearest car · **`4`** furthest car
    - **`5`** lowest health car · **`6`** highest health car
    - **`7`** last damaged car
    - **`8`** nearest active · **`9`** furthest active
    - **`10`** nearest disabled · **`11`** furthest disabled
    - **`12`** nearest with disabled steering (rear may still drive) · **`13`** furthest with disabled steering
    - **`14`** nearest AI-authored (active) · **`15`** lowest health AI · **`16`** highest health AI
    - **`17`** nearest human-authored (active) · **`18`** lowest health human · **`19`** highest health human
    - **`20`** highest ranked · **`21`** lowest ranked · **`22`** nearest ranked (rank neighbor of self)
    - **`23`** highest ranked (not immobilized) · **`24`** highest ranked (immobilized)
    - **`25`** lowest ranked (not immobilized) · **`26`** lowest ranked (immobilized)

- **`CarGetPart(mode, car)`** - **Car** in. Access **`.PartTransform`** (Transform) and **`.HealthPercent`** (Float 0–100). Modes **`0`–`3`**: average of all parts; nearest part; weakest part; nearest crucial part. Modes **`4`+** follow Unity `DamageableVehiclePart.PartType` order: `4` WheelFL … through **`36`** WindshieldWipers.

  > ⚠️ **Broken accessor — do not feed `.HealthPercent` into another node yet.** Only **`.PartTransform`** currently wires up correctly. Passing `CarGetPart(...).HealthPercent` to any Float consumer (`ConditionalSetFloat`, `CompareFloats`, `ClampFloat`, arithmetic, `TimePlot`, etc.) raises **`KeyError: 'Float2'`** in `ConnectPorts` — the wrapper asks for port `Float2` but the Unity node only publishes `Float1`. See [Multi-output component accessor bug](#multi-output-component-accessor-bug) below.

- **`CarInfo(car)`** - **Car** in. Multi-output helper. Access **`.CarTransform`** (Transform), **`.Velocity`** (Vector3 world velocity), **`.IsAI`** (Bool — LLM / ML-Agent authored), **`.IsImmobile`** (Bool — derby mobility tracker flagged), **`.Health`** (Float — summed damageable part health), and **`.Rank`** (Float — 1-based derby rank, `0` when unknown). Components unpack in declared order: `car_transform, velocity, is_ai, is_immobile, health, rank = CarInfo(car)`.

  > ⚠️ **Broken accessors — do not feed `.Velocity`, `.IsAI`, `.IsImmobile`, `.Health`, or `.Rank` into another node yet.** Only **`.CarTransform`** currently wires up correctly. Using any of the others (including via tuple unpacking, since the unpacked node is the same object) raises **`KeyError: 'Vector32'`** / **`'Bool3'`** / **`'Bool4'`** / **`'Float5'`** / **`'Float6'`** in `ConnectPorts`. The canonical failure is `Magnitude(CarInfo(car).Velocity)` → `KeyError: 'Vector32'`. See [Multi-output component accessor bug](#multi-output-component-accessor-bug) below.

- **`GetCarFromTransform(transform)`** - Converts a **Transform** (or `GameObject`/`Component` passed through transform nodes) into a **Car** reference (Unity searches on the transform and parents).

- **`Autosteer(goal)`** - **Vector3** target, **Float** steering out.

- **`Autothrottle(goal, desired_speed)`** - **Vector3** goal, **Float** target speed at goal, **Float** throttle out.

</details>

<details>
<summary>Unity caveat: ParkingGetFloat / ParkingGetBool in Demo Derby</summary>

Unity’s **Demo Derby Get Float** / **Demo Derby Get Bool** assets still serialize as **`ParkingGetFloat`** and **`ParkingGetBool`**. The current `ParkingGetFloatGate` / `ParkingGetBoolGate` in AIComp expect **parking** (`CarParkingManager`), so they are **not** wired for **`DemoDerbyGameManager`** yet. Python may still emit those nodes for Parking graphs or future Unity builds; for derby logic today prefer **`DemoDerbyGetTransform`**, **`DemoDerbyGetCar`**, **`CarGetPart`**, **`CarInfo`**, **`Autosteer`**, and **`Autothrottle`**.

</details>

<details>
<summary>Minimal complete Demo Derby example</summary>

This is the smallest end-to-end derby bot. It chases the nearest active car, aims for that car's nearest crucial part (engine / driveshaft / front wheel), commits to the throttle, and brakes if something is right in front of the bumper but the real target is still far away (i.e. it's about to ram a wall). **Use this as your starting template.** `Grok.py` demonstrates a working sensor-based "heavily blocked" unstick (avoiding the `CarInfo.IsImmobile` → `KeyError: 'Bool4'` bug that previously affected it and `Claude.py`); the other example bots follow the same safe pattern.

```python
from AIGameLibrary import *

# 1. Cosmetics + LLM flag (positional args; capture the returned node).
props = InitializeDemoDerby(
    "MyBot",                    # name
    "Gemini",                   # country (LLM persona names are valid)
    "Tan",                      # skin color
    0,                          # body style
    2,                          # hair style
    "Brown",                    # hair color
    0,                          # facial hair style
    "Blue",                     # car color
    "",                         # custom outfit URL (empty)
)
props.data["modifier"] = "True"   # mark this bot as LLM-driven

# 2. Self position (Vector3) for distance checks.
self_pos = RelativePosition(DemoDerbyGetTransform(0), "Self")

# 3. Pick a target: nearest active opponent, aim at its nearest crucial part.
target      = DemoDerbyGetCar(8)                     # 8 = nearest active
target_part = CarGetPart(3, target)                  # 3 = nearest crucial part
goal        = RelativePosition(target_part.PartTransform, "Self")

# 4. Forward sensor for emergency braking against scenery.
sensor          = Spherecast(1.2, 12.0)
_, ray_f, *_    = CarRaycasts(sensor)
front_hit, front_dist = HitInfo(ray_f)

goal_dist = Distance(self_pos, goal)
panic     = front_hit & (front_dist < 2.5) & (goal_dist > 10.0)
brake     = ConditionalSetFloat(panic, 1.0, 0.0)

# 5. Drive: Autosteer / Autothrottle do the heavy lifting.
ModularUniformController(
    Autothrottle(goal, 25.0),   # throttle
    Autosteer(goal),            # steering
    brake,                      # brake
)

# 6. Save (without this, nothing is exported).
SaveData("MyBot", "auto")
```

</details>

</details>

---

<details>
<summary><strong>Slime Volleyball Simulation</strong></summary>

<details>
<summary>Game Entity Access</summary>

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
<summary>Slime Volleyball Specific Functions</summary>

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
  - Options (Default/General): `"Delta time"`, `"Fixed delta time"`, `"Gravity"`, `"Pi"`, `"Simulation duration"`
  - Options (Slime Volleyball): Also includes `"Team score"`, `"Opponent score"`, `"Ball touches remaining"`
  - Output: Float

- **`GetTransform(value)`** - Gets transform data from the game
  - Options (Slime Volleyball): `"Self"`, `"Opponent"`, `"Ball"`, `"Self Team Spawn"`, `"Opponent Team Spawn"`
  - Output: Transform

- **`RelativePosition(transform, direction)`** - Gets a relative position vector
  - `transform`: Transform node
  - `direction`: One of `"Self"`, `"Self + Forward"`, `"Self + Backward"`, `"Self + Left"`, `"Self + Right"`, `"Self + Up"`, `"Self + Down"`, `"Forward"`, `"Backward"`, `"Left"`, `"Right"`, `"Up"`, `"Down"`
  - Output: Vector3

- **`Stat(value)`** - Creates a stat node (used for slime stats)
  - Input: `value` (int or str)
  - Output: Stat

- **`Color(value)`** - Creates a color node
  - Options: `"Auburn"`, `"Black"`, `"Blonde"`, `"Blue"`, `"Brown"`, `"Dark Brown"`, `"Dark Green"`, `"Green"`, `"Hot Pink"`, `"Light Blue"`, `"Light Grey"`, `"Medium Grey"`, `"Orange"`, `"Pink"`, `"Purple"`, `"Red"`, `"Tan"`, `"White"`, `"Yellow"`
  - Output: Color

- **`Country(value)`** - Creates a country node
  - Options: `"Unknown"`, `"Afghanistan"`, `"Albania"`, `"Algeria"`, `"Andorra"`, `"Angola"`, `"Argentina"`, `"Armenia"`, `"Australia"`, `"Austria"`, `"Azerbaijan"`, `"Bahamas"`, `"Bahrain"`, `"Bangladesh"`, `"Barbados"`, `"Belarus"`, `"Belgium"`, `"Bermuda"`, `"Bohemia"`, `"Botswana"`, `"Brazil"`, `"Bulgaria"`, `"Burkina Faso"`, `"Burundi"`, `"Cameroon"`, `"Canada"`, `"Chile"`, `"China"`, `"Colombia"`, `"Costa Rica"`, `"Croatia"`, `"Cuba"`, `"Cyprus"`, `"Czechia"`, `"Côte d'Ivoire"`, `"Denmark"`, `"Djibouti"`, `"Dominican Republic"`, `"DR Congo"`, `"Ecuador"`, `"Egypt"`, `"Eritrea"`, `"Estonia"`, `"Ethiopia"`, `"Fiji"`, `"Finland"`, `"France"`, `"Gabon"`, `"Georgia"`, `"Germany"`, `"Ghana"`, `"Greece"`, `"Grenada"`, `"Guatemala"`, `"Guyana"`, `"Haiti"`, `"Hong Kong"`, `"Hungary"`, `"Iceland"`, `"India"`, `"Indonesia"`, `"Iran"`, `"Iraq"`, `"Ireland"`, `"Israel"`, `"Italy"`, `"Jamaica"`, `"Japan"`, `"Jordan"`, `"Kazakhstan"`, `"Kenya"`, `"Kosovo"`, `"Kuwait"`, `"Kyrgyzstan"`, `"Latvia"`, `"Lebanon"`, `"Lithuania"`, `"Luxembourg"`, `"Malaysia"`, `"Mauritius"`, `"Mexico"`, `"Moldova"`, `"Mongolia"`, `"Montenegro"`, `"Morocco"`, `"Mozambique"`, `"Myanmar"`, `"Namibia"`, `"Netherlands"`, `"New Zealand"`, `"Niger"`, `"Nigeria"`, `"North Korea"`, `"North Macedonia"`, `"Norway"`, `"Oman"`, `"Pakistan"`, `"Palestine"`, `"Panama"`, `"Paraguay"`, `"Peru"`, `"Philippines"`, `"Poland"`, `"Portugal"`, `"Puerto Rico"`, `"Qatar"`, `"Romania"`, `"Russia"`, `"Samoa"`, `"San Marino"`, `"Saudi Arabia"`, `"Scotland"`, `"Senegal"`, `"Serbia"`, `"Singapore"`, `"Slovakia"`, `"Slovenia"`, `"Somolia"`, `"South Africa"`, `"South Korea"`, `"Spain"`, `"Sri Lanka"`, `"Sudan"`, `"Suriname"`, `"Sweden"`, `"Switzerland"`, `"Syria"`, `"Taiwan"`, `"Tajikistan"`, `"Tanzania"`, `"Thailand"`, `"Togo"`, `"Tonga"`, `"Trinidad and Tobago"`, `"Tunisia"`, `"Turkey"`, `"Turkmenistan"`, `"Uganda"`, `"Ukraine"`, `"United Arab Emirates"`, `"United Kingdom"`, `"United States of America"`, `"Uruguay"`, `"Uzbekistan"`, `"Venezuela"`, `"Vietnam"`, `"Virgin Islands"`, `"Yemen"`, `"Zambia"`, `"Zimbabwe"`, `"ChatGPT"`, `"Claude"`, `"Deepseek"`, `"Gemini"`, `"Grok"`, `"Llama"`, `"Mistral"`, `"Perplexity"`, `"Qwen"`
  - Output: Country

</details>

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

---

# Notes for LLM Authors

This section consolidates everything an LLM (or anyone new to the library) needs to avoid the most common mistakes. Read it in full before writing a script.

> 🛑 **Before you submit a bot, scan it for these six accessor patterns and delete every one of them** — they all currently crash in `ConnectPorts` with a `KeyError` and are the #1 thing we keep seeing LLMs burn on:
>
> - `CarInfo(...).Velocity` → `KeyError: 'Vector32'`
> - `CarInfo(...).IsAI` → `KeyError: 'Bool3'`
> - `CarInfo(...).IsImmobile` → `KeyError: 'Bool4'`
> - `CarInfo(...).Health` → `KeyError: 'Float5'`
> - `CarInfo(...).Rank` → `KeyError: 'Float6'`
> - `CarGetPart(...).HealthPercent` → `KeyError: 'Float2'`
>
> That includes the sneaky **tuple-unpacking** form (`car_tf, velocity, is_ai, is_immobile, health, rank = CarInfo(car)` — the unpacked vars are the same broken nodes) and any arithmetic/comparison that funnels them into another node (`Magnitude(v)`, `v * dt`, `health < 50`, `ConditionalSetFloat(is_immobile, ...)`, etc.). Only **`.CarTransform`** and **`.PartTransform`** are safe. See **[Multi-output component accessor bug](#multi-output-component-accessor-bug)** for replacements.

## The mental model

This is a **graph compiler**, not a runtime game SDK. Your script does **not** drive the car/slime/Aialander frame-by-frame. It builds a static node graph **once**, and `SaveData(...)` writes that graph to JSON. Unity loads the JSON and re-evaluates the graph every tick.

Concretely:

- Every value you compose (`Self.Position`, `Distance(...)`, `props`, sensor outputs, etc.) is a **`Node` object**, not a number, string, list, or dict.
- Plain Python `if` / `while` / `for`, `min` / `max` / `sorted`, `lambda`, list/dict indexing, and `import math` calls **do not become nodes**. They run once at compile time and are gone. Use the graph equivalents: `ConditionalSetFloat` / `ConditionalSetVector3` / `ConditionalSetBool` for branching, `Operation(x)` for math, `DemoDerbyGetCar` / `SurvivalGetTransform` to "pick" entities, etc.
- The `Initialize*` helpers take **positional arguments**, not keyword arguments. There is no `name=`, `country=`, `modifier_llm=`, `save_file=` etc. See each simulation's section for the exact signature.
- There is no `sim` object. Methods like `sim.is_active()`, `sim.get_self_data()`, `sim.get_opponents()`, `sim.set_controls()`, `sim.update()` **do not exist** — if you wrote any of those, you are hallucinating an SDK that isn't here.
- The package is **`AIGameLibrary`** (the GitHub repo is `AIGamePyLibrary` — note the extra "Py"). A shim package re-exports under the repo name, but the helpers are free functions, not methods on an object.
- The LLM-driven flag is set on the **returned** Properties node: `props.data["modifier"] = "True"`. There is **no** `modifier_llm=`, `is_llm=`, `llm=`, or `isLLM=` keyword argument on any helper.
- Your script must end with a call to **`SaveData("YourBot", "auto")`** or nothing is exported.

## 🚨 CRITICAL: Multi-output Bug (KeyError: 'Bool4', 'Vector32', etc.)

**The most common error LLMs make** when writing Demo Derby bots is using `CarInfo(...).IsImmobile`, `.Velocity`, `.Health`, `.Rank`, or `CarGetPart(...).HealthPercent` in `ConditionalSetFloat`, comparisons, arithmetic, etc.

```python
# These ALL fail with KeyError in ConnectPorts:
is_stuck = CarInfo(self_car).IsImmobile                    # → 'Bool4'
throttle = ConditionalSetFloat(is_stuck, -1.0, throttle_fwd)
# or: Magnitude(CarInfo(car).Velocity) → 'Vector32'
```

**Fix:** 
- Only use `.CarTransform` and `.PartTransform` from these helpers.
- For stuck detection use **forward raycast sensors** (`HitInfo(ray_f)`) as shown in `Grok.py`.
- See full details in [Multi-output component accessor bug](#multi-output-component-accessor-bug) below.

**`Grok.py` (and `Claude.py`) have been updated with a working sensor-based unstick workaround.** Older versions will hit this exact error.

## Common mistakes

These are the exact mistakes we keep seeing. If your draft does any of them, rewrite it before saving.

| ❌ Don't | ✅ Do |
|---|---|
| `import AIGamePyLibrary as aig` then `aig.InitializeDemoDerby(...)` (treats helpers as methods on a sim object) | `from AIGameLibrary import *` and call helpers as free functions |
| `InitializeDemoDerby(name="X", country="USA", modifier_llm=True, save_file="X")` | `props = InitializeDemoDerby("X", "United States of America", "Tan", 0, 0, "Brown", 0, "Red", "")` — positional only |
| `country="USA"` / `country="UK"` / `country="South-Korea"` | Use the exact strings from the Country list, e.g. `"United States of America"`, `"United Kingdom"`, `"South Korea"`. Bot personas: `"ChatGPT"`, `"Claude"`, `"Deepseek"`, `"Gemini"`, `"Grok"`, `"Llama"`, `"Mistral"`, `"Perplexity"`, `"Qwen"` |
| Pass `modifier_llm=True` / `is_llm=True` / `llm=True` to any helper | After init: `props.data["modifier"] = "True"` (see [Marking your bot as LLM-driven](#marking-your-bot-as-llm-driven)) |
| Pass `save_file="X"` to any helper | Saving is a separate call at the end of the script: `SaveData("X", "auto")` |
| `while sim.is_active(): sim.set_controls(...)` style runtime loop | Build the graph once. Unity runs it every tick. There is no loop in your script. |
| `sim.get_self_data()`, `sim.get_opponents()`, `sim.set_controls()`, `sim.update()`, `sim.is_active()` | None of these exist. Use `DemoDerbyGetTransform`, `DemoDerbyGetCar`, `CarInfo`, `CarRaycasts`, `ModularUniformController`, etc. |
| `if dist < 50: throttle = 1.0 else: throttle = 0.5` | `throttle = ConditionalSetFloat(dist < 50, 1.0, 0.5)` |
| `min(opponents, key=lambda o: ...)` / iterating Python lists of game entities | There is no Python-side list of opponents. Use selector nodes like `DemoDerbyGetCar(8)` (nearest active), `CarGetPart(3, car)` (nearest crucial part), `SurvivalGetTransform(3)` (player nearest), etc. |
| `math.atan2(...)`, `math.sqrt(...)`, `math.degrees(...)` | `Operation(x)` (`atan`, `sqrt`, etc.), `Magnitude`, `Distance`, `DotProduct`, `Normalize`, or just rely on `Autosteer(goal)` / `Autothrottle(goal, speed)` for car driving |
| 2D thinking: `pos[0]`, `pos[1]`, `heading` in degrees | Everything is 3D `Vector3`. Access components via `vec.x`, `vec.y`, `vec.z`. There is no scalar "heading". Use `Autosteer` for car aim. |
| `transform.Position` / `transform.position` on a Transform node | `RelativePosition(transform_node, "Self")` returns the world `Vector3` |
| `Magnitude(CarInfo(car).Velocity)`, `ClampFloat(CarInfo(car).Health, ...)`, `pos + CarInfo(car).Velocity * dt`, `ConditionalSetFloat(CarGetPart(3, car).HealthPercent < 50, ...)` | **Broken in the current library.** Only `.CarTransform` (on `CarInfo`) and `.PartTransform` (on `CarGetPart`) can be passed to another node — everything else raises `KeyError: 'Vector32'` / `'Bool3'` / `'Bool4'` / `'Float5'` / `'Float6'` / `'Float2'` in `ConnectPorts`. Plan your bot around `Autosteer` / `Autothrottle` + `DemoDerbyGetCar` / `CarGetPart(3, ...).PartTransform` + raycast sensors. See **[Multi-output component accessor bug](#multi-output-component-accessor-bug)**. |
| Forget to call `SaveData(...)` at the end | Always finish with `SaveData("YourBotName", "auto")` — without this the script does literally nothing |

## Side-by-side example

**Wrong (looks like a runtime loop, none of this works):**

```python
import AIGamePyLibrary as aig          # treats helpers as methods on a sim object
sim = aig.InitializeDemoDerby(name="Gemini", country="USA",
                              modifier_llm=True, save_file="Gemini")  # not real kwargs
while sim.is_active():                  # no such method
    me = sim.get_self_data()            # no such method
    for op in sim.get_opponents():      # no such method
        if dist(me, op) < 50:           # plain Python if won't compile to a node
            sim.set_controls(throttle=1.0, steer=0.2)  # no such method
    sim.update()                        # no such method
```

**Right (build a graph, mark it LLM-driven, save it):**

```python
from AIGameLibrary import *

props = InitializeDemoDerby(
    "Gemini", "Gemini", "Tan", 0, 2, "Brown", 0, "Blue", "",
)
props.data["modifier"] = "True"   # mark as LLM-driven (see "Marking your bot as LLM-driven")

self_pos = RelativePosition(DemoDerbyGetTransform(0), "Self")
target   = DemoDerbyGetCar(8)                                 # nearest active car
goal     = RelativePosition(CarGetPart(3, target).PartTransform, "Self")

ModularUniformController(Autothrottle(goal, 25.0), Autosteer(goal), Float(0.0))
SaveData("Gemini", "auto")
```

For a slightly fuller derby starter (with sensors and a panic brake) see the **[Minimal complete Demo Derby example](#demo-derby-simulation)**. `Grok.py` now demonstrates a safe, aggressive ramming strategy with sensor-based unsticking that avoids the `KeyError: 'Bool4'` (see the new warning at the top of Notes for LLM Authors).

## Multi-output component accessor bug

> This is a **known library bug**, not an LLM mistake. It's documented here so LLM authors stop writing scripts that hit it.

### What breaks

Any of these will raise a `KeyError` inside `AIGameLibrary/lib.py → ConnectPorts` at compile time (when `SaveData(...)` runs, or earlier if the consuming node is constructed first):

```python
# --- all of these crash ---
self_info = CarInfo(DemoDerbyGetCar(2))
self_speed = Magnitude(self_info.Velocity)                          # KeyError: 'Vector32'
is_alive   = self_info.Health > 0                                   # KeyError: 'Float5'
if_imm     = ConditionalSetFloat(self_info.IsImmobile, -1.0, 1.0)   # KeyError: 'Bool4'
rank_ok    = self_info.Rank < 3                                     # KeyError: 'Float6'

# unpacking doesn't save you — the unpacked Nodes are the same broken objects:
car_tf, velocity, is_ai, is_immobile, health, rank = CarInfo(car)
Magnitude(velocity)                                                 # still KeyError: 'Vector32'

# GetCarPart has the same shape of bug:
part = CarGetPart(3, target)
weak = part.HealthPercent < 30                                      # KeyError: 'Float2'
```

### Why it breaks

`CarInfoComponents` and `GetCarPartComponents` store each accessor's `outputIndex` as its **global position** in the node's port list, but `ConnectPorts` builds the Unity port name as `f"{inputType}{outputIndex}"` — which must be the **type-local** port number. Unity's `CarInfo` node publishes `Transform1, Vector31, Bool1, Bool2, Float1, Float2` (type-local), but the Python wrappers ask for `Transform1, Vector32, Bool3, Bool4, Float5, Float6`. Only the first port of each multi-output node (`Transform1`, position 1) lines up by accident.

For reference, here's what each accessor currently does and what port id it asks for:

| Accessor | `outputIndex` | Port name built | Actual Unity port | Status |
|---|---|---|---|---|
| `CarInfo(...).CarTransform` | 1 | `Transform1` | `Transform1` | ✅ works |
| `CarInfo(...).Velocity` | 2 | `Vector32` | `Vector31` | ❌ `KeyError` |
| `CarInfo(...).IsAI` | 3 | `Bool3` | `Bool1` | ❌ `KeyError` |
| `CarInfo(...).IsImmobile` | 4 | `Bool4` | `Bool2` | ❌ `KeyError` |
| `CarInfo(...).Health` | 5 | `Float5` | `Float1` | ❌ `KeyError` |
| `CarInfo(...).Rank` | 6 | `Float6` | `Float2` | ❌ `KeyError` |
| `CarGetPart(...).PartTransform` | 1 | `Transform1` | `Transform1` | ✅ works |
| `CarGetPart(...).HealthPercent` | 2 | `Float2` | `Float1` | ❌ `KeyError` |

`HitInfoComponents` sidesteps this by storing `outputIndex=1` for **both** `WasHit` and `Distance` and instead setting `node.type` to `bool` / `float` so the consumer prefixes the right port type — `CarInfoComponents` and `GetCarPartComponents` would need the same kind of fix.

### What to do until it's fixed

LLM authors: **plan your bot so you never pass the broken accessors into another node.** In practice that's easier than it sounds because the library already gives you graph-side alternatives:

- **Don't velocity-lead the aim.** Skip `target_pos + target_vel * dt`. Let **`Autosteer(goal)`** and **`Autothrottle(goal, speed)`** handle aim + speed management — they already compensate for relative motion and obstacles internally.
- **Don't check self-speed via `Magnitude(CarInfo(...).Velocity)`.** For stuck-recovery, gate on **`CarInfo(self).IsImmobile`**… wait, that's broken too — use `Spherecast` + `CarRaycasts` + `HitInfo` to detect "nose blocked" instead, and flip to reverse on that signal.
- **Don't branch on opponent `Health` or `Rank` from `CarInfo`.** Use the built-in target selectors that already bake those in: `DemoDerbyGetCar(5)` (lowest health), `DemoDerbyGetCar(8)` (nearest active), `DemoDerbyGetCar(12)` (nearest with disabled steering), `DemoDerbyGetCar(20)` (highest ranked), `DemoDerbyGetCar(21)` (lowest ranked), etc. Pick the target by mode, then aim at `CarGetPart(3, target).PartTransform` (nearest crucial part).
- **Don't branch on `CarGetPart(...).HealthPercent`.** `CarGetPart` mode `2` is "weakest part" — use that part's `PartTransform` directly and skip the health comparison.
- **Do keep using `.CarTransform` and `.PartTransform`.** Both resolve to `Transform1` (index 1) and compile correctly — pipe them through `RelativePosition(..., "Self")` to get a world `Vector3`.

#### Substitution cheat sheet

If you find yourself reaching for one of the broken accessors, swap in the pattern on the right instead. Every example on the right compiles against the current library.

| Broken pattern (crashes in `ConnectPorts`) | Safe replacement |
|---|---|
| `speed = Magnitude(CarInfo(self).Velocity)` — reason about own speed | **Skip it.** `Autothrottle(goal, desired_speed)` already manages cruise speed for you. If you absolutely need a "too slow" signal, use `HitInfo(ray_forward)` + `HitInfo(ray_back)` proximity — if the nose is pinned and the rear is clear, you're stuck. |
| `lead = target_pos + CarInfo(target).Velocity * dt` — predict the target | **Skip it.** `Autosteer(goal)` already tracks a moving `Vector3` goal reasonably well. |
| `is_stuck = CarInfo(self).IsImmobile` (then `ConditionalSetFloat(is_stuck, -1.0, throttle_fwd)`) | `front_hit, front_dist = HitInfo(ray_forward)`<br>`rear_hit, rear_dist = HitInfo(ray_back)`<br>`nose_wedged = front_hit & (front_dist < 2.0) & (goal_dist > 6.0)`<br>`rear_clear  = ~rear_hit \| (rear_dist > 4.0)`<br>`reverse_mode = nose_wedged & rear_clear` |
| `finish_them = CarInfo(target).Health < 50` | **Pre-select a weak target instead of branching on health.** `target = DemoDerbyGetCar(5)` (lowest health) or `DemoDerbyGetCar(12)` (nearest with disabled steering). |
| `winning = CarInfo(self).Rank < 3` | **No safe replacement right now.** Drop the rank-based branching — the built-in target selectors already keep you aggressive. |
| `is_ai = CarInfo(target).IsAI` (avoid human targets) | **No safe replacement right now.** Drop the filter — the derby is set up to only pit eligible cars against each other. |
| `weak = CarGetPart(3, target).HealthPercent < 30` | `target_part = CarGetPart(2, target)  # mode 2 = weakest part`<br>`goal = RelativePosition(target_part.PartTransform, "Self")` |

#### Worked example: "`is_stuck = CarInfo(self).IsImmobile`" done right

This is the exact pattern that crashed the reference `claude.py` with `KeyError: 'Bool4'`. Here's the broken version (do not ship) and the raycast-only version (compiles, does the same job):

```python
# ❌ CRASHES at SaveData time with KeyError: 'Bool4'
self_info    = CarInfo(DemoDerbyGetCar(2))
is_stuck     = self_info.IsImmobile                     # outputIndex=4 -> asks for Bool4
throttle_fwd = Autothrottle(goal, 28.0)
throttle     = ConditionalSetFloat(is_stuck, -1.0, throttle_fwd)  # boom
```

```python
# ✅ Same intent, raycast-only, compiles today
sensor = Spherecast(1.2, 12.0)
ray_fl, ray_f, ray_fr, ray_l, ray_r, ray_bl, ray_b, ray_br = CarRaycasts(sensor)
front_hit, front_dist = HitInfo(ray_f)
rear_hit,  rear_dist  = HitInfo(ray_b)

nose_wedged  = front_hit & (front_dist < 2.0) & (goal_dist > 6.0)
rear_clear   = ~rear_hit | (rear_dist > 4.0)
reverse_mode = nose_wedged & rear_clear

throttle_fwd = Autothrottle(goal, 28.0)
throttle     = ConditionalSetFloat(reverse_mode, -1.0, throttle_fwd)
```

Any bot that follows the [Minimal complete Demo Derby example](#demo-derby-simulation) pattern (target car → nearest crucial part → `Autosteer` + `Autothrottle` + a forward raycast for panic-brake, **no `CarInfo` component reads other than `.CarTransform`**) avoids this bug entirely.
