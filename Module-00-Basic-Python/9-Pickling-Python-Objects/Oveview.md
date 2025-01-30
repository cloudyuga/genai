# Pickling in Python: Saving and Loading Python Objects Efficiently
## 1. What is Pickling?
Pickling is a way to serialize (convert) Python objects into a binary format for storage and later retrieval. This is useful when you need to save complex objects like lists, dictionaries, tuples, or custom classes.

Python provides the pickle module to handle serialization.

---
## 2. Using Pickle in Python
#### 1. Saving (Pickling) Objects to a File
We use pickle.dump() to store an object in a binary file.

###### Example: Pickling a List
```python
import pickle

# Sample list of student names
students = ["Alice", "Bob", "Charlie", "David"]

# Save to a pickle file
with open("students.pkl", "wb") as file:
    pickle.dump(students, file)

print("Student list has been pickled and saved.")
```
- "wb" mode (w for write, b for binary) is used.
- pickle.dump(object, file) writes the object in a binary format.

#### 2. Loading (Unpickling) Objects from a File
We use pickle.load() to retrieve stored objects.

###### Example: Unpickling the Student List
```python
import pickle

# Load the pickled data
with open("students.pkl", "rb") as file:
    loaded_students = pickle.load(file)

print("Loaded Students:", loaded_students)
```
- "rb" mode (r for read, b for binary) is used.
- The object is restored exactly as it was before saving.
---
## 3. Using JSON for Serialization
The json module is another way to save objects, but it stores them in a text format instead of binary.

#### 1. Writing Data to a JSON File
```python
import json

# Sample dictionary of employees and their ages
employees = {"John": 30, "Emma": 28, "Sophia": 35}

# Save to a JSON file
with open("employees.json", "w") as file:
    json.dump(employees, file)

print("Employee data has been saved in JSON format.")
```
#### 2. Reading Data from a JSON File
```python
import json

# Load JSON data
with open("employees.json", "r") as file:
    loaded_employees = json.load(file)

print("Loaded Employee Data:", loaded_employees)
```
---
## 4. Pickle vs JSON: Which One to Use?

| Feature        | Pickle (`pickle`) | JSON (`json`) |
|---------------|------------------|--------------|
| Format        | Binary (not human-readable) | Text-based (human-readable) |
| Compatibility | Python-only | Works across multiple languages |
| Speed         | Faster | Slower (especially for complex objects) |
| Object Types  | Supports all Python objects (including custom classes) | Supports only basic types (lists, dicts, strings, numbers) |
| Use Case      | Best for saving Python-specific objects | Best for data exchange (APIs, files, web applications) |

#### 📌 When to Use What?

- Use pickle if you're working only in Python and need to save/restore objects quickly.
- Use json if you need human-readable data or plan to share data with other languages.
---
## Summary
- Pickling helps store Python objects efficiently, but it's not human-readable.
- JSON is more universal and works across multiple programming languages, but it cannot store complex Python objects like sets or custom classes.
- Never unpickle files from untrusted sources, as it can execute malicious code.
