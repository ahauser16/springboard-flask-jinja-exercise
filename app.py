from flask import Flask, request, render_template, redirect, url_for
from stories import Story

app = Flask(__name__)

story = Story(
    ["place", "noun", "verb", "adjective", "plural_noun"],
    """Once upon a time in a long-ago {place}, there lived a
       large {adjective} {noun}. It loved to {verb} {plural_noun}.""",
)

stories = {
    "story1": Story(
        ["place", "noun", "verb", "adjective", "plural_noun"],
        """Once upon a time in a long-ago {place}, there lived a
           large {adjective} {noun}. It loved to {verb} {plural_noun}.""",
    ),
    "story2": Story(
        ["animal", "food", "color"], "The {color} {animal} loves to eat {food}."
    ),
    # Add more stories here...
}


@app.route("/", methods=["GET", "POST"])
def select_story():
    if request.method == "POST":
        story_id = request.form["story"]
        return redirect(url_for("story_form", story_id=story_id))
    return render_template("select_story.html", stories=stories.keys())

@app.route('/story/<story_id>')
def story_view(story_id):
    story = stories[story_id]
    answers = request.args
    text = story.generate(answers)
    return render_template('story.html', text=text)


@app.route('/form/<story_id>')
def story_form(story_id):
    story = stories[story_id]
    prompts = story.prompts
    return render_template('form.html', prompts=prompts, story_id=story_id)

if __name__ == "__main__":
    app.run(debug=True)
