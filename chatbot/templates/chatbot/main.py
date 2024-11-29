import requests
import json

# Replace with your actual API key
API_KEY = "AIzaSyBQh7Bt-IpBONkJ3ZG3_7N149ZDCib7v0I"

# API endpoint
URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

# Header configuration
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Request payload
payload = {
    "prompt": "Explain the benefits of AI in healthcare.",
    "maxOutputTokens": 150,
    "temperature": 0.7
}

try:
    # Send the API request
    response = requests.post(URL, headers=headers, json=payload)

    # Check for errors
    if response.status_code == 200:
        result = response.json()
        print("AI Response:")
        print(result.get("contents", [{}])[0].get("text", "No response text found."))
    else:
        print(f"Error: {response.status_code}, {response.text}")

except Exception as e:
    print(f"An error occurred: {e}")
