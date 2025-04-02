import pytest
from unittest.mock import MagicMock, patch
from Battleship import Counter, shipsPlaced, maxShips, gameState, board, setGameState

@pytest.fixture
def mock_dependencies():
    """Fixture to mock global dependencies."""
    global shipsPlaced, maxShips, gameState, board
    shipsPlaced = 0  # Reset shipsPlaced to 0
    maxShips = 5  # Set maxShips to 5
    gameState = ""  # Reset gameState
    board = MagicMock()  # Mock the board object
    board.setText = MagicMock()  # Mock the setText method of the board object

@patch("Battleship.setGameState")
def test_increment_not_max_ships(mock_setGameState, mock_dependencies):
    """Test increment when shipsPlaced is less than maxShips."""
    Counter.increment()
    assert shipsPlaced == 1  # Ensure shipsPlaced is incremented
    board.setText.assert_called_once_with("Select 5 squares on the player grid (4 more)")
    mock_setGameState.assert_not_called()  # Ensure game state does not change

@patch("Battleship.setGameState")
def test_increment_reaches_max_ships(mock_setGameState, mock_dependencies):
    """Test increment when shipsPlaced reaches maxShips."""
    global shipsPlaced
    shipsPlaced = maxShips - 1  # Set shipsPlaced to one less than maxShips
    Counter.increment()
    assert shipsPlaced == maxShips  # Ensure shipsPlaced is incremented to maxShips
    board.setText.assert_called_once_with("Select 5 squares on the player grid (0 more)")
    mock_setGameState.assert_called_once_with("EnemyPlacing")  # Ensure game state changes to EnemyPlacing