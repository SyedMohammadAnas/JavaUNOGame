package com.unogame;

import java.util.ArrayList;
import java.util.List;

/**
 * Represents a single UNO card with color, type, and optional number.
 * Provides methods for displaying the card with colored ASCII art.
 */
public class Card {
    private final CardColor color;
    private final CardType cardType;
    private final Integer number;

    /**
     * Constructor for creating a UNO card.
     * @param color The color of the card
     * @param cardType The type of card (number, skip, etc.)
     * @param number The number value (only for number cards, can be null)
     */
    public Card(CardColor color, CardType cardType, Integer number) {
        this.color = color;
        this.cardType = cardType;
        this.number = number;
    }

    /**
     * Constructor for non-number cards (number parameter defaults to null).
     * @param color The color of the card
     * @param cardType The type of card
     */
    public Card(CardColor color, CardType cardType) {
        this(color, cardType, null);
    }

    // Getters
    public CardColor getColor() {
        return color;
    }

    public CardType getCardType() {
        return cardType;
    }

    public Integer getNumber() {
        return number;
    }

    /**
     * String representation for debugging.
     * @return String representation of the card
     */
    @Override
    public String toString() {
        if (cardType == CardType.NUMBER) {
            return color.getValue() + "_" + number;
        }
        return color.getValue() + "_" + cardType.getValue();
    }

    /**
     * Get colored ASCII representation of the card as a single string.
     * @return Colored ASCII art representation
     */
    public String getDisplay() {
        if (cardType == CardType.NUMBER) {
            String colorCode = TerminalColors.getColorCode(color);
            String numberStr = String.valueOf(number);

            if (numberStr.length() == 1) {
                return colorCode + "┌───┐\n│ " + numberStr + " │\n└───┘" + TerminalColors.RESET;
            } else {
                return colorCode + "┌───┐\n│" + numberStr + "│\n└───┘" + TerminalColors.RESET;
            }
        } else if (cardType == CardType.SKIP) {
            String colorCode = TerminalColors.getColorCode(color);
            return colorCode + "┌───┐\n│SKP│\n└───┘" + TerminalColors.RESET;
        } else if (cardType == CardType.REVERSE) {
            String colorCode = TerminalColors.getColorCode(color);
            return colorCode + "┌───┐\n│ ↻ │\n└───┘" + TerminalColors.RESET;
        } else if (cardType == CardType.DRAW_TWO) {
            String colorCode = TerminalColors.getColorCode(color);
            return colorCode + "┌───┐\n│+2 │\n└───┘" + TerminalColors.RESET;
        } else if (cardType == CardType.WILD) {
            return TerminalColors.WHITE + "┌───┐\n│WLD│\n└───┘" + TerminalColors.RESET;
        } else if (cardType == CardType.WILD_DRAW_FOUR) {
            return TerminalColors.WHITE + "┌───┐\n│+4 │\n└───┘" + TerminalColors.RESET;
        }

        return "┌───┐\n│???│\n└───┘";
    }

    /**
     * Get the card display as separate lines for proper color handling in multi-card displays.
     * @return List of strings representing each line of the card
     */
    public List<String> getDisplayLines() {
        List<String> lines = new ArrayList<>();

        if (cardType == CardType.NUMBER) {
            String colorCode = TerminalColors.getColorCode(color);
            String numberStr = String.valueOf(number);

            lines.add(colorCode + "┌───┐" + TerminalColors.RESET);
            if (numberStr.length() == 1) {
                lines.add(colorCode + "│ " + numberStr + " │" + TerminalColors.RESET);
            } else {
                lines.add(colorCode + "│" + numberStr + "│" + TerminalColors.RESET);
            }
            lines.add(colorCode + "└───┘" + TerminalColors.RESET);
        } else if (cardType == CardType.SKIP) {
            String colorCode = TerminalColors.getColorCode(color);
            lines.add(colorCode + "┌───┐" + TerminalColors.RESET);
            lines.add(colorCode + "│SKP│" + TerminalColors.RESET);
            lines.add(colorCode + "└───┘" + TerminalColors.RESET);
        } else if (cardType == CardType.REVERSE) {
            String colorCode = TerminalColors.getColorCode(color);
            lines.add(colorCode + "┌───┐" + TerminalColors.RESET);
            lines.add(colorCode + "│ ↻ │" + TerminalColors.RESET);
            lines.add(colorCode + "└───┘" + TerminalColors.RESET);
        } else if (cardType == CardType.DRAW_TWO) {
            String colorCode = TerminalColors.getColorCode(color);
            lines.add(colorCode + "┌───┐" + TerminalColors.RESET);
            lines.add(colorCode + "│+2 │" + TerminalColors.RESET);
            lines.add(colorCode + "└───┘" + TerminalColors.RESET);
        } else if (cardType == CardType.WILD) {
            lines.add(TerminalColors.WHITE + "┌───┐" + TerminalColors.RESET);
            lines.add(TerminalColors.WHITE + "│WLD│" + TerminalColors.RESET);
            lines.add(TerminalColors.WHITE + "└───┘" + TerminalColors.RESET);
        } else if (cardType == CardType.WILD_DRAW_FOUR) {
            lines.add(TerminalColors.WHITE + "┌───┐" + TerminalColors.RESET);
            lines.add(TerminalColors.WHITE + "│+4 │" + TerminalColors.RESET);
            lines.add(TerminalColors.WHITE + "└───┘" + TerminalColors.RESET);
        } else {
            lines.add("┌───┐");
            lines.add("│???│");
            lines.add("└───┘");
        }

        return lines;
    }

    /**
     * Check if this card can be played on top of another card.
     * @param topCard The card currently on top of the discard pile
     * @param currentColor The current color to match
     * @return true if this card can be played
     */
    public boolean canPlayOn(Card topCard, CardColor currentColor) {
        // Wild cards can always be played
        if (cardType == CardType.WILD || cardType == CardType.WILD_DRAW_FOUR) {
            return true;
        }

        // Match current color
        if (color == currentColor) {
            return true;
        }

        // Match top card's type and color
        if (cardType == topCard.cardType && color == topCard.color) {
            return true;
        }

        // Match number (for number cards)
        if (cardType == CardType.NUMBER && topCard.cardType == CardType.NUMBER &&
            number.equals(topCard.number)) {
            return true;
        }

        return false;
    }
}
