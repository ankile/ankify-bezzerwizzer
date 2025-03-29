import os
import base64
import json
import uuid
import argparse
import sys
from glob import glob
from typing import List, Dict, Any
from dotenv import load_dotenv

# Import Anthropic SDK
from anthropic import Anthropic

# Hard-coded list of categories in order
CATEGORIES = [
    "Bøker",
    "Dyr",
    "Film",
    "Geografi",
    "Historie",
    "Hverdag",
    "Mat og drikke",
    "Musikk",
    "Natur og miljø",
    "Naturvitenskap",
    "Samfunn",
    "Spill og lek",
    "Sport",
    "Språk", 
    "Tradisjon og tro",
    "TV og serier"
]

def encode_image(image_path: str) -> str:
    """Convert an image to base64 encoding for API transmission."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def assign_categories(extracted_cards: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Assign categories to extracted cards using the hardcoded categories list."""
    # Check if we have exactly the right number of categories
    if len(extracted_cards) != len(CATEGORIES):
        print(f"Error: Expected {len(CATEGORIES)} questions, but got {len(extracted_cards)}.")
        print("Cannot reliably map categories to questions. Exiting.")
        sys.exit(1)
    
    # Assign categories in order, preserving the question and answer
    for i, card in enumerate(extracted_cards):
        # Update the category while keeping original question and answer
        card["category"] = CATEGORIES[i]
    
    return extracted_cards

def process_image_pair(question_img: str, answer_img: str, client: Anthropic) -> List[Dict[str, Any]]:
    """Process a pair of question and answer images to create complete cards."""
    print(f"Processing image pair: {os.path.basename(question_img)} & {os.path.basename(answer_img)}")
    
    # Generate a single card_id for this image pair
    # This ensures all questions from the same card share the same ID
    card_pair_id = str(uuid.uuid4())
    
    # Encode both images
    question_base64 = encode_image(question_img)
    answer_base64 = encode_image(answer_img)
    
    # Create a prompt with an example of the expected output format and categories
    categories_text = "Each Bezzerwizzer card contains exactly 16 questions, one for each of these categories in this exact order:\n"
    for i, category in enumerate(CATEGORIES, 1):
        categories_text += f"{i}. {category}\n"
    
    prompt = f"""
I'm showing you a pair of Bezzerwizzer trivia card images in Norwegian. The first image shows questions, and the second shows the corresponding answers.

{categories_text}

Extract all 16 questions and answers from the images. The questions must be in the same order as they appear on the card.
Format your response as a JSON array of objects, with exactly 16 items.

Here's exactly how I want the output to be formatted:
```json
[
  {{
    "question": "I hvilket år endte den andre verdenskrig?",
    "answer": "1945"
  }},
  {{
    "question": "Hva er hovedstaden i Norge?",
    "answer": "Oslo"
  }},
  ...and so on for all 16 questions
]
```

Just output the JSON with no additional text, explanations, or markdown. Don't add a root object - just return the array directly.
"""

    # Create message with both images
    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=4000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text", 
                        "text": prompt
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": question_base64
                        }
                    },
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": answer_base64
                        }
                    }
                ]
            }
        ]
    )
    
    response = message.content[0].text
    
    # Parse the response into structured data
    try:
        # Extract JSON from response - strip any markdown code block formatting
        if "```json" in response:
            json_text = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            json_text = response.split("```")[1].strip()
        else:
            json_text = response.strip()
        
        # Parse JSON
        data = json.loads(json_text)
        
        # We expect a direct array of objects
        if isinstance(data, list):
            # Create cards with the same card_id for all questions
            cards = []
            for i, item in enumerate(data):
                card = {
                    "card_id": card_pair_id,
                    "question": item.get("question", ""),
                    "answer": item.get("answer", "")
                }
                cards.append(card)
            
            # Assign correct categories based on order
            cards = assign_categories(cards)
            
            return cards
        else:
            print("Warning: Expected a list but got a different data structure. Attempting to process anyway.")
            # Try to handle unexpected format (should be rare with our example)
            if isinstance(data, dict):
                if "cards" in data:
                    items = data["cards"]
                elif "questions" in data:
                    items = data["questions"]
                else:
                    items = [data]
                
                cards = []
                for item in items:
                    card = {
                        "card_id": card_pair_id,
                        "question": item.get("question", ""),
                        "answer": item.get("answer", "")
                    }
                    cards.append(card)
                
                # Assign correct categories based on order
                cards = assign_categories(cards)
                
                return cards
            else:
                raise ValueError("Unexpected data structure")
            
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        print(f"Response was: {response}")
        return []
    except Exception as e:
        print(f"Error processing response: {e}")
        print(f"Response was: {response}")
        return []

