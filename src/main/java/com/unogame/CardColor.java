package com.unogame;

/**
 * Enum representing the different colors of UNO cards.
 * BLACK is used for wild cards which can be any color.
 */
public enum CardColor {
    RED("red"),
    BLUE("blue"),
    GREEN("green"),
    YELLOW("yellow"),
    BLACK("black");  // For wild cards

    private final String value;

    CardColor(String value) {
        this.value = value;
    }

    public String getValue() {
        return value;
    }

    @Override
    public String toString() {
        return value;
    }
}
