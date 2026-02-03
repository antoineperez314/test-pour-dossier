#!/usr/bin/env python3
"""
Unit tests for the feedback system.
"""

import json
import os
import tempfile
import unittest
from feedback import FeedbackSystem


class TestFeedbackSystem(unittest.TestCase):
    """Test cases for FeedbackSystem."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.temp_file.write('[]')
        self.temp_file.close()
        self.system = FeedbackSystem(storage_file=self.temp_file.name)
    
    def tearDown(self):
        """Clean up test fixtures."""
        # Remove temporary file
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)
    
    def test_submit_feedback_success(self):
        """Test successful feedback submission."""
        result = self.system.submit_feedback(5, "Great experience!", "John Doe")
        self.assertTrue(result)
        
        feedbacks = self.system.get_all_feedbacks()
        self.assertEqual(len(feedbacks), 1)
        self.assertEqual(feedbacks[0]["rating"], 5)
        self.assertEqual(feedbacks[0]["comment"], "Great experience!")
        self.assertEqual(feedbacks[0]["user_name"], "John Doe")
    
    def test_submit_feedback_invalid_rating(self):
        """Test feedback submission with invalid rating."""
        with self.assertRaises(ValueError):
            self.system.submit_feedback(0, "Bad rating")
        
        with self.assertRaises(ValueError):
            self.system.submit_feedback(6, "Too high rating")
    
    def test_submit_multiple_feedbacks(self):
        """Test submitting multiple feedbacks."""
        self.system.submit_feedback(5, "Excellent!", "User1")
        self.system.submit_feedback(4, "Good", "User2")
        self.system.submit_feedback(3, "Average", "User3")
        
        feedbacks = self.system.get_all_feedbacks()
        self.assertEqual(len(feedbacks), 3)
    
    def test_get_average_rating_empty(self):
        """Test average rating with no feedbacks."""
        avg = self.system.get_average_rating()
        self.assertEqual(avg, 0.0)
    
    def test_get_average_rating(self):
        """Test average rating calculation."""
        self.system.submit_feedback(5, "Great")
        self.system.submit_feedback(3, "OK")
        self.system.submit_feedback(4, "Good")
        
        avg = self.system.get_average_rating()
        self.assertEqual(avg, 4.0)
    
    def test_feedback_persistence(self):
        """Test that feedbacks are persisted to file."""
        self.system.submit_feedback(5, "Test feedback")
        
        # Create a new system instance with the same file
        new_system = FeedbackSystem(storage_file=self.temp_file.name)
        feedbacks = new_system.get_all_feedbacks()
        
        self.assertEqual(len(feedbacks), 1)
        self.assertEqual(feedbacks[0]["comment"], "Test feedback")
    
    def test_feedback_has_timestamp(self):
        """Test that feedback entries have timestamps."""
        self.system.submit_feedback(5, "Test")
        feedbacks = self.system.get_all_feedbacks()
        
        self.assertIn("timestamp", feedbacks[0])
        self.assertIsInstance(feedbacks[0]["timestamp"], str)
    
    def test_feedback_has_unique_id(self):
        """Test that feedback entries have unique IDs."""
        self.system.submit_feedback(5, "First")
        self.system.submit_feedback(4, "Second")
        
        feedbacks = self.system.get_all_feedbacks()
        ids = [fb["id"] for fb in feedbacks]
        
        self.assertEqual(len(ids), len(set(ids)))  # All IDs should be unique


if __name__ == "__main__":
    unittest.main()
