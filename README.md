# Jewelry Store Project

Dự án e-commerce được xây dựng với Flask (Python) và TailwindCSS.

## 📁 Cấu trúc dự án

```
flask-app/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes/              # Route handlers
│   │   ├── __init__.py
│   │   └── main.py          # Main routes
│   ├── templates/           # Jinja2 templates
│   │   ├── base.html        # Base layout
│   │   ├── index.html       # Trang chủ
│   │   └── about.html       # Trang giới thiệu
│   ├── static/              # Static files
│   │   ├── css/
│   │   │   ├── input.css    # TailwindCSS input
│   │   │   └── output.css   # Compiled CSS (generated)
│   │   ├── js/
│   │   │   └── main.js      # JavaScript
│   │   └── images/          # Images
│   ├── services/            # Business logic
│   └── models/              # Database models
├── tailwind.config.js       # TailwindCSS config
├── package.json             # Node dependencies
├── requirements.txt         # Python dependencies
├── run.py                   # Application entry point
└── README.md                # This file
└── LICENSE                  # License
```

## 🚀 Cài đặt và chạy dự án

### Bước 1: Cài đặt Python dependencies

```bash
# Tạo virtual environment (khuyến nghị)
python -m venv venv

# Kích hoạt virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### Bước 2: Cài đặt Node dependencies và TailwindCSS

```bash
# Cài đặt Node packages
npm install

# Build CSS lần đầu
npm run build-css
```

### Bước 3: Chạy dự án

**Terminal 1 - Chạy TailwindCSS watch (để tự động compile CSS khi có thay đổi):**
```bash
npm run watch-css
```

**Terminal 2 - Chạy Flask server:**
```bash
python run.py
```

Sau đó mở trình duyệt và truy cập: `http://localhost:5000`

## 📝 Các lệnh hữu ích

### Python/Flask
```bash
# Chạy Flask app
python run.py

# Chạy với Flask CLI
flask run
```

### TailwindCSS
```bash
# Build CSS một lần
npm run build-css

# Watch mode (tự động build khi có thay đổi)
npm run watch-css
```

## 🎨 Customization

### Thay đổi màu sắc TailwindCSS

Chỉnh sửa file `tailwind.config.js` để thay đổi theme colors:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Thay đổi màu primary tại đây
      },
    },
  },
}
```

### Thêm routes mới

1. Tạo file mới trong `app/routes/` hoặc thêm vào `app/routes/main.py`
2. Đăng ký blueprint trong `app/__init__.py`

### Thêm templates mới

1. Tạo file HTML trong `app/templates/`
2. Extend từ `base.html`:
```jinja2
{% extends "base.html" %}
{% block content %}
<!-- Your content here -->
{% endblock %}
```

## 🔧 Cấu hình môi trường

Tạo file `.env` để cấu hình:

```env
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
```

## 🛠️ Dependencies

```
blinker==1.9.0
click==8.3.1
colorama==0.4.6
Flask==3.1.2
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.3
ruff==0.14.6
Werkzeug==3.1.3
```

## 📚 Tài liệu tham khảo

- [Flask Documentation](https://flask.palletsprojects.com/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)

## 📄 License

MIT License

## 👤 Author

Bùi Minh Quân - Created for e-commerce project
