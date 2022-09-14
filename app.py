from flask import Flask, render_template, request ,url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///product_inventory.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class location(db.Model):
    l_id = db.Column(db.Integer, primary_key = True)
    city = db.Column(db.String(50), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __init__(self, city):
        self.city = city

class product(db.Model):
    proId = db.Column(db.Integer, primary_key = True)
    pname = db.Column(db.String(50), nullable = False)
    price = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String(50), nullable = False)

    def __init__(self, pname, price, description):
        self.pname = pname
        self.price = price
        self.description = description

@app.route('/')
def product_home():
    allproduct = product.query.all()
    allocation = location.query.all()
    return render_template('product_home.html', allproduct=allproduct, allocation=allocation)


@app.route('/location')
def locations():
    return render_template('addlocation.html')

@app.route('/addproducts', methods=['GET', 'POST'])
def products():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        pro = product(pname=name, price=price, description=description)
        db.session.add(pro)
        db.session.commit()
        allproduct = product.query.all()
        return redirect(url_for('product_home'))
    return render_template('addproduct.html')

@app.route('/updateproduct/<int:pid>', methods=['GET', 'POST'])
def updateproduct(pid):
    prod = product.query.filter_by(proId=pid).first()
    print(prod)
    return render_template('updateproduct.html', prod=prod)

@app.route('/updateproduct1/', methods=['GET', 'POST'])
def updateproduct1():
    if request.method == 'POST':
        proId = (int)(request.form['pid'])
        print(proId)
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']

        prod = product.query.filter_by(proId=proId).first()

        # prod = product.query.get(proId)
        print(prod)
        prod.pname = name
        prod.price = price
        prod.description = description

        db.session.commit()

        # pro = product(pname=name, price=price, description=description)
        # db.session.add(pro)
        # db.session.commit()
        # allproduct = product.query.all()
    return redirect(url_for('product_home'))

@app.route('/deleteproduct/<int:pid>', methods=['GET', 'POST'])
def deleteproduct(pid):
    del_pro = product.query.filter_by(proId=pid).first()
    db.session.delete(del_pro)
    db.session.commit()
    return redirect(url_for('product_home'))

if __name__ == "__main__":
    app.run(debug=True, port=8000)