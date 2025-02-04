# Step-by-Step Guide to Create `credentials.json` for a Desktop Application

## 1. Access the Google Cloud Console
- Open your browser and navigate to the [Google Cloud Console](https://console.cloud.google.com/).
- If you don’t have a Google Cloud account, you'll need to create one.

## 2. Create a New Project
- In the top-left corner, click on the project dropdown menu.
- Select **"New Project"**.
- Provide a name for your project (e.g., "Job Interview Scheduler").
- Click **Create**.

## 3. Enable Gmail and Calendar APIs
- In the Google Cloud Console, navigate to the **API & Services** section via the left sidebar.
- Click on **"Library"**.
- Use the search function to locate and enable the following APIs:
  - **Gmail API**:
    - Click on it and then select **Enable**.
  - **Google Calendar API**:
    - Click on it and then select **Enable**.

## 4. Configure the OAuth Consent Screen
- Navigate to the **"OAuth consent screen"** under the **API & Services** section.
- Choose the **User Type**:
  - **External**: For applications intended for users outside your organization.
- Click **Create**.
- Fill out the required fields:
  - **App Name**: Enter a name for your application (e.g., "Job Interview Scheduler").
  - **User Support Email**: Provide your email address.
- Click **Save and Continue**.

## 5. Create OAuth Credentials for a Desktop Application
- After configuring the consent screen, go to the **"Credentials"** tab under **API & Services**.
- Click on **"Create Credentials"** and select **OAuth client ID**.
- For **Application Type**, choose **Desktop app**.
- Provide a name for the client (e.g., "Desktop Client for Scheduler").
- Click **Create**.

## 6. Download the `credentials.json` File
- After creating the credentials, a dialog will display your **Client ID** and **Client Secret**.
- Click the **Download JSON** button to save the `credentials.json` file to your computer.

## 7. Integrate the Credentials into Your Application
- Move the downloaded `credentials.json` file to the directory where your Python script resides.
- Ensure that your Python script references this file when setting up authentication with Google APIs.

By following these steps, you'll have a `credentials.json` file configured for your desktop application, enabling it to authenticate and interact with Google APIs such as Gmail and Calendar.
