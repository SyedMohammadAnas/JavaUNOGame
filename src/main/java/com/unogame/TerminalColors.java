package com.unogame;

/**
 * Utility class for colored terminal output.
 * Provides ANSI color codes for cross-platform colored text display.
 * Equivalent to Python's colorama library.
 */
public class TerminalColors {

    // ANSI color codes
    public static final String RESET = "\u001B[0m";
    public static final String BLACK = "\u001B[30m";
    public static final String RED = "\u001B[31m";
    public static final String GREEN = "\u001B[32m";
    public static final String YELLOW = "\u001B[33m";
    public static final String BLUE = "\u001B[34m";
    public static final String MAGENTA = "\u001B[35m";
    public static final String CYAN = "\u001B[36m";
    public static final String WHITE = "\u001B[37m";

    // Background colors
    public static final String BG_BLACK = "\u001B[40m";
    public static final String BG_RED = "\u001B[41m";
    public static final String BG_GREEN = "\u001B[42m";
    public static final String BG_YELLOW = "\u001B[43m";
    public static final String BG_BLUE = "\u001B[44m";
    public static final String BG_MAGENTA = "\u001B[45m";
    public static final String BG_CYAN = "\u001B[46m";
    public static final String BG_WHITE = "\u001B[47m";

    // Text styles
    public static final String BOLD = "\u001B[1m";
    public static final String UNDERLINE = "\u001B[4m";

    /**
     * Get the appropriate color code for a given card color.
     * @param color The card color
     * @return ANSI color code string
     */
    public static String getColorCode(CardColor color) {
        switch (color) {
            case RED:
                return RED;
            case BLUE:
                return BLUE;
            case GREEN:
                return GREEN;
            case YELLOW:
                return YELLOW;
            case BLACK:
                return WHITE;  // Wild cards display in white
            default:
                return WHITE;
        }
    }

    /**
     * Apply color to text and reset at the end.
     * @param color The color to apply
     * @param text The text to colorize
     * @return Colored text string
     */
    public static String colorize(String color, String text) {
        return color + text + RESET;
    }

    /**
     * Apply color to text with a specific card color.
     * @param cardColor The card color
     * @param text The text to colorize
     * @return Colored text string
     */
    public static String colorize(CardColor cardColor, String text) {
        return colorize(getColorCode(cardColor), text);
    }
}
