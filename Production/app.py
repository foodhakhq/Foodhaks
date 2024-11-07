import os
import random
import requests
from requests.auth import HTTPBasicAuth
import json
from flask import Flask, request, jsonify
from openai import OpenAI
from collections import OrderedDict
from flask import Response
from functools import wraps  
from dotenv import load_dotenv
import os

load_dotenv()
# Access the variables
API_KEY = os.getenv("API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Initialize the OpenAI client
client = OpenAI(
    api_key=OPENAI_API_KEY,
)

# Set environment variables for OpenSearch
os.environ["OPENSEARCH_USER"] = os.getenv("OPENSEARCH_USER")
os.environ["OPENSEARCH_PWD"] = os.getenv("OPENSEARCH_PWD")
os.environ["OPENSEARCH_HOST"] = os.getenv("OPENSEARCH_HOST")
app = Flask(__name__)

def require_api_key(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        print(f"Authorization Header: '{auth_header}'")  # Debugging output
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1].strip()
            print(f"Token extracted: '{token}'")  # Debugging output
            print(f"Token length: {len(token)}, API_KEY length: {len(API_KEY)}")
            print(f"Token bytes: {token.encode('utf-8')}")
            print(f"API_KEY bytes: {API_KEY.encode('utf-8')}")
            if token == API_KEY:
                return view_function(*args, **kwargs)
        return jsonify({"error": "Unauthorized API Key"}), 401
    return decorated_function




# Function to retrieve user profile based on ID
def get_user_profile(user_id):
    url = f"{os.getenv('OPENSEARCH_HOST')}/user-profiles/_search"
    user = os.getenv("OPENSEARCH_USER")
    password = os.getenv("OPENSEARCH_PWD")
    
    query = {
        "query": {
            "match": {
                "foodhak_user_id": user_id
            }
        }
    }
    
    response = requests.get(url, auth=HTTPBasicAuth(user, password), json=query)
    
    if response.status_code == 200:
        results = response.json()
        if results['hits']['total']['value'] > 0:
            return results['hits']['hits'][0]['_source']
        else:
            return None
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Function to generate Foodhak using GPT-4, including extracts and URL
def generate_foodhak(user_name, health_goal, ingredient_name, relationship):
    # Split extracts and URLs
    extracts_list = relationship['extracts'].split(' | ')
    urls_list = relationship['url'].split(' | ')
    
    # Randomly select one extract and its corresponding URL
    selected_index = random.randint(0, len(extracts_list) - 1)
    selected_extract = extracts_list[selected_index]
    selected_url = urls_list[selected_index]

    # Create the prompt for GPT-4
    prompt = (
        f"Create a short, insightful 'Foodhak!' for {user_name}, who is trying to {health_goal}. "
        f"Use the following ingredient and its relationship: {ingredient_name} "
        f"({relationship['relationship']} {relationship['entity']}). "
        f"Here is some additional context: {selected_extract}. "
        f"Please make it engaging and informative, with a focus on practical tips or suggestions. "
        f"Start with a friendly greeting to the user, followed by the Foodhak. "
        f"Do not start with phrases like 'Avoid [common_name]'. "
        f"Include any relevant nutritional benefits or practical applications."
        f"Do not include the role/assistant's name in your response."
    )
    
    # Call the OpenAI GPT-4 model to generate the Foodhak
    chat_completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Extract the assistant's response content
    foodhak = chat_completion.choices[0].message.content.strip()
    return foodhak, selected_url

# Function to generate a short preview
def generate_preview(selected_foodhak):
    prompt = (
        f"Create a short and catchy description (50-75 characters) for a health-oriented tip called '{selected_foodhak}'. "
        "Use puns or playful language to make it engaging and enticing. Aim to pique curiosity or bring a smile. "
        "Do not include user's name in the response."
        "Example response: Peas give peas a chance—your heart will thank you!"
    )
    chat_completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    preview = chat_completion.choices[0].message.content.strip()
    return preview

# Function to create and return a Foodhak in JSON format
def create_and_return_foodhak(user_id):
    # Retrieve user profile
    user_profile = get_user_profile(user_id)
    
    if not user_profile:
        return {"error": "User profile not found."}
    
    # Randomly pick a health goal
    selected_goal = random.choice(user_profile['user_health_goals'])
    if 'user_goals' in selected_goal:
        health_goal_title = selected_goal['user_goals']['title']
    elif 'user_goal' in selected_goal:
        health_goal_title = selected_goal['user_goal']['title']
    else:
        health_goal_title = None 
    
    foodhak_recommend = None
    foodhak_avoid = None
    selected_common_name = None
    food_type = None  # Variable to store the type of foodhak (recommend or avoid)
    
    # Randomly pick an ingredient to recommend
    if selected_goal['ingredients_to_recommend']:
        recommended_ingredient = random.choice(selected_goal['ingredients_to_recommend'])
        selected_common_name = recommended_ingredient['common_name']
        relationship = random.choice(recommended_ingredient['relationships'])
        foodhak_recommend, selected_url = generate_foodhak(
            user_profile['name'], 
            health_goal_title, 
            selected_common_name, 
            relationship
        )
    
    # Randomly pick an ingredient to avoid
    """
    if 'ingredients_to_avoid' in selected_goal and selected_goal['ingredients_to_avoid']:
        avoided_ingredient = random.choice(selected_goal['ingredients_to_avoid'])
        selected_common_name = avoided_ingredient['common_name']
        relationship = random.choice(avoided_ingredient['relationships'])
        foodhak_avoid, selected_url = generate_foodhak(
            user_profile['name'], 
            health_goal_title, 
            selected_common_name, 
            relationship
        )
    """
    """
    # Randomly choose between recommend and avoid Foodhak
    if foodhak_recommend and foodhak_avoid:
        selected_foodhak, food_type = random.choice([(foodhak_recommend, "recommended"), (foodhak_avoid, "avoided")])
    elif foodhak_recommend:
        selected_foodhak, food_type = foodhak_recommend, "recommended"
    elif foodhak_avoid:
        selected_foodhak, food_type = foodhak_avoid, "avoided"
    else:
        selected_foodhak, food_type = "No Foodhak available.", "No food_type available."
    """

    if foodhak_recommend:
        selected_foodhak, food_type = foodhak_recommend, "recommended"
    else:
        selected_foodhak, food_type = "No Foodhak available.", "No food type available."

    
    # Generate the preview
    preview = generate_preview(selected_foodhak)
    
    response_json = OrderedDict([
        ("common_name", selected_common_name),
        ("response", selected_foodhak),
        ("url", selected_url),
    	("food_type", food_type),
        ("preview", preview),

    ])
    
    return response_json

@app.route('/generate/foodhak', methods=['POST'])
@require_api_key  # Add this line to protect the route with API key authentication
def foodhak():
    data = request.json
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
    
    response = create_and_return_foodhak(user_id)
    ordered_response = json.dumps(response, ensure_ascii=False)
    return Response(ordered_response, content_type='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8889)
