import random
import string
from datetime import datetime, timedelta
from bson import ObjectId
from faker import Faker


class DataGenerator:
    def __init__(self, locale='it_IT'):
        self.fake = Faker(locale)
        random.seed(42)  # Per riproducibilità

    def generate_users(self, count):
        """
        Genera documenti utente
        """
        users = []
        for i in range(count):
            user = {
                '_id': ObjectId(),
                'username': self.fake.user_name(),
                'email': self.fake.email(),
                'first_name': self.fake.first_name(),
                'last_name': self.fake.last_name(),
                'birth_date': self.fake.date_of_birth(minimum_age=18, maximum_age=80),
                'address': {
                    'street': self.fake.street_address(),
                    'city': self.fake.city(),
                    'country': self.fake.country(),
                    'postal_code': self.fake.postcode()
                },
                'phone': self.fake.phone_number(),
                'registration_date': self.fake.date_between(start_date='-2y', end_date='today'),
                'is_active': random.choice([True, False]),
                'preferences': {
                    'language': random.choice(['it', 'en', 'es', 'fr']),
                    'currency': random.choice(['EUR', 'USD', 'GBP']),
                    'newsletter': random.choice([True, False])
                }
            }
            users.append(user)
        return users

    def generate_orders(self, count, user_ids):
        """
        Genera documenti ordini
        """
        orders = []
        statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']

        for i in range(count):
            order = {
                '_id': ObjectId(),
                'user_id': random.choice(user_ids),
                'order_number': f"ORD-{i + 1:08d}",
                'created_at': self.fake.date_time_between(start_date='-1y', end_date='now'),
                'status': random.choice(statuses),
                'items': [
                    {
                        'product_id': ObjectId(),
                        'name': self.fake.commerce_product_name(),
                        'quantity': random.randint(1, 5),
                        'price': round(random.uniform(10, 500), 2)
                    }
                    for _ in range(random.randint(1, 3))
                ],
                'total_amount': round(random.uniform(20, 1000), 2),
                'shipping_address': {
                    'street': self.fake.street_address(),
                    'city': self.fake.city(),
                    'country': self.fake.country(),
                    'postal_code': self.fake.postcode()
                },
                'payment_method': random.choice(['credit_card', 'paypal', 'bank_transfer']),
                'region': random.choice(['north', 'center', 'south'])
            }
            orders.append(order)
        return orders

    def generate_products(self, count):
        """
        Genera documenti prodotti
        """
        products = []
        categories = ['electronics', 'clothing', 'books', 'home', 'sports']

        for i in range(count):
            product = {
                '_id': ObjectId(),
                'name': self.fake.commerce_product_name(),
                'description': self.fake.text(max_nb_chars=200),
                'category': random.choice(categories),
                'price': round(random.uniform(5, 1000), 2),
                'stock_quantity': random.randint(0, 100),
                'is_active': random.choice([True, False]),
                'created_at': self.fake.date_time_between(start_date='-2y', end_date='now'),
                'updated_at': self.fake.date_time_between(start_date='-1y', end_date='now'),
                'attributes': {
                    'weight': round(random.uniform(0.1, 10), 2),
                    'dimensions': {
                        'length': round(random.uniform(1, 100), 2),
                        'width': round(random.uniform(1, 100), 2),
                        'height': round(random.uniform(1, 100), 2)
                    },
                    'color': self.fake.color_name(),
                    'material': random.choice(['plastic', 'metal', 'wood', 'fabric', 'glass'])
                }
            }
            products.append(product)
        return products

    def generate_transactions(self, count, user_ids):
        """
        Genera documenti transazioni per test isolamento
        """
        transactions = []

        for i in range(count):
            transaction = {
                '_id': ObjectId(),
                'user_id': random.choice(user_ids),
                'transaction_id': f"TXN-{i + 1:08d}",
                'amount': round(random.uniform(1, 1000), 2),
                'type': random.choice(['credit', 'debit']),
                'status': random.choice(['pending', 'completed', 'failed']),
                'created_at': self.fake.date_time_between(start_date='-1y', end_date='now'),
                'balance_before': round(random.uniform(0, 5000), 2),
                'balance_after': round(random.uniform(0, 5000), 2)
            }
            transactions.append(transaction)
        return transactions