# from flask import Flask

# app = Flask(__name__) 
# @app.route('/')
# def home(): 
#     return "Hello, Flask!"
# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask,redirect,url_for 

app=Flask(__name__) # to create an insatnce for app

@app.route('/')   # creating route for the web
def home():
	return "hello Moto!"
	
@app.route("/<name>") # this name goes to function parameter
def user(name):
	return f"hello {name}"

@app.route("/admin") #here its for redirecting it to other page like 
def admin():
	return redirect(url_for("home"))   


if __name__=="__main__":
	app.run(debug=True)


