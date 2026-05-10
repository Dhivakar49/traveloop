# Traveloop - Travel Planning Platform

A comprehensive travel planning application built with Django that helps users plan trips, create itineraries, manage budgets, and organize packing lists.

## Features

### Authentication
- **Supabase Authentication** - Modern auth with email/password
- **Forgot Password** - Email-based password reset
- **User Profiles** - Customizable user profiles with photos

### Trip Planning
- **Create Trips** - Plan trips with dates, budgets, and descriptions
- **Itinerary Builder** - Add multiple cities and activities to your trip
- **Budget Tracking** - Track expenses by category (transport, accommodation, meals, activities)
- **Visual Budget Breakdown** - See spending distribution with progress bars

### Destinations
- **22 Cities** - 12 Indian + 10 Global destinations
- **88 Activities** - Curated activities for each city
- **City Search** - Find destinations by name, country, or region
- **Activity Search** - Filter activities by type and city

### Trip Management
- **Packing Checklist** - Organize items by category, track packing progress
- **Trip Notes** - Add notes for specific stops or general trip notes
- **Public Sharing** - Share your itinerary with a public link
- **Trip Dashboard** - View all your trips at a glance

### Budget Features
- **Multi-currency Support** - All costs displayed in Indian Rupees
- **Cost Breakdown** - Detailed breakdown by transport, accommodation, meals, activities
- **Budget Alerts** - See if you're over budget
- **Daily Cost Estimates** - Per-city daily cost estimates

## Quick Start

### Prerequisites
- Python 3.8+
- PostgreSQL
- Supabase account (for authentication)

### Installation

1. **Clone the repository**
   ```bash
   cd traveloop
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   - Copy `.env.example` to `.env`
   - Update with your credentials:
     ```
     SUPABASE_URL=your_supabase_url
     SUPABASE_KEY=your_anon_key
     SUPABASE_SERVICE_KEY=your_service_role_key
     DB_NAME=traveloop
     DB_USER=postgres
     DB_PASSWORD=your_password
     ```

5. **Set up database**
   ```bash
   python manage.py migrate
   python manage.py seed_data
   ```

6. **Run the server**
   ```bash
   python manage.py runserver
   ```

7. **Visit** http://localhost:8000

## Documentation

Detailed documentation is available in the `docs/` folder:

- **[Quick Start Guide](docs/QUICK_START.md)** - 3-minute setup guide
- **[Supabase Setup](docs/SUPABASE_SETUP.md)** - Complete Supabase authentication setup
- **[Checklist Guide](docs/CHECKLIST_GUIDE.md)** - How to use the packing checklist
- **[Currency Update](docs/CURRENCY_UPDATE.md)** - Currency conversion details

## Project Structure

```
traveloop/
├── docs/                      # Documentation
├── static/                    # Static files (CSS, JS, images)
├── templates/                 # HTML templates
│   ├── base.html             # Base template
│   ├── registration/         # Auth templates
│   └── trips/                # Trip-related templates
├── traveloop/                # Django project settings
│   ├── settings.py           # Main settings
│   ├── urls.py               # URL routing
│   └── wsgi.py               # WSGI config
├── trips/                    # Main application
│   ├── management/           # Management commands
│   │   └── commands/
│   │       ├── seed_data.py  # Seed cities & activities
│   │       └── clear_users.py # Clear user data
│   ├── migrations/           # Database migrations
│   ├── models.py             # Data models
│   ├── views.py              # View logic
│   ├── forms.py              # Form definitions
│   ├── urls.py               # App URLs
│   ├── supabase_auth.py      # Supabase integration
│   └── supabase_views.py     # Supabase auth views
├── .env                      # Environment variables (not in git)
├── .env.example              # Environment template
├── .gitignore                # Git ignore rules
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Database

**PostgreSQL** is used for all application data:
- Users and profiles
- Cities and activities
- Trips, stops, and itineraries
- Checklists and notes

**Supabase** is used only for authentication.

## Management Commands

### Seed Database
```bash
python manage.py seed_data
```
Populates the database with 22 cities and 88 activities.

### Clear Users
```bash
python manage.py clear_users --confirm
```
Removes all users and their data (use with caution).

## Key URLs

| URL | Description |
|-----|-------------|
| `/` | Home (redirects to login or dashboard) |
| `/login/` | Login page (Supabase) |
| `/signup/` | Signup page (Supabase) |
| `/forgot-password/` | Password reset |
| `/dashboard/` | User dashboard |
| `/trips/` | List all trips |
| `/trips/create/` | Create new trip |
| `/trips/{id}/` | Trip details |
| `/trips/{id}/builder/` | Itinerary builder |
| `/trips/{id}/checklist/` | Packing checklist |
| `/cities/` | Browse cities |
| `/activities/` | Browse activities |
| `/profile/` | User profile |

## Features in Detail

### Itinerary Builder
- Add multiple stops (cities) to your trip
- Set arrival and departure dates for each stop
- Add activities to each stop
- Track costs per stop
- Reorder stops

### Budget Tracking
- Set overall trip budget
- Track expenses by category:
  - Transport
  - Accommodation
  - Meals
  - Activities
- Visual progress bars
- Over-budget warnings

### Packing Checklist
- Organize items by category:
  - Clothing
  - Documents
  - Electronics
  - Toiletries
  - Medicine
  - Other
- Check off items as you pack
- Track packing progress

## Security

- Environment variables for sensitive data
- CSRF protection enabled
- Password validation
- Secure session management
- `.gitignore` configured to exclude secrets

## Contributing

This is a hackathon project. Feel free to fork and modify!

## License

This project is open source and available for educational purposes.

## Acknowledgments

- Built with Django
- Authentication powered by Supabase
- Images from Unsplash
- Icons from Unicode emoji

---

**Made with care for travelers**
