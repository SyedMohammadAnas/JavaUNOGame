# UNO Game Implementation
# This file contains a complete command-line UNO game with AI players
# The game follows standard UNO rules with colored ASCII art display

import random, time, os
from typing import List, Optional
from enum import Enum
import colorama
from colorama import Fore, Style

# Initialize colorama for cross-platform colored terminal output
colorama.init()

# Enum for different types of UNO cards
class CardType(Enum):
    NUMBER, SKIP, REVERSE, DRAW_TWO, WILD, WILD_DRAW_FOUR = "number", "skip", "reverse", "draw_two", "wild", "wild_draw_four"

# Enum for card colors (BLACK is used for wild cards)
class CardColor(Enum):
    RED, BLUE, GREEN, YELLOW, BLACK = "red", "blue", "green", "yellow", "black"

# Represents a single UNO card with color, type, and optional number
class Card:
    def __init__(self, color: CardColor, card_type: CardType, number: int = None):
        self.color = color          # The color of the card
        self.card_type = card_type  # The type of card (number, skip, etc.)
        self.number = number        # The number value (only for number cards)

    # String representation for debugging
    def __str__(self):
        return f"{self.color.value}_{self.number if self.card_type == CardType.NUMBER else self.card_type.value}"

    # Returns a colored ASCII art representation of the card
    def get_display(self) -> str:
        # Map card colors to terminal color codes
        color_map = {
            CardColor.RED: Fore.RED,
            CardColor.BLUE: Fore.BLUE,
            CardColor.GREEN: Fore.GREEN,
            CardColor.YELLOW: Fore.YELLOW,
            CardColor.BLACK: Fore.WHITE
        }
        color_code = color_map.get(self.color, Fore.WHITE)

        # Create different ASCII art based on card type
        if self.card_type == CardType.NUMBER:
            num_str = str(self.number)
            # Handle single vs double digit numbers for proper alignment
            if len(num_str) == 1:
                return f"{color_code}┌───┐\n│ {num_str} │\n└───┘{Style.RESET_ALL}"
            else:
                return f"{color_code}┌───┐\n│{num_str}│\n└───┘{Style.RESET_ALL}"
        elif self.card_type == CardType.SKIP:
            return f"{color_code}┌───┐\n│SKP│\n└───┘{Style.RESET_ALL}"
        elif self.card_type == CardType.REVERSE:
            return f"{color_code}┌───┐\n│ ↻ │\n└───┘{Style.RESET_ALL}"
        elif self.card_type == CardType.DRAW_TWO:
            return f"{color_code}┌───┐\n│+2 │\n└───┘{Style.RESET_ALL}"
        elif self.card_type == CardType.WILD:
            return f"{Fore.WHITE}┌───┐\n│WLD│\n└───┘{Style.RESET_ALL}"
        elif self.card_type == CardType.WILD_DRAW_FOUR:
            return f"{Fore.WHITE}┌───┐\n│+4 │\n└───┘{Style.RESET_ALL}"
        return "┌───┐\n│???│\n└───┘"

    # Returns the card display split into lines for multi-card display
    def get_display_lines(self) -> List[str]:
        # Same color mapping as get_display()
        color_map = {
            CardColor.RED: Fore.RED,
            CardColor.BLUE: Fore.BLUE,
            CardColor.GREEN: Fore.GREEN,
            CardColor.YELLOW: Fore.YELLOW,
            CardColor.BLACK: Fore.WHITE
        }
        color_code = color_map.get(self.color, Fore.WHITE)

        # Create line-by-line ASCII art for each card type
        if self.card_type == CardType.NUMBER:
            num_str = str(self.number)
            lines = [
                f"{color_code}┌───┐{Style.RESET_ALL}",
                f"{color_code}│ {num_str} │{Style.RESET_ALL}" if len(num_str) == 1 else f"{color_code}│{num_str}│{Style.RESET_ALL}",
                f"{color_code}└───┘{Style.RESET_ALL}"
            ]
        elif self.card_type == CardType.SKIP:
            lines = [
                f"{color_code}┌───┐{Style.RESET_ALL}",
                f"{color_code}│SKP│{Style.RESET_ALL}",
                f"{color_code}└───┘{Style.RESET_ALL}"
            ]
        elif self.card_type == CardType.REVERSE:
            lines = [
                f"{color_code}┌───┐{Style.RESET_ALL}",
                f"{color_code}│ ↻ │{Style.RESET_ALL}",
                f"{color_code}└───┘{Style.RESET_ALL}"
            ]
        elif self.card_type == CardType.DRAW_TWO:
            lines = [
                f"{color_code}┌───┐{Style.RESET_ALL}",
                f"{color_code}│+2 │{Style.RESET_ALL}",
                f"{color_code}└───┘{Style.RESET_ALL}"
            ]
        elif self.card_type == CardType.WILD:
            lines = [
                f"{Fore.WHITE}┌───┐{Style.RESET_ALL}",
                f"{Fore.WHITE}│WLD│{Style.RESET_ALL}",
                f"{Fore.WHITE}└───┘{Style.RESET_ALL}"
            ]
        elif self.card_type == CardType.WILD_DRAW_FOUR:
            lines = [
                f"{Fore.WHITE}┌───┐{Style.RESET_ALL}",
                f"{Fore.WHITE}│+4 │{Style.RESET_ALL}",
                f"{Fore.WHITE}└───┘{Style.RESET_ALL}"
            ]
        else:
            lines = ["┌───┐", "│???│", "└───┘"]
        return lines

