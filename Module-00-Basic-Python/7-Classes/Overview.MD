# Classes in Python

## What is a Class?

A class is a blueprint for creating objects. Objects are instances of classes, and each object can have attributes (variables) and methods (functions defined in the class).

Think of a class as a recipe for making a cake. The class defines the ingredients and steps, but you can make multiple cakes (objects) based on that recipe, each with its own specific details (like flavor, size, etc.).

## Creating a Basic Class in Python

Let's say we're creating a class for a simple concept: a Dog. Each Dog object we create could have attributes like name and age.

Here’s what a basic class might look like in Python:
```python
class Dog:
    pass
```
This code defines an empty class called Dog. The pass statement tells Python to do nothing – it's a placeholder, so we don't get an error.

## Adding the __init__ Method
The __init__ method is a special method in Python that is called automatically every time a new object is created. It’s often referred to as the "initializer" or "constructor" of the class. This method is where we set up the initial values of our object's attributes.

Let's update our Dog class to include some attributes: name and age.
```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```
Here’s what’s happening:

def __init__(self, name, age): defines the __init__ method.
self represents the instance of the class (the specific Dog object we’re creating).
self.name = name sets the name attribute for the object, and self.age = age sets the age attribute.
