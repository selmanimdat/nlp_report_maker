import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

TURKISH_MONTHS = {
    "Ocak": "01",
    "Şubat": "02",
    "Mart": "03",
    "Nisan": "04",
    "Mayıs": "05",
    "Haziran": "06",
    "Temmuz": "07",
    "Ağustos": "08",
    "Eylül": "09",
    "Ekim": "10",
    "Kasım": "11",
    "Aralık": "12"
}

def parse_turkish_date(date_str, default_year=None):
    """
    Parses a date string like '16 Ocak 10:23' into 'YYYY-MM-DD'.
    Assumes current year if not present.
    """
    if not date_str:
        return datetime.now().strftime("%Y-%m-%d")

    try:
        if default_year is None:
            default_year = datetime.now().year

        parts = date_str.strip().split()
        # Expected formats: "16 Ocak 10:23", "16 Ocak 2024", etc.
        # We need "day month" at minimum.
        
        if len(parts) < 2:
             return datetime.now().strftime("%Y-%m-%d")

        day = parts[0].zfill(2)
        month_name = parts[1]
        
        month = TURKISH_MONTHS.get(month_name, "01")
        
        # Check if year is explicitly in the string (unlikely in the sample "16 Ocak 10:23")
        # But let's build ISO date
        
        return f"{default_year}-{month}-{day}"
    except Exception as e:
        logger.warning(f"Failed to parse date '{date_str}': {e}")
        return datetime.now().strftime("%Y-%m-%d")

def load_scraped_data(file_path):
    """
    Loads scraped data from JSON and transforms it to the system's input schema.
    """
    logger.info(f"Loading scraped data from {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error(f"Scraped file not found: {file_path}")
        return None
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in: {file_path}")
        return None

    transformed_comments = []
    
    # Check if data is list or wrapped
    items = data if isinstance(data, list) else data.get('items', [])
    
    for idx, item in enumerate(items):
        comment = {
            "id": idx + 1,
            "text": item.get("text", ""),
            "platform": "sikayetvar", # Since source is known
            "date": parse_turkish_date(item.get("date"))
        }
        transformed_comments.append(comment)

    # Determine brand/goal if possible, or use defaults/from args
    # For now, we return just the comments list and maybe basic metdata
    # The caller (main) should merge this with a base schema or defaults
    
    result = {
        "comments": transformed_comments
    }
    
    # Try to infer brand from first item if available
    if items and "company" in items[0]:
        result["brand"] = items[0]["company"]
        
    return result