# Represents a player in the game (human or AI)
class Player:
    def __init__(self, name: str, is_ai: bool = False):
        self.name = name      # Player's name
        self.hand = []        # List of cards in player's hand
        self.is_ai = is_ai    # Whether this player is controlled by AI

    # Add a card to the player's hand
    def add_card(self, card: Card):
        self.hand.append(card)

    # Remove and return a card from the player's hand by index
    def remove_card(self, card_index: int) -> Card:
        return self.hand.pop(card_index)

    # Get list of indices of cards that can be played on the current top card
    def get_playable_cards(self, top_card: Card, current_color: CardColor) -> List[int]:
        playable_indices = []
        for i, card in enumerate(self.hand):
            # A card can be played if:
            # 1. It matches the current color
            # 2. It's a wild card (can always be played)
            # 3. It matches the top card's type and color
            # 4. It's a number card that matches the top card's number
            if (card.color == current_color or
                card.card_type in [CardType.WILD, CardType.WILD_DRAW_FOUR] or
                (card.card_type == top_card.card_type and card.color == top_card.color) or
                (card.card_type == CardType.NUMBER and top_card.card_type == CardType.NUMBER and card.number == top_card.number)):
                playable_indices.append(i)
        return playable_indices

    # Display the player's hand with numbered cards and ASCII art
    def display_hand(self):
        if not self.hand:
            print(f"{self.name}'s hand is empty!")
            return

        print(f"\n{self.name}'s hand ({len(self.hand)} cards):")

        # Display cards in rows of 4 for better readability
        for i in range(0, len(self.hand), 4):
            row_cards = self.hand[i:i+4]
            # Show card numbers above the cards
            numbers = "    ".join([f"{j+i+1:>2}" for j in range(len(row_cards))])
            print(f"  {numbers}")

            # Get display lines for all cards in this row
            all_card_lines = [card.get_display_lines() for card in row_cards]

            # Print each line of the ASCII art for all cards
            for line_idx in range(3):
                line_parts = [card_lines[line_idx] for card_lines in all_card_lines]
                print("  " + " ".join(line_parts))
            print()

