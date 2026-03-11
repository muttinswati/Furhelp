import db_connection
import pymysql

def get_doc(location):
    conn = db_connection.get_db_connection()
    mycursor = conn.cursor()
    sql='''select fname,lname,city,address,pnor,did from docters where city=%s'''
    mycursor.execute(sql,(location,))
    r=mycursor.fetchall()
    conn.close()
    # if not r:
    #     return 'No docters availble for the city'
    # conn.commit()
    
    return r or []


def check_booking(doc_id,appt_date,appt_time):
    conn = db_connection.get_db_connection()
    mycursor = conn.cursor()
    sql='''select doc_id,time,date from bookings where doc_id=%s and time=%s and date=%s'''
    mycursor.execute(sql,(doc_id,appt_time,appt_date))
    r=mycursor.fetchone()
    conn.close() 
    return r

def add_doc(doc_id,user_id,appt_time,appt_date):
    conn = db_connection.get_db_connection()
    mycursor = conn.cursor()
    sql='''insert into bookings(doc_id,ur_id,time,date)values(%s,%s, %s,%s)'''
    mycursor.execute(sql,(doc_id,user_id,appt_time,appt_date))
    conn.commit()
    conn.close()    

def view_apt(user_id, doc_id, appt_date):
    conn = db_connection.get_db_connection()
    cursor = conn.cursor()
    sql = """
        SELECT d.fname, d.lname, d.pnor, d.address, b.status, b.meetlink,b.booking_id
        FROM bookings b
        JOIN docters d ON b.doc_id = d.did
        WHERE b.doc_id = %s AND b.ur_id = %s AND b.date = %s
    """
    cursor.execute(sql, (doc_id, user_id, appt_date))
    result = cursor.fetchone()
    conn.close()
    return result


# user2.py
def calculate_pet_health(name, weight, height, water, activity):
    # Adjusted BMI calculation (scaled up for pets)
    bmi = round((weight / (height ** 2)) * 5, 2)

    # BMI category thresholds tuned for pets
    if bmi < 20:
        bmi_cat = "Underweight"
    elif bmi < 40:
        bmi_cat = "Healthy"
    elif bmi < 60:
        bmi_cat = "Overweight"
    else:
        bmi_cat = "Obese"

    # Hydration score (ideal: 50ml/kg/day)
    hydration = min(round((water / (weight * 50)) * 100, 2), 100)

    # Activity score (scaled 0–100)
    activity_score = min(activity * 10, 100)

    # Overall health score (balance)
    bmi_factor = max(0, 100 - abs(40 - bmi) * 2)
    overall = round((hydration + activity_score + bmi_factor) / 3, 2)

    return {
        'name': name,
        'bmi': bmi,
        'bmi_cat': bmi_cat,
        'hydration': hydration,
        'activity': activity_score,
        'overall': overall
    }


# docters queries 
def doc_view(doc_id):
    conn = db_connection.get_db_connection()
    mycursor = conn.cursor()
    sql='''select u.fname, u.lname, u.pnor, b.time, b.date, b.meetlink, b.status,b.booking_id
    from bookings b 
    join users u on b.ur_id=u.uid
    where doc_id=%s'''
    mycursor.execute(sql,(doc_id,))
    r=mycursor.fetchall()
    conn.close()
    return r


def approve(booking_id,status):
    conn = db_connection.get_db_connection()
    mycursor = conn.cursor()
    sql='''update bookings set status=%s where booking_id=%s'''
    mycursor.execute(sql,(status,booking_id))
    conn.commit()
    conn.close()
    

def reject(booking_id,status):
    conn = db_connection.get_db_connection()
    mycursor = conn.cursor()
    sql='''update bookings set status=%s where booking_id=%s'''
    mycursor.execute(sql,(status,booking_id))
    conn.commit()
    conn.close()
    

def meetlink(booking_id,meetlink):
    conn = db_connection.get_db_connection()
    mycursor = conn.cursor()
    sql='''update bookings set meetlink=%s where booking_id=%s'''
    mycursor.execute(sql,(meetlink,booking_id))
    conn.commit()
    conn.close()
    
def validate(booking_id):
    conn = db_connection.get_db_connection()
    mycursor = conn.cursor()
    sql = '''SELECT doc_id FROM bookings WHERE booking_id=%s'''
    mycursor.execute(sql, (booking_id,))
    r = mycursor.fetchone()
    conn.close()
    if r:
        return r[0]  # returns doc_id
    return None

# prescription

def get_details(booking_id):
    conn = db_connection.get_db_connection()
    mycursor = conn.cursor()
    sql = '''SELECT ur_id,doc_id FROM bookings WHERE booking_id=%s'''
    mycursor.execute(sql, (booking_id,))
    r = mycursor.fetchone()
    conn.close()
    return r

def add_meds(booking_id,symptoms,medicines,next_visit,did,user_id):
    conn = db_connection.get_db_connection()
    mycursor = conn.cursor()
    sql = '''INSERT INTO prescriptions(usr_id,bid,doctor_id,symptoms,medicines,next_visit) VALUES(%s,%s,%s,%s,%s,%s)'''
    mycursor.execute(sql, (user_id,booking_id,did,symptoms,medicines,next_visit))
    conn.commit()
    print('inserted sucessfully')
    conn.close()

def process_meds(prescriptions):
    for p in prescriptions:
        p['structured_meds'] = []
        meds_text = p.get('medicines', '')
        # Normalize line breaks (\r\n -> \n) and split
        lines = [line.strip() for line in meds_text.replace('\r\n','\n').replace(';','\n').split('\n') if line.strip()]
        for med in lines:
            try:
                name_dosage, rest = med.split('#')
                name, dosage = name_dosage.split('-')
                days, rest2 = rest.split('@')
                time, instruction = rest2.split('!')
                p['structured_meds'].append({
                    "name": name,
                    "dosage": dosage,
                    "days": days,
                    "time": time,
                    "instruction": instruction
                })
            except ValueError:
                # fallback for malformed line
                p['structured_meds'].append({
                    "name": med,
                    "dosage": '',
                    "days": '',
                    "time": '',
                    "instruction": ''
                })
    return prescriptions


def user_meds(uid):
    conn = db_connection.get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT p.*, u.fname as user_name, d.fname as doctor_name, d.pnor as doctor_phone
        FROM prescriptions p
        JOIN users u ON p.usr_id = u.uid
        JOIN docters d ON p.doctor_id = d.did
        WHERE p.usr_id=%s
        ORDER BY p.uploaded_on DESC
    """, (uid,))
    r = cursor.fetchall()
    conn.close()
    return r

def view_meds(did):
    conn = db_connection.get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("""
        SELECT p.*, u.fname as user_name, d.fname as doctor_name, d.pnor as doctor_phone
        FROM prescriptions p
        JOIN users u ON p.usr_id = u.uid
        JOIN docters d ON p.doctor_id = d.did
        WHERE p.doctor_id=%s
        ORDER BY p.uploaded_on DESC
    """, (did,))
    r = cursor.fetchall()
    conn.close()
    return r

if __name__=='__main__':
    pass
