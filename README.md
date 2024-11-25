# 🎯 HireTrack

A modern web application to track and manage your job applications efficiently.

![image](https://github.com/user-attachments/assets/e70d4bd6-082e-4896-894e-4cf5472c94d8)

## ✨ Features

- 📝 Track job applications with detailed information
- 💼 Monitor application status (Applied, Interview, Offered, Rejected)
- 💰 Record salary ranges in multiple currencies
- 📍 Track job locations and work types (Office, Hybrid, Remote)
- 📊 Import/Export data via CSV
- 🔒 Secure user authentication

## 🚀 Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/HireTrack.git
cd HireTrack
```

2. Set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python init_db.py
```

5. Run the application:
```bash
python run.py
```

Visit `http://localhost:5000` in your browser to start using HireTrack.

## 🛠️ Tech Stack

- **Backend**: Flask
- **Database**: SQLAlchemy
- **Authentication**: Flask-Login
- **Frontend**: HTML, CSS, JavaScript
- **UI Components**: Font Awesome

## 💡 Environment Variables

Create a `.env` file in the root directory:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///hiretrack.db
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (

git commit -m 'Add amazing feature'

)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

Created by Arkadiusz Kubiszewski

---
<p align="center">Made with ❤️ for job seekers</p>
```
