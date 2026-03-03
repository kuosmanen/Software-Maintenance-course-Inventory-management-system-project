import unittest
import sqlite3
import os
from unittest.mock import patch
from tkinter import Tk, END
from supplier import supplierClass
from create_db import create_db

"""
The regression tests in this file test basic CRUD functionality of the supplier.py file.
More regression tests could be implemented for all the other python files by following the same kind of format as in test_supplier.py.
The following tests were implemented to test supplier.py: 

Test 1: Adding a new supplier works 
Test 2: Adding a supplier with the same invoice as a previous supplier should fail 
Test 3: Updating a supplier works 
Test 4: Deleting a supplier works 
Test 5: Searching for a supplier (by invoice number) works 
"""


class TestSupplier(unittest.TestCase):
    
    #Creating a test database once before all tests
    @classmethod
    def setUpClass(cls):
        cls.test_db = 'test_supplier_ims.db'
        #Using the real create_db function to ensure test database matches production schema
        create_db(db_name=cls.test_db) #this name differentiates this test database from the real one so we don't affect with real data during testing
        cls.con = sqlite3.connect(cls.test_db)
        cls.cur = cls.con.cursor()
    
    #Setting up supplier object before each test
    def setUp(self):
        #Clearing the test database
        self.cur.execute("DELETE FROM supplier")
        self.con.commit()
        
        #tkinter root window
        self.root = Tk()
        self.root.withdraw()  #Hiding the window during testing so I don't have to click them during runtime
        
        self.supplier_obj = supplierClass(self.root)
    
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
    #Unit Test 1: Add a new supplier with valid data
    #using patches to mock the database connection and messagebox calls
    #because otherwise testing would affect the real database and message popups would show up during testing
    @patch('supplier.messagebox.showinfo')
    @patch('supplier.sqlite3.connect')
    def test_add_supplier_successfully(self, mock_connect, mock_showinfo):
        #test data
        self.supplier_obj.var_sup_invoice.set("1")
        self.supplier_obj.var_name.set("Test Supplier")
        self.supplier_obj.var_contact.set("123456789")
        self.supplier_obj.txt_desc.delete('1.0', END)
        self.supplier_obj.txt_desc.insert(END, "Test description")#start position and END position must be given to text widgets
        
        #Mock database connection uses test database
        mock_connect.return_value = self.con
        self.supplier_obj.add()
        
        #success message was shown?
        mock_showinfo.assert_called_once()
        self.assertIn("Success", mock_showinfo.call_args[0][0])
        
        #supplier was added to database
        self.cur.execute("SELECT * FROM supplier WHERE invoice=?", (1,))
        row = self.cur.fetchone()
        
        self.assertIsNotNone(row)
        self.assertEqual(row[0], 1)
        self.assertEqual(row[1], "Test Supplier")
        self.assertEqual(row[2], "123456789")


    #Unit Test 2: Adding supplier with duplicate invoice should fail
    @patch('supplier.messagebox.showerror')
    @patch('supplier.sqlite3.connect')
    def test_add_supplier_duplicate_invoice_fails(self, mock_connect, mock_showerror):
        #Insert first supplier
        self.cur.execute("INSERT INTO supplier(invoice, name, contact, desc) VALUES(?, ?, ?, ?)",("2", "First Supplier", "111", "First"))
        self.con.commit()
        
        #adding duplicate?
        self.supplier_obj.var_sup_invoice.set("2")
        self.supplier_obj.var_name.set("Duplicate Supplier")
        self.supplier_obj.var_contact.set("222")
        self.supplier_obj.txt_desc.delete('1.0', END)
        self.supplier_obj.txt_desc.insert(END, "Duplicate")
        
        mock_connect.return_value = self.con
        
        self.supplier_obj.add()
        
        #Checking that the error message was shown
        mock_showerror.assert_called_once()
        self.assertIn("already assigned", mock_showerror.call_args[0][1])
    

    #Unit Test 3: Updating an existing supplier
    @patch('supplier.messagebox.showinfo')
    @patch('supplier.sqlite3.connect')
    def test_update_supplier_successfully(self, mock_connect, mock_showinfo):
        #Insert supplier to update
        self.cur.execute("INSERT INTO supplier(invoice, name, contact, desc) VALUES(?, ?, ?, ?)",("3", "Old Name", "111", "Old desc"))
        self.con.commit()
        
        #updated data
        self.supplier_obj.var_sup_invoice.set("3")
        self.supplier_obj.var_name.set("Updated Name")
        self.supplier_obj.var_contact.set("999")
        self.supplier_obj.txt_desc.delete('1.0', END)
        self.supplier_obj.txt_desc.insert(END, "Updated description")
        

        mock_connect.return_value = self.con
        self.supplier_obj.update()
        
        #success message
        mock_showinfo.assert_called_once()
        self.assertIn("Updated", mock_showinfo.call_args[0][1])
        
        #Checking that update was successful
        self.cur.execute("SELECT * FROM supplier WHERE invoice=?", (3,))
        row = self.cur.fetchone()
        
        self.assertEqual(row[1], "Updated Name")
        self.assertEqual(row[2], "999")
    

    #Unit Test 4: Delete existing supplier
    @patch('supplier.messagebox.askyesno', return_value=True) #return true -> simulates user clicking yes
    @patch('supplier.messagebox.showinfo')
    @patch('supplier.sqlite3.connect')
    def test_delete_supplier_successfully(self, mock_connect, mock_showinfo, mock_askyesno):
        #Insert supplier to delete
        self.cur.execute("INSERT INTO supplier(invoice, name, contact, desc) VALUES(?, ?, ?, ?)",("4", "To Delete", "555", "Will be deleted"))
        self.con.commit()
        
        #invoice to delete
        self.supplier_obj.var_sup_invoice.set("4")
        
        mock_connect.return_value = self.con
        #delete method
        self.supplier_obj.delete()
        
        #confirm?
        mock_askyesno.assert_called_once()
        
        #success message
        mock_showinfo.assert_called_once()
        self.assertIn("Deleted", mock_showinfo.call_args[0][1])
        
        #Check that the supplier was deleted
        self.cur.execute("SELECT * FROM supplier WHERE invoice=?", (4,))
        row = self.cur.fetchone()
        
        self.assertIsNone(row)
    

    #Unit Test 5: Searching for a supplier by invoice number
    @patch('supplier.sqlite3.connect')
    def test_search_supplier_by_invoice(self, mock_connect):
        #Insert multiple suppliers
        self.cur.execute("INSERT INTO supplier(invoice, name, contact, desc) VALUES(?, ?, ?, ?)",("5", "Supplier One", "111", "First"))
        self.cur.execute("INSERT INTO supplier(invoice, name, contact, desc) VALUES(?, ?, ?, ?)",("6", "Supplier Two", "222", "Second"))
        self.con.commit()
        
        #search text
        self.supplier_obj.var_searchtxt.set("5")
        
        mock_connect.return_value = self.con
        self.supplier_obj.search()
        
        #table now has only the searched supplier
        table_items = self.supplier_obj.SupplierTable.get_children()
        self.assertEqual(len(table_items), 1)
        
        #CCheck that the correct data is ther
        values = self.supplier_obj.SupplierTable.item(table_items[0])['values']
        self.assertEqual(str(values[0]), "5")
        self.assertEqual(values[1], "Supplier One")



if __name__ == '__main__':
    #verbose output for the tests!!
    unittest.main(verbosity=2)
