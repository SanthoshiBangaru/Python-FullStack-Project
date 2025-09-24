## 🍳Project: Recipe Finder & Manager

 A web application that allows users to search, add, and save recipes. Users can manage their personal recipe collection, browse ingredients, and bookmark favorite recipes for easy access. Built with Python (Flask) and Supabase (PostgreSQL) for backend and authentication, and a simple frontend for a seamless experience.

 ## Features:
 1. Recipe Search & Discovery

	• Integrate a recipe API like Spoonacular or Edamam.
	• Users can:
		○ Search recipes by ingredient/dish name.
		○ Filter by cuisine, dietary preferences (veg, keto, gluten-free).
		○ View recipe details (ingredients, instructions, nutrition).

2. User Recipe Manager (CRUD)

	• Save recipes from the API to personal collections.
	• Add custom recipes with images & instructions.
	• Organize with tags/categories (e.g., “breakfast,” “vegan”).

## Project Structure
Recipe Manager/
|
|___src/           # core application logic
|    |___logic.py  # Bussiness logic and task
|    |___db.py     # Database operations
|
|___Api/           # Backend Api
|    |___main.py   # FastAPI endpoints
|
|___FrontEnd/      # Frontend application
|    |___app.py    # Streamlit web interface
|
|___requirements.txt  # Python Dependencies
|___README.md      # Project documentation
|___.env           # Python variables

## Quick Start

### Prerequisites

- Python 3.8 or higher
- A Supabase account
- Git(Push, cloning)

### 1. Clone or Download the Project
# Option 1: Clone with Git
git clone <repository-url>

# Option 2: Download and extract the ZIP file

### 2. Install Dependencies
pip install -r requirements.txt

### 3. Set up Supabase Database
1. Create a supabase project
2. create the tasks table:
    - Go to SQL editor in your supabase dashboard
    -  Run the SQl command:

``` sql

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    mobile VARCHAR(15) UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE recipes (
    recipe_id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    instructions TEXT,
    image_url TEXT,
    source VARCHAR(100), -- e.g., "API" or "Custom"
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE ingredients (
    ingredient_id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);
CREATE TABLE recipe_ingredients (
    recipe_id INT REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    ingredient_id INT REFERENCES ingredients(ingredient_id),
    quantity VARCHAR(50),
    PRIMARY KEY (recipe_id, ingredient_id)
);
CREATE TABLE saved_recipes (
    user_id INT REFERENCES users(user_id) ON DELETE CASCADE,
    recipe_id INT REFERENCES recipes(recipe_id) ON DELETE CASCADE,
    saved_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (user_id, recipe_id)
);

```
3. Get your credentials.

### 4. Configure Environment variables

1. Create a `.env` file in the project root
2. Add your Supabase credentials to `.env`:
    SUPABASE_URL="your_project_url"
    SUPABASE_KEY="your_anon_key"

### 5. Run the Appllication

## Streamlit Frontend
streamlit run FrontEnd/app.py
The app will open in your browser at `http://localhost:8080`

## FastAPI Backend
cd Api
python main.py

The API will be available at `http://localhost:8000`

## How to Use
## Technical Details
## Technologies Use
    Frontend - Streamlit (Python web framework)
    Backend - FastAPI (Python REST API framework)
    Database - Supabase (PostgreSQL - based backend-as-a-service)
    Language - Python 3.8+

### Key Components

1. **`src/db.py`**: Database Operations 
    - Handles all CRUD operations with Supabase

2. **`src/logic.py`**: Bussiness logic 
    - Task validation and processing

3. **`Api/main.py`**: Backend Api
    - FastAPI endpoints

4. **`FrontEnd/app.py`**: Streamlit web interface

## Troubleshooting

## Common Issues

1. **"Module not found" error**:
    - Make sure you've installed all dependencies: pip install -r requirements.txt*
    - Check that you're running commands from the correct directory

## Future Enchancements

Ideas for extending this project:

- **User Authentication**: Add user accounts and login
- **Task Categories**: Organize tasks by subject or category
- **Notifications**: Email or push notifications for due dates
- **File Attachments**: Attach files to tasks
- **Collaboration**; Share tasks with classmates
- **Mobile App**; React Native or Flutter mobile version
- **Data Export**: Export tasks to CSV or PDF
- **Task Templates**: Create reusable task templates

## Support

If you encounter any issues or have any questions:
Contact - `+91 7032954936`
email - `itisanthoshibangaru7@gmail.com`