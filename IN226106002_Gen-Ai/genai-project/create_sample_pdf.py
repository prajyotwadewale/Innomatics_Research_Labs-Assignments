from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_sample_pdf(filename="sample.pdf"):
    """
    Create a sample PDF file for testing the RAG system.
    """
    print(f"Generating {filename}...")
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Wildlife of India: A Brief Overview")
    
    # Body text
    c.setFont("Helvetica", 12)
    text = [
        "Welcome to the Wildlife of India knowledge base.",
        "",
        "1. Bengal Tiger",
        "The Bengal tiger is the national animal of India. They are primarily found in ",
        "the Sundarbans, Ranthambore, and Bandhavgarh National Parks. These majestic ",
        "cats are apex predators and play a crucial role in maintaining ecosystem balance.",
        "",
        "2. Indian Elephant",
        "The Indian elephant is smaller than its African cousin and is found in the ",
        "forests of southern, northeastern, and central India. They are highly intelligent ",
        "and social animals, living in herds led by a matriarch.",
        "",
        "3. Indian Rhinoceros",
        "Also known as the greater one-horned rhinoceros, this species is mainly found ",
        "in the Kaziranga National Park in Assam. They are known for their thick, armor-like ",
        "skin and a single black horn.",
        "",
        "4. Snow Leopard",
        "Found in the high altitudes of the Himalayas, including Ladakh and Spiti, the ",
        "snow leopard is an elusive and beautiful predator. They are perfectly adapted ",
        "to cold, mountainous environments.",
        "",
        "5. Asiatic Lion",
        "The Asiatic lion is distinct from African lions and is only found in the wild ",
        "in the Gir Forest National Park of Gujarat. Conservation efforts have helped ",
        "their population recover from the brink of extinction.",
        "",
        "6. Indian Peafowl (Peacock)",
        "The Indian peafowl is the national bird of India, celebrated for its brilliantly ",
        "colored plumage and the male's spectacular courtship display. They are widely ",
        "found in forests and agricultural areas across the subcontinent.",
        "",
        "7. King Cobra",
        "The king cobra is the world's longest venomous snake and is highly revered ",
        "in Indian mythology. Found predominantly in the rainforests of the Western ",
        "Ghats and Northeast India, it primarily preys on other snakes.",
        "",
        "8. Sloth Bear",
        "Sloth bears are a myrmecophagous bear species native to the Indian subcontinent.",
        "They have a shaggy black coat and long lower lips used for sucking up insects ",
        "such as termites and ants, which form a major part of their diet.",
        "",
        "9. Indian Leopard",
        "The Indian leopard is one of the big cats occurring on the Indian subcontinent, ",
        "apart from the Asiatic lion, Bengal tiger, snow leopard, and clouded leopard. ",
        "They are adaptable carnivores known for their climbing skills.",
        "",
        "10. Nilgiri Tahr",
        "The Nilgiri tahr is an ungulate that is endemic to the Nilgiri Hills and the ",
        "southern portion of the Western Ghats in the states of Tamil Nadu and Kerala. ",
        "It is the state animal of Tamil Nadu."
    ]
    
    y = height - 80
    for line in text:
        if y < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y = height - 50
        c.drawString(50, y, line)
        y -= 20
        
    c.save()
    print(f"Successfully created {filename}.")

if __name__ == "__main__":
    create_sample_pdf()
