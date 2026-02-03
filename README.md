# test-pour-dossier

A simple user feedback collection system that allows users to submit feedback with ratings and comments.

## Features

- Submit feedback with ratings (1-5 stars)
- Add comments and user names
- View all submitted feedbacks
- Calculate average ratings
- Persistent storage using JSON

## Installation

No external dependencies required. Uses only Python standard library.

```bash
python3 feedback.py
```

## Usage

### Interactive CLI

Run the feedback system interactively:

```bash
python3 feedback.py
```

This will present you with a menu to:
1. Submit feedback
2. View all feedbacks
3. View average rating
4. Exit

### Programmatic Usage

You can also use the `FeedbackSystem` class in your own code:

```python
from feedback import FeedbackSystem

# Create a feedback system instance
system = FeedbackSystem()

# Submit feedback
system.submit_feedback(
    rating=5,
    comment="Great experience!",
    user_name="John Doe"
)

# Get all feedbacks
feedbacks = system.get_all_feedbacks()

# Get average rating
avg_rating = system.get_average_rating()
print(f"Average rating: {avg_rating:.2f}/5.00")
```

## Running Tests

Run the test suite:

```bash
python3 test_feedback.py
```

Or with verbose output:

```bash
python3 test_feedback.py -v
```

## Data Storage

Feedback data is stored in `feedback_data.json` in the same directory. The file is automatically created on first use.
