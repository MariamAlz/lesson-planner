# Lesson Planner

> **Competition:** Digicode-Ed Challenge · the UAE's first contest to build an educational tool with ChatGPT for teachers, by the UAE Artificial Intelligence, Digital Economy and Remote Work Applications Office and The Digital School

A ChatGPT-powered web app, built with Flask, that helps teachers create lesson plans tailored to their students. The home page is titled "TeachGenius: Simplify Lesson Planning with AI".

## How it works

1. The teacher enters the subject, grade, lesson duration, lesson title and objectives.
2. The app sends these to `gpt-3.5-turbo` together with a detailed lesson-plan guide: key vocabulary, learning outcomes (knowledge, skills, understanding), differentiation for different learners, learning experiences (prepare, plan, investigate, apply, connect, evaluate and reflect), educator assessment and educator reflection.
3. The generated lesson plan is shown on the page and can be downloaded as a `.txt` file.

## Features

- **Lesson plan form**: subjects (Math, Science, History, Geography, Artificial Intelligence), grades 1 to 12, and durations from 30 minutes to 2 hours.
- **Structured prompt**: the full lesson-plan guide is sent with every request, so each plan follows the same sections.
- **Download**: `/download_text` returns the plan as `lesson_plan.txt`.


## Project structure

```
app.py                      Routes (/, /about, /plan, /download_text) and the OpenAI call
templates/pages/            Home page with the form (placeholder.home.html) and the result page (plan.html)
templates/layouts/          Base layouts
forms.py, models.py, config.py   Boilerplate forms, database set-up and settings
static/                     Bootstrap 3.1.1, Font Awesome, jQuery
Procfile                    gunicorn entry for deployment
_updated/                   The boilerplate's newer layout (not used by app.py)
```

## Run locally

```sh
pip install -r requirements.txt openai==0.28 pdfkit
python app.py
```

Then open http://127.0.0.1:5000.

Replace `"API_KEY"` in `app.py` with your OpenAI API key before generating plans (don't commit a real key).

`app.py` imports `pdfkit` (it isn't used yet), so it is installed above. `openai==0.28` is needed because the code uses the older `openai.ChatCompletion` API. `requirements.txt` doesn't pin versions. If the latest Flask-WTF fails on `from flask_wtf import Form` in `forms.py`, install an older Flask-WTF.

## Tech

Python, Flask, OpenAI API, Bootstrap. Built on the [Flask Boilerplate](https://github.com/realpython/flask-boilerplate) by Real Python (the `_updated` folder is the boilerplate's newer layout).

## Credits

- [Flask Boilerplate](https://github.com/realpython/flask-boilerplate) by Real Python: app layout, templates, forms and static assets.
- [Bootstrap](https://getbootstrap.com/), [Font Awesome](https://fontawesome.com/) and jQuery, bundled in `static/`.

## License

Apache 2.0
