import json
from pathlib import Path

# Define paths
BASE_DIR = Path(__file__).parent
CARDS_JSON = BASE_DIR / "data" / "cards.json"
OUTPUT_JSON = BASE_DIR / "data" / "cards_ordered.json"

def load_cards(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def save_cards(cards, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump({"cards": cards}, f, indent=2, ensure_ascii=False)

def get_card_by_criteria(cards, suit=None, number=None, name=None):
    for card in cards:
        if suit and 'suit' in card and card['suit'] != suit:
            continue
        if number is not None and 'number' in card and card['number'] != number:
            continue
        if name and 'name' in card and card['name'] != name:
            continue
        return card
    return None

def create_placeholder_card(number, suit=None, name=None, element=None):
    card = {
        "keywords": [],
        "upright_meaning": "",
        "reversed_meaning": ""
    }
    
    if suit:
        # Fix court card naming
        if name and "of" in name:
            name = name.replace(f"of {suit.capitalize()} of {suit.capitalize()}", f"of {suit.capitalize()}")
        
        card.update({
            "number": number,
            "suit": suit,
            "name": name or f"{number} of {suit.capitalize()}",
            "element": element,
            "astrological": "TBD",
            "kabbalistic": "TBD",
            "decan": "TBD"
        })
    else:
        # Handle Major Arcana naming
        major_arcana_names = {
            "The 1": "The Magician",
            "The 2": "The High Priestess",
            "The 3": "The Empress",
            "The 4": "The Emperor",
            "The 5": "The Hierophant",
            "The 6": "The Lovers",
            "The 7": "The Chariot",
            "The 8": "Strength",
            "The 9": "The Hermit",
            "The 10": "Wheel of Fortune",
            "The 11": "Justice",
            "The 12": "The Hanged Man",
            "The 13": "Death",
            "The 14": "Temperance",
            "The 15": "The Devil",
            "The 16": "The Tower",
            "The 17": "The Star",
            "The 18": "The Moon",
            "The 19": "The Sun",
            "The 20": "Judgement",
            "The 21": "The World"
        }
        
        if name in major_arcana_names:
            name = major_arcana_names[name]
            
        card.update({
            "name": name,
            "element": "TBD",
            "astrological": "TBD",
            "kabbalistic": "TBD"
        })
    
    return card

def get_or_create_card(cards, suit=None, number=None, name=None, element=None):
    card = get_card_by_criteria(cards, suit, number, name)
    if not card:
        card = create_placeholder_card(number, suit, name, element)
        print(f"Created placeholder for: {card['name']}")
    return card

def reorder_cards(cards):
    ordered_cards = []
    elements = {
        "WANDS": "FIRE",
        "CUPS": "WATER",
        "SWORDS": "AIR",
        "PENTACLES": "EARTH"
    }
    
    # 1. Aces
    suits = ["WANDS", "CUPS", "SWORDS", "PENTACLES"]
    for suit in suits:
        ace = get_or_create_card(cards, suit=suit, number=1, element=elements[suit])
        ordered_cards.append(ace)
    
    # 2. Court Cards
    court_titles = ["Knight", "Queen", "King", "Princess"]
    for suit in suits:
        for title in court_titles:
            court_card = get_or_create_card(cards, suit=suit, name=f"{title} of {suit.capitalize()}", element=elements[suit])
            ordered_cards.append(court_card)
    
    # 3. Pip Cards in Book T sequence
    pip_sequence = [
        (5,7,"WANDS"), (8,10,"PENTACLES"), (2,4,"SWORDS"),
        (5,7,"CUPS"), (8,10,"WANDS"), (2,4,"PENTACLES"),
        (5,7,"SWORDS"), (8,10,"CUPS"), (2,4,"WANDS"),
        (5,7,"PENTACLES"), (8,10,"SWORDS"), (2,4,"CUPS")
    ]
    
    for start, end, suit in pip_sequence:
        for num in range(start, end + 1):
            card = get_or_create_card(cards, suit=suit, number=num, element=elements[suit])
            ordered_cards.append(card)
    
    # 4. Major Arcana
    major_sequence = ["The Fool"] + [f"The {i}" for i in range(1, 22)]
    for name in major_sequence:
        major = get_or_create_card(cards, name=name)
        ordered_cards.append(major)
    
    return ordered_cards

def main():
    try:
        # Load cards
        data = load_cards(CARDS_JSON)
        cards = data["cards"]
        
        # Reorder cards
        ordered_cards = reorder_cards(cards)
        
        # Save ordered cards
        save_cards(ordered_cards, OUTPUT_JSON)
        print(f"Successfully reordered {len(ordered_cards)} cards according to Book T sequence")
        print(f"Output saved to: {OUTPUT_JSON}")
        
    except FileNotFoundError:
        print(f"Error: Could not find {CARDS_JSON}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {CARDS_JSON}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()