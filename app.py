from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

# Load jobs.csv
data = pd.read_csv("jobs.csv")

# Separate job description and label
X = data["job_description"]
y = data["label"]

# Convert text into numbers
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Train AI model
model = LogisticRegression()
model.fit(X_vectorized, y)

from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

data = pd.read_csv("jobs.csv")

X = data["job_description"]
y = data["label"]

vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vectorized, y)

from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

app = Flask(__name__)

data = pd.read_csv("jobs.csv")

X = data["job_description"]
y = data["label"]

vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

model = LogisticRegression()
model.fit(X_vectorized, y)

reports = []


@app.route("/", methods=["GET", "POST"])
def home():
    result = ""

    if request.method == "POST":
        job = request.form["job_description"]

        job_vectorized = vectorizer.transform([job])
        prediction = model.predict(job_vectorized)[0]

        if prediction == "Fake":
            result = "⚠️ This job advertisement may be FAKE."
        else:
            result = "✅ This job advertisement appears GENUINE."

        reports.append({
            "job": job,
            "prediction": prediction
        })

    return render_template("verihire-scanner.html", result=result)


@app.route("/admin")
def admin():
    fake_count = sum(1 for r in reports if r["prediction"] == "Fake")
    genuine_count = sum(1 for r in reports if r["prediction"] == "Genuine")
    total_count = len(reports)

    return render_template(
        "admin.html",
        reports=reports,
        fake_count=fake_count,
        genuine_count=genuine_count,
        total_count=total_count
    )