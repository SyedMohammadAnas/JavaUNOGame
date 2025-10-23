package com.unogame;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/**
 * Represents a player in the UNO game (human or AI).
 * Manages the player's hand and provides methods for card management and display.
 */
public class Player {
    private final String name;
    private final List<Card> hand;
    private final boolean isAi;

    /**
     * Constructor for creating a player.
     * @param name The player's name
     * @param isAi Whether this player is controlled by AI
     */
    public Player(String name, boolean isAi) {
        this.name = name;
        this.hand = new ArrayList<>();
        this.isAi = isAi;
    }

    // Getters
    public String getName() {
        return name;
    }

    public List<Card> getHand() {
        return hand;
    }

    public boolean isAi() {
        return isAi;
    }

    /**
     * Add a card to the player's hand.
     * @param card The card to add
     */
    public void addCard(Card card) {
        hand.add(card);
    }

    /**
     * Remove and return a card from the player's hand by index.
     * @param cardIndex The index of the card to remove
     * @return The removed card
     */
    public Card removeCard(int cardIndex) {
        return hand.remove(cardIndex);
    }

    /**
     * Get indices of cards that can be played on the current top card.
     * @param topCard The card currently on top of the discard pile
     * @param currentColor The current color to match
     * @return List of indices of playable cards
     */
    public List<Integer> getPlayableCards(Card topCard, CardColor currentColor) {
        List<Integer> playableIndices = new ArrayList<>();

        for (int i = 0; i < hand.size(); i++) {
            Card card = hand.get(i);
            if (card.canPlayOn(topCard, currentColor)) {
                playableIndices.add(i);
            }
        }

        return playableIndices;
    }

    /**
     * Display the player's hand with numbered cards and ASCII art.
     * Shows cards in rows of 4 for better readability.
     */
    public void displayHand() {
        if (hand.isEmpty()) {
            System.out.println(name + "'s hand is empty!");
            return;
        }

        System.out.println("\n" + name + "'s hand (" + hand.size() + " cards):");

        // Display cards in rows of 4 for better readability
        for (int i = 0; i < hand.size(); i += 4) {
            int endIndex = Math.min(i + 4, hand.size());
            List<Card> rowCards = hand.subList(i, endIndex);

            // Show card numbers above the cards
            StringBuilder numbers = new StringBuilder();
            for (int j = 0; j < rowCards.size(); j++) {
                if (j > 0) {
                    numbers.append("    ");
                }
                numbers.append(String.format("%2d", i + j + 1));
            }
            System.out.println("  " + numbers.toString());

            // Get display lines for all cards in this row
            List<List<String>> allCardLines = new ArrayList<>();
            for (Card card : rowCards) {
                allCardLines.add(card.getDisplayLines());
            }

            // Print each line of the ASCII art for all cards
            for (int lineIdx = 0; lineIdx < 3; lineIdx++) {
                StringBuilder lineParts = new StringBuilder();
                for (int cardIdx = 0; cardIdx < allCardLines.size(); cardIdx++) {
                    if (cardIdx > 0) {
                        lineParts.append(" ");
                    }
                    lineParts.append(allCardLines.get(cardIdx).get(lineIdx));
                }
                System.out.println("  " + lineParts.toString());
            }
            System.out.println();
        }
    }

    /**
     * Check if the player has any cards left.
     * @return true if the player's hand is empty
     */
    public boolean hasWon() {
        return hand.isEmpty();
    }

    /**
     * Get the number of cards in the player's hand.
     * @return The number of cards
     */
    public int getCardCount() {
        return hand.size();
    }

    /**
     * Get a card from the hand by index.
     * @param index The index of the card
     * @return The card at the specified index
     */
    public Card getCard(int index) {
        return hand.get(index);
    }
}
