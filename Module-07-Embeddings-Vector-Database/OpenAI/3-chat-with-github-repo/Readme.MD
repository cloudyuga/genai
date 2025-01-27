# How to Generate a GitHub Personal Access Token (PAT)?

## **Steps to Generate a GitHub Personal Access Token**

### 1. **Log in to GitHub**
   - Go to [GitHub](https://github.com) and log in to your account.

### 2. **Go to Developer Settings**
   - Click on your profile picture in the top-right corner.
   - Navigate to **Settings** → **Developer Settings** (located at the bottom of the menu).

### 3. **Select Personal Access Tokens**
   - In the left sidebar, click **Personal access tokens** → **Tokens (classic)**.

### 4. **Generate a New Token**
   - Click **Generate new token** → **Generate new token (classic)**.

### 5. **Choose Scopes**
   - Add a **note** for your token (e.g., "GitHub Repo Access Token").
   - Set an **expiration date** (e.g., 30 days) or choose "No expiration" for a permanent token.
   - Select the required **scopes** based on your needs:
     - **`repo`**: Full control of private repositories (if accessing private repos).
     - **`read:org`**: Read access to organization resources (if necessary).
     - Additional permissions as needed.

### 6. **Generate the Token**
   - Click the **Generate token** button.
   - **Copy the token immediately.** You won’t be able to view it again after leaving the page.

---

## **How to Save and Use the Token**

### 1. **Save the Token Securely**
   - Store the token in a `.env` file or a secure location:
     ```plaintext
     GITHUB_TOKEN=your_personal_access_token
     ```
   - Use `.gitignore` to ensure `.env` files are not committed to your repository.

### 2. **Install `python-dotenv`**
   - Install the `dotenv` library to securely load your token in Python:
     ```bash
     pip install python-dotenv
     ```

### 3. **Use the Token in Python**
   - Example script to access a GitHub repository:
     ```python
     from github import Github
     import os
     from dotenv import load_dotenv

     # Load environment variables
     load_dotenv()

     # Access GitHub Token
     github_token = os.getenv("GITHUB_TOKEN")
     g = Github(github_token)

     # Access a repository
     repo = g.get_repo("owner/repo")
     print(repo.full_name)
     ```

---

## **Important Tips**
1. **Do Not Expose Your Token Publicly.**
   - Never share your token in public repositories or forums.
   - Use `.gitignore` to exclude sensitive files (e.g., `.env`) from version control.

2. **Restrict Token Scope.**
   - Grant only the permissions required for your application.

3. **Rotate Tokens Regularly.**
   - If your token is exposed or no longer needed, revoke it immediately and generate a new one.
