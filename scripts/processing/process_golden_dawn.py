# scripts/processing/process_golden_dawn.py                                                                                      
 import json                                                                                                                      
 from pathlib import Path                                                                                                         
 from typing import Dict, List, Optional                                                                                          
                                                                                                                                  
 from dotenv import load_dotenv                                                                                                   
 from PyPDF2 import PdfReader                                                                                                     
 from tqdm import tqdm                                                                                                            
                                                                                                                                  
 from src.tarotai.extensions.enrichment.knowledge.golden_dawn import (                                                            
     GoldenDawnKnowledge,                                                                                                         
     GoldenDawnKnowledgeBase,                                                                                                     
     GoldenDawnReadingMethod,                                                                                                     
     HistoricalApproach,                                                                                                          
     GoldenDawnLore                                                                                                               
 )                                                                                                                                
 from src.tarotai.ai.clients.providers.voyage import VoyageClient                                                                 
                                                                                                                                  
 load_dotenv()                                                                                                                    
                                                                                                                                  
 def process_golden_dawn_pdf(pdf_path: Path, output_dir: Path) -> Dict[str, Path]:                                                
     """Process the Golden Dawn PDF and save structured knowledge."""                                                             
     if not pdf_path.exists():                                                                                                    
         raise FileNotFoundError(f"Golden Dawn PDF not found at {pdf_path}")                                                      
                                                                                                                                  
     # Initialize AI clients                                                                                                      
     voyage_client = VoyageClient()                                                                                               
                                                                                                                                  
     # Create output directory                                                                                                    
     output_dir.mkdir(parents=True, exist_ok=True)                                                                                
                                                                                                                                  
     # Initialize knowledge base                                                                                                  
     knowledge_base = GoldenDawnKnowledgeBase(str(pdf_path), voyage_client)                                                       
                                                                                                                                  
     # Save processed data                                                                                                        
     output_files = {                                                                                                             
         "knowledge": output_dir / "golden_dawn_knowledge.json",                                                                  
         "images": output_dir / "golden_dawn_images.json",                                                                        
         "embeddings": output_dir / "golden_dawn_embeddings.json"                                                                 
     }                                                                                                                            
                                                                                                                                  
     # Save knowledge                                                                                                             
     with open(output_files["knowledge"], "w") as f:                                                                              
         json.dump(knowledge_base.knowledge.dict(), f, indent=2)                                                                  
                                                                                                                                  
     # Save image data if available                                                                                               
     if hasattr(knowledge_base, "image_embeddings"):                                                                              
         with open(output_files["images"], "w") as f:                                                                             
             json.dump(knowledge_base.image_embeddings, f, indent=2)                                                              
                                                                                                                                  
     # Save embeddings                                                                                                            
     with open(output_files["embeddings"], "w") as f:                                                                             
         json.dump({                                                                                                              
             "text_embeddings": knowledge_base.embeddings,                                                                        
             "version": knowledge_base.version                                                                                    
         }, f, indent=2)                                                                                                          
                                                                                                                                  
     return output_files                                                                                                          
                                                                                                                                  
 def main():                                                                                                                      
     # Paths                                                                                                                      
     pdf_path = Path("data/golden_dawn.pdf")                                                                                      
     output_dir = Path("data/processed/golden_dawn")                                                                              
                                                                                                                                  
     print(f"Processing Golden Dawn PDF at {pdf_path}...")                                                                        
     try:                                                                                                                         
         output_files = process_golden_dawn_pdf(pdf_path, output_dir)                                                             
         print("\nProcessing complete! Output files:")                                                                            
         for name, path in output_files.items():                                                                                  
             print(f"- {name}: {path}")                                                                                           
     except Exception as e:                                                                                                       
         print(f"\nError processing PDF: {str(e)}")                                                                               
         raise                                                                                                                    
                                                                                                                                  
 if __name__ == "__main__":                                                                                                       
     main()                      