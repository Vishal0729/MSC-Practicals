# Install MongoDB Community Edition on Windows
# Download from: mongodb.com/try/download/community

# Install R driver
#install.packages("mongolite")

library(mongolite)

# ===== CONNECT TO MONGODB =====
con <- mongo(collection = "employees", db = "company_db", 
             url = "mongodb://localhost:27017/")

# Drop existing collection
con$drop()

cat(strrep("=", 65), "\n")
cat("   PART 1: STORING LARGE DATASET IN MONGODB\n")
cat(strrep("=", 65), "\n")


# ===== GENERATE LARGE DATASET (10,000 Records) =====
set.seed(42)

departments <- c("Engineering", "Marketing", "Finance", "HR",
                 "Sales", "Operations", "Research", "Support")

cities <- c("New York", "London", "Tokyo", "Mumbai", "Sydney",
            "Berlin", "Toronto", "Singapore", "Dubai", "Paris")

skills_pool <- c("Python", "Java", "SQL", "Excel", "Machine Learning",
                 "Data Analysis", "Communication", "Leadership", "JavaScript",
                 "Cloud Computing", "Project Management", "R", "Tableau")

first_names <- c("Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona",
                 "George", "Hannah", "Isaac", "Julia", "Kevin", "Laura",
                 "Michael", "Natalie", "Oscar", "Patricia", "Quinn", "Robert")

last_names <- c("Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
                "Miller", "Davis", "Martinez", "Anderson", "Taylor", "Thomas")

n <- 10000
cat(sprintf("\n[1] Generating %d employee records...\n", n))

# Generate data frame
dataset <- data.frame(
  emp_id = sprintf("EMP%05d", 1:n),
  first_name = sample(first_names, n, replace = TRUE),
  last_name = sample(last_names, n, replace = TRUE),
  age = sample(22:60, n, replace = TRUE),
  gender = sample(c("Male", "Female", "Other"), n, replace = TRUE, 
                  prob = c(0.45, 0.45, 0.10)),
  department = sample(departments, n, replace = TRUE),
  city = sample(cities, n, replace = TRUE),
  salary = round(runif(n, 30000, 150000), 2),
  experience_years = sample(0:35, n, replace = TRUE),
  join_date = as.character(as.Date("2015-01-01") + sample(0:3500, n, replace = TRUE)),
  is_active = sample(c(TRUE, FALSE), n, replace = TRUE, prob = c(0.75, 0.25)),
  performance_rating = round(runif(n, 1.0, 5.0), 1),
  projects_completed = sample(0:50, n, replace = TRUE),
  email = paste0("emp", 1:n, "@company.com"),
  stringsAsFactors = FALSE
)

cat(sprintf("    Records generated: %d\n", nrow(dataset)))


# ===== INSERT INTO MONGODB =====
cat("\n[2] Inserting records into MongoDB...\n")
con$insert(dataset)
cat(sprintf("    Records inserted: %d\n", nrow(dataset)))


# ===== VERIFY INSERTION =====
cat("\n[3] Verifying insertion...\n")
total_count <- con$count()
cat(sprintf("    Total documents in collection: %d\n", total_count))


# ===== SHOW SAMPLE RECORD =====
cat("\n[4] Sample record from MongoDB:\n")
sample_rec <- con$find('{"emp_id": "EMP00001"}')
print(sample_rec)


# ===== CREATE INDEXES =====
cat("\n[5] Creating indexes...\n")
con$index(add = '{"emp_id": 1}')
con$index(add = '{"department": 1}')
con$index(add = '{"salary": 1}')
con$index(add = '{"city": 1}')
cat("    Indexes created: emp_id, department, salary, city\n")


# ===== SHOW STATS =====
cat("\n[6] Collection Statistics:\n")
cat(sprintf("    Document count: %d\n", con$count()))
cat(sprintf("    Indexes: %d\n", nrow(con$index())))

cat("\n", strrep("=", 65), "\n")
cat("   DATASET STORED SUCCESSFULLY!\n")
cat(strrep("=", 65), "\n")


#++Seperate-file++++Seperate-file++++Seperate-file++++Seperate-file++++Seperate-file++++Seperate-file++++Seperate-file++++Seperate-file++++Seperate-file++++Seperate-file++


library(mongolite)

# ===== CONNECT =====
con <- mongo(collection = "employees", db = "company_db",
             url = "mongodb://localhost:27017/")

cat(strrep("=", 65), "\n")
cat("   PART 2: BASIC MONGODB QUERIES USING R\n")
cat(strrep("=", 65), "\n")


# ===== QUERY 1: Find One Document =====
cat("\n[Query 1] Find one employee from Engineering department:\n")
result <- con$find('{"department": "Engineering"}', limit = 1)
cat(sprintf("  Name: %s %s\n", result$first_name, result$last_name))
cat(sprintf("  Salary: $%s\n", format(result$salary, big.mark = ",")))


# ===== QUERY 2: Find with Filter =====
cat("\n[Query 2] Employees in Tokyo with salary > $100,000:\n")
results <- con$find(
  query = '{"city": "Tokyo", "salary": {"$gt": 100000}}',
  limit = 5
)
print(results[, c("first_name", "last_name", "salary", "department")])


# ===== QUERY 3: Count Documents =====
cat("\n[Query 3] Count queries:\n")
cat(sprintf("  Total employees:    %d\n", con$count()))
cat(sprintf("  Active employees:   %d\n", con$count('{"is_active": true}')))
cat(sprintf("  Engineering dept:   %d\n", con$count('{"department": "Engineering"}')))
cat(sprintf("  Salary > $100,000:  %d\n", con$count('{"salary": {"$gt": 100000}}')))


# ===== QUERY 4: Sorting =====
cat("\n[Query 5] Top 5 highest paid employees:\n")
results <- con$find(
  query = '{}',
  fields = '{"_id": false, "first_name": true, "last_name": true, 
             "salary": true, "department": true}',
  sort = '{"salary": -1}',
  limit = 5
)
print(results)



# ===== QUERY 5: Update & Delete =====
cat("\n[Query 10] Update and Delete operations:\n")

# Update one
con$update(
  query = '{"emp_id": "EMP00001"}',
  update = '{"$set": {"salary": 95000, "designation": "Senior Engineer"}}'
)
cat("  Update one: Done\n")

# Update many
con$update(
  query = '{"department": "Engineering", "experience_years": {"$gt": 10}}',
  update = '{"$set": {"is_senior": true}}',
  multiple = TRUE
)
cat("  Update many (senior flag): Done\n")

# Delete one
con$remove('{"emp_id": "EMP09999"}', just_one = TRUE)
cat("  Delete one: Done\n")

cat(sprintf("\n  Final document count: %d\n", con$count()))

cat("\n", strrep("=", 65), "\n")
cat("   ALL QUERIES EXECUTED SUCCESSFULLY!\n")
cat(strrep("=", 65), "\n")