def export_to_anki_csv(cards: List[Dict[str, Any]], output_file: str) -> None:
    """Export cards to Anki-compatible CSV format."""
    with open(output_file, 'w', encoding='utf-8') as f:
        # Write CSV header
        f.write("#separator:semicolon\n")
        f.write("#html:true\n")
        f.write("#columns:Question;Answer;Category;CardID\n")
        
        # Write card data
        for card in cards:
            question = card["question"].replace(";", ",")
            answer = card["answer"].replace(";", ",")
            category = card["category"].replace(";", ",")
            card_id = card["card_id"]
            
            f.write(f"{question};{answer};{category};{card_id}\n")
    
    print(f"Exported {len(cards)} cards to {output_file}")

def save_json(cards: List[Dict[str, Any]], output_file: str) -> None:
    """Save cards to JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({"questions": cards}, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(cards)} cards to {output_file}")

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Process Bezzerwizzer cards from images")
    parser.add_argument("folder", help="Folder containing image pairs")
    parser.add_argument("--api-key", help="Claude API Key (overrides .env)")
    parser.add_argument("--output-csv", help="Output CSV file for Anki (defaults to folder/bezzerwizzer_anki.csv)")
    parser.add_argument("--output-json", help="Output JSON file (defaults to folder/bezzerwizzer_cards.json)")
    
    args = parser.parse_args()
    
    # Use API key from command line args if provided, otherwise use from .env
    api_key = args.api_key or os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("Error: Anthropic API key not found. Please set it in .env file or provide with --api-key")
        return
    
    # Set default output paths to be in the same folder as the images
    if not args.output_csv:
        args.output_csv = os.path.join(args.folder, "bezzerwizzer_anki.csv")
    if not args.output_json:
        args.output_json = os.path.join(args.folder, "bezzerwizzer_cards.json")
    
    print(f"Using {len(CATEGORIES)} predefined categories.")
    
    # Initialize the Anthropic client
    client = Anthropic(api_key=api_key)
    
    # Find all image files in the folder
    image_files = sorted(glob(os.path.join(args.folder, "*.jpg"))) + \
                 sorted(glob(os.path.join(args.folder, "*.jpeg"))) + \
                 sorted(glob(os.path.join(args.folder, "*.png")))
    
    if len(image_files) == 0:
        print(f"No image files found in {args.folder}")
        return
    
    if len(image_files) % 2 != 0:
        print(f"Warning: Odd number of images ({len(image_files)}). Each question needs an answer.")
    
    # Process images in pairs (even indices: questions, odd indices: answers)
    all_cards = []
    for i in range(0, len(image_files) - 1, 2):
        question_img = image_files[i]
        answer_img = image_files[i + 1]
        
        print(f"\nProcessing pair {i//2 + 1}/{len(image_files)//2}:")
        cards = process_image_pair(question_img, answer_img, client)
        all_cards.extend(cards)
    
    # Save results
    if all_cards:
        export_to_anki_csv(all_cards, args.output_csv)
        save_json(all_cards, args.output_json)
        print(f"\nSuccessfully processed {len(image_files)//2} cards from {len(image_files)//2} image pairs.")
    else:
        print("No cards were successfully processed.")

if __name__ == "__main__":
    main()
