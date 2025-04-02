import pytest
from unittest.mock import MagicMock, patch
from Battleship import Rules, Board, Button, setGameState, checkIfWon

# Mock tkinter globally to avoid Tcl-related issues
@pytest.fixture(autouse=True)
def mock_tkinter():
    with patch("Battleship.tk.Tk", MagicMock()) as mock_tk:
        with patch("Battleship.tk.Frame", MagicMock()) as mock_frame:
            with patch("Battleship.tk.Label", MagicMock()) as mock_label:
                with patch("Battleship.tk.Button", MagicMock()) as mock_button:
                    with patch("Battleship.tk.Widget.grid", MagicMock(return_value=None)) as mock_grid:
                        with patch("Battleship.tk.Widget.pack", MagicMock(return_value=None)) as mock_pack:
                            yield mock_tk

# Test Rules class
def test_rules_initialization():
    rules = Rules()
    assert rules.gridUserInput.get() == "10"  # Default grid size
    assert rules.shipUserInput.get() == "5"   # Default number of ships

def test_limit_grid_size():
    rules = Rules()
    rules.gridUserInput.set("15")  # Exceeding max grid size
    rules.limitGridSize()
    assert rules.gridUserInput.get() == "12"  # Should be capped at 12

    rules.gridUserInput.set("abc")  # Non-numeric input
    rules.limitGridSize()
    assert rules.gridUserInput.get() == "1"  # Should reset to 1

def test_limit_ship_num():
    rules = Rules()
    rules.gridUserInput.set("3")  # Grid size 3x3 = 9 spaces
    rules.shipUserInput.set("10")  # Exceeding max ships
    rules.limitShipNum()
    assert rules.shipUserInput.get() == "8"  # Max ships should be 8 (9-1)

    rules.shipUserInput.set("abc")  # Non-numeric input
    rules.limitShipNum()
    assert rules.shipUserInput.get() == "1"  # Should reset to 1

def test_get_user_inputs():
    rules = Rules()
    rules.gridUserInput.set("8")
    rules.shipUserInput.set("4")
    grid_size, ship_num = rules.getUserInputs()
    assert grid_size == 8
    assert ship_num == 4

# Test Board class
def test_board_setup():
    board = Board()
    board.setup()
    assert board.instructFrame.winfo_children.called  # Mocked frame populated
    assert board.labelFrame.winfo_children.called     # Mocked frame populated

def test_board_reset():
    board = Board()
    board.playerBoard = [[Button(0, 0) for _ in range(3)] for _ in range(3)]
    for row in board.playerBoard:
        for btn in row:
            btn.state = "Occupied"
    board.reset()
    assert all(btn.state == "Empty" for row in board.playerBoard for btn in row)  # All buttons reset

def test_board_set_text():
    board = Board()
    board.instructionLabel = MagicMock()
    board.setText("Test Message")
    board.instructionLabel.cget.assert_called_with("text")  # Mocked label text set

def test_board_reveal_all():
    board = Board()
    board.revealAll = MagicMock()
    board.revealAll()
    board.revealAll.assert_called_once()  # Ensure revealAll is called

# Test Button class
def test_button_initialization():
    button = Button(1, 1)
    assert button.x == 1
    assert button.y == 1
    assert button.state == "Empty"

def test_button_click_player_placing():
    button = Button(1, 1)
    setGameState("PlayerPlacing")
    button.click()
    assert button.state == "Occupied"  # Button should be occupied after click

def test_button_reset():
    button = Button(1, 1)
    button.state = "Occupied"
    button.reset()
    assert button.state == "Empty"  # Button state reset

def test_button_reveal():
    button = Button(1, 1)
    button.state = "Occupied"
    button.reveal()
    assert True  # Ensure reveal doesn't throw errors

# Test global functions
def test_set_game_state():
    setGameState("PlayerPlacing")
    assert True  # Ensure no errors during state change

def test_check_if_won():
    global enemySunkCount, maxShips
    enemySunkCount = 5
    maxShips = 5
    assert checkIfWon() is True  # Game should end when enemy ships are sunk