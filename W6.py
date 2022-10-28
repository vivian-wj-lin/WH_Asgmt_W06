from flask import Flask, render_template, request, redirect, session
import mysql.connector
import mysql.connector.cursor

app = Flask(
    __name__,
    static_folder="public",
    static_url_path="/"
)

app.secret_key = "secret"

IS_LOGIN = "isLogin..."

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="mysqlpwd2022",
    database="mysql"
)

mycursor = mydb.cursor()
mycursor.execute("CREATE DATABASE IF NOT EXISTS week6")
mydb.commit()
mycursor.close()
mydb.close()

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="mysqlpwd2022",
    database="week6"
)
mycursor = mydb.cursor()
mycursor.execute(
    '''
    CREATE Table IF NOT EXISTS member
    (
        username varchar(20) not null,
        accountName varchar(20) not null,
        password char(20) not null
    );
    '''
)
mydb.commit()


@app.route("/")
def index():
    return render_template("W6.html")


@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    accountName = request.form["accountName"]
    password = request.form["password"]

    # 檢查帳號
    mycursor = mydb.cursor()
    select_stmt = "SELECT * FROM member WHERE username = %(username)s"
    mycursor.execute(select_stmt, {'username': username})
    myresult = mycursor.fetchall()

    if not myresult:
        mycursor = mydb.cursor()
        sql = "INSERT INTO member (username,accountName,password) VALUES (%s, %s, %s)"
        val = [(username, accountName, password)]
        mycursor.executemany(sql, val)
        mydb.commit()
        return redirect("/")

    else:
        return redirect("/error?message=帳號已經被註冊")


@app.route("/member")
def index_member():
    if session.get(IS_LOGIN, None):
        return render_template("member.html", Hello=session['username'])
    return redirect("/")


@app.route("/signout")
def signout():
    session[IS_LOGIN] = False  # 設定登出為 False
    return redirect("/")


@app.route("/error")
def index_error():
    message = request.args.get("message")
    return render_template("signInFailure.html", reason=message)


@app.route("/signin", methods=["POST"])
def signin():
    accountName = request.form["accountName"]
    password = request.form["password"]
    if (accountName == "" or password == ""):
        return redirect("/error?message=請輸入帳號、密碼")
    mycursor = mydb.cursor()
    mycursor.execute(
        "SELECT username FROM member WHERE accountName = %s AND password = %s", (accountName, password))
    myresult = mycursor.fetchall()[0][0]  # username

    if myresult:
        session[IS_LOGIN] = True
        session["username"] = myresult
        return redirect("/member")

    if not myresult:
        return redirect("/error?message=帳號、或密碼輸入錯誤")


app.run(debug=True, port=3000)

# python W6.py
