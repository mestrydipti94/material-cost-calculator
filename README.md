📌 Material Cost Calculator

A Python Flask-based web application designed to simplify material quantity and cost calculations for product planning and pre-production estimation.

The application allows users to manage material details, calculate material costs, estimate material requirements for products, and maintain a history of calculations using SQLite.

Project Overview

The Material Cost Calculator helps reduce manual calculations when estimating the quantity and cost of materials required for a product.

The application provides two main calculation approaches:

- **Normal Material Calculator** – Calculate material quantity and cost based on entered material details.
- **Pre-Production Calculator** – Estimate material requirements and cost for a product before starting production.

The project uses Flask for the backend, SQLite for data storage, and HTML/CSS for the user interface.

 ✨ Features

  Material Management
- Add new materials
- Store material name, unit, and price
- View available materials
- Manage material information

 Material Calculation
- Calculate required material quantity
- Calculate material cost
- Calculate price per unit
- Calculate total estimated material cost

Pre-Production Estimation
- Enter product details
- Estimate material requirements before production
- Calculate estimated material cost
- Perform product-based cost estimation

Calculation History
- Store previous calculations
- View calculation history
- Track product and material estimates
- Store calculation type and cost details

 User Interface
- Clean and simple interface
- Responsive layout
- Custom background and logo
- Separate pages for different calculator functions

 🛠️ Technologies Used

- **Python** – Application logic
- **Flask** – Web application framework
- **SQLite** – Database management
- **HTML5** – Web page structure
- **CSS3** – Styling and responsive design
- **Git** – Version control
- **GitHub** – Source code hosting
- **VS Code** – Development environment

 📂 Project Structure

material-cost-calculator/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── static/
│   ├── bg.png
│   ├── logo.png
│   └── style.css
│
├── templates/
│   ├── home.html
│   ├── add_material.html
│   ├── materials.html
│   ├── normal_calculator.html
│   ├── pre_production.html
│   └── history.html
│
└── database.db

⚙️ Application Flow
User
  │
  ▼
Flask Web Application
  │
  ├── Material Management
  │
  ├── Normal Calculator
  │
  ├── Pre-Production Calculator
  │
  └── Calculation History
          │
          ▼
      SQLite Database
      
🚀 Getting Started
1. Clone the Repository
git clone https://github.com/mestrydipti94/material-cost-calculator.git
2. Navigate to the Project
cd material-cost-calculator
3. Create a Virtual Environment

For Windows:

python -m venv venv

Activate the virtual environment:

venv\Scripts\activate
4. Install Dependencies
pip install -r requirements.txt
5. Run the Application
python app.py

The Flask development server will start locally.

Open the URL displayed in your terminal, usually:

http://127.0.0.1:5000/

🗄️ Database
The application uses SQLite to store material information and calculation history.

The database can contain information such as:

Material name
Unit
Material price
Product name
Required quantity
Total material
Price per unit
Total cost
Calculation type

The local database file is excluded from GitHub using .gitignore.

🎯 Project Objectives
The main objectives of this project are to:
Reduce manual material cost calculations
Make material estimation easier
Calculate product material costs efficiently
Store calculation history for reference
Practice Python and Flask web development
Understand database integration using SQLite

💡 What I Learned
Through this project, I gained practical experience with:
Python programming
Flask application development
Flask routes and templates
HTML template rendering
Form handling
SQLite database integration
CRUD operations
Connecting frontend pages with backend logic
Git and GitHub
Organizing a Python web application

🔮 Future Improvements
Possible future improvements include:
User authentication
Export calculations to PDF or Excel
Advanced reporting
Product-wise cost reports
Improved dashboard with charts
Cloud database integration
Deployment to a production server

👩‍💻 Author

Dipti Mestry
BCA Graduate | Aspiring Python Developer
GitHub:
https://github.com/mestrydipti94

📄 License
This project is created for learning, portfolio, and educational purposes.
