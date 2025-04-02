import pytest
from unittest.mock import MagicMock, patch
from Battleship import Board, setGameState, gridSize, maxShips, playerBoard, enemyBoard

@pytest.fixture
def mock_tkinter():
    """Fixture to mock tkinter components."""
    with patch("Battleship.tk.Tk", MagicMock()) as mock_tk:
        with patch("Battleship.tk.Frame", MagicMock()) as mock_frame:
            with patch("Battleship.tk.Label", MagicMock()) as mock_label:
                with patch("Battleship.tk.Button", MagicMock()) as mock_button:
                    yield mock_tk

@pytest.fixture
def board(mock_tkinter):
    """Fixture to create a Board instance."""
    return Board()

def test_board_setup(board):
    """Test the setup method of the Board class."""
    board.setup()
    assert board.instructFrame.pack.called  # Ensure the instruction frame is packed
    assert board.labelFrame.pack.called     # Ensure the label frame is packed
    assert board.resetButton.grid.called    # Ensure the reset button is placed in the grid

def test_board_reset(board):
    """Test the reset method of the Board class."""
    # Mock playerBoard and enemyBoard
    global playerBoard, enemyBoard
    playerBoard = [[MagicMock(state="Occupied") for _ in range(gridSize)] for _ in range(gridSize)]
    enemyBoard = [[MagicMock(state="Occupied") for _ in range(gridSize)] for _ in range(gridSize)]

    board.reset()

    # Ensure all buttons are reset
    for row in playerBoard:
        for btn in row:
            btn.reset.assert_called_once()

    for row in enemyBoard:
        for btn in row:
            btn.reset.assert_called_once()

def test_board_set_text(board):
    """Test the setText method of the Board class."""
    board.instructionLabel = MagicMock()
    board.setText("Test Message")
    board.instructionLabel.config.assert_called_once_with(text="Test Message")

def test_board_reveal_all(board):
    """Test the revealAll method of the Board class."""
    # Mock gameState and enemyBoard
    global enemyBoard
    enemyBoard = [[MagicMock(state="Occupied") for _ in range(gridSize)] for _ in range(gridSize)]

    # Test when gameState is PlayerShooting
    with patch("Battleship.gameState", "PlayerShooting"):
        board.revealAll()
        for row in enemyBoard:
            for btn in row:
                btn.reveal.assert_called_once()

    # Test when gameState is not PlayerShooting or EnemyShooting
    with patch("Battleship.gameState", "PlayerPlacing"):
        with patch("Battleship.messagebox.showinfo") as mock_messagebox:
            board.revealAll()
            mock_messagebox.assert_called_once_with(title="Reveal", message="There are no pieces to reveal")

def test_board_destroy_reset(board):
    """Test the destroyReset method of the Board class."""
    board.resetButton = MagicMock()
    board.destroyReset()
    board.resetButton.destroy.assert_called_once()