# booking.py
from file import app,login_required_user,doclogin_required_user
from flask import Flask, session, redirect, url_for,render_template,request
from datetime import date,datetime
import user2

@app.route('/search_results',methods=['POST','GET'])
@login_required_user
def results():
    location=request.form.get('locationInput')
    docters=user2.get_doc(location)

    if docters:
        return render_template('search_results.html',results=docters)
    else:
        return render_template('no_result.html',city=location)

@app.route('/book_appointment',methods=['POST'])
@login_required_user
def book_appointment():
    doc_id=request.form.get('doc_id')
    if not doc_id:
        return redirect(url_for('results'))

    today = date.today().isoformat() 
    return render_template('selectdate.html',doc_id=doc_id,current_date=today)
    

# @app.route('/select_booking',methods=['POST','GET'])
# @login_required_user
# def select_booking():
#     return render_template('selectdate.html')


@app.route('/confirm_appointment',methods=['POST'])
@login_required_user
def confirm_booking():
    doc_id=request.form.get('doc_id')
    appt_date=request.form.get('appt_date')
    appt_time=request.form.get('appt_time')
    user_id=session.get('user_id')

    if not all([doc_id, appt_date, appt_time, user_id]):
        return redirect(url_for('results'))

    try:
        appt_dt = datetime.strptime(appt_date, '%Y-%m-%d').date()
    except ValueError:
        return redirect(url_for('book_appointment'))

    if appt_dt < date.today():
        return redirect(url_for('book_appointment'))
    
    existing = user2.check_booking(doc_id, appt_date, appt_time)
    if existing:
        return "This slot is already booked! Please choose another time.", 400
    
    user2.add_doc(doc_id,user_id,appt_time,appt_date)
    
    return redirect(url_for('view_appointment',doc_id=doc_id,date=appt_date,time=appt_time))


@app.route('/view_appointment')
@login_required_user
def view_appointment():
    did = request.args.get('doc_id')
    d = request.args.get('date')
    t = request.args.get('time')
    user_id = session.get('user_id')

    r = user2.view_apt(user_id, did, d)
    if r:
        return render_template('view.html', date=d, time=t, doctor=r)
    else:
        return redirect(url_for('dashboard'))
    

@app.route('/pet-health', methods=['GET', 'POST'])
def pet_health():
    result = None
    if request.method == 'POST':
        name = request.form['name']
        weight = float(request.form['weight'])
        height = float(request.form['height'])
        water = float(request.form['water'])
        activity = float(request.form['activity'])

        # Call the function from user2.py
        result = user2.calculate_pet_health(name, weight, height, water, activity)

    return render_template('pet_health.html', result=result)


@app.route('/appointments')
@login_required_user
def appointments():
    user_id = session.get('user_id')
    # Get all appointments for this user
    appointments = user2.get_all_user_appointments(user_id)  
    # appointments should be a list of dicts or tuples with:
    # doctor id, name, date, time, status, meeting link
    return render_template('appointments.html', appointments=appointments)


@app.route('/user_prescriptions')
@login_required_user   # for doctors
def user_prescriptions():
    uid = session.get('user_id')
    prescriptions=user2.user_meds(uid)
    prescriptions = user2.process_meds(prescriptions)
    return render_template('display_meds.html', prescriptions=prescriptions, is_doctor=False)



# docters

@app.route('/manage_appointment',methods=['GET','POST'])
@doclogin_required_user
def manage_appointment():
    doc_id=session.get('doc_id')
    if request.method=='POST':
        action=request.form.get('action')
        booking_id=request.form.get('booking_id')
        meetlink=request.form.get('meetlink',None)

        print("ACTION:", action)
        print("BOOKING_ID:", booking_id)
        print("MEETLINK:", meetlink)

        # validation
        valid_doc_id = user2.validate(booking_id)
        print("VALIDATED DOC_ID:", valid_doc_id)
        if not valid_doc_id or valid_doc_id != doc_id:
            return redirect(url_for('manage_appointment'))
        
        if action=='approve':
            user2.approve(booking_id,'approved')


        elif action=='reject':
            user2.reject(booking_id,'rejected')

        elif action=='meetlink' and meetlink:
            user2.meetlink(booking_id,meetlink)

        elif action=='prescription':
            return redirect(url_for('add_prescription',booking_id=booking_id))
        return redirect(url_for('manage_appointment'))
    
    appointments=user2.doc_view(doc_id)
    return render_template('manage_appoint.html',appointments=appointments)

@app.route('/add_prescription',methods=['GET','POST'])
@doclogin_required_user
def add_prescription():
    did=session.get('doc_id')
    if request.method=='POST':
        booking_id=request.form.get('booking_id')
        symptoms=request.form.get('symptoms')
        medicines=request.form.get('medicines')
        next_visit=request.form.get('next_visit')
        r=user2.get_details(booking_id)

        if not all([booking_id, symptoms, medicines]):
            return redirect(request.url)
        if r:
            user_id=r[0]
            user2.add_meds(booking_id,symptoms,medicines,next_visit,did,user_id)
            return redirect(url_for('view_prescriptions'))

        return redirect(request.url)

    else:
        booking_id = request.args.get('booking_id')
        return render_template('add_prescription.html', booking_id=booking_id)
    

@app.route('/view_prescriptions')
@doclogin_required_user   # for doctors
def view_prescriptions():
    did = session.get('doc_id')
    prescriptions=user2.view_meds(did)
    prescriptions = user2.process_meds(prescriptions)
    return render_template('display_meds.html', prescriptions=prescriptions, is_doctor=True)



