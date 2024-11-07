```markdown
# FoodHaks
This repo contains the scripts for Foodhaks staging and production environment.
## Overview

This documentation provides an overview of the API used to generate personalized food-related tips, known as "Foodhak." The API leverages GPT-4o, a Large Language Model (LLM) from OpenAI, to create these tips based on a user’s health goals, dietary preferences, and specific ingredients. The system utilizes OpenSearch for retrieving user profiles and is hosted on a Google Cloud Platform (GCP) VM instance running a Flask server.

## Endpoint

### Generate Foodhak

This endpoint generates a personalized Foodhak for a user based on their profile information stored in OpenSearch. The Foodhak includes practical dietary advice, a relevant URL, and a preview description.

**Endpoint URL:**

`https://www.foodhakai.com/generate/foodhak`

**HTTP Method:**

`POST`

**Headers:**

- `Content-Type: application/json`
- `Authorization: Bearer test123`

**Request Payload:**

```json
{
  "user_id": "32a40b12-2434-473a-9270-df47db9ceefd"
}
```

**Parameters:**

- `user_id`: A unique identifier for the user. This is required to retrieve the user’s profile and generate a personalized Foodhak.

### Example Response

```json
{
  "common_name": "potato",
  "response": "Hey Sakshi!\\n\\nLooking to shed some pounds while staying satisfied? Here's a simple yet super effective food hack for you: Embrace the power of potatoes! 🍠\\n\\n**Foodhak Alert: Preload with Potatoes for Weight Loss**\\n\\n**Why Potatoes?** They're not just comfort food, but they are also amazing at keeping you full for longer. Potatoes improve satiety, which means they help curb those pesky hunger pangs.\\n\\n**How to Use This Hack:**\\n- **Start a Meal with a Small Potato Dish**: Enjoying a small serving of boiled or baked potatoes before your main meal can help you feel fuller and reduce overall calorie intake.\\n- **Healthy Preparation Matters**: Keep it healthy by avoiding frying. Instead, try boiling, baking, or steaming your potatoes. Spice them up with herbs, a squeeze of lemon, or a sprinkle of your favorite low-calorie seasonings.\\n- **Pair with Protein**: Combine with a source of lean protein for a balanced, satisfying start to your meal.\\n\\n**Benefits of Potatoes:**\\n- **Rich in Fiber**: Keeps your digestive system happy.\\n- **High in Vitamins and Minerals**: Packed with Vitamin C, potassium, and Vitamin B6.\\n- **Low-Calorie but Filling**: Helps you manage weight without feeling deprived.\\n\\nSo next time you're prepping your meals, think potatoes! They might just become your new go-to for a delicious, satisfying start that supports your weight loss goals.\\n\\nHappy, healthy eating!\\n\\n👩‍🍳✨",
  "url": "<https://pubmed.ncbi.nlm.nih.gov/32927753>",
  "food_type": "recommended",
  "preview": "\\"Spud-tacular Weight Loss: Potatoes to Curb Cravings! 🥔✨\\""
}
```

### Response Fields:

- `common_name`: The name of the ingredient related to the Foodhak (e.g., "potato").
- `response`: A detailed, engaging Foodhak message that includes dietary advice tailored to the user's health goals.
- `url`: A link to a relevant study or article that supports the advice provided in the Foodhak.
- `food_type`: Indicates whether the Foodhak is a recommendation or something to avoid (e.g., "recommended").
- `preview`: A short, catchy preview of the Foodhak designed to pique the user’s interest.

## Technical Details

- **OpenAI GPT-4o**: The model used to generate the Foodhak and preview content.
- **OpenSearch**: Utilized for retrieving user profiles based on the `user_id`.
- **Flask Server**: The API is hosted on a GCP VM instance running Flask.
- **Random Selection**: The system randomly selects a relevant ingredient and relationship from the user's profile to generate a personalized Foodhak.

## Example Usage

### Foodhak (Production)

```bash
curl -X POST https://www.foodhakai.com/generate/foodhak \
-H "Content-Type: application/json" \
-H "Authorization: Bearer viJ8u142.NaQl7JEW5u8bEJpqnnRuvilTfDbHyWty" \
-d '{
  "user_id": "9acc25b6-b238-407e-bc85-44d723bf4551"
}'
```

### Foodhak (Staging)

```bash
curl -X POST https://www.staging-foodhakai.com/generate2/foodhak \
-H "Content-Type: application/json" \
-H "Authorization: Bearer mS6WabEO.1Qj6ONyvNvHXkWdbWLFi9mLMgHFVV4m7" \
-d '{
  "user_id": "32a40b12-2434-473a-9270-df47db9ceefd"
}'
```

## Conclusion

This API allows for the generation of personalized, health-oriented tips known as Foodhak. By integrating user-specific data with advanced AI models, it delivers tailored dietary advice designed to be both informative and engaging. The system efficiently retrieves user profiles, processes the data, and produces a Foodhak that aligns with the user's health goals, making it a powerful tool for personalized nutrition advice.
```

This README.md will help explain the capabilities and usage of the FoodHak API clearly and effectively to potential users and contributors to the project.
