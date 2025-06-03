from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = None
    if request.method == 'POST':
        article_text = request.form.get('article_text')
        # TODO: Replace this placeholder with your real summarizer function
        summary = f"Summary (first 100 chars): {article_text[:100]}..." if article_text else "No article text provided."
    return render_template('index.html', summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
