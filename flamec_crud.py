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
        sql = """
        SELECT * FROM Suppliers
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

    #Grabs all data from the InventoryItems Entity
    def get_all_inventory_items(self):
        cursor = self.cursor
        sql = """
        SELECT * FROM InventoryItems
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

    
    #Performing CRUD operations on RecipeIngredients Intersection Table
    def get_all_recipe_ingredients(self):
        cursor = self.cursor
        sql = """
        SELECT * FROM RecipeIngredients
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

    def add_recipe_ingredient(self, r=None, i=None, q=None):
        cursor = self.cursor
                
        try:
            sql = """
            INSERT INTO RecipeIngredients (recipe_id, ingredient_id, quantity_needed)
            VALUES (%s, %s, %s);
            """
            cursor.execute(sql, (r, i, q))
            self._commit()
            rowcount = cursor.rowcount
            return rowcount
        except mysql.connector.Error as err:
            if err.errno == 1062:
                return "Trying to insert duplicate data"
        pass

    def update_recipe_ingredient(self, r=None, q=None):
        cursor = self.cursor
        sql = """
        UPDATE RecipeIngredients SET quantity_needed = %s WHERE recipe_ingredients_id = %s
        """
        cursor.execute(sql, (q, r))
        self._commit()
        rowcount = cursor.rowcount
        return rowcount

    def delete_recipe_ingredient(self, c=None):
        cursor = self.cursor
        sql = """
        DELETE FROM RecipeIngredients WHERE recipe_ingredients_id = %s
        """
        cursor.execute(sql, (c,))
        self._commit()
        rowcount = cursor.rowcount
        return rowcount

    
    #Grabbing all data from Recipes Entity
    def get_all_recipes(self):
        cursor = self.cursor
        sql = """
        SELECT * FROM Recipes
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

    #Grabs all data from the MenuItems Entity
    def get_all_menu_items(self):
        cursor = self.cursor
        sql = """
        SELECT * FROM MenuItems
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

    #Performing CRUD operations on OrderDetails Intersection Table
    def get_all_order_details(self):
        cursor = self.cursor
        sql = """
        SELECT * FROM OrderDetails
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

    def add_order_detail(self, o=None, m=None, q=None, t=None):
        cursor = self.cursor
                        
        try:
            sql = """
            INSERT INTO OrderDetails (order_id, menu_id, quantity_ordered, total_cost)
            VALUES (%s, %s, %s, %s);
            """
            cursor.execute(sql, (o, m, q, t))
            self._commit()
            rowcount = cursor.rowcount
            return rowcount
        except mysql.connector.Error as err:
            if err.errno == 1062:
                return "Trying to insert duplicate data"
            pass

    def update_order_detail(self, o=None, q=None, t=None):
        cursor = self.cursor
        sql = """
        UPDATE OrderDetails SET quantity_ordered = %s, total_cost = %s WHERE order_details_id = %s
        """
        cursor.execute(sql, (q, t, o))
        self._commit()
        rowcount = cursor.rowcount
        return rowcount

    def delete_order_detail(self, c=None):
        cursor = self.cursor
        sql = """
        DELETE FROM OrderDetails WHERE order_details_id = %s
        """
        cursor.execute(sql, (c,))
        self._commit()
        rowcount = cursor.rowcount
        return rowcount


    #Grabbing all data from Orders Entity
    def get_all_orders(self):
        cursor = self.cursor
        sql = """ 
        SELECT * FROM Orders
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        return results

    #Grabbing all data from Customers Entity
    def get_all_customers(self):
        cursor = self.cursor
        sql = """
        SELECT * FROM Customers
        """
        cursor.execute(sql)
        results = cursor.fetchall()
        return results  
