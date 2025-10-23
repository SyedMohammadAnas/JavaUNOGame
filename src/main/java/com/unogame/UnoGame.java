package com.unogame;

import java.util.*;

/**
 * Main game class that manages the entire UNO game.
 * Handles game state, player turns, card effects, and game flow.
 */
public class UnoGame {
    List<Card> deck; // Package-private for testing
    private List<Card> discardPile;
    List<Player> players; // Package-private for testing
    int currentPlayerIndex; // Package-private for testing
    int direction; // 1 for clockwise, -1 for counter-clockwise, package-private for testing
    private CardColor currentColor;
    private Scanner scanner;

    /**
     * Constructor for creating a new UNO game.
     */
    public UnoGame() {
        this.deck = new ArrayList<>();
        this.discardPile = new ArrayList<>();
        this.players = new ArrayList<>();
        this.currentPlayerIndex = 0;
        this.direction = 1;
        this.currentColor = CardColor.RED;
        this.scanner = new Scanner(System.in);
    }

    /**
     * Create a standard UNO deck with all 108 cards.
     */
    public void createDeck() {
        List<CardColor> colors = Arrays.asList(CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW);

        // Add number cards (0-9)
        for (CardColor color : colors) {
            // One zero card per color
            deck.add(new Card(color, CardType.NUMBER, 0));
            // Two of each number 1-9 per color
            for (int number = 1; number <= 9; number++) {
                deck.add(new Card(color, CardType.NUMBER, number));
                deck.add(new Card(color, CardType.NUMBER, number));
            }
        }

        // Add action cards (Skip, Reverse, Draw Two)
        for (CardColor color : colors) {
            for (int i = 0; i < 2; i++) { // Two of each action card per color
                deck.add(new Card(color, CardType.SKIP));
                deck.add(new Card(color, CardType.REVERSE));
                deck.add(new Card(color, CardType.DRAW_TWO));
            }
        }

        // Add wild cards (4 of each type)
        for (int i = 0; i < 4; i++) {
            deck.add(new Card(CardColor.BLACK, CardType.WILD));
            deck.add(new Card(CardColor.BLACK, CardType.WILD_DRAW_FOUR));
        }
    }

    /**
     * Shuffle the deck using Collections.shuffle.
     */
    public void shuffleDeck() {
        Collections.shuffle(deck);
    }

    /**
     * Deal 7 cards to each player.
     */
    public void dealCards() {
        for (int i = 0; i < 7; i++) { // Deal 7 cards
            for (Player player : players) {
                player.addCard(deck.remove(deck.size() - 1));
            }
        }
    }

    /**
     * Draw a card from the deck and add it to player's hand.
     * @param player The player drawing the card
     * @return The drawn card
     */
    public Card drawCard(Player player) {
        // If deck is empty, reshuffle discard pile (except top card)
        if (deck.isEmpty()) {
            Card topCard = discardPile.remove(discardPile.size() - 1);
            deck = new ArrayList<>(discardPile);
            discardPile = new ArrayList<>();
            discardPile.add(topCard);
            shuffleDeck();
        }

        Card card = deck.remove(deck.size() - 1);
        player.addCard(card);
        return card;
    }

    /**
     * Play a card from player's hand to discard pile.
     * @param player The player playing the card
     * @param cardIndex The index of the card to play
     * @return The played card
     */
    public Card playCard(Player player, int cardIndex) {
        Card card = player.removeCard(cardIndex);
        discardPile.add(card);
        return card;
    }

    /**
     * AI logic for choosing which card to play.
     * @param player The AI player
     * @param topCard The current top card
     * @return Index of card to play, or -1 if no playable cards
     */
    public int getAiMove(Player player, Card topCard) {
        List<Integer> playableCards = player.getPlayableCards(topCard, currentColor);
        if (playableCards.isEmpty()) {
            return -1; // No playable cards
        }

        // Prioritize number cards, then action cards, then wild cards
        List<Integer> numberCards = new ArrayList<>();
        List<Integer> actionCards = new ArrayList<>();
        List<Integer> wildCards = new ArrayList<>();

        for (int index : playableCards) {
            Card card = player.getCard(index);
            if (card.getCardType() == CardType.NUMBER) {
                numberCards.add(index);
            } else if (card.getCardType() == CardType.SKIP ||
                      card.getCardType() == CardType.REVERSE ||
                      card.getCardType() == CardType.DRAW_TWO) {
                actionCards.add(index);
            } else if (card.getCardType() == CardType.WILD ||
                      card.getCardType() == CardType.WILD_DRAW_FOUR) {
                wildCards.add(index);
            }
        }

        // Return a random choice from the highest priority category available
        Random random = new Random();
        if (!numberCards.isEmpty()) {
            return numberCards.get(random.nextInt(numberCards.size()));
        } else if (!actionCards.isEmpty()) {
            return actionCards.get(random.nextInt(actionCards.size()));
        } else if (!wildCards.isEmpty()) {
            return wildCards.get(random.nextInt(wildCards.size()));
        } else {
            return playableCards.get(random.nextInt(playableCards.size()));
        }
    }

