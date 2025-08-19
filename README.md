# Dopameme

Dopameme is an open-source platform to **document and share your lifestyle memories**.  
You can upload photos, videos, and other content to preserve your special moments and browse memories shared by others.

## Features
- Upload and share photos, videos, and more
- Browse memories from the community
- Like and comment on shared content
- Clean Python backend for easy setup
- Ready-to-use CI/CD pipeline with Jenkins (configure your own credentials)
- Environment-based configuration for secure credentials

## Getting Started

### Prerequisites
- Python 3.8+ installed
- pip (Python package manager)
- Database setup (SQLite by default; MySQL/PostgreSQL optional)
- Optional: Cloudinary / AWS / other storage service credentials for media files

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/dopameme.git
   cd dopameme
Install dependencies:

bash
Copy
Edit
pip install -r requirements.txt
Create a .env file based on .env.example and fill in your credentials:

bash
Copy
Edit
cp .env.example .env
# Edit .env with your own keys
Run the project:

bash
Copy
Edit
python app.py
Open your browser and go to http://localhost:5000 to use the app.

Contributing
We welcome contributions! To contribute:

Fork the repository

Create a new branch: git checkout -b feature-name

Make your changes and commit: git commit -m "Add feature"

Push to your branch: git push origin feature-name

Open a Pull Request

Please follow the coding style and keep secrets out of the code.

License
This project is licensed under the MIT License. See LICENSE for details.

Contact
Developer: \SambhavVinay

GitHub: https://github.com/SambhavVinay