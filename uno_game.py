import random
import time
import os
from typing import List, Dict, Optional
from enum import Enum
import colorama
from colorama import Fore, Back, Style

# Initialize colorama for Windows compatibility
colorama.init()

class CardType(Enum):
    NUMBER = "number"
    SKIP = "skip"
    REVERSE = "reverse"
    DRAW_TWO = "draw_two"
    WILD = "wild"
    WILD_DRAW_FOUR = "wild_draw_four"

class CardColor(Enum):
    RED = "red"
    BLUE = "blue"
    GREEN = "green"
    YELLOW = "yellow"
    BLACK = "black"  # For wild cards

class Card:
    def __init__(self, color: CardColor, card_type: CardType, number: int = None):
        self.color = color
        self.card_type = card_type
        self.number = number

    def __str__(self):
        if self.card_type == CardType.NUMBER:
            return f"{self.color.value}_{self.number}"
        return f"{self.color.value}_{self.card_type.value}"

    def get_display(self) -> str:
        """Get colored ASCII representation of the card"""
        if self.card_type == CardType.NUMBER:
            color_map = {
                CardColor.RED: Fore.RED,
                CardColor.BLUE: Fore.BLUE,
                CardColor.GREEN: Fore.GREEN,
                CardColor.YELLOW: Fore.YELLOW,
                CardColor.BLACK: Fore.WHITE
            }
            color_code = color_map.get(self.color, Fore.WHITE)
            # Center the number properly
            number_str = str(self.number)
            if len(number_str) == 1:
                return f"{color_code}┌───┐\n│ {number_str} │\n└───┘{Style.RESET_ALL}"
            else:
                return f"{color_code}┌───┐\n│{number_str}│\n└───┘{Style.RESET_ALL}"

        elif self.card_type == CardType.SKIP:
            color_map = {
                CardColor.RED: Fore.RED,
                CardColor.BLUE: Fore.BLUE,
                CardColor.GREEN: Fore.GREEN,
                CardColor.YELLOW: Fore.YELLOW
            }
            color_code = color_map.get(self.color, Fore.WHITE)
            return f"{color_code}┌───┐\n│SKP│\n└───┘{Style.RESET_ALL}"

        elif self.card_type == CardType.REVERSE:
            color_map = {
                CardColor.RED: Fore.RED,
                CardColor.BLUE: Fore.BLUE,
                CardColor.GREEN: Fore.GREEN,
                CardColor.YELLOW: Fore.YELLOW
            }
            color_code = color_map.get(self.color, Fore.WHITE)
            return f"{color_code}┌───┐\n│ ↻ │\n└───┘{Style.RESET_ALL}"

        elif self.card_type == CardType.DRAW_TWO:
            color_map = {
                CardColor.RED: Fore.RED,
                CardColor.BLUE: Fore.BLUE,
                CardColor.GREEN: Fore.GREEN,
                CardColor.YELLOW: Fore.YELLOW
            }
            color_code = color_map.get(self.color, Fore.WHITE)
            return f"{color_code}┌───┐\n│+2 │\n└───┘{Style.RESET_ALL}"

        elif self.card_type == CardType.WILD:
            return f"{Fore.WHITE}┌───┐\n│WLD│\n└───┘{Style.RESET_ALL}"

        elif self.card_type == CardType.WILD_DRAW_FOUR:
            return f"{Fore.WHITE}┌───┐\n│+4 │\n└───┘{Style.RESET_ALL}"

        return "┌───┐\n│???│\n└───┘"

    def get_display_lines(self) -> List[str]:
        """Get the card display as separate lines for proper color handling"""
        if self.card_type == CardType.NUMBER:
            color_map = {
                CardColor.RED: Fore.RED,
                CardColor.BLUE: Fore.BLUE,
                CardColor.GREEN: Fore.GREEN,
                CardColor.YELLOW: Fore.YELLOW,
                CardColor.BLACK: Fore.WHITE
            }
            color_code = color_map.get(self.color, Fore.WHITE)
            number_str = str(self.number)
            if len(number_str) == 1:
                return [
                    f"{color_code}┌───┐{Style.RESET_ALL}",
                    f"{color_code}│ {number_str} │{Style.RESET_ALL}",
                    f"{color_code}└───┘{Style.RESET_ALL}"
                ]
            else:
                return [
                    f"{color_code}┌───┐{Style.RESET_ALL}",
                    f"{color_code}│{number_str}│{Style.RESET_ALL}",
                    f"{color_code}└───┘{Style.RESET_ALL}"
                ]

        elif self.card_type == CardType.SKIP:
            color_map = {
                CardColor.RED: Fore.RED,
                CardColor.BLUE: Fore.BLUE,
                CardColor.GREEN: Fore.GREEN,
                CardColor.YELLOW: Fore.YELLOW
            }
            color_code = color_map.get(self.color, Fore.WHITE)
            return [
                f"{color_code}┌───┐{Style.RESET_ALL}",
                f"{color_code}│SKP│{Style.RESET_ALL}",
                f"{color_code}└───┘{Style.RESET_ALL}"
            ]

        elif self.card_type == CardType.REVERSE:
            color_map = {
                CardColor.RED: Fore.RED,
                CardColor.BLUE: Fore.BLUE,
                CardColor.GREEN: Fore.GREEN,
                CardColor.YELLOW: Fore.YELLOW
            }
            color_code = color_map.get(self.color, Fore.WHITE)
            return [
                f"{color_code}┌───┐{Style.RESET_ALL}",
                f"{color_code}│ ↻ │{Style.RESET_ALL}",
                f"{color_code}└───┘{Style.RESET_ALL}"
            ]

        elif self.card_type == CardType.DRAW_TWO:
            color_map = {
                CardColor.RED: Fore.RED,
                CardColor.BLUE: Fore.BLUE,
                CardColor.GREEN: Fore.GREEN,
                CardColor.YELLOW: Fore.YELLOW
            }
            color_code = color_map.get(self.color, Fore.WHITE)
            return [
                f"{color_code}┌───┐{Style.RESET_ALL}",
                f"{color_code}│+2 │{Style.RESET_ALL}",
                f"{color_code}└───┘{Style.RESET_ALL}"
            ]

        elif self.card_type == CardType.WILD:
            return [
                f"{Fore.WHITE}┌───┐{Style.RESET_ALL}",
                f"{Fore.WHITE}│WLD│{Style.RESET_ALL}",
                f"{Fore.WHITE}└───┘{Style.RESET_ALL}"
            ]

        elif self.card_type == CardType.WILD_DRAW_FOUR:
            return [
                f"{Fore.WHITE}┌───┐{Style.RESET_ALL}",
                f"{Fore.WHITE}│+4 │{Style.RESET_ALL}",
                f"{Fore.WHITE}└───┘{Style.RESET_ALL}"
            ]

        return [
            "┌───┐",
            "│???│",
            "└───┘"
        ]

