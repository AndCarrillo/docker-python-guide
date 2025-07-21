# 🎓 Exercise 1: Basic Dockerfile

**Objective:** Create your first Dockerfile for a Python application from scratch.

## 🎯 Learning Goals

- Understand Dockerfile syntax and structure
- Write a basic Dockerfile for a Python application
- Apply Docker best practices
- Build and run your first containerized Python app

## 📋 Task Description

You'll containerize a simple Python calculator application that performs basic mathematical operations.

## 🏗️ What You'll Build

A command-line Python calculator that:
- Accepts two numbers and an operation
- Performs basic math operations (+, -, *, /)
- Returns the result
- Includes error handling

## 🚀 Getting Started

### Step 1: Create the Python Application

Create a file called `calculator.py` with the following content:

```python
#!/usr/bin/env python3

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b

def main():
    print("🧮 Python Calculator")
    print("Operations: +, -, *, /")
    
    try:
        num1 = float(input("Enter first number: "))
        operation = input("Enter operation (+, -, *, /): ").strip()
        num2 = float(input("Enter second number: "))
        
        if operation == '+':
            result = add(num1, num2)
        elif operation == '-':
            result = subtract(num1, num2)
        elif operation == '*':
            result = multiply(num1, num2)
        elif operation == '/':
            result = divide(num1, num2)
        else:
            print("❌ Invalid operation!")
            return
        
        print(f"✅ Result: {num1} {operation} {num2} = {result}")
        
    except ValueError as e:
        print(f"❌ Error: {e}")
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
```

### Step 2: Create requirements.txt

Create a `requirements.txt` file (even though this simple app has no external dependencies):

```
# No external dependencies for this basic calculator
# This file exists for demonstration purposes
```

### Step 3: Create .dockerignore

Create a `.dockerignore` file to exclude unnecessary files:

```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.pytest_cache/
.coverage
.vscode/
.idea/
*.log
.DS_Store
Thumbs.db
```

## 📝 Your Task: Write the Dockerfile

Now it's your turn! Create a `Dockerfile` that:

### ✅ Requirements Checklist

- [ ] Uses an appropriate Python base image (3.11 recommended)
- [ ] Sets a working directory
- [ ] Copies the requirements.txt file first
- [ ] Installs dependencies (even if none)
- [ ] Copies the application code
- [ ] Creates and uses a non-root user
- [ ] Sets the default command to run the calculator
- [ ] Includes proper comments explaining each step

### 💡 Hints

1. **Base Image**: Use `python:3.11-slim` for a good balance of features and size
2. **Working Directory**: `/app` is a common choice
3. **User Creation**: Use `adduser --disabled-password --gecos '' appuser`
4. **File Ownership**: Remember to change ownership with `chown`
5. **Default Command**: Use `CMD ["python", "calculator.py"]`

### 🎯 Challenge Level

**Beginner**: Follow the hints exactly  
**Intermediate**: Try to optimize the Dockerfile further  
**Advanced**: Add health checks or multi-stage builds

## 🧪 Testing Your Solution

### 1. Build the Image

```bash
docker build -t python-calculator .
```

### 2. Run the Container

```bash
docker run -it python-calculator
```

### 3. Test the Calculator

Try different operations:
- Addition: `5 + 3`
- Division: `10 / 2`
- Error case: `5 / 0`

### 4. Verify Security

Check that the container runs as non-root:

```bash
# In a separate terminal while container is running
docker exec <container-id> whoami
# Should output: appuser (not root)
```

## ✅ Solution Verification

Your solution should:

- [ ] **Build successfully** without errors
- [ ] **Run the calculator** interactively
- [ ] **Handle user input** properly
- [ ] **Execute as non-root** user
- [ ] **Be under 200MB** in size (check with `docker images`)

## 🎉 Bonus Challenges

Once you have a working solution, try these enhancements:

### 🏆 Advanced Features

1. **Add Environment Variables**
   - Set a `CALCULATOR_VERSION` environment variable
   - Display it when the calculator starts

2. **Optimize Image Size**
   - Try using `python:3.11-alpine` instead
   - Compare the final image sizes

3. **Add Health Check**
   - Create a simple health check script
   - Add it to your Dockerfile

4. **Multi-stage Build**
   - Implement a multi-stage build pattern
   - Even though it's overkill for this simple app

## 🔍 Common Issues and Solutions

### Build Fails
```bash
# Check Docker is running
docker info

# Verify file names and syntax
cat Dockerfile
```

### Permission Denied
```bash
# Make sure you're using a non-root user in the Dockerfile
# Check the USER instruction is present
```

### Container Exits Immediately
```bash
# Check if you're using the correct command
# For interactive apps, use: docker run -it <image>
```

## 📚 Solution Example

<details>
<summary>🔽 Click to see a sample solution (try on your own first!)</summary>

```dockerfile
# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file first (for better caching)
COPY requirements.txt .

# Install dependencies (none in this case, but good practice)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY calculator.py .

# Create non-root user for security
RUN adduser --disabled-password --gecos '' --shell /bin/bash appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Run the calculator
CMD ["python", "calculator.py"]
```

</details>

## 🔗 Next Steps

After completing this exercise:

1. **Compare Solutions**: Look at the sample solution and compare with yours
2. **Try Exercise 2**: Move on to [Multi-stage Builds](../02-multistage-build/)
3. **Explore Examples**: Check out the [Flask example](../../examples/flask-basic/)
4. **Experiment**: Try building other simple Python applications

## 📖 Key Takeaways

From this exercise, you should understand:

- **Dockerfile structure** and common instructions
- **Layer caching** and why order matters
- **Security practices** with non-root users
- **Docker build process** and basic commands
- **Container execution** and interaction

---

**⏱️ Estimated Time:** 30-45 minutes  
**🎯 Difficulty:** Beginner  
**📚 Prerequisites:** Basic Python knowledge, Docker installed
