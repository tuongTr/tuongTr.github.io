from flask import Flask, request, jsonify
import json
import random
import os
from flask import render_template_string

app = Flask(__name__, static_folder="static")


def load_characters(filename="characters.json"):
    with open(filename, "r") as file:
        return json.load(file)


character_data = load_characters()
questions = set()

# Extract all possible questions from character attributes
for traits in character_data.values():
    questions.update(traits.keys())
questions = list(questions)


@app.route('/')
def index():
    selected_questions = random.sample(questions, 5)  # Select 5 random questions
    with open("index.html", "r") as file:
        html_content = file.read()
    return render_template_string(html_content, questions=selected_questions, character_data=character_data)


@app.route('/submit', methods=['POST'])
def submit():
    user_answers = request.json
    scores = {char: 0 for char in character_data}

    for question, answer in user_answers.items():
        weight = 1 if answer == "yes" else -1
        for character, traits in character_data.items():
            if question in traits:
                scores[character] += traits[question] * weight

    best_match = max(scores, key=scores.get)
    image_path = f"/static/images/{best_match.lower().replace(' ', '_')}.jpg"
    return jsonify({"character": best_match, "image": image_path})


@app.route('/new_game', methods=['GET'])
def new_game():
    return jsonify({"new_game": True})


if __name__ == "__main__":
    app.run(debug=True)