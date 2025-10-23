package com.unogame;

/**
 * Enum representing the different types of UNO cards.
 * Each card type has a string value for display purposes.
 */
public enum CardType {
    NUMBER("number"),
    SKIP("skip"),
    REVERSE("reverse"),
    DRAW_TWO("draw_two"),
    WILD("wild"),
    WILD_DRAW_FOUR("wild_draw_four");

    private final String value;

    CardType(String value) {
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
