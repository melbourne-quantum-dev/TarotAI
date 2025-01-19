#!/usr/bin/env python3
"""Extract Golden Dawn tarot correspondences from PDF source."""

import json
import logging
from pathlib import Path
import sys
from typing import Dict, List, Any, Optional
import PyPDF2
from datetime import datetime
import signal

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GoldenDawnExtractor:
    """Extract and process Golden Dawn correspondences from PDF."""
    
    def __init__(self, pdf_path: Path):
        self.pdf_path = pdf_path
        self.page_cache: Dict[int, str] = {}
        self.major_arcana: List[Dict[str, Any]] = []
        self.minor_arcana: List[Dict[str, Any]] = []
        
    def extract_text_from_page(self, page_num: int) -> str:
        """Extract text from a PDF page with caching."""
        if page_num in self.page_cache:
            return self.page_cache[page_num]
        
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                if page_num < len(pdf_reader.pages):
                    text = pdf_reader.pages[page_num].extract_text()
                    self.page_cache[page_num] = text
                    return text
        except Exception as e:
            logger.error(f"Error reading page {page_num}: {str(e)}")
        return ""

    def find_section_boundaries(self) -> Dict[str, tuple]:
        """Find major section boundaries in the PDF."""
        sections = {}
        current_page = 0
        
        while current_page < self.get_total_pages():
            text = self.extract_text_from_page(current_page)
            
            # Look for major section markers
            if "Major Arcana" in text:
                sections['major_arcana'] = (current_page, None)
            elif "Minor Arcana" in text:
                if 'major_arcana' in sections and sections['major_arcana'][1] is None:
                    sections['major_arcana'] = (sections['major_arcana'][0], current_page)
                sections['minor_arcana'] = (current_page, None)
            
            current_page += 1
        
        # Close any open sections
        if 'minor_arcana' in sections and sections['minor_arcana'][1] is None:
            sections['minor_arcana'] = (sections['minor_arcana'][0], current_page)
        
        return sections

    def extract_major_arcana(self, start_page: int, end_page: int) -> List[Dict[str, Any]]:
        """Extract Major Arcana cards and their correspondences."""
        cards = []
        current_card: Optional[Dict[str, Any]] = None
        
        for page in range(start_page, end_page):
            text = self.extract_text_from_page(page)
            lines = text.split('\n')
            
            for line in lines:
                # Look for card titles
                if any(numeral in line for numeral in ['0.', 'I.', 'II.', 'III.']):
                    if current_card:
                        cards.append(current_card)
                    current_card = {
                        'name': '',
                        'number': 0,
                        'hebrew_letter': '',
                        'title': '',
                        'meanings': {'upright': [], 'reversed': []}
                    }
                
                # Process line content for current card
                if current_card:
                    self.process_major_arcana_line(line, current_card)
        
        if current_card:
            cards.append(current_card)
        
        return cards

    def process_major_arcana_line(self, line: str, card: Dict[str, Any]) -> None:
        """Process a line of text for Major Arcana card details."""
        line = line.strip()
        
        # Match patterns for different types of information
        if 'Hebrew Letter:' in line:
            card['hebrew_letter'] = line.split(':')[1].strip()
        elif 'Title:' in line:
            card['title'] = line.split(':')[1].strip()
        elif 'Meanings:' in line:
            meanings = line.split(':')[1].strip()
            if 'Upright' in meanings:
                card['meanings']['upright'] = [m.strip() for m in meanings.split(',')]
            elif 'Reversed' in meanings:
                card['meanings']['reversed'] = [m.strip() for m in meanings.split(',')]

    def extract_minor_arcana(self, start_page: int, end_page: int) -> List[Dict[str, Any]]:
        """Extract Minor Arcana cards and their correspondences."""
        suits = []
        current_suit: Optional[Dict[str, Any]] = None
        
        for page in range(start_page, end_page):
            text = self.extract_text_from_page(page)
            lines = text.split('\n')
            
            for line in lines:
                # Look for suit headers
                if any(suit in line for suit in ['Wands', 'Cups', 'Swords', 'Pentacles']):
                    if current_suit:
                        suits.append(current_suit)
                    current_suit = {
                        'suit': line.split()[0].lower(),
                        'element': '',
                        'cards': []
                    }
                
                # Process line content for current suit
                if current_suit:
                    self.process_minor_arcana_line(line, current_suit)
        
        if current_suit:
            suits.append(current_suit)
        
        return suits

    def process_minor_arcana_line(self, line: str, suit: Dict[str, Any]) -> None:
        """Process a line of text for Minor Arcana card details."""
        line = line.strip()
        
        # Match patterns for different types of information
        if 'Element:' in line:
            suit['element'] = line.split(':')[1].strip().upper()
        elif any(rank in line for rank in ['Ace', 'Two', 'Three', 'King', 'Queen', 'Knight', 'Page']):
            card = {
                'name': f"{line.split()[0]} of {suit['suit'].capitalize()}",
                'number': self.rank_to_number(line.split()[0]),
                'meanings': {'upright': [], 'reversed': []}
            }
            suit['cards'].append(card)

    @staticmethod
    def rank_to_number(rank: str) -> int:
        """Convert rank to numeric value."""
        ranks = {
            'Ace': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5,
            'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
            'Page': 11, 'Knight': 12, 'Queen': 13, 'King': 14
        }
        return ranks.get(rank, 0)

    def get_total_pages(self) -> int:
        """Get total number of pages in PDF with timeout protection."""
        try:
            with open(self.pdf_path, 'rb') as file:
                # Add timeout protection
                def timeout_handler(signum, frame):
                    raise TimeoutError("PDF processing took too long")
                
                signal.signal(signal.SIGALRM, timeout_handler)
                signal.alarm(5)  # 5 second timeout
                
                try:
                    pages = len(PyPDF2.PdfReader(file).pages)
                    signal.alarm(0)  # Disable alarm
                    return pages
                except TimeoutError:
                    logger.error("PDF processing timed out - file may be corrupted")
                    return 0
                finally:
                    signal.alarm(0)  # Ensure alarm is disabled
        except Exception as e:
            logger.error(f"Error getting page count: {str(e)}")
            return 0

    def extract_all(self) -> Dict[str, Any]:
        """Extract all Golden Dawn correspondences."""
        sections = self.find_section_boundaries()
        
        if 'major_arcana' in sections:
            self.major_arcana = self.extract_major_arcana(*sections['major_arcana'])
        
        if 'minor_arcana' in sections:
            self.minor_arcana = self.extract_minor_arcana(*sections['minor_arcana'])
        
        return {
            'version': '1.0.0',
            'source': 'Golden Dawn Tradition',
            'last_updated': datetime.now().isoformat(),
            'major_arcana': self.major_arcana,
            'minor_arcana': self.minor_arcana
        }

def main() -> int:
    """Main entry point."""
    try:
        pdf_path = Path(__file__).parent.parent.parent / 'data' / 'golden_dawn.pdf'
        output_path = pdf_path.parent / 'golden_dawn.json'
        
        logger.info(f"Processing Golden Dawn PDF: {pdf_path}")
        extractor = GoldenDawnExtractor(pdf_path)
        data = extractor.extract_all()
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        logger.info(f"✨ Extraction complete! Output saved to: {output_path}")
        return 0
        
    except Exception as e:
        logger.error(f"Extraction failed: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())