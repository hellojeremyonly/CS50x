import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_id = session["user_id"]

    transactions = db.execute(
        "SELECT symbol, name, SUM(shares) AS shares, price FROM transactions WHERE user_id = (?) GROUP BY symbol HAVING SUM(shares) > 0;", user_id)
    cash = db.execute("SELECT cash FROM users WHERE id = (?);", user_id)

    totalcash = cash[0]["cash"]
    sum = int(totalcash)

    for row in transactions:
        look = lookup(row["symbol"])
        row["price"] = look["price"]
        row["total"] = row["price"] * row["shares"]
        sum += row["total"]

    return render_template("index.html", database=transactions, users=cash, sum=sum)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        buy = lookup(request.form.get("symbol"))

        if buy == None:
            return apology("Invalid Symbol")


        user_id = session["user_id"]
        name = buy["name"]
        price = buy["price"]
        shares = request.form.get("shares")
        symbol = request.form.get("symbol")

        if not shares.isdigit():
            return apology("You cannot purchase partial shares")

        shares = int(shares)
        if shares <= 0:
            return apology("Share amount not allowed")

        cash_db = db.execute("SELECT cash FROM users where id = (?)", user_id)
        user_cash = (cash_db[0]["cash"])
        purchase = price * shares
        update_user_cash = user_cash - purchase

        if user_cash < purchase:
            return apology("Insufficient fund in your account")

        db.execute("UPDATE users SET cash = (?) WHERE id = (?);", update_user_cash, user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price) VALUES (?, ?, ?, ?, ?)",
                   user_id, symbol, name, shares, price)
        flash("Bought!")
        return redirect("/")

    return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    transactions = db.execute("SELECT symbol, name, shares, price, Timestamp FROM transactions WHERE user_id = :user_id", user_id=user_id)

    for row in transactions:
        if row["shares"] <= 0:
            row["buy_sell"] = "SELL"
        else:
            row["buy_sell"] = "BUY"

    return render_template("history.html", database=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = :username", username=request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
def quote():
    """Get stock quote."""
    if request.method == "POST":
        quoted = lookup(request.form.get("symbol"))

        if quoted == None:
            return apology("Quote symbol doesn't exist")

        return render_template("quoted.html", quoted=quoted)

    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if request.method == "POST":
        # Ensure username was submitted
        if not username:
            return apology("Must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("Must provide password", 400)

        elif password != confirmation:
            return apology("Password do not match!", 400)

        # Query database for username
        try:
            db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=username, hash=generate_password_hash(password))
        except:
            return apology("Username is taken, please try another username", 400)

        flash("Registered Successful!")
        # Redirect user to home page
        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "GET":
        symbols = db.execute("SELECT symbol FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING SUM(shares) > 0", user_id=user_id)
        return render_template("sell.html", symbols=symbols)

    if request.method == "POST":
        sell = lookup(request.form.get("symbol"))
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        name = sell["name"]
        price = sell["price"]

        if shares <= 0:
            return apology("Share amount not allowed")

        if symbol is None:
            return apology("Invalid Symbol")

        user_cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=user_id)[0]["cash"]

        oldshares = db.execute("SELECT SUM(shares) AS shares FROM transactions WHERE user_id = :user_id AND symbol = :symbol", user_id=user_id, symbol=symbol)[0]["shares"]
        no_old_shares = oldshares if oldshares is not None else 0

        sold = price * shares
        update_user_cash = user_cash + sold

        if shares > no_old_shares:
            return apology("Insufficient share units in your account")

        db.execute("UPDATE users SET cash = :cash WHERE id = :user_id", cash=update_user_cash, user_id=user_id)
        db.execute("INSERT INTO transactions (user_id, symbol, name, shares, price) VALUES (:user_id, :symbol, :name, :shares, :price)",
                   user_id=user_id, symbol=symbol, name=name, shares=-shares, price=price)

        flash("Sold!")
        return redirect("/")
