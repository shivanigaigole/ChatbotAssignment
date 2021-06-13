# ChatbotAssignment

Create a chatbot that helps user to find out the population or capital of a specific country.

# Software Requirement

- Operating System : Windows-10-10.0.19041-SP0
- Python Version : 3.7.4
- RASA Version : 2.4.0

---

# Install required packages

- pip install -r requirement.txt

---

# Commands to run project

### **To train rasa project**

- rasa train

### **To rasa core server**

- rasa run -m models --enable-api --cors "\*"

#### **To rasa core server on different port**

- rasa run -p [PORT] -m models --enable-api --cors "\*"

### **To rasa actions server**

- rasa run actions

### **To rasa actions server on different port**

- rasa run actions -p [PORT]
