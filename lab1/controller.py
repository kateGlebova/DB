import model
import view
import sys

class Controller:

    def __init__ (self, fproduct, forder):
        self.fproduct = fproduct
        self.forder = forder

    def main(self):
        v = view.View()
        m = model.Model(self.fproduct, self.forder)
        choice = v.menu()
        while choice != 7:
            if choice == 1:
                self.display_database(v, m)
            elif choice == 2:
                self.display_table(v, m)
            elif choice == 3:
                self.insert(v, m)
            elif choice == 4:
                self.delete(v, m)
            elif choice == 5:
                self.update(v, m)
            elif choice == 6:
                self.select(v, m)
            choice = v.menu()
        m.pack()
        sys.exit(0)

    def display_database(self, v, m):
        v.display_table('product', m.get_product())
        v.display_table('order', m.get_order())

    def display_table(self, v, m):
        table = self.what_table(v, m)
        if table == 3:
            return
        if table == 1:
            v.display_table('product', m.get_product())
        else:
            v.display_table('order', m.get_order())

    def insert(self, v, m):
        table = self.what_table(v, m)
        if table == 3:
            return
        if table == 1:
            self.insert_into_product(v, m)
        else:
            self.insert_into_order(v, m)

    def delete(self, v, m):
        table = self.what_table(v, m)
        if table == 3:
            return
        if table == 1:
            self.delete_from_product(v, m)
        else:
            self.delete_from_order(v, m)

    def update(self, v, m):
        table = self.what_table(v, m)
        if table == 3:
            return
        if table == 1:
            self.update_product(v, m)
        else:
            self.update_order(v, m)

    def select(self, v, m):
        ordered_products = m.select()
        v.select(ordered_products)

    def insert_into_product(self, v, m):
        info = v.insert_info_product()
        if not info:
            return
        if not info[0] and info[1] > 0:
            v.error('Invalid input')
            return
        is_error = m.insert_into_product(info[0], info[1])
        v.is_successful(is_error)

    def insert_into_order(self, v, m):
        info = v.insert_info_order()
        if not info:
            return
        if not (info[0] and info[1] and info[2]):
            v.error('Invalid input')
            return
        is_error = m.insert_into_order(info[0], info[1], info[2].strftime("%d/%m/%y"))
        v.is_successful(is_error)

    def delete_from_product(self, v, m):
        info = v.delete_info_product()
        if info:
            is_error = m.delete_from_product(info[0])
            v.is_successful(is_error)

    def delete_from_order(self, v, m):
        info = v.delete_info_order()
        if info:
            is_error = m.delete_from_order(info[0], info[1], info[2].strftime("%d/%m/%y"))
            v.is_successful(is_error)

    def update_product(self, v, m):
        old_info = v.update_old_info_product()
        if not old_info:
            v.error('Invalid input')
            return
        existing_product = m.product_to_update(old_info[0])
        if type(existing_product) == str:
            v.error(existing_product)
            return
        new_info = v.update_new_info_product()
        if new_info:
            is_error = m.update_product(old_info[0], new_info[0], new_info[1])
            v.is_successful(is_error)

    def update_order(self, v, m):
        old_info = v.update_old_info_order()
        if not (old_info and old_info[0] and old_info[1] and old_info[2]):
            v.error('Invalid input')
            return
        existing_order = m.order_to_change(old_info[0], old_info[1], old_info[2])
        if type(existing_order) == str:
            v.error(existing_order)
            return
        new_info = v.update_new_info_order()
        if new_info:
            is_error = m.update_order(old_info[0], old_info[1], old_info[2], new_info[0], new_info[1], new_info[2])
            v.is_successful(is_error)

    def what_table(self, v, m):
        table = v.what_table()
        while not table:
            table = v.what_table()
        return table

if __name__ == '__main__':
    c = Controller('product.txt', 'order.txt')
    c.main()