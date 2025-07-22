"""
Basic test suite for the Docker Python Guide project.
"""

def test_basic_functionality():
    """Test that basic Python functionality works."""
    assert 1 + 1 == 2


def test_string_operations():
    """Test basic string operations."""
    message = "Hello, Docker!"
    assert "Docker" in message
    assert len(message) > 0


def test_list_operations():
    """Test basic list operations."""
    my_list = [1, 2, 3, 4, 5]
    assert len(my_list) == 5
    assert 3 in my_list
    assert max(my_list) == 5
