# UNO Game - Complete Implementation Guide

## Introduction

Welcome to our UNO game implementation! This is a fully functional command-line version of the classic UNO card game, complete with AI players and a beautiful colored interface. Today, I'll walk you through how this game works, from the basic rules to the sophisticated programming concepts behind it.

## Game Overview

### What is UNO?
UNO is a fast-paced card game where players race to be the first to get rid of all their cards. The game uses a special deck with colored cards numbered 0-9, plus special action cards that can change the course of the game dramatically.

### Our Implementation Features
- **4 Players**: 1 human player vs 3 AI opponents
- **Full UNO Rules**: All standard card types and effects
- **Colored ASCII Art**: Beautiful card display using terminal colors
- **Smart AI**: Basic strategy for computer players
- **Interactive Interface**: Easy-to-use command-line controls

## Game Architecture

### Core Classes

#### 1. Card Class
The `Card` class represents individual UNO cards with three main properties:
- **Color**: Red, Blue, Green, Yellow, or Black (for wild cards)
- **Type**: Number, Skip, Reverse, Draw Two, Wild, or Wild Draw Four
- **Number**: Only relevant for number cards (0-9)

```python
class Card:
    def __init__(self, color: CardColor, card_type: CardType, number: int = None):
        self.color = color          # The color of the card
        self.card_type = card_type  # The type of card (number, skip, etc.)
        self.number = number        # The number value (only for number cards)
```

#### 2. Player Class
Each player has:
- **Name**: Player identifier
- **Hand**: List of cards they currently hold
- **AI Flag**: Whether this player is controlled by the computer

```python
class Player:
    def __init__(self, name: str, is_ai: bool = False):
        self.name = name      # Player's name
        self.hand = []        # List of cards in player's hand
        self.is_ai = is_ai    # Whether this player is controlled by AI
```

#### 3. UNOGame Class
The main game controller that manages:
- **Deck**: All cards in the draw pile
- **Discard Pile**: Played cards
- **Players**: All participants
- **Game State**: Current player, direction, color to match

## How the Game Works

### 1. Game Setup
When the game starts, several things happen:

**Deck Creation**: We create a standard UNO deck with 108 cards:
- 76 Number cards (0-9, with two of each number 1-9 per color)
- 24 Action cards (8 each of Skip, Reverse, Draw Two)
- 8 Wild cards (4 each of Wild and Wild Draw Four)

**Player Creation**: We create 4 players:
- "You" (human player)
- "Alice", "Bob", "Charlie" (AI players)

**Initial Deal**: Each player receives 7 cards to start.

**Starting Card**: We draw cards until we find a number card to begin the game.

### 2. Game Flow

The game runs in a continuous loop until someone wins:

1. **Display Game State**: Show current player, direction, top card, and deck size
2. **Player Turn**: Either AI or human plays their turn
3. **Check Win Condition**: If a player has no cards left, they win
4. **Next Player**: Move to the next player in the current direction

### 3. Turn Mechanics

#### Human Player Turn:
1. **Show Hand**: Display all cards with numbers for easy selection
2. **Identify Playable Cards**: Highlight which cards can be played
3. **Get Input**: Player chooses a card number or 'd' to draw
4. **Validate Move**: Ensure the chosen card is actually playable
5. **Execute Move**: Play the card and handle any special effects

#### AI Player Turn:
1. **Thinking Delay**: 2-second pause for realistic gameplay
2. **Strategy**: AI prioritizes number cards, then action cards, then wild cards
3. **Random Choice**: Select randomly from the best available options
4. **Execute Move**: Play the card and handle special effects

### 4. Card Matching Rules

A card can be played if it matches the current top card by:
- **Color**: Same color as the current color to match
- **Number**: Same number (for number cards)
- **Type**: Same action card type (Skip, Reverse, Draw Two)
- **Wild**: Wild cards can always be played

### 5. Special Card Effects

#### Skip Card:
- Next player loses their turn
- Game continues to the player after that

#### Reverse Card:
- Changes the direction of play
- Clockwise becomes counter-clockwise and vice versa

#### Draw Two Card:
- Next player must draw 2 cards
- Next player's turn is skipped

#### Wild Card:
- Player chooses a new color to match
- No additional effects

#### Wild Draw Four Card:
- Next player must draw 4 cards
- Next player's turn is skipped
- Player chooses a new color to match

## Technical Implementation Details

### ASCII Art Display
We use Unicode box-drawing characters to create beautiful card displays:
```
┌───┐
│ 5 │
└───┘
```

### Color Management
The `colorama` library provides cross-platform colored terminal output:
- Red, Blue, Green, Yellow for colored cards
- White for wild cards
- Cyan for game information
- Yellow for warnings

### AI Strategy
Our AI uses a simple but effective strategy:
1. **Priority 1**: Play number cards (safe, no special effects)
2. **Priority 2**: Play action cards (Skip, Reverse, Draw Two)
3. **Priority 3**: Play wild cards (last resort)

### Deck Management
When the draw pile runs out:
1. Keep the top card of the discard pile
2. Shuffle all other discarded cards
3. Use them as the new draw pile

## Game Rules Summary

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

## How to Play

### Starting the Game:
```bash
python uno_game_copy.py
```

### During Your Turn:
1. **View Your Hand**: Cards are numbered 1, 2, 3, etc.
2. **See Playable Cards**: The game shows which cards you can play
3. **Make Your Choice**:
   - Enter a number to play that card
   - Type 'd' to draw a card
4. **For Wild Cards**: Choose a color (1-4) when prompted

### Controls:
- **Numbers**: Play the corresponding card
- **'d'**: Draw a card
- **Enter**: Continue after AI turns
- **Ctrl+C**: Quit the game

## Educational Value

This implementation demonstrates several important programming concepts:

1. **Object-Oriented Programming**: Classes for Card, Player, and Game
2. **Enums**: Type-safe constants for card types and colors
3. **State Management**: Tracking game state, current player, direction
4. **User Interface**: Interactive command-line interface
5. **Algorithm Design**: AI strategy and card matching logic
6. **Error Handling**: Input validation and game state validation

## Conclusion

This UNO game implementation showcases how complex game logic can be broken down into manageable, well-structured code. The modular design makes it easy to understand, modify, and extend. The combination of clear game rules, engaging interface, and intelligent AI creates an enjoyable gaming experience while demonstrating solid software engineering principles.

The game successfully balances simplicity with completeness, providing a full UNO experience while remaining accessible to players and maintainable for developers.
