import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime, timedelta

load_dotenv()

class DatabaseHandler():
    def __init__(self):
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
        self.supabase: Client = create_client(url, key)
        self.users = self.supabase.table("users")

    def register_user(self, name: str, email: str, password: str, phone: str = ""):
        try:
            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password,
            })
            self.supabase
            if not response.user:
                raise Exception("Registration failed")
            
            user_id = response.user.id

            # Insert user into 'users' table
            self.users.insert({
                "uid": user_id,
                "name": name,
                "email": email,
                "role": "user",
                "phone": phone
            }).execute()
            return {"message": "User registered successfully", "data": response, "status_code": 200}
        except Exception as e:
            return {"error": f"An error occurred during user registration: {e}", "status_code": 404}

    def login_user(self, email: str, password: str):
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            return {
                "message": "User logged in successfully", 
                "user": {
                    "id":response.user.id, 
                    "email": response.user.user_metadata["email"]
                },
                "token": response.session.access_token,
                "status_code": 200
                }
        except Exception as e:
            return {"error": f"An error occured during login: {e}", "status_code": 404}
    
    def get_all_users(self):
        try:
            users = self.users.select("*").execute()
            return {"message": "Users retrieved successfully", "data": users.data, "status_code": 200}
        except Exception as e:
            return {"error": f"An error occurred while fetching users: {e}", "status_code": 404}

    def update_user(self, user_id: str, email: str = None, name: str = None, phone: str = None, password: str = None):
        try:
            update_data = {}
            if email:
                update_data["email"] = email
            if name:
                update_data["name"] = name
            if phone:
                update_data["phone"] = phone
            if not update_data:
                raise Exception("No data provided for update")

            self.users.update(update_data).eq("uid", user_id).execute()
            if password:
                update_data["password"] = password
            self.supabase.auth.admin.update_user_by_id(user_id, {"email": email, "password": password})
            return {"message": "User updated successfully", "status_code": 200}
        except Exception as e:
            return {"error": f"An error occurred while updating user: {e}", "status_code": 404}
    
    def delete_user(self, user_id: str):
        try:
            self.users.delete().eq("uid", user_id).execute()
            self.supabase.auth.admin.delete_user(user_id)
            return {"message": "User deleted successfully", "status_code": 200}
        except Exception as e:
            return {"error": f"An error occurred while deleting user: {e}", "status_code": 404}
    
    def get_user_by_id(self, user_id: str):
        try:
            user = self.users.select("*").eq("uid", user_id).single().execute()
            return {"message": "User retrieved successfully", "data": user.data, "status_code": 200}
        except Exception as e:
            return {"error": f"An error occurred while fetching user: {e}", "status_code": 404}
        