class Player:
    def __init__(self, name: str, is_ai: bool = False):
        self.name = name
        self.hand: List[Card] = []
        self.is_ai = is_ai

    def add_card(self, card: Card):
        self.hand.append(card)

    def remove_card(self, card_index: int) -> Card:
        return self.hand.pop(card_index)

    def get_playable_cards(self, top_card: Card, current_color: CardColor) -> List[int]:
        """Get indices of cards that can be played"""
        playable = []
        for i, card in enumerate(self.hand):
            if (card.color == current_color or
                card.card_type == CardType.WILD or
                card.card_type == CardType.WILD_DRAW_FOUR or
                (card.card_type == top_card.card_type and card.color == top_card.color) or
                (card.card_type == CardType.NUMBER and top_card.card_type == CardType.NUMBER and
                 card.number == top_card.number)):
                playable.append(i)
        return playable

    def display_hand(self):
        """Display the player's hand"""
        if not self.hand:
            print(f"{self.name}'s hand is empty!")
            return

        print(f"\n{self.name}'s hand ({len(self.hand)} cards):")
        # Display cards in a more compact format with proper color handling
        for i in range(0, len(self.hand), 4):  # Show 4 cards per row
            row_cards = self.hand[i:i+4]
            # Print card numbers with more spacing
            numbers = "    ".join([f"{j+i+1:>2}" for j in range(len(row_cards))])
            print(f"  {numbers}")

            # Get display lines for each card
            all_card_lines = [card.get_display_lines() for card in row_cards]

            # Print each line of the cards
            for line_idx in range(3):  # Each card has 3 lines
                line_parts = []
                for card_lines in all_card_lines:
                    line_parts.append(card_lines[line_idx])
                print("  " + " ".join(line_parts))
            print()

