import pytest
from unittest.mock import MagicMock, patch
from Battleship import showRules, gameState, gridFrame, enemyBoard, playerBoard, rowLabels, board

@pytest.fixture
def mock_dependencies():
    """Fixture to mock global dependencies."""
    global gameState, gridFrame, enemyBoard, playerBoard, rowLabels, board
    gameState = "PlayerShooting"  # Set an initial game state
    gridFrame = MagicMock()  # Mock the gridFrame
    enemyBoard = [[MagicMock() for _ in range(5)] for _ in range(5)]  # Mock a 5x5 enemy board
    playerBoard = [[MagicMock() for _ in range(5)] for _ in range(5)]  # Mock a 5x5 player board
    rowLabels = ["A", "B", "C", "D", "E"]  # Mock row labels
    board = MagicMock()  # Mock the board object
    board.reset = MagicMock()  # Mock the reset method
    board.labelFrame = MagicMock()
    board.instructFrame = MagicMock()
    board.destroyReset = MagicMock()

    # Patch the global `board` object in the `Battleship` module
    with patch("Battleship.board", board):
        yield

@patch("Battleship.setGameState")
def test_showRules(mock_setGameState, mock_dependencies):
    """Test the showRules subroutine."""
    showRules()

    # Assert that the board's reset method was called
    board.reset.assert_called_once()

    # Assert that gridFrame was destroyed and recreated
    gridFrame.destroy.assert_called_once()

    # Assert that the labelFrame and instructFrame were removed
    board.labelFrame.pack_forget.assert_called_once()
    board.instructFrame.pack_forget.assert_called_once()

    # Assert that the reset button was destroyed
    board.destroyReset.assert_called_once()

    # Assert that enemyBoard, playerBoard, and rowLabels were cleared
    assert enemyBoard == []
    assert playerBoard == []
    assert rowLabels == []

    # Assert that the game state was set to "Rules"
    mock_setGameState.assert_called_once_with("Rules")