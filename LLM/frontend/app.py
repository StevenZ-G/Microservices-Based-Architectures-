from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = "recom-secret"

# URL del orquestador
ORCHESTRATOR_URL = "http://localhost:5016/orchestrate"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_id = request.form['user_id']
        emotion = request.form['emotion']

        if not user_id or not emotion:
            flash("Please complete all fields.")
            return redirect(url_for('index'))

        try:
            response = requests.post(ORCHESTRATOR_URL, json={
                "user_id": user_id,
                "emotion": emotion
            })
            if response.status_code == 200:
                data = response.json()
                return render_template('index.html', recommendation=data['recommendation'], submitted=True)
            else:
                flash(f"Orchestrator Error: {response.json().get('error')}")
        except Exception as e:
            flash(f"Conection Error: {str(e)}")

    return render_template('index.html', submitted=False)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5020)
