from . import db
from flask import render_template, Blueprint, request
from flask_login import current_user, login_required
from .models import Product, User
from flask import redirect, url_for, flash
import stripe

routes = Blueprint("routes", __name__)

stripe.api_key = 'sk_test_51OpBytCm3Ol5Jv5CM6UbwIqpraPgR0GY5uQgy5pG4LY78CikYOBJkKpMQzh9yahGp91oEa2PXHa2sJaZK5S6uazN00r1sgl7Tq'

@routes.route('/')
def home():
    return render_template("home.html", user = current_user)

@routes.route('/buy_creatine', methods=['POST','GET'])
def creatine():
    name = 'Creatine Monohydrate 300g'
    price = '19.99$'
    quantity = request.form.get('quantity')
    if request.method == 'POST':
        existing_product = Product.query.filter_by(user_id=current_user.id, name=name).first()
        if existing_product:
            existing_product.quantity += int(quantity)
            db.session.commit()
        else:
            buy_product(name, quantity, price)
        try:
            flash('Creatine Monohydrate 300g added to cart.')
        except Exception:
            flash('error')

    return render_template("creatine.html", user = current_user)

@routes.route('/buy_dumbbells', methods=['POST','GET'])
def dumbbells():
    name = 'Adjustable Dumbbells 10KG'
    price = '30.99$'
    quantity = request.form.get('quantity')
    if request.method == 'POST':
        existing_product = Product.query.filter_by(user_id=current_user.id, name=name).first()
        if existing_product:
            existing_product.quantity += int(quantity)
            db.session.commit()
        else:
            buy_product(name, quantity, price)
        try:
            flash('Adjustable Dumbbells 10KG added to cart.')
        except Exception:
            flash('error')

    return render_template("dumbbells.html", user = current_user)

@routes.route('/buy_gloves', methods=['POST','GET'])
def gloves():
    name = 'Boxing Gloves 12oz'
    price = '9.99$'
    quantity = request.form.get('quantity')
    if request.method == 'POST':
        existing_product = Product.query.filter_by(user_id=current_user.id, name=name).first()
        if existing_product:
            existing_product.quantity += int(quantity)
            db.session.commit()
        else:
            buy_product(name, quantity, price)
        try:
            flash('Boxing Gloves 12oz added to cart.')
        except Exception:
            flash('error')
            
    return render_template("boxing_gloves.html", user = current_user)

@routes.route('/buy_shirt', methods=['POST','GET'])
def shirt():
    name = 'Gym Spandex T-shirt'
    price = '25.89$'
    quantity = request.form.get('quantity')
    if request.method == 'POST':
        existing_product = Product.query.filter_by(user_id=current_user.id, name=name).first()
        if existing_product:
            existing_product.quantity += int(quantity)
            db.session.commit()
        else:
            buy_product(name, quantity, price)
        try:
            flash('Gym Spandex T-shirt added to cart.')
        except Exception:
            flash('error')

    return render_template("shirt.html", user = current_user)

@routes.route('/buy_whey', methods=['POST','GET'])
def whey():
    name = 'Whey Protein Powder 5kg'
    price = '40.69$'
    quantity = request.form.get('quantity')
    if request.method == 'POST':
        existing_product = Product.query.filter_by(user_id=current_user.id, name=name).first()
        if existing_product:
            existing_product.quantity += int(quantity)
            db.session.commit()
        else:
            buy_product(name, quantity, price)
        try:
            flash('Whey Protein Powder 5kg added to cart.')
        except Exception:
            flash('error')
    
    return render_template("whey.html", user = current_user)

@routes.route('/buy_drink', methods=['POST','GET'])
def drink():
    name = 'Eletrolyte Hydration Drink 16oz'
    price = '3.99$'
    quantity = request.form.get('quantity')
    if request.method == 'POST':
        existing_product = Product.query.filter_by(user_id=current_user.id, name=name).first()
        if existing_product:
            existing_product.quantity += int(quantity)
            db.session.commit()
        else:
            buy_product(name, quantity, price)
        try:
            flash('Eletrolyte Hydration Drink 16oz added to cart.')
        except Exception:
            flash('error')


    return render_template("drink.html", user = current_user)


@routes.route('/my_cart')
@login_required
def cart():
    cart = Product.query.filter_by(user_id = current_user.id).all()
    total = 0
    for product in cart:
        product.image_path = url_for('static', filename=f"{product.name}.webp")
        total += float(product.price[:-1])*int(product.quantity)
    total = round(total, 2)
    return render_template("my_cart.html", user=current_user, cart=cart, total=total)


@routes.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    product_id = request.form.get('product_id')
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect('/my_cart')


def buy_product(name, quantity, price):
    product = Product(name=name, price=price, quantity=quantity, user_id=current_user.id)
    db.session.add(product)
    db.session.commit()

@routes.route('/process_payment', methods=['POST'])
def process_payment():
    cart = Product.query.filter_by(user_id=current_user.id).all()
    line_items = []
    for product in cart:

        if product.name == 'Creatine Monohydrate 300g':
            stripe_price = 'price_1OpDReCm3Ol5Jv5C9AOxGWPj'
        elif product.name == 'Adjustable Dumbbells 10KG':
            stripe_price = 'price_1OpDS6Cm3Ol5Jv5CYHLlG5MW'
        elif product.name == 'Boxing Gloves 12oz':
            stripe_price = 'price_1OpDSNCm3Ol5Jv5CHoltyZ3y'
        elif product.name == 'Gym Spandex T-shirt':
            stripe_price = 'price_1OpDSfCm3Ol5Jv5CsPsWoSep'
        elif product.name == 'Whey Protein Powder 5kg':
            stripe_price = 'price_1OpDStCm3Ol5Jv5CNPmF58wm'
        elif product.name == 'Eletrolyte Hydration Drink 16oz':
            stripe_price = 'price_1OpDT9Cm3Ol5Jv5CP5p9Z6NK'

        line_items.append({
            'price': stripe_price, 
            'quantity': product.quantity
        })

    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=line_items,
    mode='payment',
    success_url=url_for('routes.payment_success', _external=True),
    cancel_url=url_for('routes.cart', _external=True)
)
    
    return redirect(session.url, code=303)

@routes.route('/payment_success')
def payment_success():
    flash('Order was successful. You will receive a confirmation email shortly. Enjoy your products!')
    Product.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    return redirect('/my_cart')

