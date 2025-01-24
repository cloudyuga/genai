# Introduction to Lists, Dictionaries, and Sets in Python

## 1. Lists
A list is an ordered collection of items. You can think of it as a sequence of things, like a shopping list or a list of favorite movies. In Python, lists are created by putting items inside square brackets [], separated by commas.

#### Example
```python
```python
# Creating a list of cities
cities = ["London", "Paris", "Tokyo"]

# Accessing items
print(cities[0])  # Output: London
print(cities[2])  # Output: Tokyo

# Adding an item
cities.append("New York")
print(cities)  # Output: ['London', 'Paris', 'Tokyo', 'New York']

# Removing an item
cities.remove("Paris")
print(cities)  # Output: ['London', 'Tokyo', 'New York']
```
- Lists are ordered: The items stay in the order you add them.
- Lists are mutable: You can change items in a list, add new items, or remove items.

---

## 2. Dictionaries

A dictionary (or dict) is a collection of key-value pairs. Each item in a dictionary has a key and a value. You use keys to access the values, similar to looking up a word in a dictionary to find its definition. Dictionaries are created using curly braces {}, with each key-value pair separated by a colon :.

#### Example:
```python
# Creating a dictionary with details about a book
book = {
    "title": "1984",
    "author": "George Orwell",
    "year": 1949
}

# Accessing values by key
print(book["title"])  # Output: 1984
print(book["year"])   # Output: 1949

# Adding a new key-value pair
book["genre"] = "Dystopian"
print(book)  # Output: {'title': '1984', 'author': 'George Orwell', 'year': 1949, 'genre': 'Dystopian'}

# Changing a value
book["year"] = 1950
print(book)  # Output: {'title': '1984', 'author': 'George Orwell', 'year': 1950, 'genre': 'Dystopian'}

```

- Dictionaries are unordered: The items do not maintain a specific order.
- Dictionaries are mutable: You can add, remove, and change items.

#### Using get() with Dictionaries

The get() method lets you access values in a dictionary by key. If the key doesn’t exist, it returns None by default, or you can provide a default value.

print following details using above example
```python
# Using get() without a default value
print(book.get("title"))  # Output: 1984
print(book.get("publisher"))  # Output: None (key doesn't exist)

# Using get() with a default value
print(book.get("publisher", "Not available"))  # Output: Not available
```
---
## 3. Sets
A set is an unordered collection of unique items. Sets are useful when you want to store items without any duplicates, like a list of unique colors. Sets are created using curly braces {}, like dictionaries, but without key-value pairs.

#### Example
```python
# Creating a set of sports
sports = {"football", "cricket", "tennis"}

# Adding an item
sports.add("basketball")
print(sports)  # Output: {'football', 'cricket', 'tennis', 'basketball'}

# Trying to add a duplicate item
sports.add("football")
print(sports)  # Output: {'football', 'cricket', 'tennis', 'basketball'} (no duplicate added)

# Removing an item
sports.remove("tennis")
print(sports)  # Output: {'football', 'cricket', 'basketball'}
```
- Sets are unordered: There’s no specific order to items.
- Sets store unique items: Duplicate items are not allowed.

---

## Summary

| **Concept**       | **Description**                                                                                     | **Key Features**                                                                                   |
|--------------------|-----------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------|
| **Lists**          | Ordered, mutable collection of items, useful for maintaining sequences.                            | - Items stay in the order added. <br> - Supports item addition, removal, and modification.         |
| **Dictionaries**   | Unordered, mutable collection of key-value pairs, used for associating keys with values.            | - Access values using keys. <br> - Use `get()` method to avoid KeyErrors and provide default values. |
| **Sets**           | Unordered collection of unique items, useful for storing non-duplicate elements.                   | - Ensures uniqueness of items. <br> - Does not maintain order. <br> - Supports addition and removal of items. |
