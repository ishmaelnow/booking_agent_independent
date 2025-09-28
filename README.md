📦 Booking Agent (Independent CLI Version)
A modular, CLI-driven taxi booking agent built with LangGraph, geocoding, fare calculation, and LLM-powered explanations. Designed for extensibility, backend integration, and real-world deployment.

🚀 Features
- 📍 User input: pickup, dropoff, ride time, phone number
- 🧮 Real mileage estimation via OpenStreetMap + geopy
- 💰 Fare calculation with dynamic pricing logic
- 🧠 LLM-generated fare explanations (via OpenAI)
- 💾 SQLite persistence for bookings
- 🧼 Modular architecture with clean separation of concern
🧱 Project Structur
booking_agent_independent/
├── main.py                  # CLI entry point
├── graph.py                 # LangGraph pipeline
├── state.py                 # BookingState container
├── .env.example             # Safe template for secrets
├── resources/               # Core logic modules
│   ├── geo_utils.py         # Geocoding + mileage
│   └── fare_engine.py       # Fare calculation
├── nodes/                   # LangGraph nodes
│   ├── generate_booking.py  # CLI prompt node
│   └── explain_fare.py      # Geocode + fare + LLM
└── db/                      # Persistence layer
    └── writer.py            # SQLite booking saver

⚙️ Setup Instruction

# Clone and enter the project
git clone https://github.com/your-username/booking_agent_independent.git
cd booking_agent_independent

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt  # or manually install:
pip install langchain langgraph geopy geocoder python-dotenv langchain-openai

# Create your .env file
cp .env.example .env