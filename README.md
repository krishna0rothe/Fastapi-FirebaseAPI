# Fastapi-FirebaseAPI
This is a sample project that demonstrates how to build a FastAPI-based web API with Firebase Authentication for user registration, login, and profile management.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)


## Prerequisites

Before you begin, ensure you have the following prerequisites:

- Python 3.11.0 or higher
- A Firebase project with Firebase Authentication enabled
- Firebase Admin SDK credentials JSON file
- [FastAPI](https://fastapi.tiangolo.com/) installed

## Getting Started

1. #### Clone the repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/your-fastapi-firebase-project.git
   cd your-fastapi-firebase-project

2. #### Install project dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. #### Set up Firebase:
   - Create a Firebase project on the Firebase Console.
   - Download the Firebase Admin SDK credentials JSON file and save it as __serviceAccountKey.json__ in the project directory.

4. #### Configure Firebase:
   Open the __main.py__ file and update  the __firebaseConfig__ dictionary with your Firebase project's configuration
    
5. #### Run the FastAPI server:
   ```bash
   uvicorn main:app
   ```
6. ##### Access the API documentation:
   Open your web browser and navigate to `http://localhost:8000/` to view the interactive API documentation.

## Project Structure
  The project structure is organized as follows:
  -  `main.py`: The main FastAPI application.
  -  `models.py`: Pydantic models for data validation.
  -  `requirements.txt`: A list of Python dependencies.
  -  `serviceAccountKey.json`: Firebase Admin SDK credentials (replace with your own).
  -  `README.md`: This documentation file.

## Configuration
  To configure the project, open the `main.py` file and update the Firebase configuration in the `firebaseConfig` dictionary. Additionally, initialize the Firestore client as shown below:
```python
# Firebase configuration for the web app
firebaseConfig = {
    "apiKey": "YOUR_API_KEY",
    "authDomain": "YOUR_AUTH_DOMAIN",
    "projectId": "YOUR_PROJECT_ID",
    "storageBucket": "YOUR_STORAGE_BUCKET",
    "messagingSenderId": "YOUR_MESSAGING_SENDER_ID",
    "appId": "YOUR_APP_ID",
    "measurementId": "YOUR_MEASUREMENT_ID",
    "databaseURL": ""  # Leave this as an empty string
}

# Initialize Firestore client
db = firestore.Client(project="YOUR_PROJECT_ID")
```
Replace `YOUR_API_KEY`, `YOUR_AUTH_DOMAIN`, `YOUR_PROJECT_ID`, and other placeholders with your Firebase project's actual configuration values.

## API Endpoints
  - `POST /register`: Register a new user.
  - `POST /login`: Log in a user and receive an authentication token.
  - `GET /profile`: Retrieve the user's profile.
  - `PUT /update`: Update the user's profile.
  - `DELETE /delete`: Delete the user's profile.



    


   
