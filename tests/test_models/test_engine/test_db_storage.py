#!/usr/bin/python3
""" Test for storage model """

import unittest
import os
import models
from models.receptionist import Receptionist


class TestDBStorage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set the environment to "testing"
        os.environ['CBASE_ENV'] = 'test'

    @classmethod
    def tearDownClass(cls):
        # Clean up after the test class
        del os.environ['CBASE_ENV']

    def test_all_method(self):
        # Test the 'all' method
        all_receptionists = models.storage.all(Receptionist)
        self.assertTrue(isinstance(all_receptionists, dict))

    def test_new_and_save_methods(self):
        # Test the 'new' and 'save' methods
        new_receptionist = Receptionist(name="John Doe",
                                        email="john@example.com",
                                        password="password")

        # Add the receptionist and save
        models.storage.new(new_receptionist)
        models.storage.save()

        # Check if the receptionist is in the database
        retrieved_receptionist = models.storage.get(Receptionist, new_receptionist.id)
        self.assertIsNotNone(retrieved_receptionist)

    def test_delete_method(self):
        # Test the 'delete' method
        new_receptionist = Receptionist(name="Jane Doe",
                                        email="jane@example.com",
                                        password="password")
        models.storage.new(new_receptionist)
        models.storage.save()

        # Delete the receptionist
        models.storage.delete(new_receptionist)
        models.storage.save()

        # Check if the receptionist is no longer in the database
        retrieved_receptionist = models.storage.get(Receptionist, new_receptionist.id)
        self.assertIsNone(retrieved_receptionist)

    def test_get_method(self):
        # Test the 'get' method
        new_receptionist = Receptionist(name="Alice Doe",
                                        email="alice@example.com",
                                        password="password")
        models.storage.new(new_receptionist)
        models.storage.save()

        # Retrieve the receptionist
        retrieved_receptionist = models.storage.get(Receptionist, new_receptionist.id)
        self.assertEqual(retrieved_receptionist, new_receptionist)

    def test_count_method(self):
        # Test the 'count' method
        count_receptionists = models.storage.count(Receptionist)
        self.assertEqual(count_receptionists, 0)  # No receptionists added yet

    def test_update_method(self):
        # Test the 'update' method
        new_receptionist = Receptionist(name="Original Name",
                                        email="original@example.com",
                                        password="password")
        models.storage.new(new_receptionist)
        models.storage.save()

        # Modify the receptionist's attributes
        new_receptionist.name = "Updated Name"
        new_receptionist.email = "updated@example.com"
        models.storage.save()

        # Retrieve the updated receptionist
        retrieved_receptionist = models.storage.get(Receptionist, new_receptionist.id)
        self.assertEqual(retrieved_receptionist.name, "Updated Name")
        self.assertEqual(retrieved_receptionist.email, "updated@example.com")

    def test_count_method_with_filter(self):
        # Test the 'count' method with a filter
        new_receptionist1 = Receptionist(name="Receptionist 1",
                                         email="receptionist1@example.com",
                                         password="password")
        new_receptionist2 = Receptionist(name="Receptionist 2",
                                         email="receptionist2@example.com",
                                         password="password")
        models.storage.new(new_receptionist1)
        models.storage.new(new_receptionist2)
        models.storage.save()

        # Count receptionists with a specific name
        count_receptionists = models.storage.count(Receptionist)
        self.assertEqual(count_receptionists, 2)  # 2 receptionists added

    def test_reload_method(self):
        # Test the 'reload' method
        original_session = models.storage._DBStorage__session

        # Reload the session
        models.storage.reload()
        reloaded_session = models.storage._DBStorage__session

        # Ensure the session was reloaded
        self.assertIsNot(original_session, reloaded_session)


if __name__ == "__main__":
    unittest.main()
