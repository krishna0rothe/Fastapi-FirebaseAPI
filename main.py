# Import required Libraries and modules
from fastapi import FastAPI, Depends
import uvicorn
from fastapi.security import OAuth2PasswordBearer
import firebase_admin
from firebase_admin import credentials, auth
import pyrebase
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from google.cloud import firestore
from models import *

# Create a FastAPI application instance
app = FastAPI(
    description="This  is app to complete my internship assignment",
    title="Fastapi & Firebase",
    docs_url="/"
)

# Initialize Firebase Admin using credentials
if not firebase_admin._apps:
    cred = credentials.Certificate("path/to/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

# Firebase configuration for the web app
firebaseConfig = {
  "apiKey": "YOUR_API_KEY",
  "authDomain": "YOUR_AUTH_DOMAIN",
  "projectId": "YOUR_PROJECT_ID",
  "storageBucket": "YOUR_STORAGE_BUCKET",
  "messagingSenderId": "YOUR_MESSAGING_SENDER_ID",
  "appId": "YOUR_APP_ID",
  "measurementId": "YOUR_MEASUREMENT_ID",
  "databaseURL":"" # Leave this as it is "empty-string"
}

# Initialize Firestore client
db = firestore.Client(project="YOUR_PROJECT_ID")

# Initialize Pyrebase with Firebase configuration
firebase = pyrebase.initialize_app(firebaseConfig)

# Define OAuth2 password bearer for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Define the '/register' endpoint for user registration
@app.post("/register") 
def register_user(user: UserRegistration):
    username = user.username
    email= user.email
    full_name= user.full_name
    password= user.password

    try:
        # Create the user in Firebase Authentication
        user_record = auth.create_user(
            email=email,
            password=password
        )
        
        # Store user data in Firestore (excluding password)
        user_data = {
            "username": username,
            "email": email,
            "full_name": full_name,
            "created_at": firestore.SERVER_TIMESTAMP
        }

        # Access the user's UID from the user_record object
        user_data["uid"] = user_record.uid

        # Add user data to Firestore
        db.collection("users").document(user_record.uid).set(user_data)
        
        # Return a success responce 
        return JSONResponse(content={"message":f"User account created suessfuly for user {user_record.uid}"},status_code=201)
    
    except auth.EmailAlreadyExistsError:
        # Return an error if the email alrady exists
        raise HTTPException(status_code=400,detail=f"Account already created for this email {email}")

# Define the '/login' endpoint for user login
@app.post('/login')
async def create_access_token(user_data:LoginSchema):
    email = user_data.email
    password = user_data.password

    try:
        # Sign in the user with Firebase Authentication 
        user = firebase.auth().sign_in_with_email_and_password(
            email= email,
            password= password
        )
        token = user['idToken']

        # Return the token as a JSON response
        return JSONResponse(content={"token":token},status_code=200)
    
    except:
        # Return an error if login credentials are invalid
        raise HTTPException(
            status_code=400,detail="Invalid credentials"
        )

# Define the '/profile' endpoint to retrive user's profile
@app.get("/profile")
async def retriveve_user_profile(token: str = Depends(oauth2_scheme)):
    try:
        # Verify the token and extract the user's UID
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']

        user_doc_ref = db.collection("users").document(uid)
        user_data = user_doc_ref.get()

        if not user_data.exists:
            # Return an error if the user does not exist
            raise HTTPException(status_code=404,detail="User not found")
        
        user = user_data.to_dict()
        created_at = user.get("created_at")
        
        if created_at:
            created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")
        
        # Create a UserInDB instance and return
        user_in_db = UserInDB(uid=uid, username=user.get("username"),email=user.get("email"),
                              full_name=user.get("full_name"),created_at=created_at)
        return user_in_db
    except Exception as e:
        # Catch any exceptions and raise an HTTP error with a failure message
        raise HTTPException(
            status_code=400,
            detail="Profile retrieval failed: " + str(e)
        )

# Define the '/update' endpoint to update user's profile
@app.put("/update")
async def update_user_profile(user: Update_user, token: str = Depends(oauth2_scheme)):
    try:
        # Verify the user's authentication token
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']

        # Prepare the updated user data from the request
        user_data = {
            "username": user.username,
            "email":user.email,
            "full_name":user.full_name
        }

        # Update the user's profile in Firestore 
        db.collection("users").document(uid).update(user_data)

        # Return a success message if the profile is updated successfully
        return {"message":"Profile updated successfully"}
    except Exception as e:
        # Catch any exceptions and raise an HTTP error with a failure message
        raise HTTPException(
            status_code=400,
            detail="Profile update failed"
        )

# Define the '/delete' endpoint to delete a user's profile
@app.delete("/delete")
def delete_user_profile(token: str = Depends(oauth2_scheme)):
    try:
        # Verify the user's authentication token
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid'] # Extract the user's UID from the token

        # Delete the user's document from Firestore
        db.collection("users").document(uid).delete()

        # Delete the user's Firebase Authentication account
        auth.delete_user(uid)

        # Rreturn a success message id the user profile is deleted successfully
        return{"message":"User profile deleted successfuly"}
    except Exception as e:
        # Catch any exceptions and raise an HTTP error with a failure message
        raise HTTPException(status_code=400,detail="Profile deletion failed"+ str(e))
    

if __name__ == "__main__":
    uvicorn.run("main:app")
