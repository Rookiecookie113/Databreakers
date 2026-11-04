import mysql.connector
from flamec_crud import FlamebackCaterData

# replace with your actual DB credentials
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='flamebackcater_db'
)
cursor = conn.cursor()

q = FlamebackCaterData(cursor, conn)

#checking the select statements for all tables
print(q.get_all_suppliers())
print(q.get_all_inventory_items())
print(q.get_all_recipe_ingredients())
print(q.get_all_recipes())
print(q.get_all_menu_items())
print(q.get_all_order_details())
print(q.get_all_orders())
print(q.get_all_customers())


#checking CUD Operations in RecipeIngredients
print(q.add_recipe_ingredient(2, 5, 5))
conn.commit()

print(q.update_recipe_ingredient(4, 10))
conn.commit()

print(q.delete_recipe_ingredient(4))
conn.commit()


#Checking CUD Operations in OrderDetails
print(q.add_order_detail(1, 2, 3, 4))
conn.commit()

print(q.update_order_detail(1, 2))
conn.commit()

print(q.delete_order_detail(1))
conn.commit()


cursor.close()
conn.close()