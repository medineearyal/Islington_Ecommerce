The Islington Marketplace is a Django-based web application designed as a digital platform where students, staff, and residents of Islington can buy, sell, and compare items easily. The project focuses on creating a simple yet efficient marketplace tailored to the needs of the local community, especially Islington students.

The system is role-based and provides separate dashboards for different types of users: Admin, Seller, and Buyer. The Admin dashboard offers complete control of the platform, including managing users, monitoring product listings, and handling reported issues to maintain the integrity of the marketplace. The Seller/User dashboard allows sellers to manage their shop profile, add product listings with details such as name, description, and price, and also upload a personal QR code during registration to enable direct payments from buyers. Buyers, on the other hand, can browse through products, search and filter by price range, compare prices from different sellers, and track their orders through a clean and simple interface.

The platform integrates Khalti for secure digital payments and supports QR-based payments uploaded by sellers, providing flexibility and ease for students and other users who prefer cashless transactions. Built with Django and Python, using PostgreSQL as the database, and Tailwind CSS for a modern, responsive frontend, the Islington Marketplace demonstrates the combination of robust backend functionality with a sleek user experience, tailored to the unique needs of the Islington student community.

Features of Islington Marketplace:

The Islington Marketplace offers a role-based system with distinct dashboards for Admins, Sellers, and Buyers, ensuring that each user type has access to the tools needed. Admins have full control over the platform, including user management, monitoring product listings, and handling reported issues to maintain a safe and organized marketplace.

SetUp Instructions:

- To run the Islington Marketplace project locally, the repository should first be cloned from GitHub or the ZIP file downloaded and extracted to a preferred folder. A Python virtual environment is recommended to keep dependencies isolated, which can be created by running python -m venv venv and activated using venv\Scripts\activate on Windows or source venv/bin/activate on Mac/Linux. Once active, all required packages listed in requirements.txt can be installed using pip install -r requirements.txt.

- After installing dependencies, the PostgreSQL database must be set up and configured. Once the database is ready, Django migrations should be executed by running python manage.py makemigrations followed by python manage.py migrate, which creates all necessary tables in the database. A superuser account for the admin dashboard can be created using python manage.py createsuperuser, with email, username, and password entered as prompted.

- .env file should be created in the root directory to store environment variables such as the Django secret key, debug mode, Khalti API keys, and database connection details. After completing these steps, the development server can be started with python manage.py runserver, and the application will be accessible in a browser at http://127.0.0.1:8000/
# Sample Env
- DATABASE_URL=postgres://<DB_USER>:<DB_PASS>@<HOST>:<PORT>/<DB_NAME>
- DEFAULT_FROM_EMAIL= 
- EMAIL_HOST= 
- EMAIL_HOST_USER= 
- EMAIL_HOST_PASSWORD= 
- EMAIL_PORT= 
- KHALTI_BASE_URL= 
- KHALTI_API_KEY=
