# Academic OS 🎓

A comprehensive, next-generation platform for school management, integrating HR, Academic Monitoring, and Intelligent Task Management into a single ecosystem.

![Dashboard Preview](static/img/dashboard-preview.png)
*(Note: Replace with actual screenshot path if available)*

## 🚀 Features

### 1. Digital HR & Competency
- **Employee Profiles**: Complete digital personnel files with contracts, categories, and bio.
- **KPI Tracking**: Real-time performance indicators for teachers based on lesson observations and task completion.
- **Role-Based Access**: Dynamic permissions for Directors, Heads of Departments, and Teachers.

### 2. Intelligent Workflow
- **Task Management**: Create, assign, and track tasks with deadlines.
- **Smart Dependencies**: Ensure tasks follow a logical order (Task B blocked by Task A).
- **Notifications**: Automated alerts for upcoming deadlines.

### 3. Academic Monitoring
- **Lesson Observations**: Digital checklist for evaluating teaching quality.
- **Resource Center**: Repository for sharing educational materials with version control.
- **Analytics**: Visual charts for performance tracking.

### 4. Premium UI/UX
- **Modern Dashboard**: Clean, responsive interface built with Bootstrap 5 and custom CSS.
- **Dark Sidebar**: Professional navigation menu with high contrast.
- **Glassmorphism**: Subtle modern effects for a premium feel.

## 🛠️ Tech Stack
- **Backend**: Django 5.0 (Python)
- **Database**: PostgreSQL (Production) / SQLite (Dev)
- **Frontend**: Django Templates + Bootstrap 5 + Vanilla JS
- **API**: Django REST Framework + JWT
- **Task Queue**: Celery + Redis (Ready for integration)

## 🏁 Getting Started

### Prerequisites
- Python 3.10+
- Virtualenv

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/academic-os.git
   cd academic-os
   ```

2. **Set up Virtual Environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate # Linux/Mac
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables**:
   Create a `.env` file in the root directory (see `.env.example`).

5. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Server**:
   ```bash
   python manage.py runserver
   ```

## 🧪 Verification

Run the included verification scripts to test module integrity:

```bash
python verify_org_setup.py   # Test Auth & Org Structure
python verify_hr_setup.py    # Test HR & KPI Logic
python verify_workflow.py    # Test Task Dependencies
python verify_academic.py    # Test Academic Modules
```

## 📄 License
This project is licensed under the MIT License.
