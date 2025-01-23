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

- def __init__(self, name, age): defines the __init__ method.
- self represents the instance of the class (the specific Dog object we’re creating).
- self.name = name sets the name attribute for the object, and self.age = age sets the age attribute.

## Using self
self is a reference to the current instance of the class. It lets you access the instance’s attributes and methods from within the class.

When you call a method on an object, Python automatically passes the object as the first argument, which we call self. You don’t have to explicitly pass it; Python does it for you.

## Adding a Method to Our Class
Now, let’s add a simple method to make our dog "speak."
```python
class Dog:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        print(f"{self.name} says woof!")
```
- speak is a method, just like a function, but it’s defined within a class.
- self is used as the first parameter, allowing the method to access the object's attributes.

## Creating an Object (Instance) of the Class
To create an object, we call the class like a function, passing in any required arguments. Let’s make a dog named “Buddy” who is 3 years old.
```python
my_dog = Dog("Buddy", 3)
```
Here’s what happens:

- Dog("Buddy", 3) calls the __init__ method.
- Inside __init__, self.name is set to "Buddy", and self.age is set to 3.
- Now my_dog is an instance of Dog with its own unique name and age.

## Using the Object’s Methods and Attributes
Once we have an object, we can access its attributes and call its methods.
```python
print(my_dog.name)  # Output: Buddy
print(my_dog.age)   # Output: 3
my_dog.speak()      # Output: Buddy says woof!
```
---
## Example
#### car Class
```python
class Car:
    # Constructor to initialize the car's attributes
    def __init__(self, brand, model, year, mileage):
        self.brand = brand  # Car's brand (e.g., Toyota, Honda)
        self.model = model  # Car's model (e.g., Corolla, Civic)
        self.year = year    # Manufacturing year
        self.mileage = mileage  # Mileage in kilometers

    # Method to display car details
    def display_info(self):
        print(f"Car Details: {self.brand} {self.model}, Year: {self.year}, Mileage: {self.mileage} km")

    # Method to update the mileage
    def update_mileage(self, new_mileage):
        if new_mileage >= self.mileage:
            self.mileage = new_mileage
            print(f"Updated mileage: {self.mileage} km")
        else:
            print("Mileage cannot be rolled back!")

    # Method to calculate the car's age
    def car_age(self, current_year):
        return current_year - self.year


# Create an instance of the Car class
my_car = Car("Toyota", "Corolla", 2015, 75000)

# Display car details
my_car.display_info()  # Output: Car Details: Toyota Corolla, Year: 2015, Mileage: 75000 km

# Update the mileage
my_car.update_mileage(80000)  # Output: Updated mileage: 80000 km

# Attempt to roll back mileage (will fail)
my_car.update_mileage(70000)  # Output: Mileage cannot be rolled back!

# Calculate and display the car's age
current_year = 2025
car_age = my_car.car_age(current_year)
print(f"The car is {car_age} years old.")  # Output: The car is 10 years old.
```
