
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
data = {
  "appointment_booking": [
    "how can i schedule an appointment",
    "i need to book an appointment with a doctor",
    "whats the procedure for booking an appointment",
    "hello",
    "id like to schedule an appointment.",
    "book an appointment",
    "appointment",
    "need an appointment"
  ],
    "billing_and_insurance": [
      "how do I pay my medical bills",
      "do you accept my insurance",
      "what's the billing process for a hospital stay",
      "bills",
      "insurance",
      "pay bill"
    ],
    "department_information": [
      "which departments are available in the hospital",
      "can you provide details about the cardiology department",
      "tell me more about the pediatric department",
      "department",
      "which department",
      "department info"
    ],
    "doctor_information": [
      "tell me more about dr. abc",
      "whats the specialty of dr. abc",
      "give me the contact details for dr. abcdoctor",
      "contact doctor",
      "doctor contact",
      "doctor detail",
      "detail doctor"
    ],
    "finaltest": [
      "None"
    ],
    "general_information": [
      "tell me more about the hospital",
      "what services do you offer",
      "is there a cafeteria in the hospital",
      "information",
      "cafeteria",
      "services",
      "services offered",
      "offered services"
    ],
    "location_and_directions": [
      "how do I get to the hospital",
      "can you provide me with directions to your location",
      "where is the hospital situated",
      "direction",
      "direction hospital",
      "hospital direction",
      "location",
      "hospital location"
    ],
    "visiting_hours": [
      "what are the visiting hours for patients",
      "when can I visit a patient in the hospital",
      "is there a specific time for visiting hours",
      "visiting time",
      "visit",
      "time",
      "time to visit",
      "visit time",
      "hospital visit",
      "visit hospital"
    ]
  }

def get_intent_firebase(text):
  lowercase_text = text.lower()
  matching_intent = []
  # Find the closest matching question for each intent
  for intent, questions in data.items():
    closest_q, score = process.extractOne(lowercase_text, questions, scorer=fuzz.ratio)
    print(score)
    if score > 70:  # Set a threshold for confidence
      matching_intent.append(intent)

  # Return the first matching intent or "no_answer" if no match is found
  return matching_intent[0] if matching_intent else "no_answer"

# Example usage (data dictionary remains the same)
text = input("Pleas ask your questions:",)
intent = get_intent_firebase(text)
print(f"Matched intent: {intent}")
