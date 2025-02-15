import os
import pandas as pd
import firebase_admin
from firebase_admin import credentials, db
from fastapi import FastAPI
import time  

# 🔥 Initialize Firebase
try:
    cred = credentials.Certificate("serviceAccountKey.json")  
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://trialthree-9e8be-default-rtdb.firebaseio.com/'
    })
    print("🔥 Firebase Initialized Successfully")
except Exception as e:
    print("❌ Firebase Initialization Error:", str(e))

# 🚀 Initialize FastAPI
app = FastAPI()

@app.post("/upload-data")
def upload_to_firebase():
    try:
        print("🔄 Starting data upload...")

        # ✅ Check if Excel file exists
        file_path = "sample_data.xlsx"
        if not os.path.exists(file_path):
            print("❌ Error: Excel file not found!")
            return {"error": "Excel file not found"}

        df = pd.read_excel(file_path)

        # ✅ Check if DataFrame is empty
        if df.empty:
            print("❌ Error: Excel file is empty!")
            return {"error": "Excel file is empty"}

        print("✅ Excel file read successfully")

        # ✅ Convert DataFrame to dictionary format
        data = df.to_dict(orient="records")
        print("📂 Data from Excel:", data)  # Print data

        ref = db.reference("/uploads")  # ✅ Store data under 'uploads' node

        # ✅ Push data to Firebase
        for record in data:
            ref.push(record)
            print("✔️ Uploaded:", record)  # Print each uploaded record

        time.sleep(1)  # ✅ Ensure Firebase processes the data

        print("✅ Data Uploaded Successfully")
        return {"message": "Data uploaded successfully"}
    except Exception as e:
        print("❌ Error Uploading:", str(e))
        return {"error": str(e)}

@app.get("/fetch-data")
def fetch_data():
    try:
        ref = db.reference("/uploads")  # ✅ Fetching from 'uploads' node
        print("📡 Fetching data from Firebase...")

        for i in range(3):  # 🔄 Retry 3 times
            data = ref.get()
            if data:
                print("✅ Data Fetched:", data)
                return data
            time.sleep(2**i)  # Wait 1s, 2s, 4s

        print("❌ No data found in Firebase.")
        return {"message": "No data found in Firebase, even after retries."}
    except Exception as e:
        print("❌ Error Fetching Data:", str(e))
        return {"error": str(e)}

# 🔄 Run FastAPI Server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
