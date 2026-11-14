# Lesson Planner

> **Competition:** Digicode-Ed Challenge · the UAE's first contest to build an educational tool with ChatGPT for teachers, by the UAE Artificial Intelligence, Digital Economy and Remote Work Applications Office and The Digital School

A ChatGPT-powered web app, built with Flask, that helps teachers create lesson plans tailored to their students.

## How it works

1. The teacher enters the subject, grade, lesson duration, lesson title and objectives.
2. The app sends these to `gpt-3.5-turbo` together with a detailed lesson-plan guide: key vocabulary, learning outcomes (knowledge, skills, understanding), differentiation for different learners, learning experiences (prepare, plan, investigate, apply, connect, evaluate and reflect), educator assessment and educator reflection.
3. The generated lesson plan is shown on the page and can be downloaded as a `.txt` file.

## Run locally

```sh
pip install -r requirements.txt openai==0.28
python app.py
```

Replace `"API_KEY"` in `app.py` with your OpenAI API key before generating plans (don't commit a real key).

## Tech

Python, Flask, OpenAI API, Bootstrap. Built on the [Flask Boilerplate](https://github.com/realpython/flask-boilerplate) by Real Python (the `_updated` folder is the boilerplate's newer layout).

## License

Apache 2.0
