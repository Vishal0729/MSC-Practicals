# Install MongoDB Community Edition on Windows
# Download from: mongodb.com/try/download/community

# Install Python driver
#pip install pymongo

from pymongo import MongoClient
import random
from datetime import datetime, timedelta

# ===== CONNECT TO MONGODB =====
client = MongoClient("mongodb://localhost:27017/")
db = client["company_db"]
collection = db["employees"]

# Drop existing collection (fresh start)
collection.drop()

print("=" * 65)
print("   PART 1: STORING LARGE DATASET IN MONGODB")
print("=" * 65)


# ===== GENERATE LARGE DATASET (10,000+ Records) =====
random.seed(42)

departments = ["Engineering", "Marketing", "Finance", "HR", 
               "Sales", "Operations", "Research", "Support"]

designations = {
    "Engineering": ["Software Engineer", "Senior Engineer", "Tech Lead", 
                    "Principal Engineer", "DevOps Engineer"],
    "Marketing": ["Marketing Analyst", "Campaign Manager", "SEO Specialist",
                  "Content Strategist", "Brand Manager"],
    "Finance": ["Financial Analyst", "Accountant", "Auditor", 
                "Tax Consultant", "Finance Manager"],
    "HR": ["HR Executive", "Recruiter", "HR Manager", 
           "Training Coordinator", "Payroll Specialist"],
    "Sales": ["Sales Executive", "Account Manager", "Sales Lead",
              "Business Developer", "Regional Manager"],
    "Operations": ["Operations Analyst", "Supply Chain Manager", 
                   "Logistics Coordinator", "Process Engineer", "QA Analyst"],
    "Research": ["Research Scientist", "Data Analyst", "Lab Technician",
                 "Research Lead", "Statistician"],
    "Support": ["Support Engineer", "Help Desk Analyst", "IT Admin",
                "System Administrator", "Network Engineer"]
}

cities = ["New York", "London", "Tokyo", "Mumbai", "Sydney",
          "Berlin", "Toronto", "Singapore", "Dubai", "Paris"]

skills_pool = ["Python", "Java", "SQL", "Excel", "Machine Learning",
               "Data Analysis", "Communication", "Leadership", "JavaScript",
               "Cloud Computing", "Project Management", "R", "Tableau",
               "Power BI", "Docker", "Kubernetes", "AWS", "Azure"]

first_names = ["Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona",
               "George", "Hannah", "Isaac", "Julia", "Kevin", "Laura",
               "Michael", "Natalie", "Oscar", "Patricia", "Quinn", "Robert",
               "Sarah", "Thomas", "Uma", "Victor", "Wendy", "Xavier", "Yara", "Zack"]

last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
              "Miller", "Davis", "Martinez", "Anderson", "Taylor", "Thomas",
              "Moore", "Jackson", "Martin", "Lee", "Walker", "Hall", "Allen", "Young"]


def generate_employee(emp_id):
    """Generate a single employee record"""
    dept = random.choice(departments)
    join_date = datetime(2015, 1, 1) + timedelta(days=random.randint(0, 3500))
    
    record = {
        "emp_id": f"EMP{emp_id:05d}",
        "first_name": random.choice(first_names),
        "last_name": random.choice(last_names),
        "age": random.randint(22, 60),
        "gender": random.choice(["Male", "Female", "Other"]),
        "department": dept,
        "designation": random.choice(designations[dept]),
        "city": random.choice(cities),
        "salary": round(random.uniform(30000, 150000), 2),
        "experience_years": random.randint(0, 35),
        "skills": random.sample(skills_pool, random.randint(2, 6)),
        "join_date": join_date,
        "is_active": random.choice([True, True, True, False]),  # 75% active
        "performance_rating": round(random.uniform(1.0, 5.0), 1),
        "projects_completed": random.randint(0, 50),
        "email": f"emp{emp_id}@company.com",
        "phone": f"+1-{random.randint(100,999)}-{random.randint(1000,9999)}"
    }
    return record


# ===== GENERATE 10,000 RECORDS =====
print("\n[1] Generating 10,000 employee records...")
dataset = [generate_employee(i) for i in range(1, 10001)]
print(f"    Records generated: {len(dataset)}")


# ===== INSERT INTO MONGODB =====
print("\n[2] Inserting records into MongoDB...")

# Method 1: Bulk insert (efficient for large data)
result = collection.insert_many(dataset)
print(f"    Records inserted: {len(result.inserted_ids)}")


