import os

from flask import render_template, request, redirect,  url_for
from flask_bcrypt import Bcrypt
from flask_cors import CORS

from models import *
import click
from flask.cli import FlaskGroup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Configuration.SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)
db.init_app(app)

CORS(app)


ma = Marshmallow(app)
bcrypt = Bcrypt(app)


@click.group(cls=FlaskGroup, create_app=lambda: app)
def cli():
    """Management script for the flask application."""


@cli.command('init_db')
def init_db():
    # Initialize tables
    db.create_all()
    db.session.commit()
    print("Tables Created")


@cli.command('drop_db')
def delete_db():
    with app.app_context():
        db.drop_all()
    print("Tables dropped")


def verifyCC(cc):
    if len(cc) == 12 and cc[7] == cc[11] and ' ' not in cc:
        x = True
    else:
        x = False
    return x







@app.route("/", methods=["POST"])
def  index():
    message = ""
    payload = request.get_json()
    username = payload.get('username')
    password = payload.get('password')
    try:
        if username != "" and password != "" and Account.query.filter_by(username=username).first() == None  :
            password = bcrypt.generate_password_hash(password)
            account = Account(username=username, password=password)
            db.session.add(account)
            db.session.commit()
            message = "Account Created"
            return message
        elif Account.query.filter_by(username=username).first() != None:
            message = "User already exists"
            return message
        else:
            message = "Invalid input details"
            return message
    except Exception as e:
            return message



@app.route("/signin", methods=["POST"])
def signin():
    logged = ""
    payload = request.get_json()
    username = payload.get('username')
    password = payload.get('password')
    account = Account.query.filter_by(username=username).first()
    if account == None:
        logged = "0"
        return logged
    else:
        if bcrypt.check_password_hash(account.password, password):
            loggedinaccount = loggedin(username=account.username)
            db.session.add(loggedinaccount)
            db.session.commit()
            logged = account.password
            return logged
        else:
            logged = "0"
            return logged
    return logged

@app.route("/logout", methods=["POST"])
def logout():
    payload = request.get_json()
    logged = payload.get('logged')
    accountlogged = loggedin.query.filter_by(account_id="1").first()
    db.session.delete(accountlogged)
    db.session.commit()
    return logged


@app.route("/sell", methods=["GET", "POST"])
def sell():
    message = ""
    if loggedin.query.filter_by(account_id="1").first() is  None:
        return {redirect("/")}
    else:
        accountloggedin = loggedin.query.filter_by(account_id=1).first()

        if request.form:
            if request.form.get("name") != "" and request.form.get("price") != "":
                item = Item(name=request.form.get("name"), price=request.form.get("price"), link=request.form.get("link"), seller_name= accountloggedin.username)
                db.session.add(item)
                db.session.commit()
                message = "item successfully posted"
            else:
                message = "Invalid item details"

    return render_template("sell.html", message = message )


@app.route("/items", methods=["GET"])
def items_to_sell():
    account = loggedin.query.filter_by(account_id=1).first()
    items = Item.query.filter(Item.seller_name != account.username).all()
    schema = DetailedUserSchema(many=True)
    response = schema.jsonify(items)
    return response


@app.route("/boughtitem", methods=["POST"])
def item_to_be_bought():
    payload = request.get_json()
    bought_item_id = payload.get('id_item')
    bought_item = Item.query.filter_by(item_id=bought_item_id).first()
    schema = DetailedUserSchema()
    response = schema.jsonify(bought_item)
    return response

@app.route("/buy", methods=["POST"])
def buy():
    payload = request.get_json()
    bought_id = payload.get('bought_id')
    cc = payload.get('cc')
    bought = bought_id
    return {'Location': url_for('.hello_id', bought_id=bought, cc=cc)}


@app.route("/buyitem/<int:bought_id>", methods=["GET"])
def hello_id(bought_id, cc):
    message = ""
    bought_item = Item.query.filter_by(item_id= bought_id).first()
    accountloggedin = loggedin.query.filter_by(account_id=1).first()
    if verifyCC(cc) == True:
        toHistory = History(name=bought_item.name, price = bought_item.price, seller_name=bought_item.seller_name, link=bought_item.link, buyer_name=accountloggedin.username )
        db.session.add(toHistory)
        db.session.delete(bought_item)
        db.session.commit()
        message = ""
        return message
    else:
        message = "Error buying item"
        return message
    return message


@app.route("/edit", methods=["GET", "POST"])
def edit():
    if loggedin.query.filter_by(account_id="1").first() is  None:
        return redirect("/")
    else:
        accountloggedin = loggedin.query.filter_by(account_id=1).first()
        message = ""
        if request.form:
            if request.form.get("newname") != "" and request.form.get("newprice") != "":
                item_id = request.form.get("item_id")

                newname = request.form.get("newname")
                item = Item.query.filter_by(item_id=item_id).first()
                item.name = newname

                newprice = request.form.get("newprice")
                item = Item.query.filter_by(item_id=item_id).first()
                item.price = newprice

                newlink = request.form.get("newlink")
                item = Item.query.filter_by(item_id=item_id).first()
                item.link = newlink

                db.session.commit()
                message = "Item successfully updated"
            else:
                message = "Failed to Edit item"

    items = Item.query.filter_by(seller_name=accountloggedin.username).all()
    return render_template("edit.html", items=items, message=message)


@app.route("/delete", methods=["POST"])
def delete():
    item_id = request.form.get("item_id")
    item = Item.query.filter_by(item_id=item_id).first()
    db.session.delete(item)

    db.session.commit()
    return redirect("/edit")


@app.route("/history", methods=["GET"])
def history():
    if loggedin.query.filter_by(account_id="1").first() is  None:
        return redirect("/")
    else:
        accountloggedin = loggedin.query.first()
        history = History.query.filter((History.buyer_name == accountloggedin.username) | (History.seller_name == accountloggedin.username)).all()

    return render_template("history.html", history=history)


if __name__ == '__main__':
    cli()