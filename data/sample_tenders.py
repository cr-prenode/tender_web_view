import pandas as pd
from datetime import datetime, timedelta

def get_tenders():
    """
    Create and return a DataFrame of public tenders.
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
            "id": "TEN001",
            "title": "Road Infrastructure Development",
            "date": next_week_str,
            "activity_type": "Construction",
            "location": "Denver, Colorado",
            "difficulty": "Infrastructure",
            "duration": "24 months",
            "description": "Tender for the construction and maintenance of 15km of roadway infrastructure in the metropolitan area. Requires expertise in urban road development, traffic management systems, and sustainable construction practices.",
        },
        {
            "id": "TEN002",
            "title": "Medical Equipment Supply",
            "date": two_weeks_str,
            "activity_type": "Supply",
            "location": "Portland, Oregon",
            "difficulty": "Healthcare",
            "duration": "12 months",
            "description": "Supply of specialized medical equipment for regional hospitals. The tender covers diagnostic imaging equipment, patient monitoring systems, and laboratory equipment. Must meet ISO 13485 standards.",
        },
        {
            "id": "TEN003",
            "title": "IT Systems Modernization",
            "date": month_ahead_str,
            "activity_type": "IT Services",
            "location": "Billings, Montana",
            "difficulty": "Technology",
            "duration": "18 months",
            "description": "Complete modernization of government IT infrastructure, including hardware upgrades, software implementation, and staff training. The project aims to improve efficiency and cybersecurity across all departments.",
        },
        {
            "id": "TEN004",
            "title": "Renewable Energy Installation",
            "date": today_str,
            "activity_type": "Energy",
            "location": "Moab, Utah",
            "difficulty": "Environment",
            "duration": "36 months",
            "description": "Installation of solar panel arrays for public buildings. This project includes design, installation, maintenance, and integration with existing power systems. Must comply with local and federal renewable energy standards.",
        },
        {
            "id": "TEN005",
            "title": "Public School Renovation",
            "date": next_week_str,
            "activity_type": "Construction",
            "location": "Manchester, New Hampshire",
            "difficulty": "Education",
            "duration": "12 months",
            "description": "Comprehensive renovation of three public school buildings including modernization of classrooms, energy efficiency upgrades, and accessibility improvements. All work must be scheduled around school holidays.",
        },
        {
            "id": "TEN006",
            "title": "Wildlife Conservation Research",
            "date": two_weeks_str,
            "activity_type": "Research",
            "location": "Wyoming",
            "difficulty": "Environment",
            "duration": "48 months",
            "description": "Research program focused on wildlife conservation in protected areas. The project includes population monitoring, habitat assessment, and development of management recommendations for endangered species.",
        },
        {
            "id": "TEN007",
            "title": "Municipal Waste Management",
            "date": month_ahead_str,
            "activity_type": "Services",
            "location": "Seattle, Washington",
            "difficulty": "Environment",
            "duration": "60 months",
            "description": "Comprehensive waste management services for the metropolitan area, including collection, recycling, and disposal. Proposals must emphasize sustainable practices and include community education components.",
        },
        {
            "id": "TEN008",
            "title": "Public Transportation Network",
            "date": next_week_str,
            "activity_type": "Transport",
            "location": "Phoenix, Arizona",
            "difficulty": "Infrastructure",
            "duration": "36 months",
            "description": "Development of an integrated public transportation network connecting suburban areas to the city center. The project includes route planning, infrastructure development, and implementation of a smart ticketing system.",
        }
    ]
    
    # Create a DataFrame from the tenders data
    return pd.DataFrame(tenders_data)
