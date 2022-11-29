from sqlalchemy.orm import Session

from model import Product, User
from schema import ProductSchema

def db_register_user(db: Session, name, password):
    db_item = User(name = name, password = password)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def db_get_product(db: Session, seller: int):
    if not seller == None:
        return db.query(Product).filter(Product.seller_id == seller).all()
    else:
        return db.query(Product).all()


def db_add_product(db: Session, user: User, product: ProductSchema):
    db_item = Product(name = product.name, description = product.description, seller_id = user.id, price = product.price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def db_del_product(db:Session, user:User, product:ProductSchema):
    db.query(Product).filter(Product.seller_id == user.id).filter(Product.id == product.id).delete()
    db.commit()
    return True

def db_search_product(db: Session, product: ProductSchema):
    db_items =db.query(Product).filter(Product.name.contains(product.name))
    if db_items:
        return db_items.all()
    return None


def db_auction(db: Session, product: ProductSchema, auction_price: int, buyer: int):
    db.query(Product).filter(id == product.id).update({"id":product.id, "description":product.description, "seller_id":product.seller_id, "buyer_id":buyer, "price":auction_price})
    db.commit()
    return True