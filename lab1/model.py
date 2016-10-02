import pickle

class Model:

    def __init__(self, fproduct, forder):
        try:
            self.fproduct = fproduct
            self.forder = forder
            db = open(fproduct, 'rb')
            self.product = pickle.load(db)
            db.close()
            db = open(forder, 'rb')
            self.order = pickle.load(db)
            db.close()
        except:
            #table(list of dictionaries) product with columns (keys) 'product_id', 'product_name', 'price'
            self.product = list()
            # table(list of dictionaries) order with columns (keys) 'product_id', 'client', 'date'
            self.order = list()

    def get_product(self):
        return self.product

    def get_order(self):
        return self.order

    def insert_into_product(self, product_name, price):
        '''
        :return: None in case of success
                 error message as a string otherwise
        '''
        if not self.product:
            product_id = 0
        else:
            product_id = len(self.product)
        if self.product_name_in_table(product_name):
            return 'Such product already exists'
        self.product.append({'product_id': product_id, 'product_name': product_name, 'price': price})

    def insert_into_order(self, product_name, client, date):
        '''
        :return: None in case of success
                 error message as a string otherwise
        '''
        if not self.product_name_in_table(product_name):
            return 'No such product'
        product_id = self.product_name_in_table(product_name)[0]['product_id']
        if self.order_in_table(product_id, client, date):
            return 'Such order already exists'
        self.order.append({'product_id': product_id, 'client': client, 'date': date})

    def delete_from_product (self, product_name):
        '''
        :return: None in case of success
                 error message as a string otherwise
        '''
        existing_product = self.product_name_in_table(product_name)
        if not existing_product:
            return 'No such product'
        if filter(lambda x: x['product_id'] == existing_product[0]['product_id'], self.order):
            return 'Cannot delete an ordered product'
        self.product.remove(existing_product[0])

    def delete_from_order (self, product_name, client, date):
        '''
        :return: None in case of success
                 error message as a string otherwise
        '''
        order = self.order_to_change(product_name, client, date)
        if type(order) == str:
            return order
        self.order.remove(order)

    def product_to_update(self, product_name):
        existing_product = self.product_name_in_table(product_name)
        if not existing_product:
            return 'No such product'
        if filter(lambda x: x['product_id'] == existing_product[0]['product_id'], self.order):
            return 'Cannot update an ordered product'

    def update_product (self, product_name, new_product_name, new_price):
        if self.product_name_in_table(new_product_name):
            return 'Such product already exists'
        existing_product = self.product_name_in_table(product_name)
        if new_product_name:
            existing_product[0]['product_name'] = new_product_name
        if new_price:
            existing_product[0]['price'] = new_price

    def order_to_change(self, product_name, client, date):
        product = self.product_name_in_table(product_name)
        if not product:
            return 'No such order'
        existing_order = self.order_in_table(product[0]['product_id'], client, date.strftime("%d/%m/%y"))
        if not existing_order:
            return 'No such order'
        return existing_order[0]

    def update_order (self, product_name, client, date, new_product_name, new_client, new_date):
        new_product = self.product_name_in_table(new_product_name)
        if new_product_name and not new_product:
            return 'No such product'
        if new_date and self.order_in_table(new_product[0]['product_id'], new_client, new_date.strftime("%d/%m/%y")):
            return 'Such order already exists'
        existing_order = self.order_in_table(self.product_name_in_table(product_name)[0]['product_id'], client, date.strftime("%d/%m/%y"))
        if new_product_name and self.product_name_in_table(new_product_name):
            existing_order[0]['product_id'] = self.product_name_in_table(new_product_name)[0]['product_id']
        if new_client:
            existing_order[0]['client'] = new_client
        if new_date:
           existing_order[0]['date'] = new_date.strftime("%d/%m/%y")

    def select (self):
        orders = filter(lambda x: self.product_id_in_table(x['product_id'])[0]['price'] > 100, self.order)
        ordered_products_ids = {x['product_id']for x in orders}
        return [[self.product_id_in_table(x)[0]['product_name'], self.product_id_in_table(x)[0]['price']] for x in ordered_products_ids]

    def pack(self):
        db = open(self.fproduct, 'wb')
        pickle.dump(self.product, db)
        db.close()
        db = open(self.forder, 'wb')
        pickle.dump(self.order, db)
        db.close()

    def product_name_in_table(self, product_name):
        return filter(lambda x: x['product_name'] == product_name, self.product)

    def product_id_in_table(self, product_id):
        return filter(lambda y: y['product_id'] == product_id, self.product)
    
    def order_in_table(self, product_id, client, date):
        return filter(lambda x: x['product_id'] == product_id and x['client'] == client and x['date'] == date,
                      self.order)