    /**
     * Handle special card effects (Skip, Reverse, Draw Two, Wild, Wild Draw Four).
     * @param card The card that was played
     * @param player The player who played the card
     */
    public void handleSpecialCard(Card card, Player player) {
        if (card.getCardType() == CardType.SKIP) {
            System.out.println(TerminalColors.colorize(TerminalColors.YELLOW, "⏭️  " + player.getName() + " is skipped!"));
            nextPlayer(); // Skip next player's turn
        } else if (card.getCardType() == CardType.REVERSE) {
            System.out.println(TerminalColors.colorize(TerminalColors.CYAN, "🔄 Direction reversed!"));
            direction *= -1; // Change direction
        } else if (card.getCardType() == CardType.DRAW_TWO) {
            Player nextPlayer = players.get((currentPlayerIndex + direction + players.size()) % players.size());
            System.out.println(TerminalColors.colorize(TerminalColors.MAGENTA, "📚 " + nextPlayer.getName() + " draws 2 cards!"));
            for (int i = 0; i < 2; i++) {
                drawCard(nextPlayer);
            }
            nextPlayer(); // Skip next player's turn
        } else if (card.getCardType() == CardType.WILD || card.getCardType() == CardType.WILD_DRAW_FOUR) {
            // Handle Wild Draw Four effect
            if (card.getCardType() == CardType.WILD_DRAW_FOUR) {
                Player nextPlayer = players.get((currentPlayerIndex + direction + players.size()) % players.size());
                System.out.println(TerminalColors.colorize(TerminalColors.MAGENTA, "📚 " + nextPlayer.getName() + " draws 4 cards!"));
                for (int i = 0; i < 4; i++) {
                    drawCard(nextPlayer);
                }
                nextPlayer(); // Skip next player's turn
            }

            // Choose a new color
            if (player.isAi()) {
                // AI randomly chooses a color
                List<CardColor> colors = Arrays.asList(CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW);
                Random random = new Random();
                currentColor = colors.get(random.nextInt(colors.size()));
                System.out.println(TerminalColors.colorize(TerminalColors.CYAN, "🤖 " + player.getName() + " chose color: " + currentColor.getValue()));
            } else {
                // Human player chooses color
                System.out.println(TerminalColors.colorize(TerminalColors.WHITE, "Choose a color:"));
                List<CardColor> colors = Arrays.asList(CardColor.RED, CardColor.BLUE, CardColor.GREEN, CardColor.YELLOW);
                String[] colorNames = {"Red", "Blue", "Green", "Yellow"};
                String[] colorCodes = {TerminalColors.RED, TerminalColors.BLUE, TerminalColors.GREEN, TerminalColors.YELLOW};

                for (int i = 0; i < colors.size(); i++) {
                    System.out.println(TerminalColors.colorize(colorCodes[i], (i + 1) + ". " + colorNames[i]));
                }

                // Get valid color choice from user
                while (true) {
                    try {
                        System.out.print("Enter choice (1-4): ");
                        int choice = Integer.parseInt(scanner.nextLine()) - 1;
                        if (choice >= 0 && choice < colors.size()) {
                            currentColor = colors.get(choice);
                            break;
                        }
                    } catch (NumberFormatException e) {
                        // Invalid input, continue loop
                    }
                    System.out.println("Invalid choice. Please enter 1-4.");
                }
            }
        }
    }

    /**
     * Move to the next player based on current direction.
     */
    public void nextPlayer() {
        currentPlayerIndex = (currentPlayerIndex + direction + players.size()) % players.size();
    }

