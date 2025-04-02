import pytest
from unittest.mock import MagicMock, patch
from Battleship import Rules

@pytest.fixture
def mock_tkinter():
    """Fixture to mock tkinter components."""
    with patch("Battleship.tk.Tk", MagicMock()) as mock_tk:
        with patch("Battleship.tk.StringVar", MagicMock()) as mock_stringvar:
            with patch("Battleship.tk.Frame", MagicMock()):
                with patch("Battleship.tk.Label", MagicMock()):
                    with patch("Battleship.tk.Entry", MagicMock()):
                        with patch("Battleship.tk.Button", MagicMock()):
                            with patch("Battleship.messagebox.showinfo", MagicMock()) as mock_messagebox:
                                yield mock_tk, mock_stringvar, mock_messagebox

@pytest.fixture
def rules(mock_tkinter):
    """Fixture to create a Rules instance."""
    mock_tk, mock_stringvar, _ = mock_tkinter
    mock_stringvar.side_effect = lambda window, value="": MagicMock(get=MagicMock(return_value=value), set=MagicMock())
    return Rules()

def test_limitShipNum_non_numeric_input(rules, mock_tkinter):
    """Test limitShipNum with non-numeric input."""
    _, _, mock_messagebox = mock_tkinter
    rules.shipUserInput.get.return_value = "abc"
    rules.limitShipNum()
    rules.shipUserInput.set.assert_called_once_with("1")
    mock_messagebox.assert_called_once_with(title="Invalid Entry", message="Please only input digits")

def test_limitShipNum_exceeds_max_spaces(rules):
    """Test limitShipNum when ship number exceeds max grid spaces."""
    rules.gridUserInput.get.return_value = "5"  # Grid size 5x5 = 25 spaces
    rules.shipUserInput.get.return_value = "30"
    rules.limitShipNum()
    rules.shipUserInput.set.assert_called_once_with("24")  # Max ships = grid spaces - 1

def test_limitShipNum_exceeds_double_digits(rules):
    """Test limitShipNum when ship number exceeds double digits."""
    rules.gridUserInput.get.return_value = "12"  # Grid size 12x12 = 144 spaces
    rules.shipUserInput.get.return_value = "150"
    rules.limitShipNum()
    rules.shipUserInput.set.assert_any_call("99")  # Max ships capped at 99

def test_limitShipNum_below_minimum(rules):
    """Test limitShipNum when ship number is below the minimum."""
    rules.shipUserInput.get.return_value = "0"
    rules.limitShipNum()
    rules.shipUserInput.set.assert_called_once_with("1")  # Minimum ships = 1

def test_limitShipNum_valid_input(rules):
    """Test limitShipNum with valid input."""
    rules.gridUserInput.get.return_value = "5"  # Grid size 5x5 = 25 spaces
    rules.shipUserInput.get.return_value = "10"
    rules.limitShipNum()
    rules.shipUserInput.set.assert_not_called()  # No changes should be made for valid input