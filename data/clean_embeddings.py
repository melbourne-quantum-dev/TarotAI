import json                                                                                    
from pathlib import Path                                                                       
                                                                                                
def clean_embeddings(card_data):                                                               
     """Remove 0.0 placeholder embeddings from a card's data."""                                
     if "embeddings" in card_data:                                                              
         for orientation in ["upright", "reversed"]:                                            
             if orientation in card_data["embeddings"]:                                         
                 # Remove all 0.0 values from the embeddings list                               
                 card_data["embeddings"][orientation] = [                                       
                     val for val in card_data["embeddings"][orientation] if val != 0.0          
                 ]                                                                              
     return card_data                                                                           
                                                                                                
def process_file(input_file, output_file=None):                                                
     """Process the JSON file to remove 0.0 embeddings."""                                      
     if output_file is None:                                                                    
         output_file = input_file  # Overwrite the input file by default                        
                                                                                                
     # Load the data                                                                            
     with open(input_file, "r", encoding="utf-8") as f:                                         
         data = json.load(f)                                                                    
                                                                                                
     # Clean each card's embeddings                                                             
     if "cards" in data:                                                                        
         data["cards"] = [clean_embeddings(card) for card in data["cards"]]                     
                                                                                                
     # Save the cleaned data                                                                    
     with open(output_file, "w", encoding="utf-8") as f:                                        
         json.dump(data, f, indent=2, ensure_ascii=False)                                       
                                                                                                
     print(f"Processed file saved to: {output_file}")                                           
                                                                                                
if __name__ == "__main__":                                                                     
     # Path to your cards_ordered.json file                                                     
     input_file = Path("data/cards_ordered.json")                                               
                                                                                                
     # Process the file (this will overwrite the original file)                                 
     process_file(input_file)   