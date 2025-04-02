import pytest
from unittest.mock import MagicMock, patch
from Battleship import Button, gridFrame, gameState, playerSunkCount, enemySunkCount, rowLabels

@pytest.fixture
def mock_dependencies():
    """Fixture to mock global dependencies."""
    global gridFrame, rowLabels
    gridFrame = MagicMock()  # Mock the gridFrame
    rowLabels = ["A", "B", "C", "D", "E"]  # Mock row labels for a 5x5 grid

@pytest.fixture
def mock_tkinter():
    """Fixture to mock tkinter components."""
    with patch("Battleship.tk.Button", MagicMock()) as mock_button:
        yield mock_button

@pytest.fixture
def button(mock_dependencies, mock_tkinter):
    """Fixture to create a Button instance."""
    return Button(1, 1)  # Create a button at position (1, 1)

def test_button_initialization(button, mock_tkinter):
    """Test the initialization of a Button."""
    assert button.x == 1
    assert button.y == 1
    assert button.state == "Empty"
    mock_tkinter.assert_called_once_with(
        gridFrame, text=button.label, font=("Arial", 18), command=button.click, bg="#00AAFF"
    )

def test_button_click_player_placing(button):
    """Test the click method during the PlayerPlacing game state."""
    global gameState
    gameState = "PlayerPlacing"
    button.playerSquare = True
    button.state = "Empty"
    button.click()
    assert button.state == "Occupied"

def test_button_click_enemy_shooting(button):
    """Test the click method during the EnemyShooting game state."""
    global gameState, playerSunkCount
    gameState = "EnemyShooting"
    button.state = "Occupied"
    playerSunkCount = 0
    button.click()
    assert button.state == "Sunk"
    assert playerSunkCount == 1

def test_button_reset(button):
    """Test the reset method of the Button."""
    button.state = "Occupied"
    button.reset()
    assert button.state == "Empty"
    assert button.x == 1
    assert button.y == 1

def test_button_reveal(button):
    """Test the reveal method of the Button."""
    button.state = "Occupied"
    button.reveal()
    button.btn.config.assert_called_once_with(bg="#FFFF00")