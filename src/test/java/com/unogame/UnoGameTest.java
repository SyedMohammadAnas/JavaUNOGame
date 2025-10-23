package com.unogame;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Test class for UNO game functionality.
 * Tests core game mechanics to ensure they work correctly.
 */
public class UnoGameTest {

    private UnoGame game;
    private Player humanPlayer;
    private Player aiPlayer;

    @BeforeEach
    public void setUp() {
        game = new UnoGame();
        humanPlayer = new Player("TestHuman", false);
        aiPlayer = new Player("TestAI", true);

        game.players.add(humanPlayer);
        game.players.add(aiPlayer);
    }

    @Test
    public void testCardCreation() {
        Card redFive = new Card(CardColor.RED, CardType.NUMBER, 5);
        assertEquals(CardColor.RED, redFive.getColor());
        assertEquals(CardType.NUMBER, redFive.getCardType());
        assertEquals(Integer.valueOf(5), redFive.getNumber());

        Card wildCard = new Card(CardColor.BLACK, CardType.WILD);
        assertEquals(CardColor.BLACK, wildCard.getColor());
        assertEquals(CardType.WILD, wildCard.getCardType());
        assertNull(wildCard.getNumber());
    }

    @Test
    public void testCardCanPlayOn() {
        Card redFive = new Card(CardColor.RED, CardType.NUMBER, 5);
        Card blueFive = new Card(CardColor.BLUE, CardType.NUMBER, 5);
        Card redSeven = new Card(CardColor.RED, CardType.NUMBER, 7);
        Card wildCard = new Card(CardColor.BLACK, CardType.WILD);

        // Same number should be playable
        assertTrue(blueFive.canPlayOn(redFive, CardColor.RED));

        // Same color should be playable
        assertTrue(redSeven.canPlayOn(redFive, CardColor.RED));

        // Wild card should always be playable
        assertTrue(wildCard.canPlayOn(redFive, CardColor.BLUE));

        // Different color and number should not be playable
        Card greenThree = new Card(CardColor.GREEN, CardType.NUMBER, 3);
        assertFalse(greenThree.canPlayOn(redFive, CardColor.RED));
    }

    @Test
    public void testPlayerHandManagement() {
        Card card1 = new Card(CardColor.RED, CardType.NUMBER, 5);
        Card card2 = new Card(CardColor.BLUE, CardType.SKIP);

        humanPlayer.addCard(card1);
        humanPlayer.addCard(card2);

        assertEquals(2, humanPlayer.getCardCount());
        assertEquals(card1, humanPlayer.getCard(0));
        assertEquals(card2, humanPlayer.getCard(1));

        Card removed = humanPlayer.removeCard(0);
        assertEquals(card1, removed);
        assertEquals(1, humanPlayer.getCardCount());
        assertEquals(card2, humanPlayer.getCard(0));
    }

    @Test
    public void testPlayerGetPlayableCards() {
        Card topCard = new Card(CardColor.RED, CardType.NUMBER, 5);
        Card playableCard1 = new Card(CardColor.RED, CardType.NUMBER, 7); // Same color
        Card playableCard2 = new Card(CardColor.BLUE, CardType.NUMBER, 5); // Same number
        Card wildCard = new Card(CardColor.BLACK, CardType.WILD); // Wild card
        Card unplayableCard = new Card(CardColor.GREEN, CardType.NUMBER, 3); // Different color and number

        humanPlayer.addCard(playableCard1);
        humanPlayer.addCard(playableCard2);
        humanPlayer.addCard(wildCard);
        humanPlayer.addCard(unplayableCard);

        var playableIndices = humanPlayer.getPlayableCards(topCard, CardColor.RED);

        assertEquals(3, playableIndices.size());
        assertTrue(playableIndices.contains(0)); // playableCard1
        assertTrue(playableIndices.contains(1)); // playableCard2
        assertTrue(playableIndices.contains(2)); // wildCard
        assertFalse(playableIndices.contains(3)); // unplayableCard
    }

    @Test
    public void testDeckCreation() {
        game.createDeck();
        assertEquals(108, game.deck.size()); // Standard UNO deck has 108 cards

        // Count different card types
        int numberCards = 0;
        int actionCards = 0;
        int wildCards = 0;

        for (Card card : game.deck) {
            if (card.getCardType() == CardType.NUMBER) {
                numberCards++;
            } else if (card.getCardType() == CardType.WILD || card.getCardType() == CardType.WILD_DRAW_FOUR) {
                wildCards++;
            } else {
                actionCards++;
            }
        }

        assertEquals(76, numberCards); // 4 colors * (1 zero + 2 each of 1-9)
        assertEquals(24, actionCards); // 4 colors * 2 each of Skip, Reverse, Draw Two
        assertEquals(8, wildCards); // 4 each of Wild and Wild Draw Four
    }

    @Test
    public void testGameDirection() {
        game.players.add(new Player("Player1", true));
        game.players.add(new Player("Player2", true));
        game.players.add(new Player("Player3", true));
        game.players.add(new Player("Player4", true));

        game.currentPlayerIndex = 0;
        game.direction = 1; // Clockwise

        game.nextPlayer();
        assertEquals(1, game.currentPlayerIndex);

        game.nextPlayer();
        assertEquals(2, game.currentPlayerIndex);

        game.direction = -1; // Counter-clockwise
        game.nextPlayer();
        assertEquals(1, game.currentPlayerIndex);

        game.nextPlayer();
        assertEquals(0, game.currentPlayerIndex);
    }

    @Test
    public void testPlayerWinCondition() {
        // Player starts with empty hand, so they have won
        assertTrue(humanPlayer.hasWon());

        // Add a card, now they haven't won
        Card card = new Card(CardColor.RED, CardType.NUMBER, 5);
        humanPlayer.addCard(card);
        assertFalse(humanPlayer.hasWon());

        // Remove the card, now they have won again
        humanPlayer.removeCard(0);
        assertTrue(humanPlayer.hasWon());
    }

    @Test
    public void testCardDisplay() {
        Card redFive = new Card(CardColor.RED, CardType.NUMBER, 5);
        String display = redFive.getDisplay();

        assertTrue(display.contains("┌───┐"));
        assertTrue(display.contains("│ 5 │"));
        assertTrue(display.contains("└───┘"));

        Card wildCard = new Card(CardColor.BLACK, CardType.WILD);
        String wildDisplay = wildCard.getDisplay();

        assertTrue(wildDisplay.contains("┌───┐"));
        assertTrue(wildDisplay.contains("│WLD│"));
        assertTrue(wildDisplay.contains("└───┘"));
    }

    @Test
    public void testCardDisplayLines() {
        Card redFive = new Card(CardColor.RED, CardType.NUMBER, 5);
        var lines = redFive.getDisplayLines();

        assertEquals(3, lines.size());
        assertTrue(lines.get(0).contains("┌───┐"));
        assertTrue(lines.get(1).contains("│ 5 │"));
        assertTrue(lines.get(2).contains("└───┘"));
    }
}
