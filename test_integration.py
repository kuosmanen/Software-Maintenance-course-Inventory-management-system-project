import unittest
import sqlite3
import os
from unittest.mock import patch
from tkinter import Tk, END
from create_db import create_db
from category import categoryClass
from supplier import supplierClass
from product import productClass

"""
The integration tests test some of the core flows of the system to make sure that the components work together, and the database saving plus reading works for the components.
Because integration tests are supposed to make sure that the functionalities of the components work together, the GUI will not be tested in these integration tests.
The implemented integration tests were the following:

Test 1: Creating a category -> adding a product to the new category -> searching products by that category
Test 2: Creating a supplier -> adding a product that uses that supplier -> searching products by that supplier
"""


class TestIntegration(unittest.TestCase):
     
    #Creating a test database once before all tests
    @classmethod
    def setUpClass(cls):
        cls.test_db = 'test_integration_ims.db'
        create_db(db_name=cls.test_db)
        cls.con = sqlite3.connect(cls.test_db)
        cls.cur = cls.con.cursor()
        
    #Setting up before each test
    @patch('category.Image.open')
    @patch('supplier.Image.open')
    @patch('product.Image.open')
    def setUp(self, mock_prod_image, mock_sup_image, mock_cat_image):
        #Mocking image loading so tests don't need actual image files
        #this must be done so that the tests don't crash, because the images don't exist
        from PIL import Image
        mock_image = Image.new('RGB', (1, 1))
        mock_cat_image.return_value = mock_image
        mock_sup_image.return_value = mock_image
        mock_prod_image.return_value = mock_image
        
        #Clearing the test database
        self.cur.execute("DELETE FROM product")
        self.cur.execute("DELETE FROM category")
        self.cur.execute("DELETE FROM supplier")
        self.con.commit()
        
        #tkinter root window
        self.root = Tk()
        self.root.withdraw()  #Hiding the window during testing
        
        self.category_obj = categoryClass(self.root)
        self.supplier_obj = supplierClass(self.root)
        self.product_obj = productClass(self.root)
    
    #Cleaning up after each test
    def tearDown(self):
        self.root.destroy()
    
    #Deleting the entire testing database after all tests have run
    @classmethod
    def tearDownClass(cls):
        cls.con.close()
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)
    

#------------------------------------------------------------------------------------------------------------
    #Integration Test 1: Category -> Product -> searching products by category
    @patch('category.messagebox.showinfo')
    @patch('category.sqlite3.connect')
    @patch('product.messagebox.showinfo')
    @patch('product.sqlite3.connect')
    def test_category_product_integration(self, mock_prod_connect, mock_prod_info,mock_cat_connect, mock_cat_info):
        #Mocking database connections to use test database
        mock_cat_connect.return_value = self.con
        mock_prod_connect.return_value = self.con
        
        #Adding a category
        self.category_obj.var_name.set("Graphics cards")
        self.category_obj.add()
        
        #category was added?
        self.cur.execute("SELECT * FROM category WHERE name=?", ("Graphics cards",))
        category_row = self.cur.fetchone()
        self.assertEqual(category_row[1], "Graphics cards")
        
        #Adding a product with the category
        self.product_obj.var_cat.set("Graphics cards")
        self.product_obj.var_name.set("RTX 3070")
        self.product_obj.var_price.set("1299.99")
        self.product_obj.var_qty.set("10")
        self.product_obj.var_status.set("Active")
        self.product_obj.add()
        
        #Prroduct was added with correct category?
        self.cur.execute("SELECT * FROM product WHERE name=?", ("RTX 3070",))
        product_row = self.cur.fetchone()
        self.assertEqual(product_row[1], "Graphics cards")
        self.assertEqual(product_row[3], "RTX 3070")
        self.assertEqual(product_row[4], "1299.99")
        
        #can query products by category?
        self.cur.execute("SELECT * FROM product WHERE Category=?", ("Graphics cards",))
        products_in_category =self.cur.fetchall()
        self.assertEqual(len(products_in_category), 1)
        self.assertEqual(products_in_category[0][3], "RTX 3070")



    #Integration Test 2: Supplier -> Product integration -> query product by the supplier
    @patch('category.messagebox.showinfo')
    @patch('category.sqlite3.connect')
    @patch('supplier.messagebox.showinfo')
    @patch('supplier.sqlite3.connect')
    @patch('product.messagebox.showinfo')
    @patch('product.sqlite3.connect')
    def test_supplier_product_integration(self, mock_prod_connect, mock_prod_info,mock_sup_connect, mock_sup_info, mock_cat_connect, mock_cat_info):
        #Mocking the database connections to use test database
        mock_cat_connect.return_value = self.con
        mock_sup_connect.return_value = self.con
        mock_prod_connect.return_value = self.con
        
        #Adding a category
        self.category_obj.var_name.set("CPUs")
        self.category_obj.add()
        
        #Adding a supplier
        self.supplier_obj.var_sup_invoice.set("12345")
        self.supplier_obj.var_name.set("Advanced Micro Devices")
        self.supplier_obj.var_contact.set("050999444666")
        self.supplier_obj.txt_desc.insert(END, "AMD supplier")
        self.supplier_obj.add()
        
        #supplier was added?
        self.cur.execute("SELECT * FROM supplier WHERE invoice=?",("12345",))
        supplier_row = self.cur.fetchone()
        self.assertEqual(supplier_row[1], "Advanced Micro Devices")
        
        #Adding a product with thesupplier
        self.product_obj.var_cat.set("CPUs")
        self.product_obj.var_sup.set("Advanced Micro Devices")
        self.product_obj.var_name.set("Ryzen 5 5600x")
        self.product_obj.var_price.set("300")
        self.product_obj.var_qty.set("25")
        self.product_obj.var_status.set("Active")
        self.product_obj.add()
        
        #product was added with correct supplier?
        self.cur.execute("SELECT * FROM product WHERE name=?", ("Ryzen 5 5600x",))
        product_row = self.cur.fetchone()
        self.assertEqual(product_row[2], "Advanced Micro Devices")
        self.assertEqual(product_row[3], "Ryzen 5 5600x")
        self.assertEqual(product_row[4], "300")

        #query products by supplier?
        self.cur.execute("SELECT * FROM product WHERE Supplier=?", ("Advanced Micro Devices",))
        products_from_supplier = self.cur.fetchall()
        self.assertEqual(len(products_from_supplier), 1)
        self.assertEqual(products_from_supplier[0][3],"Ryzen 5 5600x")



if __name__ == '__main__':
    #verbose output for the tests!!
    unittest.main(verbosity=2)