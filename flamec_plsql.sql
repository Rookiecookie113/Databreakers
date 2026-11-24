-- Flameback Catering - Stored Procedures
-- CS 340 Project Step 4, Group 12
-- Hurrsh Misttry, Tetsuya Bassler, Allen Dickey

DELIMITER $$

DROP PROCEDURE IF EXISTS sp_save_recipe_ingredients $$
CREATE PROCEDURE sp_save_recipe_ingredients(
	IN p_recipe_id INT,
	IN p_ingredient_id INT,
	IN p_quantity INT,
	INOUT p_id INT,
	OUT p_affected_rows INT
)
BEGIN
	IF p_id IS NULL THEN
		INSERT INTO RecipeIngredients (recipe_id, ingredient_id, quantity_needed)
		VALUES (p_recipe_id, p_ingredient_id, p_quantity);
		SET p_affected_rows = ROW_COUNT();
		SET p_id = LAST_INSERT_ID();
	ELSE
		UPDATE RecipeIngredients
		SET recipe_id = p_recipe_id,
			ingredient_id = p_ingredient_id,
			quantity_needed = p_quantity
		WHERE recipe_ingredients_id = p_id;
		SET p_affected_rows = ROW_COUNT();
	END IF;
END $$

DROP PROCEDURE IF EXISTS sp_delete_recipe_ingredients $$
CREATE PROCEDURE sp_delete_recipe_ingredients(IN p_id INT, OUT p_affected_rows INT)
BEGIN
	DELETE FROM RecipeIngredients
	WHERE recipe_ingredients_id = p_id;
	SET p_affected_rows = ROW_COUNT();
END $$

DROP PROCEDURE IF EXISTS sp_save_order_details $$
CREATE PROCEDURE sp_save_order_details(
	IN p_order_id INT,
	IN p_menu_id INT,
	IN p_quantity INT,
	IN p_total_cost DECIMAL(10,2),
	INOUT p_id INT,
	OUT p_affected_rows INT
)
BEGIN
	IF p_id IS NULL THEN
		INSERT INTO OrderDetails (order_id, menu_id, quantity_ordered, total_cost)
		VALUES (p_order_id, p_menu_id, p_quantity, p_total_cost);
		SET p_affected_rows = ROW_COUNT();
		SET p_id = LAST_INSERT_ID();
	ELSE
		UPDATE OrderDetails
		SET order_id = p_order_id,
			menu_id = p_menu_id,
			quantity_ordered = p_quantity,
			total_cost = p_total_cost
		WHERE order_details_id = p_id;
		SET p_affected_rows = ROW_COUNT();
	END IF;
END $$

DROP PROCEDURE IF EXISTS sp_delete_order_details $$
CREATE PROCEDURE sp_delete_order_details(IN p_id INT, OUT p_affected_rows INT)
BEGIN
	DELETE FROM OrderDetails
	WHERE order_details_id = p_id;
	SET p_affected_rows = ROW_COUNT();
END $$

DROP PROCEDURE IF EXISTS sp_set_supplier_active $$
CREATE PROCEDURE sp_set_supplier_active(
	IN p_supplier_id INT,
	IN p_is_active BOOLEAN,
	OUT p_affected_rows INT
)
BEGIN
	UPDATE Suppliers
	SET is_active = p_is_active
	WHERE supplier_id = p_supplier_id;
	SET p_affected_rows = ROW_COUNT();
END $$

DROP PROCEDURE IF EXISTS sp_delete_supplier $$
CREATE PROCEDURE sp_delete_supplier(IN p_supplier_id INT, OUT p_affected_rows INT)
BEGIN
	DELETE FROM Suppliers
	WHERE supplier_id = p_supplier_id AND is_active = FALSE;
	SET p_affected_rows = ROW_COUNT();
END $$

-- Additional procedures used to set up and clean up supplier tests.
DROP PROCEDURE IF EXISTS sp_insert_supplier $$
CREATE PROCEDURE sp_insert_supplier(
	IN p_name VARCHAR(50), IN p_phone VARCHAR(20), OUT p_id INT,
	OUT p_affected_rows INT
)
BEGIN
	INSERT INTO Suppliers (supplier_name, supplier_phone)
	VALUES (p_name, p_phone);
	SET p_affected_rows = ROW_COUNT();
	SET p_id = LAST_INSERT_ID();
END $$

DROP PROCEDURE IF EXISTS sp_insert_inventory_item $$
CREATE PROCEDURE sp_insert_inventory_item(
	IN p_supplier_id INT, IN p_name VARCHAR(50),
	IN p_quantity INT, IN p_price DECIMAL(10,2), OUT p_id INT,
	OUT p_affected_rows INT
)
BEGIN
	INSERT INTO InventoryItems (supplier_id, ingredient_name, quantity_on_hand, price_per_unit)
	VALUES (p_supplier_id, p_name, p_quantity, p_price);
	SET p_affected_rows = ROW_COUNT();
	SET p_id = LAST_INSERT_ID();
END $$

DROP PROCEDURE IF EXISTS sp_insert_recipe $$
CREATE PROCEDURE sp_insert_recipe(IN p_name VARCHAR(50), OUT p_id INT, OUT p_affected_rows INT)
BEGIN
	INSERT INTO Recipes (recipe_name) VALUES (p_name);
	SET p_affected_rows = ROW_COUNT();
	SET p_id = LAST_INSERT_ID();
END $$

DROP PROCEDURE IF EXISTS sp_delete_inventory_item $$
CREATE PROCEDURE sp_delete_inventory_item(IN p_id INT, OUT p_affected_rows INT)
BEGIN
	DELETE FROM InventoryItems WHERE ingredient_id = p_id;
	SET p_affected_rows = ROW_COUNT();
END $$

DROP PROCEDURE IF EXISTS sp_delete_recipe $$
CREATE PROCEDURE sp_delete_recipe(IN p_id INT, OUT p_affected_rows INT)
BEGIN
	DELETE FROM Recipes WHERE recipe_id = p_id;
	SET p_affected_rows = ROW_COUNT();
END $$

DELIMITER ;
