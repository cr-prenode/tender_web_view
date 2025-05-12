import pandas as pd
from datetime import datetime, timedelta

def get_tenders():
    """
    Create and return a DataFrame of adventure tenders.
    This is representative of what would typically come from a database or API.
    """
    # Calculate dates relative to today
    today = datetime.now().date()
    next_week = today + timedelta(days=7)
    two_weeks = today + timedelta(days=14)
    month_ahead = today + timedelta(days=30)
    
    # Format the dates as strings
    today_str = today.strftime('%Y-%m-%d')
    next_week_str = next_week.strftime('%Y-%m-%d')
    two_weeks_str = two_weeks.strftime('%Y-%m-%d')
    month_ahead_str = month_ahead.strftime('%Y-%m-%d')
    
    # Create the tenders data
    tenders_data = [
        {
            "id": "ADV001",
            "title": "Rocky Mountain Trail Photography",
            "date": next_week_str,
            "activity_type": "Hiking",
            "location": "Rocky Mountains, Colorado",
            "difficulty": "Moderate",
            "duration": "2 days",
            "description": "Join us for a photography-focused hiking adventure through the stunning Rocky Mountains. This trip is perfect for photography enthusiasts who want to capture the majestic landscapes and wildlife. Professional guide included.",
        },
        {
            "id": "ADV002",
            "title": "Coastal Sunset Photography",
            "date": two_weeks_str,
            "activity_type": "Photography",
            "location": "Pacific Coast, Oregon",
            "difficulty": "Easy",
            "duration": "1 day",
            "description": "Capture the breathtaking sunsets along the Oregon coast. This tender offers transportation to the best spots for sunset photography, with tips from an experienced landscape photographer.",
        },
        {
            "id": "ADV003",
            "title": "Alpine Lake Camping",
            "date": month_ahead_str,
            "activity_type": "Camping",
            "location": "Glacier National Park, Montana",
            "difficulty": "Hard",
            "duration": "3 days",
            "description": "Experience the serene beauty of Alpine lakes with this camping adventure. Hike to remote lakes and set up camp with magnificent views. Great opportunities for astrophotography and nature shots.",
        },
        {
            "id": "ADV004",
            "title": "Desert Night Sky Photography",
            "date": today_str,
            "activity_type": "Photography",
            "location": "Arches National Park, Utah",
            "difficulty": "Moderate",
            "duration": "2 days",
            "description": "Photograph the stars and iconic rock formations in Arches National Park. This adventure includes transportation, expert guidance on night photography techniques, and camping equipment.",
        },
        {
            "id": "ADV005",
            "title": "Autumn Foliage Tour",
            "date": next_week_str,
            "activity_type": "Hiking",
            "location": "White Mountains, New Hampshire",
            "difficulty": "Easy",
            "duration": "1 day",
            "description": "Experience the vibrant colors of autumn in the White Mountains. This guided hiking tour takes you to the best spots for capturing fall foliage at its peak, with professional tips on seasonal photography.",
        },
        {
            "id": "ADV006",
            "title": "Wildlife Safari Adventure",
            "date": two_weeks_str,
            "activity_type": "Wildlife",
            "location": "Yellowstone National Park, Wyoming",
            "difficulty": "Moderate",
            "duration": "4 days",
            "description": "Join this wildlife photography expedition in Yellowstone. Learn techniques for capturing wildlife in their natural habitat, with special focus on bison, elk, and potentially wolves and bears from a safe distance.",
        },
        {
            "id": "ADV007",
            "title": "Extreme Mountain Expedition",
            "date": month_ahead_str,
            "activity_type": "Climbing",
            "location": "Mount Rainier, Washington",
            "difficulty": "Expert",
            "duration": "5 days",
            "description": "For experienced climbers only! This challenging expedition takes you to breathtaking vantage points for photography at high altitudes. Includes professional climbing guides and specialized equipment.",
        },
        {
            "id": "ADV008",
            "title": "Canyon River Rafting",
            "date": next_week_str,
            "activity_type": "Water Sports",
            "location": "Grand Canyon, Arizona",
            "difficulty": "Hard",
            "duration": "3 days",
            "description": "Combine the thrill of white-water rafting with photography in the majestic Grand Canyon. Waterproof camera equipment recommendations provided. Experienced rafting guides will ensure your safety.",
        }
    ]
    
    # Create a DataFrame from the tenders data
    return pd.DataFrame(tenders_data)