# ===== VERIFY INSERTION =====
print("\n[3] Verifying insertion...")
total_count = collection.count_documents({})
print(f"    Total documents in collection: {total_count}")


# ===== SHOW SAMPLE RECORD =====
print("\n[4] Sample record from MongoDB:")
sample = collection.find_one({"emp_id": "EMP00001"})
for key, value in sample.items():
    if key != "_id":
        print(f"    {key:<22}: {value}")


# ===== CREATE INDEXES (Performance Optimization) =====
print("\n[5] Creating indexes for better query performance...")
collection.create_index("emp_id", unique=True)
collection.create_index("department")
collection.create_index("city")
collection.create_index("salary")
collection.create_index("age")
print("    Indexes created: emp_id, department, city, salary, age")


# ===== SHOW COLLECTION STATS =====
print("\n[6] Collection Statistics:")
stats = db.command("collstats", "employees")
print(f"    Collection: employees")
print(f"    Document count: {stats['count']}")
print(f"    Storage size: {stats['storageSize'] / 1024:.2f} KB")
print(f"    Avg document size: {stats['avgObjSize']} bytes")
print(f"    Number of indexes: {stats['nindexes']}")

print("\n" + "=" * 65)
print("   DATASET STORED SUCCESSFULLY!")
print("=" * 65)




#++Seperate-file++++Seperate-file++++Seperate-file++++Seperate-file++++Seperate-file++++Seperate-file++++Seperate-file++++Seperate-file++++Seperate-file++++Seperate-file++

from pymongo import MongoClient

# ===== CONNECT =====
client = MongoClient("mongodb://localhost:27017/")
db = client["company_db"]
collection = db["employees"]

print("=" * 65)
print("   PART 2: BASIC MONGODB QUERIES USING PYTHON")
print("=" * 65)


# ===== QUERY 1: Find One Document =====
print("\n[Query 1] Find one employee from Engineering department:")
result = collection.find_one({"department": "Engineering"})
print(f"  Name: {result['first_name']} {result['last_name']}")
print(f"  Designation: {result['designation']}")
print(f"  Salary: ${result['salary']:,.2f}")


# ===== QUERY 2: Find with Filter =====
print("\n[Query 2] Employees in Tokyo with salary > $100,000:")
results = collection.find({
    "city": "Tokyo",
    "salary": {"$gt": 100000}
}).limit(5)

for emp in results:
    print(f"  {emp['first_name']:<10} {emp['last_name']:<12} "
          f"${emp['salary']:>10,.2f}  {emp['department']}")


# ===== QUERY 3: Count Documents =====
print("\n[Query 3] Count queries:")
total = collection.count_documents({})
active = collection.count_documents({"is_active": True})
engineering = collection.count_documents({"department": "Engineering"})
high_salary = collection.count_documents({"salary": {"$gt": 100000}})

print(f"  Total employees:        {total}")
print(f"  Active employees:       {active}")
print(f"  Engineering dept:       {engineering}")
print(f"  Salary > $100,000:      {high_salary}")


# ===== QUERY 4: Sorting =====
print("\n[Query 5] Top 5 highest paid employees:")
results = collection.find(
    {},
    {"_id": 0, "first_name": 1, "last_name": 1, "salary": 1, "department": 1}
).sort("salary", -1).limit(5)

for i, emp in enumerate(results, 1):
    print(f"  {i}. {emp['first_name']} {emp['last_name']:<12} "
          f"${emp['salary']:>10,.2f}  ({emp['department']})")



# ===== QUERY 5: Update & Delete =====
print("\n[Query 10] Update and Delete operations:")

# Update one document
update_result = collection.update_one(
    {"emp_id": "EMP00001"},
    {"$set": {"salary": 95000, "designation": "Senior Engineer"}}
)
print(f"  Update one - Modified: {update_result.modified_count}")

# Update many documents
update_result = collection.update_many(
    {"department": "Engineering", "experience_years": {"$gt": 10}},
    {"$set": {"is_senior": True}}
)
print(f"  Update many (senior flag) - Modified: {update_result.modified_count}")

# Delete one document
delete_result = collection.delete_one({"emp_id": "EMP10000"})
print(f"  Delete one - Deleted: {delete_result.deleted_count}")

# Final count
print(f"\n  Final document count: {collection.count_documents({})}")


print("\n" + "=" * 65)
print("   ALL QUERIES EXECUTED SUCCESSFULLY!")
print("=" * 65)