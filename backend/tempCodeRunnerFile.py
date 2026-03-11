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