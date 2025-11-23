# MongoDB Database Setup Guide

## Prerequisites
- Docker and Docker Compose installed (recommended)
- OR MongoDB installed locally

## Option 1: Using Docker (Recommended)

### 1. Start MongoDB with Docker Compose

```bash
cd backend
docker-compose up -d
```

This will start:
- **MongoDB** on port `27017`
- **Mongo Express** (Web UI) on port `8081`

### 2. Access Mongo Express (Web UI)
- URL: http://localhost:8081
- Username: `admin`
- Password: `admin123`

### 3. Update Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cp .env.example .env
```

Make sure your `.env` has:
```env
MONGODB_URL=mongodb://admin:admin123@localhost:27017/ecommerce_db?authSource=admin
DATABASE_NAME=ecommerce_db
```

### 4. Initialize Database with Sample Data

Install Python dependencies first:
```bash
pip install -r requirements.txt
```

Run the initialization script:
```bash
python scripts/init_db.py
```

This will create:
- **3 users** (1 admin, 2 regular users)
- **18+ products** across multiple categories
- **Database indexes** for optimal performance
- **Sample orders** and empty carts

### 5. (Optional) Add More Products

```bash
python scripts/seed_more_products.py
```

### 6. Verify Setup

Check the database using Mongo Express or run:
```bash
python -c "from pymongo import MongoClient; client = MongoClient('mongodb://admin:admin123@localhost:27017/?authSource=admin'); print(client.ecommerce_db.products.count_documents({}))"
```

---

## Option 2: Local MongoDB Installation

### 1. Install MongoDB

**Windows:**
- Download from https://www.mongodb.com/try/download/community
- Install MongoDB Community Server
- Start MongoDB service

**macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

**Linux (Ubuntu):**
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
```

### 2. Update Environment Variables

Create `.env` file:
```env
MONGODB_URL=mongodb://localhost:27017/ecommerce_db
DATABASE_NAME=ecommerce_db
```

### 3. Initialize Database

```bash
pip install -r requirements.txt
python scripts/init_db.py
```

---

## Test Credentials

After running `init_db.py`, use these credentials to test:

### Admin Account
- **Email:** admin@ecommerce.com
- **Password:** admin123
- **Access:** Full admin privileges

### Regular User Accounts
- **Email:** john@example.com
  - **Password:** password123

- **Email:** jane@example.com
  - **Password:** password123

---

## Database Collections

### `users`
- Stores user accounts with authentication data
- Fields: email, hashed_password, first_name, last_name, phone, is_active, is_admin
- Index: unique on email

### `products`
- Product catalog with details
- Fields: name, description, price, category, stock, images
- Indexes: category, price, text search on name/description

### `carts`
- Shopping carts for users
- Fields: user_id, items (array), updated_at
- Index: unique on user_id

### `orders`
- Order history and tracking
- Fields: user_id, items, total, status, shipping_address, payment_method
- Indexes: user_id, status, created_at

---

## Database Management Commands

### Stop MongoDB (Docker)
```bash
docker-compose down
```

### Stop and Remove Data (Docker)
```bash
docker-compose down -v
```

### Restart MongoDB (Docker)
```bash
docker-compose restart
```

### View MongoDB Logs (Docker)
```bash
docker-compose logs -f mongodb
```

### Connect to MongoDB Shell (Docker)
```bash
docker exec -it ecommerce_mongodb mongosh -u admin -p admin123 --authenticationDatabase admin
```

### Reset Database
```bash
python scripts/init_db.py
```
This drops existing collections and recreates them with fresh data.

---

## Backup and Restore

### Backup Database
```bash
docker exec ecommerce_mongodb mongodump --username admin --password admin123 --authenticationDatabase admin --db ecommerce_db --out /tmp/backup
docker cp ecommerce_mongodb:/tmp/backup ./backup
```

### Restore Database
```bash
docker cp ./backup ecommerce_mongodb:/tmp/backup
docker exec ecommerce_mongodb mongorestore --username admin --password admin123 --authenticationDatabase admin --db ecommerce_db /tmp/backup/ecommerce_db
```

---

## Troubleshooting

### MongoDB Connection Error
- Ensure MongoDB is running: `docker ps` or `sudo systemctl status mongod`
- Check port 27017 is not blocked by firewall
- Verify connection string in `.env` file

### Authentication Failed
- Make sure you're using the correct credentials
- For Docker: use `authSource=admin` in connection string
- For local: authentication might not be enabled by default

### Port Already in Use
- Change ports in `docker-compose.yml`:
  ```yaml
  ports:
    - "27018:27017"  # Use different port
  ```
- Update `MONGODB_URL` accordingly

### Container Won't Start
- Check logs: `docker-compose logs mongodb`
- Ensure no other MongoDB instance is running on port 27017
- Try: `docker-compose down -v` and start again

---

## Production Deployment

For production:
1. Use MongoDB Atlas (managed cloud service)
2. Enable authentication and SSL
3. Set up regular backups
4. Configure connection pooling
5. Use environment-specific connection strings
6. Enable monitoring and alerting

---

## Useful Resources

- [MongoDB Documentation](https://docs.mongodb.com/)
- [Motor (Async Driver) Documentation](https://motor.readthedocs.io/)
- [MongoDB Atlas (Cloud)](https://www.mongodb.com/cloud/atlas)
- [Mongo Express](https://github.com/mongo-express/mongo-express)
