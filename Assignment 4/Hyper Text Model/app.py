from flask import Flask, render_template, request
import json

app = Flask(__name__)

# Load data from the scraped JSON file
with open("pakistan_content.json", "r", encoding="utf-8") as file:
    content = json.load(file)

# Convert sections into a format suitable for navigation
sections = list(content.keys())

# Homepage route

"""
    section_title="Home": The title of the section
    content=None: No specific content is passed.
    sections=sections: Passes the list of sections for navigation purposes.
"""
@app.route("/")
def index():
    return render_template("section.html", section_title="Home", content=None, sections=sections)

# Section route


@app.route("/section/<section_title>")
def show_section(section_title):
    if section_title in content:
        section_content = content[section_title]

        return render_template("section.html", section_title=section_title, content=section_content, sections=sections)
    else:
        return f"Section '{section_title}' not found.", 404

# Search functionality
@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query", "").strip().lower()
    
        results = {title: paras for title, paras in content.items() if query in title.lower()}
        
        return render_template("search.html", query=query, results=results)
    return render_template("search.html", query="", results={})


if __name__ == "__main__":
    app.run(debug=True)
