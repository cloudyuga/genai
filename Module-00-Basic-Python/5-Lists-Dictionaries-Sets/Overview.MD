# Introduction to Lists, Dictionaries, and Sets in Python

## 1. Lists
A list is an ordered collection of items. You can think of it as a sequence of things, like a shopping list or a list of favorite movies. In Python, lists are created by putting items inside square brackets [], separated by commas.

#### Example
```python
# Creating a list of fruits
fruits = ["apple", "banana", "cherry"]

# Accessing items
print(fruits[0])  # Output: apple
print(fruits[1])  # Output: banana

# Adding an item
fruits.append("orange")
print(fruits)  # Output: ['apple', 'banana', 'cherry', 'orange']

# Removing an item
fruits.remove("banana")
print(fruits)  # Output: ['apple', 'cherry', 'orange']
```
- Lists are ordered: The items stay in the order you add them.
- Lists are mutable: You can change items in a list, add new items, or remove items.

---

## 2. Dictionaries

A dictionary (or dict) is a collection of key-value pairs. Each item in a dictionary has a key and a value. You use keys to access the values, similar to looking up a word in a dictionary to find its definition. Dictionaries are created using curly braces {}, with each key-value pair separated by a colon :.

#### Example:
```python
# Creating a dictionary with some information about a person
person = {
    "name": "Alice",
    "age": 25,
    "city": "New York"
}

# Accessing values by key
print(person["name"])  # Output: Alice
print(person["age"])   # Output: 25

# Adding a new key-value pair
person["job"] = "Engineer"
print(person)  # Output: {'name': 'Alice', 'age': 25, 'city': 'New York', 'job': 'Engineer'}

# Changing a value
person["city"] = "San Francisco"
print(person)  # Output: {'name': 'Alice', 'age': 25, 'city': 'San Francisco', 'job': 'Engineer'}

```

- Dictionaries are unordered: The items do not maintain a specific order.
- Dictionaries are mutable: You can add, remove, and change items.

#### Using get() with Dictionaries

The get() method lets you access values in a dictionary by key. If the key doesn’t exist, it returns None by default, or you can provide a default value.

print following details using above example
```python
# Using get() without a default value
print(person.get("name"))  # Output: Alice
print(person.get("country"))  # Output: None (since 'country' is not a key)

# Using get() with a default value
print(person.get("country", "USA"))  # Output: USA (default value provided)
```
---
## 3. Sets
A set is an unordered collection of unique items. Sets are useful when you want to store items without any duplicates, like a list of unique colors. Sets are created using curly braces {}, like dictionaries, but without key-value pairs.

#### Example
```python
# Creating a set of colors
colors = {"red", "green", "blue"}

# Adding an item
colors.add("yellow")
print(colors)  # Output: {'red', 'green', 'blue', 'yellow'}

# Trying to add a duplicate item
colors.add("red")
print(colors)  # Output: {'red', 'green', 'blue', 'yellow'} (no duplicate)

# Removing an item
colors.remove("green")
print(colors)  # Output: {'red', 'blue', 'yellow'}
```
- Sets are unordered: There’s no specific order to items.
- Sets store unique items: Duplicate items are not allowed.
