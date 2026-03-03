import unittest
import sqlite3
import os
from unittest.mock import patch, MagicMock
from tkinter import Tk
from login import Login_System
from create_db import create_db

"""
The unit tests in this file are for testing the newly implemented login functionality.
The new tests test the access rights of the login function and also basic login functionality.
The implemented tests test the following:

Test 1: Admins can login to the dashboard 
Test 2: Admin can login to billing 
Test 3: Employee account can login to billing 
Test 4: Employee account can not login to the dashboard 
Test 5: Invalid password -> cannot login -> “Invalid email or password” message 
"""


class TestLogin(unittest.TestCase):
     
    #Creating a test database once before all tests
    @classmethod
    def setUpClass(cls):
        cls.test_db = 'test_login_ims.db'
        #Using the real create_db function to ensure test database matches production schema
        create_db(db_name=cls.test_db) #this name differentiates this test database from the real one so we don't affect with real data during testing
        #Not keeping a connection open at class level since each test creates its own
    
    #Setting up login object before each test
    def setUp(self):
        #Creating a fresh connection for this test since login.py closes it
        self.test_con = sqlite3.connect(self.test_db)#this is very important because otherwise the connection would be closed after first test and all the other tests would fail!!!
        
        #tkinter root window 
        self.root = Tk()
        self.root.withdraw()  #Hiding the window during testing so I don't have to click them during runtime
        
        self.login_obj = Login_System(self.root)
    
    #Cleaning up after each test
    def tearDown(self):
        self.root.destroy()
    
    #Deleting the entire testing database after all tests have run
    @classmethod
    def tearDownClass(cls):
        #no need to close the connection because each test creates its own and login.py closes it after eeach test
        if os.path.exists(cls.test_db):
            os.remove(cls.test_db)
    

#------------------------------------------------------------------------------------------------------------
    #Unit Test 1: Admin user logs in successfully and opens Dashboard
    @patch('login.Login_System.open_dashboard')
    @patch('login.messagebox.showinfo')
    @patch('login.sqlite3.connect')
    def test_admin_login_dashboard_successfully(self, mock_connect, mock_showinfo, mock_open_dashboard):
        #test data for admin user
        self.login_obj.var_email.set("admin@admin.com")
        self.login_obj.var_password.set("123456" )
        self.login_obj.var_destination.set("Dashboard")
        
        #Mock database connection uses test database
        mock_connect.return_value = self.test_con
        
        #Mock root.destroy to prevent actual window closure
        self.login_obj.root.destroy = MagicMock()
        
        self.login_obj.login() 
        
        #success message was shown?
        mock_showinfo.assert_called_once()
        self.assertIn("Login successful", mock_showinfo.call_args[0][1])
        
        #dashboard was opened?
        mock_open_dashboard.assert_called_once()
        
        #window was destroyed?
        self.login_obj.root.destroy.assert_called_once()


    #Unit Test 2: Admin user logs in successfully and opens Billing
    @patch('login.Login_System.open_billing')
    @patch('login.messagebox.showinfo')
    @patch('login.sqlite3.connect')
    def test_admin_login_billing_successfully(self, mock_connect, mock_showinfo, mock_open_billing):
        #test data for admin user
        self.login_obj.var_email.set("admin@admin.com")
        self.login_obj.var_password.set( "123456")
        self.login_obj.var_destination.set("Billing")
        
        #Mock database connection uses test database
        mock_connect.return_value = self.test_con
        
        #Mock root.destroy to prevent actual window closure
        self.login_obj.root.destroy = MagicMock()
        
        self.login_obj.login()
        
        #success message was shown?
        mock_showinfo.assert_called_once()
        self.assertIn("Login successful", mock_showinfo.call_args[0][1])
        
        #billing was opened?
        mock_open_billing.assert_called_once()
        
        #window was destroyed?
        self.login_obj.root.destroy.assert_called_once()


    #Unit Test 3: Employee user logs in successfully and opens Billing 
    @patch('login.Login_System.open_billing')
    @patch('login.messagebox.showinfo')
    @patch('login.sqlite3.connect')
    def test_employee_login_billing_successfully(self, mock_connect, mock_showinfo, mock_open_billing):
        #test data for employee user 
        self.login_obj.var_email.set("employee@employee.com")
        self.login_obj.var_password.set("123456")
        self.login_obj.var_destination.set("Billing")
        
        #Mock database connection uses test database
        mock_connect.return_value = self.test_con
        
        #Mock root.destroy to prevent actual window closure
        self.login_obj.root.destroy = MagicMock()
        
        self.login_obj.login()
        
        #success message was shown?
        mock_showinfo.assert_called_once()
        self.assertIn("Login successful", mock_showinfo.call_args[0][1])
        
        #billing was opened? 
        mock_open_billing.assert_called_once()
        
        #window was destroyed?
        self.login_obj.root.destroy.assert_called_once() 


    #Unit Test 4: Employee user cannot access Dashboard (access denied)
    @patch('login.messagebox.showerror')
    @patch('login.sqlite3.connect')
    def test_employee_login_dashboard_denied(self, mock_connect, mock_showerror):
        #test data for employee trying to access dashboard
        self.login_obj.var_email.set("employee@employee.com")
        self.login_obj.var_password.set("123456")
        self.login_obj.var_destination.set("Dashboard")
        
        #Mock database connection uses test database
        mock_connect.return_value = self.test_con
        
        self.login_obj.login()
        
        #access denied error was shown?
        mock_showerror.assert_called_once()
        self.assertIn("Access Denied", mock_showerror.call_args[0][0])
        self.assertIn("Admin users only", mock_showerror.call_args[0][1])


    #Unit Test 5: Login fails with invalid credentials
    @patch('login.messagebox.showerror')
    @patch('login.sqlite3.connect')
    def test_login_invalid_credentials(self, mock_connect, mock_showerror):
        #test data with wrong password
        self.login_obj.var_email.set("admin@admin.com")
        self.login_obj.var_password.set("wrongpassword")
        self.login_obj.var_destination.set("Dashboard")
        
        #Mock database connection uses test database
        mock_connect.return_value = self.test_con
        
        self.login_obj.login()
        
        #error message was shown?
        mock_showerror.assert_called_once()
        self.assertIn("Invalid email or password", mock_showerror.call_args[0][1])



if __name__ == '__main__':
    #verbose output for the tests!!
    unittest.main(verbosity=2)
