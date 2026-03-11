from flask import Flask, render_template, request, session ,redirect,url_for
import user
import os
from functools import wraps

app = Flask(
    __name__,
    template_folder="../templates",  # relative path to templates
    static_folder="../static"        # relative path to static
)

app.secret_key = os.environ.get('sessioncode')

@app.route("/settings")
def settings():
    return render_template("settings.html", theme=session.get("theme", "light-mode"))

@app.route("/toggle-theme", methods=["POST"])
def toggle_theme():
    current = session.get("theme", "light-mode")
    session["theme"] = "dark-mode" if current == "light-mode" else "light-mode"
    return redirect("/settings")


# ----------------- User Routes -----------------

def login_required_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_route'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/user_home')
def user_home():
    return render_template("user_home.html")

@app.route('/')
def homepage():
    diseases = [
        {"emoji":"🐕","name":"Rabies","slug":"rabies","points":["Aggression","Drooling","Paralysis"]},
        {"emoji":"🐶","name":"Tick Fever","slug":"tick-fever","points":["Lethargy","Fever","Pale gums"]},
        {"emoji":"🐕","name":"Parvovirus","slug":"parvovirus","points":["Vomiting","Diarrhea","Dehydration"]},
        {"emoji":"🐶","name":"Distemper","slug":"distemper","points":["Coughing","Sneezing","Fever"]},
        {"emoji":"🐱","name":"Feline Panleukopenia","slug":"feline-panleukopenia","points":["Vomiting","Diarrhea","Weight loss"]},
        {"emoji":"🐕","name":"Leptospirosis","slug":"leptospirosis","points":["Fever","Weakness","Jaundice"]},
        {"emoji":"🐱","name":"Ringworm","slug":"ringworm","points":["Hair loss","Skin lesions","Itching"]}
    ]
    return render_template('homepage.html', diseases=diseases)


@app.route('/signin', methods=['GET', 'POST'])
def sign_route():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        phnor = request.form.get('phnor')
        city = request.form.get('city')

        if not all([fname, lname, email, password, phnor, city]):
            return "Please fill in all fields!"

        user.add_user(fname, lname, email, password, phnor, city)
        return render_template('login.html')
    else:
        return render_template("signin.html")

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([email, password]):
            return render_template('login.html', error="Please fill in all fields!")

        user_data = user.check_stat(email, password)
        if user_data:
            session['user_id'] = user_data[2]
            return render_template('base.html', redirect_url=url_for('dashboard'))
        else:
            return render_template('login.html', error="Invalid email or password!")
    else:
        return render_template('login.html')

# ----------------- Doctor Routes -----------------\

def doclogin_required_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'doc_id' not in session:
            return redirect(url_for('doclogin_route'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/docsignin', methods=['GET', 'POST'])
def docsign_route():
    if request.method == 'POST':
        fname = request.form.get('fname')
        lname = request.form.get('lname')
        email = request.form.get('email')
        password = request.form.get('password')
        pnor = request.form.get('pnor')
        city = request.form.get('city')
        address = request.form.get('address')

        if not all([fname, lname, email, password, pnor, city, address]):
            return "Please fill in all fields!"

        user.add_doc(fname, lname, email, pnor, password, city, address)
        return render_template('doclogin.html')
    else:
        return render_template("docsignin.html")

@app.route('/doclogin', methods=['GET', 'POST'])
def doclogin_route():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([email, password]):
            return render_template('doclogin.html', error="Please fill in all fields!")

        user_data = user.doc_check_stat(email, password)
        if user_data:
            session['doc_id'] = user_data[2]
            return render_template('base.html', redirect_url=url_for('doc_dashboard'))
        else:
            return render_template('doclogin.html', error="Invalid email or password!")
    else:
        return render_template('doclogin.html')
    

@app.route('/user_dashboard')
def dashboard():
    if 'user_id' in session:
        return render_template('user_dashboard.html')
    return redirect(url_for('login_route'))

@app.route('/doc_dashboard')
def doc_dashboard():
    if 'doc_id' in session:
        return render_template('doc_dashboard.html')
    return redirect(url_for('doclogin_route'))


@app.route('/rabies')
def rabies_info():
    return render_template('diseases/rabies.html')

@app.route('/tick-fever')
def tick_fever_info():
    return render_template('diseases/tick_fever.html')

@app.route('/parvovirus')
def parvo_info():
    return render_template('diseases/parvovirus.html')

@app.route('/distemper')
def distemper_info():
    return render_template('diseases/distemper.html')

@app.route('/feline-panleukopenia')
def feline_panleuko_info():
    return render_template('diseases/feline_panleuko.html')

@app.route('/leptospirosis')
def lepto_info():
    return render_template('diseases/leptospirosis.html')

@app.route('/ringworm')
def ringworm_info():
    return render_template('diseases/ringworm.html')



if __name__ == "__main__":
    app.run(debug=True)
