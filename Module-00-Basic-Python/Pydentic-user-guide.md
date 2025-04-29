# Pydantic User Guide

## 📌 Introduction to Pydantic

Pydantic is a powerful data validation and settings management library in Python. It helps ensure your data is correct and well-structured by defining models using Python classes.

- **Data Validation**: Automatically checks data types and values.
- **Serialization**: Convert data between different formats (e.g., JSON to Python objects).
- **Parsing**: Easily parse external data like API responses or user input.

---

## 🛠️ Installation
To install Pydantic, use pip:
```bash
pip install pydantic
```

---

## 🧑‍💻 Basic Example
Let's start with a simple example to understand how Pydantic works.

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    is_active: bool

# Valid Data
user = User(id=1, name='Aarya Naik', is_active=True)
print(user)

# Invalid Data (will raise an error)
user = User(id='abc', name='Aarya Naik', is_active='yes')
```

✅ **Output:**
```
id=1 name='Aarya Naik' is_active=True
```
❗ **Error Example:**
```
ValueError: invalid literal for int() with base 10: 'abc'
```

---

## 🛡️ Data Validation with Pydantic
Pydantic ensures all input data is valid. You can specify more complex validations using Pydantic's built-in types.

```python
from pydantic import BaseModel, PositiveInt, EmailStr

class Employee(BaseModel):
    name: str
    age: PositiveInt
    email: EmailStr

# Valid Example
employee = Employee(name='Alice', age=30, email='alice@example.com')
print(employee)

# Invalid Example
employee = Employee(name='Bob', age=-5, email='invalid-email')
```

---

## 🗂️ Using Default Values
You can set default values for fields.

```python
from pydantic import BaseModel
class Product(BaseModel):
    name: str = 'Unknown'
    price: float = 0.0
    in_stock: bool = True

product = Product()
print(product)
```

✅ **Output:**
```
name='Unknown' price=0.0 in_stock=True
```

---

## 🧬 Type Conversion
Pydantic will automatically try to convert data to the correct type.

```python
from pydantic import BaseModel
class Order(BaseModel):
    order_id: int
    amount: float

order = Order(order_id='123', amount='99.99')
print(order)
```

✅ **Output:**
```
order_id=123 amount=99.99
```

---

## ⏳ Working with Optional Fields
You can define optional fields using `Optional`.

```python
from pydantic import BaseModel
from typing import Optional

class Profile(BaseModel):
    username: str
    bio: Optional[str] = None

profile = Profile(username='Aarya Naik')
print(profile)
```

✅ **Output:**
```
username='Aarya Naik' bio=None
```

---

## 📤 Exporting Data
You can convert Pydantic objects to dictionaries or JSON.

```python
from pydantic import BaseModel
class User(BaseModel):
    id: int
    name: str
    is_active: bool

# Valid Data
user = User(id=5, name='Aditya Jain', is_active=True)
user_data = user.model_dump()
print(user_data)
print(user.model_dump_json())
```

✅ **Output:**
```
{'id': 5, 'name': 'Aditya Jain', 'is_active': True}
{"id":5,"name":"Aditya Jain","is_active":true}
```

---
## 📤 Parsing API Response Data
You can parse external data that are in JSON format.

```python
from pydantic import BaseModel
from typing import List

# Define a Pydantic model for validation
class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

# Simulating an external API response (e.g., JSON data)
api_response = {
    "id": 101,
    "name": "Aditya Jain",
    "email": "aditya@example.com",
    "is_active": True
}

# Parsing and validating the data using Pydantic
user = User(**api_response)

print(user)
print(user.model_dump())  # Convert back to a dictionary
```

✅ **Output:**
```
id=101 name='Aditya Jain' email='aditya@example.com' is_active=True
{'id': 101, 'name': 'Aditya Jain', 'email': 'aditya@example.com', 'is_active': True}
```

---

## 🛎️ Conclusion
Pydantic makes it easy to work with data by providing:
- Automatic data validation
- Type conversion
- Clean data models
- Easy serialization and parsing

Start using Pydantic in your Python projects for cleaner and safer code! 🚀
