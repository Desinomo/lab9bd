Для запуску проекту потрібно:

1. Встановити залежності:

```bash
pip install flask pymongo python-dotenv
```

2. Створити файл .env з посиланням на MongoDB:

```
MONGODB_URI=mongodb+srv://your_username:your_password@your_cluster.mongodb.net/sport_club
```

3. Запустити додаток:

```bash
python app.py
```