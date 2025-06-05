````markdown
# Foodhak "Foodhaks" Service

**Personalized, bite-sized health tips (Foodhaks!) for Foodhak users.  
Uses GPT-4o for playful, evidence-based recommendations from user profile data.  
Outputs a ready-to-display message, preview, and context URL.**

---

## 🌐 Environments

- **Production:** `https://ai-foodhak.com`
- **Staging:**    `https://staging.ai-foodhak.com`

---

## 🧠 What does it do?

- Takes a user ID and fetches their Foodhak profile.
- Picks a random health goal and recommended ingredient.
- Crafts a unique "Foodhak!" tip with extracts, context URL, and preview using GPT-4o.
- Focuses on *positive* ("recommended") ingredients and practical tips—no negative/avoidance messaging.
- Returns all fields in a consistent JSON schema for UI or in-app use.

---

## 🚦 Endpoints

| Method | Endpoint              | Description                                      |
|--------|----------------------|--------------------------------------------------|
| POST   | `/generate2/foodhak` | Generate a new Foodhak! for a user               |
| GET    | `/health`            | Service health check                             |

> **All endpoints require:**  
> `Authorization: Bearer <API_KEY>`

---

## 🛠️ Usage

### 1. Generate a Foodhak — POST `/generate2/foodhak`

#### Production

```bash
curl -X POST https://ai-foodhak.com/generate2/foodhak \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "YOUR_USER_ID"}'
````

#### Staging

```bash
curl -X POST https://staging.ai-foodhak.com/generate2/foodhak \
  -H "Authorization: Bearer <API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "YOUR_USER_ID"}'
```

#### Example Success Response

```json
{
  "common_name": "chia seeds",
  "response": "Hey there! For your heart health, add a sprinkle of chia seeds to your breakfast. These little seeds pack in omega-3s and fiber—easy way to keep things moving and stay full!",
  "url": "https://www.healthline.com/nutrition/chia-seeds-benefits",
  "food_type": "recommended",
  "preview": "Chia seeds: small size, mighty heart-loving impact!"
}
```

#### Example Error Response

```json
{
  "error": "User profile not found."
}
```

---

### 2. Health Check

```bash
curl https://ai-foodhak.com/health
```

**Result:**

```json
{
  "status": "healthy",
  "message": "Foodhak Service is up and running."
}
```

---

## ⚡ Features

* **AI-generated, evidence-based health tips** ("Foodhaks!") customized per user profile.
* **Always positive**: Recommends beneficial ingredients, avoids negative or restrictive language.
* **Includes a preview** (short, catchy version for UI teasers).
* **Response includes**: ingredient, full tip, preview, type, and context URL.
* **Uses OpenSearch for profiles and GPT-4o for content generation.**
* **API-key protected.**

---

## 📝 Developer Notes

* All secrets/API keys are sourced from environment variables.
* Only `"recommended"` Foodhaks are enabled; avoidance can be enabled in future if needed.
* The route is `/generate2/foodhak` to avoid conflicts with previous implementations.

---
