# !python3

from flask import Flask, request, render_template, redirect, url_for, session
import pymysql
import mysqlconnector
import price_update
import secrets

app = Flask(__name__)
token = secrets.token_urlsafe(16)
app.config["SECRET_KEY"] = token

# GLOBAL VARIABLES
CURR_STOCK = ""

@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/login',methods=['POST','GET'])
def login():
    email_ = str(request.form.get('email'))
    pwd_ = str(request.form.get('password'))

    email = "'" + email_ + "'"
    pwd = "'" + pwd_ + "'"

    records = mysqlconnector.authorizeUser(email, pwd)

    if len(records) == 0 or email_ == 'None':
        print("invalid password or username")
        return render_template('login.html')
    else:
        session["USER_NAME"] = records[0][1]
        session["USER_ID"] = records[0][0]

        if not session.get("USER_NAME") is None:
            records = mysqlconnector.displayWatchlist(int(session["USER_ID"]))
            return render_template('profile.html', name = session["USER_NAME"], records = records)
        else:
            print("No username found in session")
            return redirect(url_for("login"))
    
@app.route('/signup',methods=['POST','GET'])
def signup():
    fname = str(request.form.get('fname'))
    lname = str(request.form.get('lname'))
    phone_number = str(request.form.get('phone_number'))
    email = str(request.form.get('email'))
    pwd = str(request.form.get('password'))

    fname = "'" + fname + "'"
    lname = "'" + lname + "'"
    phone_number = "'" + phone_number + "'"
    email = "'" + email + "'"
    pwd = "'" + pwd + "'"

    records = mysqlconnector.checkUserExists(email)

    if len(records) != 0 or email == 'None':
        print("already esisting account")
        return render_template('signup.html')
    else:
        mysqlconnector.createNewUser(fname, lname, phone_number, email, pwd)
        records = mysqlconnector.authorizeUser(email, pwd)

        session["USER_NAME"] = records[0][1]
        session["USER_ID"] = records[0][0]

        records = mysqlconnector.displayWatchlist(int(session["USER_ID"]))

        return render_template('profile.html',name = session["USER_NAME"], records = records)

@app.route('/search', methods=['POST','GET'])
def search():
    global CURR_STOCK
    CURR_STOCK = str(request.form.get('company_name'))

    query_company_name = "'" + CURR_STOCK + "'"

    stock_data = mysqlconnector.GetCompanyPrice(query_company_name)

    records = mysqlconnector.displayWatchlist(int(session["USER_ID"]))

    return render_template("profile.html", name = session["USER_NAME"], company_name = CURR_STOCK, stock_data = stock_data, records = records)

@app.route('/insert_watchlist', methods=['POST','GET'])
def insert_watchlist():
    mysqlconnector.callProcedureInsert(int(session["USER_ID"]),CURR_STOCK)

    records = mysqlconnector.displayWatchlist(session["USER_ID"])

    return render_template("profile.html", name = session["USER_NAME"], records = records)

@app.route('/delete_watchlist', methods=['POST','GET'])
def delete_watchlist():
    mysqlconnector.callProcedureDelete(int(session["USER_ID"]),CURR_STOCK)

    records = mysqlconnector.displayWatchlist(session["USER_ID"])

    return render_template("profile.html", name = session["USER_NAME"], records = records)

@app.route('/refresh', methods=['POST','GET'])
def refresh():
    records = mysqlconnector.displayWatchlist(session["USER_ID"])

    for record in records:
        price_update.stockPriceUpdate(record[0])
    
    return render_template("profile.html", name = session["USER_NAME"], records = records)

@app.route('/create_portfolio', methods=['POST','GET'])
def create_portfolio():
    # records = mysqlconnector.displayWatchlist(session["USER_ID"])

    # for record in records:
    #     price_update.stockPriceUpdate(record[0])

    # we get input from customer when they submit the form 
    # we want to add the result to the portfolio table
    # we want to store that info into an array and pass it back when rendering
    
    return render_template("portfolio.html", name = session["USER_NAME"])

@app.route("/sign-out")
def sign_out():
    global CURR_STOCK
    CURR_STOCK = ""

    session.pop("USER_NAME", None)
    session.pop("USER_ID", None)
    print(session)

    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run()
