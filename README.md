# Aialander PyLib

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
    - `RaycastHit4` rear left
    - `RaycastHit5` rear
    - `RaycastHit6` rear right

- **`HitInfo(raycastHit)`** - Extracts collision info from a `RaycastHit`
  - Inputs: RaycastHit (connect one of `RaycastHit1`..`RaycastHit6`)
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
