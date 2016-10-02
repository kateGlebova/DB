import sys
import datetime

class View:

    def menu(self):
        print '\n[1] Display database'
        print '[2] Display table'
        print '[3] Insert row into the table'
        print '[4] Delete row from the table'
        print '[5] Update the row in the table'
        print '[6] Select ordered products with the price higher than 100 UAH'
        print '[7] Quit'
        try:
            selection = int(raw_input('Choose an option: '))
            if not 1 <= selection <= 7:
                raise ValueError
            return selection
        except ValueError:
            self.error('Invalid input')
            return None

    def display_table(self, table_name, table):
        print '{:^124}'.format(table_name + ' table')
        if not table:
            print '{:^124}'.format('empty')
        else:
            columns = table[0].keys()
            print '|{:^40}|{:^40}|{:^40}|'.format(columns[0],columns[1], columns[2])
            print '-' * 124
            for row in table:
                print '|{:^40}|{:^40}|{:^40}|'.format(row[columns[0]],row[columns[1]], row[columns[2]])
            print '-' * 124

    def delete_info_product(self):
        row = list()
        print '\nDeleting product'
        product_name = raw_input("Enter product_name: ")
        row.append(product_name)
        return row

    def delete_info_order(self):
        row = list()
        print '\nDeleting order'
        try:
            row.append(raw_input("Enter product_name: "))
            row.append(raw_input("Enter client: "))
            date_str = raw_input("Enter date (dd/mm/yy): ")
            if not date_str:
                raise ValueError
            row.append(datetime.datetime.strptime(date_str, "%d/%m/%y").date())
            return row
        except ValueError:
            self.error('Invalid input')
            return None

    def insert_info_product(self):
        row = list()
        print '\nInserting product'
        try:
            row.append(raw_input("Enter product_name: "))
            row.append(float(raw_input('Enter price: ')))
            return row
        except ValueError:
            self.error('Invalid input')
            return None

    def insert_info_order(self):
        row = list()
        print '\nInserting order'
        try:
            row.append(raw_input("Enter product_name: "))
            row.append(raw_input("Enter client: "))
            date_str = raw_input("Enter date (dd/mm/yy): ")
            if not date_str:
                raise ValueError
            row.append(datetime.datetime.strptime(date_str, "%d/%m/%y").date())
            return row
        except ValueError:
            self.error('Invalid input')
            return None

    def update_old_info_product(self):
        row = list()
        print '\nUpdating product'
        row.append(raw_input("Enter product_name of product to update: "))
        return row

    def update_old_info_order(self):
        row = list()
        print '\nUpdating order'
        try:
            row.append(raw_input("Enter product_name of order to update: "))
            row.append(raw_input("Enter client of order to update: "))
            date_str = raw_input("Enter date (dd/mm/yy) of order to update: ")
            if not date_str:
                row.append(date_str)
            else:
                row.append(datetime.datetime.strptime(date_str, "%d/%m/%y").date())
            return row
        except ValueError:
            self.error('Invalid input')
            return None

    def update_new_info_product(self):
        row = list()
        try:
            row.append(raw_input("Enter new product_name (press Enter if you don't want to update this attribute): "))
            row.append(float(raw_input("Enter new price (press '0' if you don't want to update this attribute): ")))
            return row
        except ValueError:
            self.error('Invalid input')
            return None

    def update_new_info_order(self):
        row = list()
        try:
            row.append(raw_input("Enter new product_name (press Enter if you don't want to update this attribute): "))
            row.append(raw_input("Enter new client (press Enter if you don't want to update this attribute): "))
            date_str = raw_input("Enter new date (dd/mm/yy) (press Enter if you don't want to update this attribute): ")
            if not date_str:
                row.append(date_str)
            else:
                row.append(datetime.datetime.strptime(date_str, "%d/%m/%y").date())
            return row
        except ValueError:
            self.error('Invalid input')
            return None

    def is_successful(self, error_message):
        '''
        Indicates whether operation was successful
        :param error_message:
        :param func: insert_successful() or delete_successful or update_successful
        :return: None
        '''
        if not error_message:
            print '\nSuccess'
        else:
            self.error(error_message)

    def what_table(self):
        print '\nChoose the table: '
        print '[1] product'
        print '[2] order'
        print '[3] Back to menu'
        try:
            selection = int(raw_input('Choose an option: '))
            if not 1 <= selection <= 3:
                raise ValueError
            return selection
        except ValueError:
            self.error('Invalid input')
            return None

    def select(self, ordered_products):
        print '{:^103}'.format('Ordered products with the price higher than 100 UAH')
        print '|{:^50}|{:^50}|'.format('product_name', 'price')
        print '-' * 103
        for product in ordered_products:
            print '|{:^50}|{:^50}|'.format(product[0], product[1])
        print '-' * 103

    def error(self, message):
        print '\n' + message
