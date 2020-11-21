# !python3

from flask import Flask, request, render_template
import pymysql
import mysqlconnector
import price_update

app = Flask(__name__)

# GLOBAL VARIABLES
USER_ID = ""
CURR_STOCK = ""
USER_NAME = ""

# @app.route('/',methods=['GET','POST']) # decorator: provides additional functionality to an existing function

# def rootpage():
#     if request.method == 'POST' and 'email' in request.form:
#         fname = "'" + request.form.get('fname') + "'"
#         lname = "'" + request.form.get('lname') + "'"
#         phone_number = "'" + request.form.get('phone_number') + "'"
#         email = "'" + request.form.get('email') + "'"
#         mysqlconnector.createNewUser(fname, lname, phone_number, email)
#     return render_template("signup.html")
#     # need to ad logic for checking if user already exists

@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/search', methods=['POST','GET'])
def search():
    unedited_company_name = str(request.form.get('company_name'))
    company_name = "'" + unedited_company_name + "'"

    stock_data = mysqlconnector.GetCompanyPrice(company_name)

    mod_id = int(USER_ID)
    records = mysqlconnector.displayWatchlist(mod_id)

    global CURR_STOCK
    CURR_STOCK = unedited_company_name

    return render_template("profile.html", name = USER_NAME, id_ = USER_ID, company_name = unedited_company_name, stock_data = stock_data, records = records)

@app.route('/insert_watchlist', methods=['POST','GET'])
def insert_watchlist():
    mod_id = int(USER_ID)
    
    mysqlconnector.callProcedureInsert(mod_id,CURR_STOCK)

    records = mysqlconnector.displayWatchlist(USER_ID)

    return render_template("profile.html", name = USER_NAME, id_ = USER_ID, records = records)

@app.route('/delete_watchlist', methods=['POST','GET'])
def delete_watchlist():
    mod_id = int(USER_ID)

    mysqlconnector.callProcedureDelete(mod_id,CURR_STOCK)
    records = mysqlconnector.displayWatchlist(USER_ID)

    return render_template("profile.html", name = USER_NAME, id_ = USER_ID, records = records)

@app.route('/refresh', methods=['POST','GET'])
def refresh():
    mod_id = int(USER_ID)

    records = mysqlconnector.displayWatchlist(USER_ID)
    print(records)

    for record in records:
        print(record)
        price_update.stockPriceUpdate(record[0])
    
    return render_template("profile.html", name = USER_NAME, id_ = USER_ID, records = records)

@app.route('/login',methods=['POST','GET'])
def login():
    email = str(request.form.get('email'))
    email = "'" + email + "'"
    pwd = str(request.form.get('password'))
    pwd = "'" + pwd + "'"

    records = mysqlconnector.checkUserExists(email, pwd)
    
    if len(records) == 0 or records[0][1] == 'None':
        print("invalid password or username")
        return render_template('login.html')
    else:
        global USER_ID
        USER_ID = records[0][0]
        name = records[0][1]

        global USER_NAME
        USER_NAME = name

        mod_id = int(USER_ID)
        records = mysqlconnector.displayWatchlist(mod_id)

        return render_template('profile.html',name = USER_NAME, id_ = USER_ID, records = records)

@app.route('/signup',methods=['POST','GET'])
def signup():
    if len(request.form.get('fname')) > 0:
        fname = "'" + str(request.form.get('fname')) + "'"
        fname = "'" + fname + "'"
        lname = "'" + str(request.form.get('lname')) + "'"
        lname = "'" + lname + "'"
        phone_number = "'" + str(request.form.get('phone_number')) + "'"
        phone_number = "'" + phone_number + "'"
        email = str(request.form.get('email'))
        email = "'" + email + "'"
        pwd = "'" + str(request.form.get('password')) + "'"
        pwd = "'" + pwd + "'"

        records = mysqlconnector.checkUserExists(email, pwd)

        if temp == 0:
            return render_template('profile.html',name = email)
        else:
            return render_template('profile.html',name = email)

if __name__ == '__main__':
    app.run()