# Main game class that manages the entire UNO game
class UNOGame:
    def __init__(self):
        self.deck = []                    # List of cards in the draw pile
        self.discard_pile = []            # List of cards in the discard pile
        self.players = []                 # List of Player objects
        self.current_player_index = 0     # Index of current player
        self.direction = 1                # 1 for clockwise, -1 for counter-clockwise
        self.current_color = CardColor.RED # Current color to match

    # Create a standard UNO deck with all 108 cards
    def create_deck(self):
        colors = [CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW]

        # Add number cards (0-9)
        for color in colors:
            # One zero card per color
            self.deck.append(Card(color, CardType.NUMBER, 0))
            # Two of each number 1-9 per color
            for number in range(1, 10):
                self.deck.extend([Card(color, CardType.NUMBER, number)] * 2)

        # Add action cards (Skip, Reverse, Draw Two)
        for color in colors:
            for _ in range(2):  # Two of each action card per color
                for card_type in [CardType.SKIP, CardType.REVERSE, CardType.DRAW_TWO]:
                    self.deck.append(Card(color, card_type))

        # Add wild cards (4 of each type)
        for _ in range(4):
            self.deck.extend([
                Card(CardColor.BLACK, CardType.WILD),
                Card(CardColor.BLACK, CardType.WILD_DRAW_FOUR)
            ])

    # Shuffle the deck using Python's random.shuffle
    def shuffle_deck(self):
        random.shuffle(self.deck)

    # Deal 7 cards to each player
    def deal_cards(self):
        for _ in range(7):  # Deal 7 cards
            for player in self.players:
                player.add_card(self.deck.pop())

    # Draw a card from the deck and add it to player's hand
    def draw_card(self, player: Player) -> Card:
        # If deck is empty, reshuffle discard pile (except top card)
        if not self.deck:
            top_card = self.discard_pile.pop()
            self.deck = self.discard_pile
            self.discard_pile = [top_card]
            self.shuffle_deck()

        card = self.deck.pop()
        player.add_card(card)
        return card

    # Play a card from player's hand to discard pile
    def play_card(self, player: Player, card_index: int) -> Card:
        card = player.remove_card(card_index)
        self.discard_pile.append(card)
        return card

    # AI logic for choosing which card to play
    def get_ai_move(self, player: Player, top_card: Card) -> Optional[int]:
        playable_cards = player.get_playable_cards(top_card, self.current_color)
        if not playable_cards:
            return None  # No playable cards

        # Prioritize number cards, then action cards, then wild cards
        number_cards = [i for i in playable_cards if player.hand[i].card_type == CardType.NUMBER]
        action_cards = [i for i in playable_cards if player.hand[i].card_type in [CardType.SKIP, CardType.REVERSE, CardType.DRAW_TWO]]
        wild_cards = [i for i in playable_cards if player.hand[i].card_type in [CardType.WILD, CardType.WILD_DRAW_FOUR]]

        # Return a random choice from the highest priority category available
        return random.choice(number_cards or action_cards or wild_cards or playable_cards)

    # Handle special card effects (Skip, Reverse, Draw Two, Wild, Wild Draw Four)
    def handle_special_card(self, card: Card, player: Player):
        if card.card_type == CardType.SKIP:
            print(f"{Fore.YELLOW}⏭️  {player.name} is skipped!{Style.RESET_ALL}")
            self.next_player()  # Skip next player's turn

        elif card.card_type == CardType.REVERSE:
            print(f"{Fore.CYAN}🔄 Direction reversed!{Style.RESET_ALL}")
            self.direction *= -1  # Change direction

        elif card.card_type == CardType.DRAW_TWO:
            next_player = self.players[(self.current_player_index + self.direction) % len(self.players)]
            print(f"{Fore.MAGENTA}📚 {next_player.name} draws 2 cards!{Style.RESET_ALL}")
            for _ in range(2):
                self.draw_card(next_player)
            self.next_player()  # Skip next player's turn

        elif card.card_type in [CardType.WILD, CardType.WILD_DRAW_FOUR]:
            # Handle Wild Draw Four effect
            if card.card_type == CardType.WILD_DRAW_FOUR:
                next_player = self.players[(self.current_player_index + self.direction) % len(self.players)]
                print(f"{Fore.MAGENTA}📚 {next_player.name} draws 4 cards!{Style.RESET_ALL}")
                for _ in range(4):
                    self.draw_card(next_player)
                self.next_player()  # Skip next player's turn

            # Choose a new color
            if player.is_ai:
                # AI randomly chooses a color
                colors = [CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW]
                self.current_color = random.choice(colors)
                print(f"{Fore.CYAN}🤖 {player.name} chose color: {self.current_color.value}{Style.RESET_ALL}")
            else:
                # Human player chooses color
                print(f"{Fore.WHITE}Choose a color:")
                for i, color in enumerate([CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW]):
                    color_code = [Fore.RED, Fore.BLUE, Fore.GREEN, Fore.YELLOW][i]
                    print(f"{color_code}{i+1}. {color.value}{Style.RESET_ALL}")

                # Get valid color choice from user
                while True:
                    try:
                        choice = int(input("Enter choice (1-4): ")) - 1
                        if 0 <= choice <= 3:
                            self.current_color = [CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW][choice]
                            break
                    except ValueError:
                        pass
                    print("Invalid choice. Please enter 1-4.")

    # Move to the next player based on current direction
    def next_player(self):
        self.current_player_index = (self.current_player_index + self.direction) % len(self.players)

    # Create a visual representation of the game direction and player order
    def get_direction_display(self) -> str:
        player_names = ["You", "Alice", "Bob", "Charlie"]
        direction_parts = []

        for i, name in enumerate(player_names):
            player = self.players[i]
            card_count = len(player.hand)

            # Highlight current player
            if i == self.current_player_index:
                direction_parts.append(f"{Fore.CYAN}{name}({card_count}){Style.RESET_ALL}")
            else:
                direction_parts.append(f"{name}({card_count})")

        # Show direction with arrows
        return " → ".join(direction_parts) if self.direction == 1 else " ← ".join(direction_parts)

        # Display the current game state with colored interface
    def display_game_state(self):
        # Clear the screen for better presentation
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Game header
        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"║                        UNO GAME                              ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")
        
        current_player = self.players[self.current_player_index]
        print(f"\n{Fore.YELLOW}🎯 {current_player.name}'s turn{Style.RESET_ALL} | {Fore.CYAN}🔄 {self.get_direction_display()}{Style.RESET_ALL}")
        
        # Show top card and game info
        if self.discard_pile:
            top_card = self.discard_pile[-1]
            print(f"\n{Fore.GREEN}📄 Top: \n{top_card.get_display()} \n| Color: {self.current_color.value} | Deck: {len(self.deck)} cards{Style.RESET_ALL} | ")

    # Determine whether to play AI or human turn based on player type
    def play_turn(self, player: Player) -> bool:
        return self.play_ai_turn(player) if player.is_ai else self.play_human_turn(player)

    # Handle AI player's turn
    def play_ai_turn(self, player: Player) -> bool:
        print(f"\n{Fore.CYAN}🤖 {player.name} is thinking...{Style.RESET_ALL}")
        time.sleep(2)  # Add delay for realistic AI thinking

        top_card = self.discard_pile[-1] if self.discard_pile else None
        card_index = self.get_ai_move(player, top_card)

        # If no playable cards, draw a card
        if card_index is None:
            drawn_card = self.draw_card(player)
            print(f"{Fore.YELLOW}📚 {player.name} draws: \n{drawn_card.get_display()}{Style.RESET_ALL}")
            time.sleep(1.5)
            return True

        # Play the chosen card
        played_card = self.play_card(player, card_index)
        print(f"{Fore.GREEN}🎴 {player.name} plays: \n{played_card.get_display()}{Style.RESET_ALL}")
        time.sleep(1)

        # Update current color if not a wild card
        if played_card.color != CardColor.BLACK:
            self.current_color = played_card.color

        # Handle special card effects
        self.handle_special_card(played_card, player)

        # Check for win condition
        if len(player.hand) == 0:
            print(f"\n{Fore.GREEN}🎉 {player.name} wins!{Style.RESET_ALL}")
            return False  # Game over
        return True

    # Handle human player's turn
    def play_human_turn(self, player: Player) -> bool:
        # Show player's hand
        player.display_hand()
        top_card = self.discard_pile[-1] if self.discard_pile else None
        playable_cards = player.get_playable_cards(top_card, self.current_color)

        # If no playable cards, draw a card
        if not playable_cards:
            print(f"{Fore.YELLOW}📚 No playable cards. Drawing a card...{Style.RESET_ALL}")
            drawn_card = self.draw_card(player)
            print(f"Drew: \n{drawn_card.get_display()}")
            input("Press Enter to continue...")
            return True

        # Show which cards can be played
        print(f"\n{Fore.GREEN}✅ Playable cards: {[i+1 for i in playable_cards]}{Style.RESET_ALL}")

        # Get player's choice
        while True:
            try:
                choice = input(f"Choose a card to play (1-{len(player.hand)}) or 'd' to draw: ").lower()

                # Handle draw option
                if choice == 'd':
                    drawn_card = self.draw_card(player)
                    print(f"Drew: {drawn_card.get_display()}")
                    input("Press Enter to continue...")
                    return True

                # Handle card play
                card_index = int(choice) - 1
                if card_index in playable_cards:
                    played_card = self.play_card(player, card_index)
                    print(f"Played: \n{played_card.get_display()}")

                    # Update current color if not a wild card
                    if played_card.color != CardColor.BLACK:
                        self.current_color = played_card.color

                    # Handle special card effects
                    self.handle_special_card(played_card, player)

                    # Check for win condition
                    if len(player.hand) == 0:
                        print(f"\n{Fore.GREEN}🎉 {player.name} wins!{Style.RESET_ALL}")
                        return False  # Game over
                    break
                else:
                    print("Invalid choice. Please select a playable card or draw.")
            except ValueError:
                print("Invalid input. Please enter a number or 'd' to draw.")

        input("Press Enter to continue...")
        return True

    # Main game loop
    def run_game(self):
        print(f"{Fore.CYAN}🎮 Welcome to UNO!{Style.RESET_ALL}")

        # Create players (1 human, 3 AI)
        self.players = [
            Player("You", is_ai=False),
            Player("Alice", is_ai=True),
            Player("Bob", is_ai=True),
            Player("Charlie", is_ai=True)
        ]

        # Setup the game
        self.create_deck()
        self.shuffle_deck()
        self.deal_cards()

        # Find a valid starting card (must be a number card)
        while True:
            card = self.deck.pop()
            if card.card_type == CardType.NUMBER:
                self.discard_pile.append(card)
                self.current_color = card.color
                break
            else:
                self.deck.insert(0, card)  # Put non-number cards back

        # Main game loop
        while True:
            self.display_game_state()
            current_player = self.players[self.current_player_index]

            # Play turn and check if game is over
            if not self.play_turn(current_player):
                break

            self.next_player()

        print(f"\n{Fore.GREEN}🎉 Game Over! Thanks for playing!{Style.RESET_ALL}")

# Main function to start the game
def main():
    game = UNOGame()
    try:
        game.run_game()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Game interrupted. Thanks for playing!{Style.RESET_ALL}")

# Entry point
if __name__ == "__main__":
    main()
