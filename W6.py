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

mycursor.execute("SELECT * FROM member; ")
result = mycursor.fetchall()
# for x in result:
#     print(x)
# mycursor.close()
# mydb.close()


@app.route("/")
def index():
    return render_template("W6.html")


@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    accountName = request.form["accountName"]
    password = request.form["password"]
    print(username, accountName, password)

    # 檢查帳號
    mycursor.execute(
        f'SELECT * FROM member WHERE username = "{username}"; '
    )
    myresult = mycursor.fetchall()
    # for x in myresult:
    #     print(x)

    if not myresult:
        mycursor.execute(
            f'''INSERT INTO member (username,accountName,password) VALUES("{username}","{accountName}","{password}");'''
        )
        mydb.commit()
        return redirect("/")

    else:
        return redirect("/error?message=帳號已經被註冊")


@app.route("/member")
def index_member():
    if session.get(IS_LOGIN, None):
        return render_template("member.html")

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
    mycursor.execute(
        f'SELECT * FROM member WHERE accountName = "{accountName}" AND password = "{password}"; '
    )
    myresult = mycursor.fetchall()
    # for x in myresult:
    #     print(x)

    if myresult:
        session[IS_LOGIN] = True
        mycursor.execute(
            f'SELECT username FROM member where accountname="{request.form["accountName"]}";'
        )
        Theusername = mycursor.fetchall()[0][0]

        # for x in Theusername:
        #     print(x)  # 印出test
        # print(Theusername)

        # session["username"] = Theusername
        # print(Theusername)

        return render_template("member.html", Hello=Theusername)

    if not myresult:
        return redirect("/error?message=帳號、或密碼輸入錯誤")


app.run(debug=True, port=3000)

# python W6.py