    /**
     * Create a visual representation of the game direction and player order.
     * @return String representation of player order and direction
     */
    public String getDirectionDisplay() {
        String[] playerNames = {"You", "Alice", "Bob", "Charlie"};
        List<String> directionParts = new ArrayList<>();

        for (int i = 0; i < playerNames.length && i < players.size(); i++) {
            Player player = players.get(i);
            int cardCount = player.getCardCount();

            // Highlight current player
            if (i == currentPlayerIndex) {
                directionParts.add(TerminalColors.colorize(TerminalColors.CYAN, playerNames[i] + "(" + cardCount + ")"));
            } else {
                directionParts.add(playerNames[i] + "(" + cardCount + ")");
            }
        }

        // Show direction with arrows
        String separator = direction == 1 ? " → " : " ← ";
        return String.join(separator, directionParts);
    }

    /**
     * Display the current game state with colored interface.
     */
    public void displayGameState() {
        // Clear the screen for better presentation
        clearScreen();

        // Game header
        System.out.println(TerminalColors.colorize(TerminalColors.CYAN, "╔══════════════════════════════════════════════════════════════╗"));
        System.out.println(TerminalColors.colorize(TerminalColors.CYAN, "║                        UNO GAME                              ║"));
        System.out.println(TerminalColors.colorize(TerminalColors.CYAN, "╚══════════════════════════════════════════════════════════════╝"));

        Player currentPlayer = players.get(currentPlayerIndex);
        System.out.println("\n" + TerminalColors.colorize(TerminalColors.YELLOW, "🎯 " + currentPlayer.getName() + "'s turn") +
                          " | " + TerminalColors.colorize(TerminalColors.CYAN, "🔄 " + getDirectionDisplay()));

        // Show top card and game info
        if (!discardPile.isEmpty()) {
            Card topCard = discardPile.get(discardPile.size() - 1);
            System.out.println("\n" + TerminalColors.colorize(TerminalColors.GREEN, "📄 Top: \n" + topCard.getDisplay() +
                              " \n| Color: " + currentColor.getValue() + " | Deck: " + deck.size() + " cards") + " | ");
        }
    }

    /**
     * Clear the screen (cross-platform).
     */
    private void clearScreen() {
        try {
            String os = System.getProperty("os.name").toLowerCase();
            if (os.contains("win")) {
                new ProcessBuilder("cmd", "/c", "cls").inheritIO().start().waitFor();
            } else {
                System.out.print("\033[H\033[2J");
                System.out.flush();
            }
        } catch (Exception e) {
            // If clearing fails, just print some newlines
            for (int i = 0; i < 50; i++) {
                System.out.println();
            }
        }
    }

    /**
     * Determine whether to play AI or human turn based on player type.
     * @param player The current player
     * @return true if game should continue, false if game is over
     */
    public boolean playTurn(Player player) {
        return player.isAi() ? playAiTurn(player) : playHumanTurn(player);
    }

