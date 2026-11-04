import mysql.connector


class FlamebackCaterData(object):

    def __init__(self, cursor, connection=None):
        self.cursor = cursor
        self.connection = connection

    def _commit(self):
        """Commit if a connection object was provided."""
        if self.connection is not None:
            self.connection.commit()

        
    #Grabs all data from the Suppliers Entity
    def get_all_suppliers(self):
        cursor = self.cursor
      
        cursor.execute(sql)
        results = cursor.fetchall()
        return results
        pass

    #Grabs all data from the InventoryItems Entity
    def get_all_inventory_items(self):
        cursor = self.cursor
        
       
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

    
    #Performing CRUD operations on RecipeIngredients Intersection Table
    def get_all_recipe_ingredients(self):
        """Insert cert-person pair into bsg_cert_people."""
        cursor = self.cursor
        # TODO: INSERT INTO bsg_cert_people (cid, pid)
        # TODO: handle mysql.connector.Error duplicate (errno 1062)
        # TODO: commit and return rowcount or duplicate error text
        try:
            sql = """
            INSERT INTO bsg_cert_people (cid, pid)
            VALUES (%s, %s)
            """
            cursor.execute(sql)
            self._commit()
            rowcount = cursor.rowcount
            return rowcount
        except mysql.connector.Error as err:
            if err.errno == 1062:
                return "Trying to insert duplicate data"
        pass

    def add_recipe_ingredient(self, c=None, p=None):
        cursor = self.cursor
        
        cursor.execute(sql, (c, p))
        self._commit()
        rowcount = cursor.rowcount
        return rowcount
        pass

    def update_recipe_ingredient(self, c=None, p=None):
        cursor = self.cursor
        
        cursor.execute(sql, (c, p))
        self._commit()
        rowcount = cursor.rowcount
        return rowcount
        pass

    def delete_recipe_ingredient(self, c=None, p=None):

        pass

    
    #Grabbing all data from Recipes Entity
    def get_all_recipes(self):
        cursor = self.cursor

    #Grabs all data from the MenuItems Entity
    def get_all_menu_items(self):
        cursor = self.cursor

    
    #Performing CRUD operations on OrderDetails Intersection Table
    def get_all_order_details(self):
        cursor = self.cursor

    def add_new_order_detail(self, c=None, p=None):
        cursor = self.cursor

    def update_order_detail(self, c=None, p=None):
        cursor = self.cursor

    def delete_order_detail(self, c=None, p=None):
        pass


    #Grabbing all data from Orders Entity
    def get_all_orders(self):
        cursor = self.cursor


    #Grabbing all data from Customers Entity
    def get_all_customers(self):
            cursor = self.cursor

