from app.predictor import IdeaPredictor

predictor = IdeaPredictor()

examples = [
    "AI tool for planning trips based on budget and preferences",
    "Chrome extension for saving and organizing links",
    "Platform for hiring freelance designers",
    "App for tracking workouts and nutrition",
    "API for sending transactional emails",
    "Tool for students to improve essay writing with AI"
]

for text in examples:
    result = predictor.predict(text, top_k=3)

    print("\n" + "=" * 80)
    print("Idea:", result["input_idea"])
    print("Predicted category:", result["predicted_category"])
    print("Confidence:", result["confidence"])
    print("Top predictions:")
    for pred in result["top_predictions"]:
        print(f"  - {pred['category']}: {pred['probability']}")