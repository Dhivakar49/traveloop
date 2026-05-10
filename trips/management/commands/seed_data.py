from django.core.management.base import BaseCommand
from trips.models import City, Activity


CITIES = [
    # Indian Cities
    {"name": "Mumbai", "country": "India", "region": "West India", "cost_index": 5000, "popularity": 98,
     "description": "The City of Dreams – Bollywood, beaches, and bustling markets.",
     "image_url": "https://images.unsplash.com/photo-1567157577867-05ccb1388e66?w=600"},
    {"name": "Delhi", "country": "India", "region": "North India", "cost_index": 4500, "popularity": 97,
     "description": "India's capital with rich Mughal heritage and modern vibrancy.",
     "image_url": "https://images.unsplash.com/photo-1587474260584-136574528ed5?w=600"},
    {"name": "Jaipur", "country": "India", "region": "North India", "cost_index": 4000, "popularity": 92,
     "description": "The Pink City – majestic forts, palaces, and vibrant bazaars.",
     "image_url": "https://images.unsplash.com/photo-1599661046289-e31897846e41?w=600"},
    {"name": "Goa", "country": "India", "region": "West India", "cost_index": 5500, "popularity": 95,
     "description": "Beach paradise with Portuguese heritage and vibrant nightlife.",
     "image_url": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=600"},
    {"name": "Varanasi", "country": "India", "region": "North India", "cost_index": 3500, "popularity": 88,
     "description": "Ancient spiritual city on the banks of the holy Ganges.",
     "image_url": "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?w=600"},
    {"name": "Bangalore", "country": "India", "region": "South India", "cost_index": 6000, "popularity": 85,
     "description": "India's Silicon Valley with pleasant weather and gardens.",
     "image_url": "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?w=600"},
    {"name": "Udaipur", "country": "India", "region": "North India", "cost_index": 4500, "popularity": 90,
     "description": "The City of Lakes – romantic palaces and stunning sunsets.",
     "image_url": "https://images.unsplash.com/photo-1587135941948-670b381f08ce?w=600"},
    {"name": "Kerala", "country": "India", "region": "South India", "cost_index": 5000, "popularity": 93,
     "description": "God's Own Country – backwaters, beaches, and lush greenery.",
     "image_url": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=600"},
    {"name": "Agra", "country": "India", "region": "North India", "cost_index": 3800, "popularity": 96,
     "description": "Home to the iconic Taj Mahal, symbol of eternal love.",
     "image_url": "https://images.unsplash.com/photo-1564507592333-c60657eea523?w=600"},
    {"name": "Rishikesh", "country": "India", "region": "North India", "cost_index": 4000, "popularity": 87,
     "description": "Yoga capital of the world nestled in the Himalayan foothills.",
     "image_url": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600"},
    {"name": "Kolkata", "country": "India", "region": "East India", "cost_index": 4200, "popularity": 84,
     "description": "City of Joy – colonial architecture, art, and Bengali culture.",
     "image_url": "https://images.unsplash.com/photo-1558431382-27e303142255?w=600"},
    {"name": "Mysore", "country": "India", "region": "South India", "cost_index": 4500, "popularity": 86,
     "description": "Palace city known for silk, sandalwood, and yoga.",
     "image_url": "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?w=600"},
    
    # Global Destinations
    {"name": "Paris", "country": "France", "region": "Europe", "cost_index": 12500, "popularity": 98,
     "description": "The City of Light – art, fashion, and gastronomy.",
     "image_url": "https://images.unsplash.com/photo-1499856871958-5b9627545d1a?w=600"},
    {"name": "Tokyo", "country": "Japan", "region": "Asia", "cost_index": 10000, "popularity": 95,
     "description": "A dazzling blend of tradition and futurism.",
     "image_url": "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=600"},
    {"name": "New York", "country": "USA", "region": "North America", "cost_index": 16500, "popularity": 97,
     "description": "The city that never sleeps.",
     "image_url": "https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=600"},
    {"name": "Bali", "country": "Indonesia", "region": "Asia", "cost_index": 5000, "popularity": 90,
     "description": "Island of the Gods – temples, rice fields, and beaches.",
     "image_url": "https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=600"},
    {"name": "Rome", "country": "Italy", "region": "Europe", "cost_index": 11000, "popularity": 93,
     "description": "Eternal city with millennia of history.",
     "image_url": "https://images.unsplash.com/photo-1529260830199-42c24126f198?w=600"},
    {"name": "Bangkok", "country": "Thailand", "region": "Asia", "cost_index": 4200, "popularity": 88,
     "description": "Vibrant street life and ornate temples.",
     "image_url": "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=600"},
    {"name": "Barcelona", "country": "Spain", "region": "Europe", "cost_index": 9200, "popularity": 91,
     "description": "Gaudí's masterpieces and lively beaches.",
     "image_url": "https://images.unsplash.com/photo-1539037116277-4db20889f2d4?w=600"},
    {"name": "Dubai", "country": "UAE", "region": "Middle East", "cost_index": 15000, "popularity": 92,
     "description": "Futuristic skyline and luxury at every turn.",
     "image_url": "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=600"},
    {"name": "London", "country": "UK", "region": "Europe", "cost_index": 14000, "popularity": 96,
     "description": "Historic capital with royal palaces and modern culture.",
     "image_url": "https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=600"},
    {"name": "Singapore", "country": "Singapore", "region": "Asia", "cost_index": 11500, "popularity": 89,
     "description": "Garden city with futuristic architecture and diverse cuisine.",
     "image_url": "https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=600"},
]

ACTIVITIES = {
    "Mumbai": [
        {"name": "Gateway of India Visit", "type": "sightseeing", "cost": 0, "duration": 1,
         "description": "Iconic arch monument overlooking the Arabian Sea."},
        {"name": "Bollywood Studio Tour", "type": "culture", "cost": 800, "duration": 4,
         "description": "Behind-the-scenes tour of India's film industry."},
        {"name": "Marine Drive Evening Walk", "type": "sightseeing", "cost": 0, "duration": 1.5,
         "description": "Stroll along the Queen's Necklace at sunset."},
        {"name": "Street Food Tour", "type": "food", "cost": 500, "duration": 3,
         "description": "Taste vada pav, pav bhaji, and Mumbai's famous chaat."},
    ],
    "Delhi": [
        {"name": "Red Fort Tour", "type": "culture", "cost": 50, "duration": 2,
         "description": "Magnificent Mughal fort and UNESCO World Heritage Site."},
        {"name": "Qutub Minar", "type": "sightseeing", "cost": 30, "duration": 1.5,
         "description": "World's tallest brick minaret from the 12th century."},
        {"name": "Chandni Chowk Food Walk", "type": "food", "cost": 600, "duration": 3,
         "description": "Explore Old Delhi's legendary street food scene."},
        {"name": "India Gate & Rajpath", "type": "sightseeing", "cost": 0, "duration": 1,
         "description": "War memorial and ceremonial boulevard."},
    ],
    "Jaipur": [
        {"name": "Amber Fort", "type": "culture", "cost": 100, "duration": 3,
         "description": "Majestic hilltop fort with stunning mirror palace."},
        {"name": "Hawa Mahal", "type": "sightseeing", "cost": 50, "duration": 1,
         "description": "Palace of Winds with 953 intricate windows."},
        {"name": "City Palace", "type": "culture", "cost": 200, "duration": 2,
         "description": "Royal residence with museums and courtyards."},
        {"name": "Rajasthani Cooking Class", "type": "food", "cost": 1500, "duration": 3,
         "description": "Learn to cook dal baati churma and other delicacies."},
    ],
    "Goa": [
        {"name": "Beach Hopping Tour", "type": "adventure", "cost": 800, "duration": 6,
         "description": "Visit Baga, Calangute, and Anjuna beaches."},
        {"name": "Old Goa Churches", "type": "culture", "cost": 0, "duration": 2,
         "description": "Explore Portuguese colonial churches and cathedrals."},
        {"name": "Spice Plantation Tour", "type": "sightseeing", "cost": 500, "duration": 3,
         "description": "Learn about Indian spices with traditional lunch."},
        {"name": "Water Sports Package", "type": "adventure", "cost": 2000, "duration": 2,
         "description": "Parasailing, jet skiing, and banana boat rides."},
    ],
    "Varanasi": [
        {"name": "Ganga Aarti Ceremony", "type": "culture", "cost": 0, "duration": 1.5,
         "description": "Mesmerizing evening prayer ritual on the ghats."},
        {"name": "Sunrise Boat Ride", "type": "sightseeing", "cost": 300, "duration": 2,
         "description": "Witness the spiritual awakening of the holy city."},
        {"name": "Sarnath Buddhist Site", "type": "culture", "cost": 20, "duration": 3,
         "description": "Where Buddha gave his first sermon."},
        {"name": "Banarasi Food Tour", "type": "food", "cost": 700, "duration": 3,
         "description": "Taste kachori, lassi, and famous Banarasi paan."},
    ],
    "Bangalore": [
        {"name": "Lalbagh Botanical Garden", "type": "sightseeing", "cost": 20, "duration": 2,
         "description": "Historic garden with glasshouse and diverse flora."},
        {"name": "Bangalore Palace", "type": "culture", "cost": 230, "duration": 2,
         "description": "Tudor-style palace with elegant architecture."},
        {"name": "Craft Beer Brewery Tour", "type": "food", "cost": 1000, "duration": 3,
         "description": "Sample India's craft beer scene in the pub capital."},
        {"name": "Nandi Hills Sunrise Trek", "type": "adventure", "cost": 500, "duration": 4,
         "description": "Early morning trek to hilltop with panoramic views."},
    ],
    "Udaipur": [
        {"name": "City Palace Complex", "type": "culture", "cost": 300, "duration": 3,
         "description": "Magnificent palace overlooking Lake Pichola."},
        {"name": "Lake Pichola Boat Ride", "type": "sightseeing", "cost": 400, "duration": 1.5,
         "description": "Sunset cruise with views of palaces and ghats."},
        {"name": "Jag Mandir Island", "type": "sightseeing", "cost": 350, "duration": 2,
         "description": "Beautiful marble palace on an island."},
        {"name": "Rajasthani Cultural Show", "type": "culture", "cost": 500, "duration": 2,
         "description": "Traditional dance and music performance."},
    ],
    "Kerala": [
        {"name": "Backwater Houseboat Cruise", "type": "sightseeing", "cost": 8000, "duration": 24,
         "description": "Overnight stay on traditional kettuvallam houseboat."},
        {"name": "Kathakali Dance Performance", "type": "culture", "cost": 300, "duration": 2,
         "description": "Classical Kerala dance-drama with elaborate costumes."},
        {"name": "Ayurvedic Spa Treatment", "type": "relaxation", "cost": 2000, "duration": 2,
         "description": "Traditional Kerala massage and wellness therapy."},
        {"name": "Tea Plantation Tour", "type": "sightseeing", "cost": 500, "duration": 3,
         "description": "Visit Munnar's lush tea estates and factory."},
    ],
    "Agra": [
        {"name": "Taj Mahal Sunrise Tour", "type": "culture", "cost": 50, "duration": 3,
         "description": "Marvel at the world's most beautiful monument at dawn."},
        {"name": "Agra Fort", "type": "culture", "cost": 50, "duration": 2,
         "description": "Massive red sandstone Mughal fort complex."},
        {"name": "Mehtab Bagh Sunset View", "type": "sightseeing", "cost": 25, "duration": 1,
         "description": "View Taj Mahal from across the Yamuna River."},
        {"name": "Mughlai Food Experience", "type": "food", "cost": 800, "duration": 2,
         "description": "Taste authentic Mughlai cuisine and petha sweet."},
    ],
    "Rishikesh": [
        {"name": "Yoga & Meditation Session", "type": "relaxation", "cost": 500, "duration": 2,
         "description": "Morning yoga class by the Ganges."},
        {"name": "White Water Rafting", "type": "adventure", "cost": 1500, "duration": 3,
         "description": "Thrilling rapids on the holy Ganges river."},
        {"name": "Beatles Ashram Visit", "type": "culture", "cost": 150, "duration": 1.5,
         "description": "Where the Beatles learned meditation in 1968."},
        {"name": "Ganga Aarti at Parmarth", "type": "culture", "cost": 0, "duration": 1,
         "description": "Evening prayer ceremony at famous ashram."},
    ],
    "Kolkata": [
        {"name": "Victoria Memorial", "type": "culture", "cost": 30, "duration": 2,
         "description": "Grand marble monument with museum and gardens."},
        {"name": "Howrah Bridge Walk", "type": "sightseeing", "cost": 0, "duration": 1,
         "description": "Iconic cantilever bridge over Hooghly River."},
        {"name": "Bengali Food Tour", "type": "food", "cost": 800, "duration": 3,
         "description": "Taste rosogolla, mishti doi, and street food."},
        {"name": "Kumartuli Potter's Quarter", "type": "culture", "cost": 0, "duration": 1.5,
         "description": "Watch artisans craft clay idols for festivals."},
    ],
    "Mysore": [
        {"name": "Mysore Palace", "type": "culture", "cost": 70, "duration": 2,
         "description": "Opulent Indo-Saracenic palace lit up at night."},
        {"name": "Chamundi Hills Temple", "type": "culture", "cost": 0, "duration": 2,
         "description": "Hilltop temple with panoramic city views."},
        {"name": "Devaraja Market", "type": "sightseeing", "cost": 0, "duration": 1.5,
         "description": "Colorful market selling flowers, spices, and silk."},
        {"name": "Yoga Class at Ashram", "type": "relaxation", "cost": 500, "duration": 2,
         "description": "Traditional Ashtanga yoga in the city of yoga."},
    ],
    
    # Global Cities Activities
    "Paris": [
        {"name": "Eiffel Tower Visit", "type": "sightseeing", "cost": 2100, "duration": 2,
         "description": "Iconic iron tower with panoramic views of Paris."},
        {"name": "Louvre Museum", "type": "culture", "cost": 1400, "duration": 4,
         "description": "World's largest art museum, home to the Mona Lisa."},
        {"name": "Seine River Cruise", "type": "sightseeing", "cost": 1250, "duration": 1.5,
         "description": "Relaxing cruise along Paris's iconic river."},
        {"name": "French Cooking Class", "type": "food", "cost": 6600, "duration": 3,
         "description": "Learn to cook classic French dishes with a local chef."},
    ],
    "Tokyo": [
        {"name": "Senso-ji Temple", "type": "culture", "cost": 0, "duration": 2,
         "description": "Tokyo's oldest temple in the historic Asakusa district."},
        {"name": "Shibuya Crossing", "type": "sightseeing", "cost": 0, "duration": 1,
         "description": "World's busiest pedestrian crossing."},
        {"name": "Tsukiji Outer Market Food Tour", "type": "food", "cost": 3300, "duration": 2,
         "description": "Sample fresh sushi and street food at the famous market."},
        {"name": "TeamLab Borderless", "type": "culture", "cost": 2650, "duration": 3,
         "description": "Immersive digital art museum experience."},
    ],
    "Bali": [
        {"name": "Tanah Lot Temple", "type": "culture", "cost": 420, "duration": 2,
         "description": "Iconic sea temple perched on a rock."},
        {"name": "Ubud Rice Terrace Trek", "type": "adventure", "cost": 1250, "duration": 3,
         "description": "Hike through stunning terraced rice paddies."},
        {"name": "Balinese Cooking Class", "type": "food", "cost": 2900, "duration": 4,
         "description": "Learn to prepare traditional Balinese dishes."},
        {"name": "Surf Lesson Kuta Beach", "type": "adventure", "cost": 2100, "duration": 2,
         "description": "Learn to surf on Bali's famous beginner waves."},
    ],
    "Rome": [
        {"name": "Colosseum Tour", "type": "culture", "cost": 1500, "duration": 2,
         "description": "Explore the ancient amphitheatre of the Roman Empire."},
        {"name": "Vatican Museums", "type": "culture", "cost": 1650, "duration": 4,
         "description": "Art and history in the world's smallest state."},
        {"name": "Roman Food Tour", "type": "food", "cost": 5400, "duration": 3,
         "description": "Taste pasta, gelato, and espresso in hidden trattorias."},
        {"name": "Trevi Fountain", "type": "sightseeing", "cost": 0, "duration": 0.5,
         "description": "Toss a coin in the world's most famous fountain."},
    ],
    "New York": [
        {"name": "Central Park Bike Tour", "type": "adventure", "cost": 2500, "duration": 2,
         "description": "Cycle through NYC's iconic 843-acre park."},
        {"name": "Broadway Show", "type": "culture", "cost": 10000, "duration": 3,
         "description": "World-class theatre in the heart of Manhattan."},
        {"name": "High Line Walk", "type": "sightseeing", "cost": 0, "duration": 1.5,
         "description": "Elevated park on a historic freight rail line."},
        {"name": "NYC Food Markets", "type": "food", "cost": 2100, "duration": 2,
         "description": "Sample cuisines from around the world."},
    ],
    "Bangkok": [
        {"name": "Grand Palace", "type": "culture", "cost": 1250, "duration": 3,
         "description": "Dazzling royal palace complex in the heart of the city."},
        {"name": "Street Food Night Tour", "type": "food", "cost": 2500, "duration": 3,
         "description": "Explore Bangkok's legendary street food scene after dark."},
        {"name": "Wat Pho Temple", "type": "culture", "cost": 420, "duration": 1.5,
         "description": "Home to the massive Reclining Buddha statue."},
        {"name": "Thai Cooking Class", "type": "food", "cost": 3300, "duration": 4,
         "description": "Master pad thai and green curry."},
    ],
    "Barcelona": [
        {"name": "Sagrada Família", "type": "culture", "cost": 2150, "duration": 2,
         "description": "Gaudí's breathtaking unfinished basilica."},
        {"name": "Park Güell", "type": "sightseeing", "cost": 830, "duration": 1.5,
         "description": "Colourful mosaic park with city views."},
        {"name": "La Boqueria Market", "type": "food", "cost": 0, "duration": 1,
         "description": "Vibrant food market with fresh produce and tapas."},
        {"name": "Flamenco Show", "type": "culture", "cost": 3750, "duration": 2,
         "description": "Passionate Spanish dance performance."},
    ],
    "Dubai": [
        {"name": "Burj Khalifa At the Top", "type": "sightseeing", "cost": 3300, "duration": 2,
         "description": "Observation deck of the world's tallest building."},
        {"name": "Desert Safari", "type": "adventure", "cost": 7000, "duration": 6,
         "description": "Dune bashing, camel rides and BBQ under the stars."},
        {"name": "Dubai Food Tour", "type": "food", "cost": 5000, "duration": 3,
         "description": "Explore Old Dubai's spice souks and street food."},
        {"name": "Dubai Mall & Fountain Show", "type": "sightseeing", "cost": 0, "duration": 2,
         "description": "World's largest mall and spectacular water fountain."},
    ],
    "London": [
        {"name": "Tower of London", "type": "culture", "cost": 2500, "duration": 3,
         "description": "Historic castle housing the Crown Jewels."},
        {"name": "British Museum", "type": "culture", "cost": 0, "duration": 3,
         "description": "World-famous museum with free entry."},
        {"name": "Thames River Cruise", "type": "sightseeing", "cost": 1650, "duration": 1.5,
         "description": "See London's landmarks from the water."},
        {"name": "Afternoon Tea Experience", "type": "food", "cost": 4150, "duration": 2,
         "description": "Traditional British tea with scones and sandwiches."},
    ],
    "Singapore": [
        {"name": "Gardens by the Bay", "type": "sightseeing", "cost": 2300, "duration": 2,
         "description": "Futuristic gardens with Supertree Grove."},
        {"name": "Marina Bay Sands SkyPark", "type": "sightseeing", "cost": 2100, "duration": 1,
         "description": "Observation deck with stunning city views."},
        {"name": "Hawker Centre Food Tour", "type": "food", "cost": 1650, "duration": 3,
         "description": "Sample Singapore's diverse street food culture."},
        {"name": "Sentosa Island", "type": "adventure", "cost": 3300, "duration": 5,
         "description": "Beach resort island with attractions and activities."},
    ],
}


class Command(BaseCommand):
    help = 'Seed database with Indian cities and activities'

    def handle(self, *args, **options):
        self.stdout.write('Seeding Indian cities...')
        city_map = {}
        for c in CITIES:
            obj, created = City.objects.update_or_create(
                name=c['name'], country=c['country'],
                defaults={
                    'region': c['region'],
                    'cost_index': c['cost_index'],
                    'popularity': c['popularity'],
                    'description': c['description'],
                    'image_url': c['image_url'],
                }
            )
            city_map[c['name']] = obj
            status = 'Created' if created else 'Updated'
            self.stdout.write(f'  {status}: {obj}')

        self.stdout.write('Seeding activities...')
        for city_name, acts in ACTIVITIES.items():
            city = city_map.get(city_name)
            if not city:
                continue
            for a in acts:
                obj, created = Activity.objects.update_or_create(
                    name=a['name'], city=city,
                    defaults={
                        'activity_type': a['type'],
                        'cost': a['cost'],
                        'duration_hours': a['duration'],
                        'description': a['description'],
                    }
                )
                status = 'Created' if created else 'Updated'
                self.stdout.write(f'  {status}: {obj}')

        self.stdout.write(self.style.SUCCESS('✅ Indian cities and activities seeded successfully!'))

