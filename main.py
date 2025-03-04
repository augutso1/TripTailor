import requests
import math
import urllib.parse
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variables
API_KEY = os.getenv('GEOAPIFY_API_KEY')
if not API_KEY:
    print("WARNING: GEOAPIFY_API_KEY environment variable not set. API calls will fail.")

# Preferências iniciais com pesos (IA ajustável)
PREFERENCES_WEIGHTS = {
    'mais pontos turísticos': {'tourism.attraction': 0.7, 'catering.restaurant': 0.2, 'natural': 0.1},
    'foco em gastronomia': {'catering.restaurant': 0.7, 'tourism.attraction': 0.2, 'natural': 0.1},
    'paisagens naturais': {'natural': 0.7, 'tourism.attraction': 0.2, 'catering.restaurant': 0.1},
    'mix de tudo': {'tourism.attraction': 0.33, 'catering.restaurant': 0.33, 'natural': 0.34}
}

# Função para calcular distância entre dois pontos (fórmula de Haversine)
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Raio da Terra em km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# Função para obter coordenadas do hotel
def get_coordinates(hotel, destino):
    url = f"https://api.geoapify.com/v1/geocode/search?text={hotel},{destino}&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if data['features']:
        lat = data['features'][0]['properties']['lat']
        lon = data['features'][0]['properties']['lon']
        return lat, lon
    else:
        print("Erro ao geocodificar o hotel.")
        return None, None

# Função para buscar pontos de interesse
def get_places(lat, lon, radius=5000, category='tourism.attraction'):
    url = f"https://api.geoapify.com/v2/places?categories={category}&filter=circle:{lon},{lat},{radius}&limit=20&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    if 'features' in data:
        return data['features']
    else:
        print("Erro ao buscar locais próximos.")
        return []

# Função principal para gerar o itinerário com IA
def generate_itinerary(destino, hotel, duracao, preferencia):
    # Obter coordenadas do hotel
    hotel_lat, hotel_lon = get_coordinates(hotel, destino)
    if not hotel_lat or not hotel_lon:
        return
    
    # Obter pesos da preferência escolhida
    weights = PREFERENCES_WEIGHTS.get(preferencia.lower(), PREFERENCES_WEIGHTS['mix de tudo'])
    
    # Buscar locais para cada categoria
    places = []
    for category in weights.keys():
        category_places = get_places(hotel_lat, hotel_lon, category=category)
        for place in category_places:
            place_lat = place['properties']['lat']
            place_lon = place['properties']['lon']
            distance = haversine(hotel_lat, hotel_lon, place_lat, place_lon)
            # Adicionar peso baseado na preferência e distância
            score = weights[category] * (1 - distance / 50)  # Normaliza distância até 50 km
            place['score'] = score
            place['distance'] = distance
            places.append(place)
    
    # Ordenar locais por pontuação (IA recomenda os melhores)
    places.sort(key=lambda x: x['score'], reverse=True)
    
    # Gerar itinerário otimizado por proximidade
    itinerary = []
    current_lat, current_lon = hotel_lat, hotel_lon
    for day in range(duracao):
        day_plan = []
        available_places = places.copy()
        for _ in range(3):  # 3 atividades por dia
            if not available_places:
                break
            # Escolher o local mais próximo do ponto atual
            available_places.sort(key=lambda x: haversine(current_lat, current_lon, x['properties']['lat'], x['properties']['lon']))
            chosen = available_places.pop(0)
            day_plan.append(chosen)
            current_lat, current_lon = chosen['properties']['lat'], chosen['properties']['lon']
            places.remove(chosen)  # Remove para evitar repetição
        itinerary.append(day_plan)
    
    # Exibir o itinerário
    print(f"\nPlano de Viagem para {destino} - {duracao} dias")
    print(f"Hotel: {hotel}")
    for day, day_plan in enumerate(itinerary, 1):
        print(f"\nDia {day}:")
        times = ['Manhã', 'Tarde', 'Noite']
        for time, place in zip(times, day_plan):
            name = place['properties'].get('name', 'Nome não disponível')
            category = place['properties'].get('categories', [''])[0].replace('_', ' ').title()
            distance = place['distance']
            print(f"- {time}: {name} ({category}) - Distância do ponto anterior: {distance:.2f} km")
    
    # Resumo
    total_locais = sum(len(day) for day in itinerary)
    print("\nResumo:")
    print(f"- Total de locais visitados: {total_locais}")

# Function to validate API key
def validate_api_key():
    if not API_KEY:
        print("DEBUG: No API key provided")
        return False
        
    try:
        # Make a simple request to test the API key
        test_url = f"https://api.geoapify.com/v1/geocode/search?text=Paris&apiKey={API_KEY}"
        response = requests.get(test_url, timeout=5)
        
        if response.status_code == 200:
            print("DEBUG: API key is valid")
            return True
        else:
            print(f"DEBUG: API key validation failed with status code {response.status_code}")
            return False
    except Exception as e:
        print(f"DEBUG: API key validation error: {str(e)}")
        return False

# Validate API key on module import
API_KEY_VALID = validate_api_key()
if not API_KEY_VALID:
    print("WARNING: API key validation failed. API calls may not work correctly.")

# Entrada do usuário e execução
if __name__ == "__main__":
    destino = input("Destino: ")
    hotel = input("Hotel: ")
    duracao = int(input("Duração (dias): "))
    preferencia = input("Preferência (ex: mais pontos turísticos, foco em gastronomia): ")
    generate_itinerary(destino, hotel, duracao, preferencia)