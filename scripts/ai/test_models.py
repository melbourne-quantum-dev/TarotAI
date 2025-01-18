#!/usr/bin/env python3
"""
AI Model Testing and Benchmarking Script
"""
import asyncio
import json
from pathlib import Path
from typing import Dict, List

from rich.console import Console
from rich.table import Table

from tarotai.ai.clients import initialize_ai_clients
from tarotai.config import get_config
from tarotai.core.logging import setup_logging

# Setup logging
logger = setup_logging()
console = Console()

TEST_PROMPTS = [
    {
        "type": "interpretation",
        "prompt": "Interpret the Fool card in a career reading",
        "expected": ["beginnings", "risk", "potential"]
    },
    {
        "type": "embedding",
        "text": "The Magician represents skill and manifestation",
        "expected_length": 1024
    },
    {
        "type": "conversation",
        "messages": [{"role": "user", "content": "Explain the meaning of the Tower"}],
        "expected": ["sudden change", "upheaval", "revelation"]
    }
]

async def test_model(client_name: str, client: Any, results: Dict) -> None:
    """Run standardized tests on a single AI client"""
    client_results = {
        "passed": 0,
        "failed": 0,
        "errors": 0,
        "details": []
    }
    
    try:
        # Test interpretation
        interpretation = await client.generate_response(
            TEST_PROMPTS[0]["prompt"]
        )
        if all(kw in interpretation.lower() for kw in TEST_PROMPTS[0]["expected"]):
            client_results["passed"] += 1
            client_results["details"].append("Interpretation test passed")
        else:
            client_results["failed"] += 1
            client_results["details"].append("Interpretation test failed")
            
        # Test embeddings
        embedding = await client.generate_embedding(
            TEST_PROMPTS[1]["text"]
        )
        if len(embedding) == TEST_PROMPTS[1]["expected_length"]:
            client_results["passed"] += 1
            client_results["details"].append("Embedding test passed")
        else:
            client_results["failed"] += 1
            client_results["details"].append("Embedding test failed")
            
        # Test conversation
        conversation = await client.conversational_prompt(
            TEST_PROMPTS[2]["messages"]
        )
        if all(kw in conversation.lower() for kw in TEST_PROMPTS[2]["expected"]):
            client_results["passed"] += 1
            client_results["details"].append("Conversation test passed")
        else:
            client_results["failed"] += 1
            client_results["details"].append("Conversation test failed")
            
    except Exception as e:
        client_results["errors"] += 1
        client_results["details"].append(f"Error during testing: {str(e)}")
        logger.error(f"Error testing {client_name}: {str(e)}")
        
    results[client_name] = client_results

def display_results(results: Dict) -> None:
    """Display test results in a formatted table"""
    table = Table(title="AI Model Test Results", show_header=True)
    table.add_column("Model", style="cyan")
    table.add_column("Passed", justify="right")
    table.add_column("Failed", justify="right")
    table.add_column("Errors", justify="right")
    
    for client_name, result in results.items():
        table.add_row(
            client_name,
            str(result["passed"]),
            str(result["failed"]),
            str(result["errors"])
        )
        
    console.print(table)
    
    # Show details
    for client_name, result in results.items():
        console.print(f"\n[bold]{client_name} Details:[/]")
        for detail in result["details"]:
            console.print(f"  - {detail}")

async def main():
    """Main testing function"""
    try:
        # Initialize clients
        config = get_config()
        clients = await initialize_ai_clients()
        
        # Run tests
        results = {}
        for client_name, client in clients.items():
            if config.ai_providers[client_name].enabled:
                await test_model(client_name, client, results)
                
        # Display results
        display_results(results)
        
        # Save results
        results_path = Path("data/test_results.json")
        with open(results_path, "w") as f:
            json.dump(results, f, indent=2)
        logger.info(f"Saved test results to {results_path}")
        
    except Exception as e:
        logger.error(f"Testing failed: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
