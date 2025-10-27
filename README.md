# UNO Game - Java Implementation

A complete Java implementation of the classic UNO card game with AI players and colored terminal interface. This is a clean, standalone Java project with no Python dependencies.
  
## Features

- **4 Players**: 1 human player vs 3 AI opponents
- **Colored ASCII Art**: Beautiful card display using ANSI terminal colors
- **Smart AI**: Basic strategy for computer players
- **Interactive Interface**: Easy-to-use command-line controls
- **Cross-platform**: Works on Windows, macOS, and Linux

## Quick Start

### Prerequisites
- Java 11 or higher
- Maven 3.6 or higher

### Building and Running

```bash
# Build the project
mvn clean package

# Run the game (recommended)
java -jar target/uno-game-1.0.0.jar

# Or run directly from class files
mvn compile
java -cp target/classes com.unogame.Main
```

## How to Play

- **Numbers**: Play the corresponding card by entering its number
- **'d'**: Draw a card when you can't play
- **Enter**: Continue after AI turns
- **Ctrl+C**: Quit the game

## Project Structure

```
src/main/java/com/unogame/
├── Main.java              # Entry point
├── UnoGame.java           # Main game controller
├── Card.java              # Card representation with ASCII art
├── Player.java            # Player management and hand display
├── CardType.java          # Enum for card types
├── CardColor.java         # Enum for card colors
└── TerminalColors.java    # ANSI color utilities
```

## Architecture

The Java implementation follows the same architecture as the Python version:

### 1. Card Class
Represents individual UNO cards with:
- **Color**: Red, Blue, Green, Yellow, or Black (for wild cards)
- **Type**: Number, Skip, Reverse, Draw Two, Wild, or Wild Draw Four
- **Number**: Only relevant for number cards (0-9)

### 2. Player Class
Each player has:
- **Name**: Player identifier
- **Hand**: List of cards they currently hold
- **AI Flag**: Whether this player is controlled by the computer

### 3. UnoGame Class
The main game controller that manages:
- **Deck**: All cards in the draw pile
- **Discard Pile**: Played cards
- **Players**: All participants
- **Game State**: Current player, direction, color to match

## Game Rules

### Basic Rules:
- Match cards by color, number, or symbol
- Play one card per turn
- Draw a card if you can't play
- First player to get rid of all cards wins

### Special Rules:
- **UNO**: Say "UNO!" when you have 1 card left (automatic in our version)
- **Wild Cards**: Can be played anytime, choose a new color
- **Draw Cards**: Must draw if you can't play, then your turn ends
- **Direction**: Can be reversed during the game

## Technical Implementation

### ASCII Art Display
Uses Unicode box-drawing characters to create beautiful card displays:
```
┌───┐
│ 5 │
└───┘
```

### Color Management
The `TerminalColors` class provides ANSI color codes for cross-platform colored terminal output:
- Red, Blue, Green, Yellow for colored cards
- White for wild cards
- Cyan for game information
- Yellow for warnings

### AI Strategy
The AI uses a simple but effective strategy:
1. **Priority 1**: Play number cards (safe, no special effects)
2. **Priority 2**: Play action cards (Skip, Reverse, Draw Two)
3. **Priority 3**: Play wild cards (last resort)

### Deck Management
When the draw pile runs out:
1. Keep the top card of the discard pile
2. Shuffle all other discarded cards
3. Use them as the new draw pile

## Differences from Python Version

The Java implementation maintains 100% functional compatibility with the Python version:

- **Same Game Logic**: All rules and mechanics are identical
- **Same AI Behavior**: AI strategy and decision-making is preserved
- **Same Display**: ASCII art and colors match exactly
- **Same User Experience**: Controls and interface are identical

### Technical Differences:
- Uses Java collections (`ArrayList`, `List`) instead of Python lists
- Uses `Scanner` for input instead of Python's `input()`
- Uses `Thread.sleep()` for delays instead of Python's `time.sleep()`
- Uses ANSI escape codes directly instead of the `colorama` library
- Uses `Collections.shuffle()` instead of Python's `random.shuffle()`

## Building and Development

### Maven Commands

```bash
# Compile the project
mvn compile

# Run tests
mvn test

# Package the application
mvn package

# Clean build artifacts
mvn clean

# Run the application
mvn exec:java -Dexec.mainClass="com.unogame.Main"
```

### IDE Setup

This project can be imported into any Java IDE that supports Maven:
- IntelliJ IDEA
- Eclipse
- VS Code with Java extensions
- NetBeans

## Testing

The project includes JUnit 5 for testing. Run tests with:

```bash
mvn test
```

## Educational Value

This implementation demonstrates several important Java programming concepts:

1. **Object-Oriented Programming**: Classes for Card, Player, and Game
2. **Enums**: Type-safe constants for card types and colors
3. **Collections**: Using ArrayList and List for dynamic data structures
4. **Exception Handling**: Proper error handling and resource management
5. **Input/Output**: Console input/output with colored text
6. **Threading**: Sleep for AI delays and game timing
7. **Maven**: Build system and dependency management

## Conclusion

This Java UNO game implementation showcases how complex game logic can be implemented in Java while maintaining the same functionality as the original Python version. The modular design makes it easy to understand, modify, and extend. The combination of clear game rules, engaging interface, and intelligent AI creates an enjoyable gaming experience while demonstrating solid Java software engineering principles.

The game successfully balances simplicity with completeness, providing a full UNO experience while remaining accessible to players and maintainable for developers.
