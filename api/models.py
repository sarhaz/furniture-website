from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Float, Table
from sqlalchemy.orm import relationship
from database import Base

# Association table for many-to-many relationship between Cart and Product
cart_products = Table('cart_products', Base.metadata,
                      Column('cart_id', Integer, ForeignKey('index_cart.id')),
                      Column('product_id', Integer, ForeignKey('index_product.id'))
                     )

# Association table for many-to-many relationship between Blog and Comments
blog_comments = Table('blog_comments', Base.metadata,
                      Column('blog_id', Integer, ForeignKey('index_blog.id')),
                      Column('comment_id', Integer, ForeignKey('index_comments.id'))
                     )


class User(Base):
    __tablename__ = 'auth_user'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean, default=False)
    cart = relationship('Cart', back_populates='user')
    products = relationship('Product', back_populates='user')
    comments = relationship('Comments', back_populates='user')

    def __repr__(self):
        return self.first_name


class Team(Base):
    __tablename__ = 'index_team'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    position = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return f"{self.first_name} {self.last_name}"


class Product(Base):
    __tablename__ = 'index_product'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('auth_user.id'), nullable=False)
    user = relationship('User', back_populates='products')
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    price_type = Column(String(50), nullable=False, default="$")
    description = Column(Text, nullable=False)
    carts = relationship('Cart', secondary=cart_products, back_populates='products')

    def __repr__(self):
        return self.name


class Comments(Base):
    __tablename__ = 'index_comments'
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('auth_user.id'), nullable=False)
    user = relationship('User', back_populates='comments')
    blogs = relationship('Blog', secondary=blog_comments, back_populates='comments')

    def __repr__(self):
        return self.text


class Blog(Base):
    __tablename__ = 'index_blog'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    author = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime)
    comments = relationship('Comments', secondary=blog_comments, back_populates='blogs')

    def __repr__(self):
        return self.title


class Cart(Base):
    __tablename__ = 'index_cart'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('auth_user.id'), nullable=False)
    user = relationship('User', back_populates='cart')
    products = relationship('Product', secondary=cart_products, back_populates='carts')

    def __repr__(self):
        return str(self.id)
