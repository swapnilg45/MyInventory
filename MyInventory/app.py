from flask import Flask,render_template,request,redirect,url_for,flash
from models import db, Product, Location, ProductMovement
from forms import AddProductForm, LocationForm, MoveProductForm
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:swapnilg45@localhost:3307/myinventory'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)
app.config['SECRET_KEY'] = 'swapnilBhai'



@app.route('/home')
def home():
    return render_template('base.html')

@app.route('/products')
def products():
    product =  Product.query.all()
    return render_template('products.html',product=product)

@app.route('/location')
def location():
    location = Location.query.all()
    return render_template('location.html', location=location)

@app.route('/',methods = ['GET','POST'])
def add_product():
    form = AddProductForm()
    if form.validate_on_submit():
        product_id = form.product_id.data
        name = form.name.data
        qty=form.qty.data
        new_product = Product(product_id=product_id,name=name,qty=qty)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added successfully!', 'success')
        return redirect(url_for('products'))
    return render_template('add_product.html', form=form)

@app.route('/add_location', methods=['GET', 'POST'])
def add_location():
    form = LocationForm()
    if form.validate_on_submit():
        location_id = form.location_id.data
        name = form.name.data
        new_location = Location(location_id=location_id, name=name)
        db.session.add(new_location)
        db.session.commit()
        flash('Location added successfully!', 'success')
        return redirect(url_for('add_location'))  
    return render_template('add_location.html', form=form)

@app.route('/edit_location/<int:id>', methods=['GET', 'POST'])
def edit_location(id):
    location = Location.query.get_or_404(id)
    form = LocationForm()
    if form.validate_on_submit():
        location.location_id = form.location_id.data
        location.name = form.name.data
        db.session.commit()
        flash('Location updated successfully!', 'success')
        return redirect(url_for('location'))
    elif request.method == 'GET':
        form.location_id.data = location.location_id
        form.name.data = location.name
    return render_template('edit_location.html', form=form)

@app.route('/edit_product/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = AddProductForm()
    if form.validate_on_submit():
        product.product_id = form.product_id.data
        product.name = form.name.data
        product.qty=form.qty.data
        db.session.commit()
        flash('Product updated successfully!', 'success')
        return redirect(url_for('products'))
    elif request.method == 'GET':
        form.product_id.data = product.product_id
        form.name.data = product.name
    return render_template('edit_Product.html', form=form)

@app.route('/move_product', methods=['GET', 'POST'])
def move_product():
    form = MoveProductForm()
    form.product_id.choices = [(p.product_id, p.name) for p in Product.query.all()]
    form.from_location.choices.extend([(l.location_id, l.name) for l in Location.query.all()])
    form.to_location.choices.extend([(l.location_id, l.name) for l in Location.query.all()])
    
    if form.validate_on_submit():
        product_id = form.product_id.data
        from_location = form.from_location.data if form.from_location.data else None
        to_location = form.to_location.data if form.to_location.data else None
        qty = form.qty.data

        # Check for enough quantity in from_location if applicable
        if from_location:
            total_qty_in_from = db.session.query(
                db.func.sum(ProductMovement.qty)
            ).filter_by(product_id=product_id, to_location=from_location).scalar() or 0
            total_qty_out_from = db.session.query(
                db.func.sum(ProductMovement.qty)
            ).filter_by(product_id=product_id, from_location=from_location).scalar() or 0

            if total_qty_in_from - total_qty_out_from < qty:
                flash('Not enough quantity in the from location', 'danger')
                return redirect(url_for('move_product'))
        
        movement = ProductMovement(
            timestamp=datetime.now(),
            from_location=from_location,
            to_location=to_location,
            product_id=product_id,
            qty=qty
        )
        db.session.add(movement)
        db.session.commit()
        flash('Product moved successfully!', 'success')
        return redirect(url_for('move_product'))
    
    return render_template('move_product.html', form=form)

@app.route('/report')
def report():
    balances = db.session.query(
        Product.name.label('product_name'),
        Location.name.label('location_name'),
        db.func.sum(ProductMovement.qty).label('quantity')
    ).join(ProductMovement, Product.product_id == ProductMovement.product_id)\
     .join(Location, Location.location_id == ProductMovement.to_location)\
     .group_by(Product.name, Location.name)\
     .all()

    return render_template('report.html', balances=balances)

@app.route('/balance_report')
def balance_report():
    balances = db.session.query(
        Product.name.label('product_name'),
        Location.name.label('location_name'),
        (db.func.sum(
            db.case(
                (ProductMovement.to_location == Location.location_id, ProductMovement.qty), 
                else_=0
            )
        ) - db.func.sum(
            db.case(
                (ProductMovement.from_location == Location.location_id, ProductMovement.qty), 
                else_=0
            )
        )).label('quantity')
    ).join(ProductMovement, Product.product_id == ProductMovement.product_id)\
     .join(Location, db.or_(
        Location.location_id == ProductMovement.to_location, 
        Location.location_id == ProductMovement.from_location)
     )\
     .group_by(Product.name, Location.name)\
     .all()

    return render_template('balance_report.html', balances=balances)

@app.route('/movements')
def movements():
    # Query to get the product movements
    movements = db.session.query(
        ProductMovement.movement_id,
        Product.name.label('product_name'),
        db.session.query(Location.name).filter(Location.location_id == ProductMovement.from_location).label('from_location'),
        db.session.query(Location.name).filter(Location.location_id == ProductMovement.to_location).label('to_location'),
        ProductMovement.qty,
        ProductMovement.timestamp
    ).join(Product, Product.product_id == ProductMovement.product_id)\
     .all()
    
    return render_template('movements.html', movements=movements)





if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)