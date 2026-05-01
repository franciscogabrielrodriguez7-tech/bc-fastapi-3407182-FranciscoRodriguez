# ============================================
# PROJECT: AeroTech - Airport Management
# ============================================
# Week 01 - FastAPI Zero to Hero Bootcamp
# Criterion: Full domain adaptation (Aeronautics)
# ============================================

from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import Optional

# ============================================
# Domain Databases (Mock In-Memory Data)
# ============================================

# Multilingual welcome messages
WELCOME_MESSAGES: dict[str, str] = {
    "es": "Bienvenido a AeroTech, {name}. ¡Feliz vuelo!",
    "en": "Welcome to AeroTech, {name}. Have a great flight!",
    "pt": "Bem-vindo à AeroTech, {name}. Tenha um ótimo voo!",
    "it": "Benvenuti in AeroTech, {name}. Buon volo!",
    "fr": "Bienvenue à AeroTech, {name}. Bon voyage!",
    "de": "Willkommen bei AeroTech, {name}. Guten Flug!",
    "ru": "Добро пожаловать в AeroTech, {name}. Приятного полета!",
    "jp": "AeroTechへようこそ、{name}様。良いフライトを！",
    "cn": "欢迎来到 AeroTech, {name}。 旅途愉快！",
    "ar": "مرحباً بك في AeroTech، {name}. نتمنى لك رحلة سعيدة!"
}

# Entity: Aircraft (Tiered detail structure)
AIRCRAFT_DATABASE: dict[int, dict] = {
    1: {"model": "Boeing 737-800", "range": "Short-haul", "seats": 160},
    2: {"model": "Airbus A350-900", "range": "Long-haul", "seats": 315},
    3: {"model": "Embraer 190", "range": "Regional", "seats": 100},
    4: {"model": "Boeing 787 Dreamliner", "range": "Long-haul", "seats": 250},
    5: {"model": "Airbus A321neo", "range": "Medium-haul", "seats": 220}
}

# Entity: Crews
CREWS_DATABASE: dict[int, dict] = {
    101: {"name": "Cap. Laura Restrepo", "role": "Pilot"},
    102: {"name": "Carlos Ruiz", "role": "Co-pilot"},
    103: {"name": "Ana Gómez", "role": "Attendant"}
}

# Entity: Passengers
PASSENGERS_DATABASE: dict[int, dict] = {
    501: {"name": "Andrés Cepeda", "passport": "COL123"},
    502: {"name": "Mariana Pajón", "passport": "COL456"}
}

# Entity: Flights (Associates Aircraft, Crew, and Passengers)
FLIGHTS_DATABASE: list[dict] = [
    {
        "flight_number": "1", 
        "origin": "Bogotá", 
        "destination": "Miami",
        "aircraft_id": 1,
        "crew_ids": [101, 103],
        "passenger_ids": [501, 502] 
    }
]

# ============================================
# FASTAPI INSTANCE
# ============================================
app = FastAPI(
    title="AeroTech Management System",
    description="Professional fleet and air services management system",
    version="1.0.0"
)

# ============================================
# ENDPOINTS
# ============================================

@app.get("/")
async def root() -> dict:
    """Returns basic information about the AeroTech API."""
    return {
        "name": "AeroTech API",
        "industry": "Aviation",
        "status": "Active",
        "docs": "/docs",
        "supported_languages": list(WELCOME_MESSAGES.keys())
    }


@app.get("/health")
async def health() -> dict:
    """Health check endpoint to monitor API status."""
    return {
        "status": "healthy", 
        "timestamp": str(datetime.now())
    }


@app.get("/welcome/{name}")
async def welcome_passenger(name: str, lang: str = "es") -> dict:
    """Provides a localized welcome message for passengers."""
    message_template = WELCOME_MESSAGES.get(lang, WELCOME_MESSAGES["es"])
    return {
        "message": message_template.format(name=name),
        "language": lang,
        "passenger": name
    }


@app.get("/fleet/{aircraft_id}")
async def get_aircraft_info(aircraft_id: int, detail_level: int = 1) -> dict:
    """
    Retrieves aircraft information based on the requested detail level.
    Level 1: Basic info (ID, Model).
    Level 2: Advanced info (Includes Range and Capacity).
    """
    aircraft = AIRCRAFT_DATABASE.get(aircraft_id)
    
    if not aircraft:
        raise HTTPException(status_code=404, detail="Aircraft not found in AeroTech fleet")
    
    response = {"id": aircraft_id, "model": aircraft["model"]}
    
    if detail_level >= 2:
        response.update({"range": aircraft["range"], "capacity": aircraft["seats"]})
        
    return response


@app.get("/services/lounge")
async def check_lounge_access(hour: Optional[int] = None) -> dict:
    """
    Determines the VIP Lounge service status based on the provided or system hour.
    """
    if hour is None:
        hour = datetime.now().hour
        
    if 5 <= hour < 12:
        status = "Open - Premium Breakfast"
    elif 12 <= hour < 20:
        status = "Open - Lunch and Snacks"
    else:
        status = "Closed - Maintenance Only"
        
    return {
        "service": "VIP Lounge",
        "current_status": status,
        "server_hour": hour
    }


@app.get("/crews/{crew_id}")
async def get_crew_member(crew_id: int) -> dict:
    """Retrieves details of a specific crew member by ID."""
    member = CREWS_DATABASE.get(crew_id)
    
    if not member:
        raise HTTPException(status_code=404, detail="Crew member not found")
        
    return {"id": crew_id, **member}


@app.get("/flights/all")
async def list_all_flights() -> dict:
    """Returns a list of all scheduled flights."""
    return {
        "total_flights": len(FLIGHTS_DATABASE), 
        "flights": FLIGHTS_DATABASE
    }


@app.get("/flights/{flight_number}")
async def get_flight_details(flight_number: str) -> dict:
    """
    Retrieves comprehensive flight details by associating data from 
    Aircraft, Crew, and Passenger databases.
    """
    # Find the flight in the database
    flight = next((f for f in FLIGHTS_DATABASE if f["flight_number"] == flight_number), None)
    
    if not flight:
        raise HTTPException(status_code=404, detail="Flight not found")

    # Associate relational data
    aircraft_info = AIRCRAFT_DATABASE.get(flight["aircraft_id"])
    crew_info = [CREWS_DATABASE.get(crew_id) for crew_id in flight["crew_ids"]]
    passenger_info = [PASSENGERS_DATABASE.get(pass_id) for pass_id in flight["passenger_ids"]]

    return {
        "flight_number": flight["flight_number"],
        "route": f"{flight['origin']} to {flight['destination']}",
        "aircraft": aircraft_info,
        "crew": crew_info,
        "passengers": passenger_info
    }