    /**
     * Handle AI player's turn.
     * @param player The AI player
     * @return true if game should continue, false if game is over
     */
    public boolean playAiTurn(Player player) {
        System.out.println("\n" + TerminalColors.colorize(TerminalColors.CYAN, "🤖 " + player.getName() + " is thinking..."));

        try {
            Thread.sleep(2000); // Add delay for realistic AI thinking
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        Card topCard = discardPile.isEmpty() ? null : discardPile.get(discardPile.size() - 1);
        int cardIndex = getAiMove(player, topCard);

        // If no playable cards, draw a card
        if (cardIndex == -1) {
            Card drawnCard = drawCard(player);
            System.out.println(TerminalColors.colorize(TerminalColors.YELLOW, "📚 " + player.getName() + " draws: \n" + drawnCard.getDisplay()));
            try {
                Thread.sleep(1500);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return true;
        }

        // Play the chosen card
        Card playedCard = playCard(player, cardIndex);
        System.out.println(TerminalColors.colorize(TerminalColors.GREEN, "🎴 " + player.getName() + " plays: \n" + playedCard.getDisplay()));
        try {
            Thread.sleep(1000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        // Update current color if not a wild card
        if (playedCard.getColor() != CardColor.BLACK) {
            currentColor = playedCard.getColor();
        }

        // Handle special card effects
        handleSpecialCard(playedCard, player);

        // Check for win condition
        if (player.hasWon()) {
            System.out.println("\n" + TerminalColors.colorize(TerminalColors.GREEN, "🎉 " + player.getName() + " wins!"));
            return false; // Game over
        }
        return true;
    }

    /**
     * Handle human player's turn.
     * @param player The human player
     * @return true if game should continue, false if game is over
     */
    public boolean playHumanTurn(Player player) {
        // Show player's hand
        player.displayHand();
        Card topCard = discardPile.isEmpty() ? null : discardPile.get(discardPile.size() - 1);
        List<Integer> playableCards = player.getPlayableCards(topCard, currentColor);

        // If no playable cards, draw a card
        if (playableCards.isEmpty()) {
            System.out.println(TerminalColors.colorize(TerminalColors.YELLOW, "📚 No playable cards. Drawing a card..."));
            Card drawnCard = drawCard(player);
            System.out.println("Drew: \n" + drawnCard.getDisplay());
            System.out.print("Press Enter to continue...");
            scanner.nextLine();
            return true;
        }

        // Show which cards can be played
        List<Integer> playableNumbers = new ArrayList<>();
        for (int index : playableCards) {
            playableNumbers.add(index + 1);
        }
        System.out.println("\n" + TerminalColors.colorize(TerminalColors.GREEN, "✅ Playable cards: " + playableNumbers));

        // Get player's choice
        while (true) {
            try {
                System.out.print("Choose a card to play (1-" + player.getCardCount() + ") or 'd' to draw: ");
                String choice = scanner.nextLine().toLowerCase();

                // Handle draw option
                if ("d".equals(choice)) {
                    Card drawnCard = drawCard(player);
                    System.out.println("Drew: " + drawnCard.getDisplay());
                    System.out.print("Press Enter to continue...");
                    scanner.nextLine();
                    return true;
                }

                // Handle card play
                int cardIndex = Integer.parseInt(choice) - 1;
                if (cardIndex >= 0 && cardIndex < player.getCardCount() && playableCards.contains(cardIndex)) {
                    Card playedCard = playCard(player, cardIndex);
                    System.out.println("Played: \n" + playedCard.getDisplay());

                    // Update current color if not a wild card
                    if (playedCard.getColor() != CardColor.BLACK) {
                        currentColor = playedCard.getColor();
                    }

                    // Handle special card effects
                    handleSpecialCard(playedCard, player);

                    // Check for win condition
                    if (player.hasWon()) {
                        System.out.println("\n" + TerminalColors.colorize(TerminalColors.GREEN, "🎉 " + player.getName() + " wins!"));
                        return false; // Game over
                    }
                    break;
                } else {
                    System.out.println("Invalid choice. Please select a playable card or draw.");
                }
            } catch (NumberFormatException e) {
                System.out.println("Invalid input. Please enter a number or 'd' to draw.");
            }
        }

        System.out.print("Press Enter to continue...");
        scanner.nextLine();
        return true;
    }

    /**
     * Main game loop.
     */
    public void runGame() {
        System.out.println(TerminalColors.colorize(TerminalColors.CYAN, "🎮 Welcome to UNO!"));

        // Create players (1 human, 3 AI)
        players.add(new Player("You", false));
        players.add(new Player("Alice", true));
        players.add(new Player("Bob", true));
        players.add(new Player("Charlie", true));

        // Setup the game
        createDeck();
        shuffleDeck();
        dealCards();

        // Find a valid starting card (must be a number card)
        while (true) {
            Card card = deck.remove(deck.size() - 1);
            if (card.getCardType() == CardType.NUMBER) {
                discardPile.add(card);
                currentColor = card.getColor();
                break;
            } else {
                deck.add(0, card); // Put non-number cards back
            }
        }

        // Main game loop
        while (true) {
            displayGameState();
            Player currentPlayer = players.get(currentPlayerIndex);

            // Play turn and check if game is over
            if (!playTurn(currentPlayer)) {
                break;
            }

            nextPlayer();
        }

        System.out.println("\n" + TerminalColors.colorize(TerminalColors.GREEN, "🎉 Game Over! Thanks for playing!"));
    }

    /**
     * Close resources.
     */
    public void close() {
        if (scanner != null) {
            scanner.close();
        }
    }
}
