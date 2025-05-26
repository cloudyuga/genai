# 🧪 What is a Virtual Environment (venv)?

- A virtual environment is like a separate lab for each of your Python projects.

- Imagine you're doing science experiments. One experiment needs red chemicals. Another needs blue chemicals.
 
If you mix both in one lab, it might explode! 💥

Similarly, if two Python projects use different versions of the same library (like numpy), they can conflict.

# Why Do We Need venv (Virtual Environment)?

Here’s why it's useful:

- Separate Projects

- Each project has its own Python libraries.

  - No mixing!

- Avoid Version Conflicts

  - One project might need numpy v1.21, another needs numpy v1.25. Without venv, you can only have one version globally.

- Easy to Manage

   - You can install, update, and remove packages just for that project.

- Cleaner System

   - Keeps your global Python clean and untouched.

# Step-by-step: How to Start with Conda (from Scratch)

### ✅ Step 1: Download and Install Miniconda

Miniconda is a lighter version of Anaconda and is easier to install.

##### Go to the official site:
👉 https://docs.conda.io/en/latest/miniconda.html

###### Note: You should your email to download distribution(Windows, MacOS, or Linux)
- Download the installer for your OS
- For Windows,
   - Windows 64-bit
   - Choose Miniconda3 Windows 64-bit (EXE installer)

##### Run the installer:

- Keep all default settings

- ✅ Check "Add Miniconda to my PATH environment variable" during installation

##### Finish installing.

### ✅ Step 2. Open Command prompt

```conda --version```

### ✅ Step 3. Create a new environment

```conda create --name myenv python=3.10```

OR

```conda create -n myenv python=3.10 -y``` 

This creates a new environment called schoolenv with Python 3.10.

### ✅ Step 4. Activate the environment

```conda activate myenv```

You are now inside your new Python world.

```(myenv) c:/user/project $```

### ✅ Step 5. Install packages

```pip install gradio```

Your Enviroment is ready for development.

### ✅ Step 6. Deactivate the environment

```conda deactivate```

