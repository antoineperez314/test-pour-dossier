#!/usr/bin/env python3
"""
Simple user feedback collection system.
Allows users to submit feedback with a rating and comments.
"""

import json
import os
from datetime import datetime
from typing import Dict, List


class FeedbackSystem:
    """A simple feedback collection system."""
    
    def __init__(self, storage_file: str = "feedback_data.json"):
        """Initialize the feedback system.
        
        Args:
            storage_file: Path to the JSON file for storing feedback.
        """
        self.storage_file = storage_file
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Create storage file if it doesn't exist."""
        if not os.path.exists(self.storage_file):
            with open(self.storage_file, 'w') as f:
                json.dump([], f)
    
    def submit_feedback(self, rating: int, comment: str, user_name: str = "Anonymous") -> bool:
        """Submit user feedback.
        
        Args:
            rating: Rating from 1 to 5.
            comment: User's feedback comment.
            user_name: Name of the user (optional).
            
        Returns:
            True if feedback was successfully submitted.
        """
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        
        feedback_entry = {
            "id": self._generate_id(),
            "timestamp": datetime.now().isoformat(),
            "rating": rating,
            "comment": comment,
            "user_name": user_name
        }
        
        feedbacks = self._load_feedbacks()
        feedbacks.append(feedback_entry)
        self._save_feedbacks(feedbacks)
        
        return True
    
    def get_all_feedbacks(self) -> List[Dict]:
        """Get all submitted feedbacks.
        
        Returns:
            List of feedback entries.
        """
        return self._load_feedbacks()
    
    def get_average_rating(self) -> float:
        """Calculate the average rating from all feedbacks.
        
        Returns:
            Average rating, or 0.0 if no feedbacks exist.
        """
        feedbacks = self._load_feedbacks()
        if not feedbacks:
            return 0.0
        
        total_rating = sum(f["rating"] for f in feedbacks)
        return total_rating / len(feedbacks)
    
    def _generate_id(self) -> str:
        """Generate a unique ID for feedback entry."""
        feedbacks = self._load_feedbacks()
        return str(len(feedbacks) + 1)
    
    def _load_feedbacks(self) -> List[Dict]:
        """Load feedbacks from storage file."""
        with open(self.storage_file, 'r') as f:
            return json.load(f)
    
    def _save_feedbacks(self, feedbacks: List[Dict]):
        """Save feedbacks to storage file."""
        with open(self.storage_file, 'w') as f:
            json.dump(feedbacks, f, indent=2)


def main():
    """Interactive CLI for feedback system."""
    system = FeedbackSystem()
    
    print("=== User Feedback System ===")
    print("1. Submit feedback")
    print("2. View all feedbacks")
    print("3. View average rating")
    print("4. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == "1":
            try:
                name = input("Your name (or press Enter for Anonymous): ").strip() or "Anonymous"
                rating = int(input("Rating (1-5): ").strip())
                comment = input("Your feedback: ").strip()
                
                system.submit_feedback(rating, comment, name)
                print("✓ Feedback submitted successfully!")
            except ValueError as e:
                print(f"✗ Error: {e}")
            except Exception as e:
                print(f"✗ An error occurred: {e}")
        
        elif choice == "2":
            feedbacks = system.get_all_feedbacks()
            if not feedbacks:
                print("No feedbacks yet.")
            else:
                print(f"\n=== All Feedbacks ({len(feedbacks)} total) ===")
                for fb in feedbacks:
                    print(f"\nID: {fb['id']}")
                    print(f"User: {fb['user_name']}")
                    print(f"Rating: {'⭐' * fb['rating']} ({fb['rating']}/5)")
                    print(f"Comment: {fb['comment']}")
                    print(f"Date: {fb['timestamp']}")
        
        elif choice == "3":
            avg = system.get_average_rating()
            count = len(system.get_all_feedbacks())
            print(f"\nAverage Rating: {avg:.2f}/5.00 (from {count} feedbacks)")
        
        elif choice == "4":
            print("Thank you for using the Feedback System!")
            break
        
        else:
            print("Invalid choice. Please enter 1-4.")


if __name__ == "__main__":
    main()
