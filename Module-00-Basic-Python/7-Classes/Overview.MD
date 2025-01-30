# Classes in Python

## 1. What is a Class?

A class in Python is a template for creating objects. Objects are instances of a class, and each object has its own set of attributes (variables) and methods (functions defined in the class). Classes allow us to structure our code in a way that models real-world entities and their behaviors.

Think of a class as the blueprint for building a house. The class defines the design (attributes) and the construction steps (methods), while each house (object) built from that blueprint can have different features (like color, size, number of rooms, etc.).

---

## 2. Creating a Basic Class in Python

Let’s begin by creating a simple class for a `Person`. Each `Person` object will have attributes such as `name`, `age`, and `gender`.

Here's a basic class structure:

```python
class Person:
    pass
```

This code defines an empty class called `Person`. The `pass` statement is used here to indicate that the class doesn't do anything yet. It’s a placeholder, preventing syntax errors.

---

## 3. Adding the `__init__` Method

The `__init__` method is a special method in Python that is automatically invoked every time a new object is created. It’s often referred to as the "initializer" or "constructor" of the class. This method sets up the initial state of the object by initializing its attributes.

Let’s modify the `Person` class to include three attributes: `name`, `age`, and `gender`.

```python
class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
```

### What’s Happening Here:
- `def __init__(self, name, age, gender):` defines the `__init__` method.
- `self` refers to the instance of the class (the specific `Person` object we're creating).
- `self.name = name` sets the `name` attribute for the object.
- `self.age = age` sets the `age` attribute for the object.
- `self.gender = gender` sets the `gender` attribute for the object.

---

## 4. Using `self`

In Python classes, `self` refers to the instance of the class. It allows you to access and modify the attributes and methods of that instance.

When you create an object and call a method, Python automatically passes the object to the method as the first argument (`self`). You don't need to pass `self` explicitly.

---

## 5. Adding a Method to Our Class

Let’s add a method to greet a person by name.

```python
class Person:
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def greet(self):
        print(f"Hello, my name is {self.name}.")
```

### Key Points:
- `greet` is a method inside the `Person` class.
- `self` allows us to refer to the attributes (e.g., `self.name`) of the current instance of the class.

---

## 6. Creating an Object (Instance) of the Class

Once the class is defined, we can create objects (instances) of that class. To do this, you call the class like a function, passing in any required arguments.

For example, let’s create a `Person` object named `John` who is 30 years old and male:

```python
john = Person("John", 30, "Male")
```

### What Happens Here:
- `Person("John", 30, "Male")` invokes the `__init__` method.
- Inside the `__init__` method, `self.name` is set to `"John"`, `self.age` is set to `30`, and `self.gender` is set to `"Male"`.
- `john` is now an instance of the `Person` class with those attributes.

---

## 7. Using the Object’s Methods and Attributes

Once we have an instance of the class, we can access its attributes and call its methods.

```python
print(john.name)  # Output: John
print(john.age)   # Output: 30
print(john.gender) # Output: Male
john.greet()      # Output: Hello, my name is John.
```

---

## 8. Example: `Book` Class

Let’s create a class for a `Book` to demonstrate more features, such as displaying book details, updating the year of publication, and calculating the book’s age.

```python
class Book:
    def __init__(self, title, author, year, genre):
        self.title = title  # Title of the book
        self.author = author  # Author of the book
        self.year = year  # Year of publication
        self.genre = genre  # Genre of the book

    def display_info(self):
        print(f"Book Details: {self.title} by {self.author}, Year: {self.year}, Genre: {self.genre}")

    def update_year(self, new_year):
        if new_year >= self.year:
            self.year = new_year
            print(f"Updated year of publication: {self.year}")
        else:
            print("Year of publication cannot be earlier than the current year!")

    def book_age(self, current_year):
        return current_year - self.year


# Create an instance of the Book class
my_book = Book("1984", "George Orwell", 1949, "Dystopian")

# Display book details
my_book.display_info()  # Output: Book Details: 1984 by George Orwell, Year: 1949, Genre: Dystopian

# Update the year of publication
my_book.update_year(1950)  # Output: Updated year of publication: 1950

# Attempt to roll back the year of publication (will fail)
my_book.update_year(1940)  # Output: Year of publication cannot be earlier than the current year!

# Calculate and display the book's age
current_year = 2025
book_age = my_book.book_age(current_year)
print(f"The book is {book_age} years old.")  # Output: The book is 75 years old.
```

#### Explanation of the `Book` Class:
- The `Book` class has an `__init__` method that initializes the attributes: `title`, `author`, `year`, and `genre`.
- `display_info` prints the book's details.
- `update_year` checks that the new publication year is not earlier than the current year before updating it.
- `book_age` calculates and returns the age of the book based on the current year.

---
## 9. Example: `car` Class
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
---

## 10. Class Methods

You can also define class methods that operate on the class itself, rather than instances. These methods are defined using the `@classmethod` decorator.

```python
class MyClass:
    class_variable = "I am a class variable"

    @classmethod
    def display_class_variable(cls):
        print(cls.class_variable)

# Call the class method without creating an instance
MyClass.display_class_variable()  # Output: I am a class variable
```
---

## 11. Summary of the Steps
- Define a class with the class keyword.
- Add the __init__ method to set initial attributes when an object is created.
- Use self in methods to access attributes and other methods of the instance.
- Create an object (instance) by calling the class with any required arguments.
- Access attributes and call methods using the object.
