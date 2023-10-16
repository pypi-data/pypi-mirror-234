def greet(name):
    """Greet the specified name."""
    return f"Hello, {name}!"

def is_palindrome(word):
    """Check if the given word is a palindrome."""
    word = word.lower()
    return word == word[::-1]

def multiply(a, b):
    """Calculate the product of two numbers."""
    return a * b