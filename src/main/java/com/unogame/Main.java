package com.unogame;

/**
 * Main class to start the UNO game.
 * This is the entry point for the Java UNO game application.
 */
public class Main {

    /**
     * Main method - entry point of the application.
     * @param args Command line arguments (not used)
     */
    public static void main(String[] args) {
        UnoGame game = new UnoGame();

        try {
            game.runGame();
        } catch (Exception e) {
            System.err.println("An error occurred during the game: " + e.getMessage());
            e.printStackTrace();
        } finally {
            game.close();
        }
    }
}