class UNOGame:
    def __init__(self):
        self.deck: List[Card] = []
        self.discard_pile: List[Card] = []
        self.players: List[Player] = []
        self.current_player_index = 0
        self.direction = 1  # 1 for clockwise, -1 for counterclockwise
        self.current_color: CardColor = CardColor.RED

    def create_deck(self):
        """Create a standard UNO deck"""
        colors = [CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW]

        # Add number cards (0-9, two of each except 0)
        for color in colors:
            # One zero card
            self.deck.append(Card(color, CardType.NUMBER, 0))
            # Two of each number 1-9
            for number in range(1, 10):
                self.deck.append(Card(color, CardType.NUMBER, number))
                self.deck.append(Card(color, CardType.NUMBER, number))

        # Add action cards (two of each per color)
        for color in colors:
            for _ in range(2):
                self.deck.append(Card(color, CardType.SKIP))
                self.deck.append(Card(color, CardType.REVERSE))
                self.deck.append(Card(color, CardType.DRAW_TWO))

        # Add wild cards (4 of each)
        for _ in range(4):
            self.deck.append(Card(CardColor.BLACK, CardType.WILD))
            self.deck.append(Card(CardColor.BLACK, CardType.WILD_DRAW_FOUR))

    def shuffle_deck(self):
        """Shuffle the deck"""
        random.shuffle(self.deck)

    def deal_cards(self):
        """Deal 7 cards to each player"""
        for _ in range(7):
            for player in self.players:
                player.add_card(self.deck.pop())

    def draw_card(self, player: Player) -> Card:
        """Draw a card from the deck"""
        if not self.deck:
            # Reshuffle discard pile (except top card)
            top_card = self.discard_pile.pop()
            self.deck = self.discard_pile
            self.discard_pile = [top_card]
            self.shuffle_deck()

        card = self.deck.pop()
        player.add_card(card)
        return card

    def play_card(self, player: Player, card_index: int) -> Card:
        """Play a card from player's hand"""
        card = player.remove_card(card_index)
        self.discard_pile.append(card)
        return card

    def get_ai_move(self, player: Player, top_card: Card) -> Optional[int]:
        """Get AI player's move"""
        playable_cards = player.get_playable_cards(top_card, self.current_color)

        if not playable_cards:
            return None

        # Simple AI: prefer number cards, then action cards, then wild cards
        number_cards = [i for i in playable_cards if player.hand[i].card_type == CardType.NUMBER]
        action_cards = [i for i in playable_cards if player.hand[i].card_type in [CardType.SKIP, CardType.REVERSE, CardType.DRAW_TWO]]
        wild_cards = [i for i in playable_cards if player.hand[i].card_type in [CardType.WILD, CardType.WILD_DRAW_FOUR]]

        if number_cards:
            return random.choice(number_cards)
        elif action_cards:
            return random.choice(action_cards)
        elif wild_cards:
            return random.choice(wild_cards)

        return random.choice(playable_cards)

    def handle_special_card(self, card: Card, player: Player):
        """Handle special card effects"""
        if card.card_type == CardType.SKIP:
            print(f"{Fore.YELLOW}⏭️  {player.name} is skipped!{Style.RESET_ALL}")
            self.next_player()

        elif card.card_type == CardType.REVERSE:
            print(f"{Fore.CYAN}🔄 Direction reversed!{Style.RESET_ALL}")
            self.direction *= -1

        elif card.card_type == CardType.DRAW_TWO:
            next_player = self.players[(self.current_player_index + self.direction) % len(self.players)]
            print(f"{Fore.MAGENTA}📚 {next_player.name} draws 2 cards!{Style.RESET_ALL}")
            for _ in range(2):
                self.draw_card(next_player)
            self.next_player()

        elif card.card_type == CardType.WILD:
            if player.is_ai:
                # AI chooses random color
                colors = [CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW]
                self.current_color = random.choice(colors)
                print(f"{Fore.CYAN}🤖 {player.name} chose color: {self.current_color.value}{Style.RESET_ALL}")
            else:
                # Human player chooses color
                print(f"{Fore.WHITE}Choose a color:")
                print(f"{Fore.RED}1. Red{Style.RESET_ALL}")
                print(f"{Fore.BLUE}2. Blue{Style.RESET_ALL}")
                print(f"{Fore.GREEN}3. Green{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}4. Yellow{Style.RESET_ALL}")

                while True:
                    try:
                        choice = int(input("Enter choice (1-4): ")) - 1
                        if 0 <= choice <= 3:
                            colors = [CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW]
                            self.current_color = colors[choice]
                            break
                    except ValueError:
                        pass
                    print("Invalid choice. Please enter 1-4.")

        elif card.card_type == CardType.WILD_DRAW_FOUR:
            next_player = self.players[(self.current_player_index + self.direction) % len(self.players)]
            print(f"{Fore.MAGENTA}📚 {next_player.name} draws 4 cards!{Style.RESET_ALL}")
            for _ in range(4):
                self.draw_card(next_player)

            if player.is_ai:
                colors = [CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW]
                self.current_color = random.choice(colors)
                print(f"{Fore.CYAN}🤖 {player.name} chose color: {self.current_color.value}{Style.RESET_ALL}")
            else:
                print(f"{Fore.WHITE}Choose a color:")
                print(f"{Fore.RED}1. Red{Style.RESET_ALL}")
                print(f"{Fore.BLUE}2. Blue{Style.RESET_ALL}")
                print(f"{Fore.GREEN}3. Green{Style.RESET_ALL}")
                print(f"{Fore.YELLOW}4. Yellow{Style.RESET_ALL}")

                while True:
                    try:
                        choice = int(input("Enter choice (1-4): ")) - 1
                        if 0 <= choice <= 3:
                            colors = [CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW]
                            self.current_color = colors[choice]
                            break
                    except ValueError:
                        pass
                    print("Invalid choice. Please enter 1-4.")

            self.next_player()

    def next_player(self):
        """Move to next player"""
        self.current_player_index = (self.current_player_index + self.direction) % len(self.players)

    def get_direction_display(self) -> str:
        """Get the current direction as a string with player names and card counts"""
        player_names = ["You", "Alice", "Bob", "Charlie"]
        direction_parts = []

        for i, name in enumerate(player_names):
            player = self.players[i]
            card_count = len(player.hand)

            if i == self.current_player_index:
                # Current player in cyan
                direction_parts.append(f"{Fore.CYAN}{name}({card_count}){Style.RESET_ALL}")
            else:
                # Other players in default color
                direction_parts.append(f"{name}({card_count})")

        if self.direction == 1:
            return " → ".join(direction_parts)
        else:
            return " ← ".join(direction_parts)

    def display_game_state(self):
        """Display current game state"""
        os.system('cls' if os.name == 'nt' else 'clear')

        print(f"{Fore.CYAN}╔══════════════════════════════════════════════════════════════╗")
        print(f"║                        UNO GAME                              ║")
        print(f"╚══════════════════════════════════════════════════════════════╝{Style.RESET_ALL}")

        # Show current player and direction in one line
        current_player = self.players[self.current_player_index]
        print(f"\n{Fore.YELLOW}🎯 {current_player.name}'s turn{Style.RESET_ALL} | {Fore.CYAN}🔄 {self.get_direction_display()}{Style.RESET_ALL}")

        # Show top card and deck info in compact format
        if self.discard_pile:
            top_card = self.discard_pile[-1]
            print(f"\n{Fore.GREEN}📄 Top: \n{top_card.get_display()} \n| Color: {self.current_color.value} | Deck: {len(self.deck)} cards{Style.RESET_ALL} | ")


    def play_turn(self, player: Player) -> bool:
        """Play a single turn, return True if game should continue"""
        if player.is_ai:
            return self.play_ai_turn(player)
        else:
            return self.play_human_turn(player)

    def play_ai_turn(self, player: Player) -> bool:
        """Handle AI player's turn"""
        print(f"\n{Fore.CYAN}🤖 {player.name} is thinking...{Style.RESET_ALL}")
        time.sleep(2)  # Slower AI thinking time

        top_card = self.discard_pile[-1] if self.discard_pile else None
        card_index = self.get_ai_move(player, top_card)

        if card_index is None:
            # AI must draw a card
            drawn_card = self.draw_card(player)
            print(f"{Fore.YELLOW}📚 {player.name} draws: \n{drawn_card.get_display()}{Style.RESET_ALL}")
            time.sleep(1.5)
            return True

        # AI plays a card
        played_card = self.play_card(player, card_index)
        print(f"{Fore.GREEN}🎴 {player.name} plays: \n{played_card.get_display()}{Style.RESET_ALL}")
        time.sleep(1)  # Pause to show the move

        # Update current color if it's a colored card
        if played_card.color != CardColor.BLACK:
            self.current_color = played_card.color

        # Handle special card effects
        self.handle_special_card(played_card, player)

        # Check for win
        if len(player.hand) == 0:
            print(f"\n{Fore.GREEN}🎉 {player.name} wins!{Style.RESET_ALL}")
            return False

        return True

    def play_human_turn(self, player: Player) -> bool:
        """Handle human player's turn"""
        player.display_hand()

        top_card = self.discard_pile[-1] if self.discard_pile else None
        playable_cards = player.get_playable_cards(top_card, self.current_color)

        if not playable_cards:
            print(f"{Fore.YELLOW}📚 No playable cards. Drawing a card...{Style.RESET_ALL}")
            drawn_card = self.draw_card(player)
            print(f"Drew: \n{drawn_card.get_display()}")
            input("Press Enter to continue...")
            return True

        print(f"\n{Fore.GREEN}✅ Playable cards: {[i+1 for i in playable_cards]}{Style.RESET_ALL}")

        while True:
            try:
                choice = input(f"Choose a card to play (1-{len(player.hand)}) or 'd' to draw: ").lower()

                if choice == 'd':
                    drawn_card = self.draw_card(player)
                    print(f"Drew: {drawn_card.get_display()}")
                    input("Press Enter to continue...")
                    return True

                card_index = int(choice) - 1
                if card_index in playable_cards:
                    played_card = self.play_card(player, card_index)
                    print(f"Played: \n{played_card.get_display()}")

                    # Update current color if it's a colored card
                    if played_card.color != CardColor.BLACK:
                        self.current_color = played_card.color

                    # Handle special card effects
                    self.handle_special_card(played_card, player)

                    # Check for win
                    if len(player.hand) == 0:
                        print(f"\n{Fore.GREEN}🎉 {player.name} wins!{Style.RESET_ALL}")
                        return False

                    break
                else:
                    print("Invalid choice. Please select a playable card or draw.")
            except ValueError:
                print("Invalid input. Please enter a number or 'd' to draw.")

        input("Press Enter to continue...")
        return True

    def run_game(self):
        """Run the complete UNO game"""
        print(f"{Fore.CYAN}🎮 Welcome to UNO!{Style.RESET_ALL}")

        # Create players
        self.players = [
            Player("You", is_ai=False),
            Player("Alice", is_ai=True),
            Player("Bob", is_ai=True),
            Player("Charlie", is_ai=True)
        ]

        # Setup game
        self.create_deck()
        self.shuffle_deck()
        self.deal_cards()

        # Start with a number card
        while True:
            card = self.deck.pop()
            if card.card_type == CardType.NUMBER:
                self.discard_pile.append(card)
                self.current_color = card.color
                break
            else:
                self.deck.insert(0, card)

        # Game loop
        while True:
            self.display_game_state()
            current_player = self.players[self.current_player_index]

            if not self.play_turn(current_player):
                break

            self.next_player()

        print(f"\n{Fore.GREEN}🎉 Game Over! Thanks for playing!{Style.RESET_ALL}")

def main():
    """Main function to start the game"""
    game = UNOGame()
    try:
        game.run_game()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Game interrupted. Thanks for playing!{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
