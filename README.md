# FlaskShop - Flask + TailwindCSS Project

Dự án e-commerce được xây dựng với Flask (Python) và TailwindCSS, có cấu trúc sạch và dễ mở rộng.

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

Tạo file `.env` (không commit vào git) để cấu hình:

```env
SECRET_KEY=your-secret-key-here
FLASK_DEBUG=True
```

## 📦 Mở rộng cho E-commerce

### Các tính năng cần thêm:

1. **Models & Database**
   - Cài đặt SQLAlchemy hoặc MongoDB
   - Tạo models: User, Product, Order, Cart, Category
   - Thêm vào `app/models/`

2. **Authentication**
   - Flask-Login cho user session
   - Flask-Bcrypt cho password hashing
   - Routes: `/login`, `/register`, `/logout`

3. **Product Management**
   - Routes: `/products`, `/product/<id>`
   - CRUD operations cho products
   - Image upload (Flask-Uploads)

4. **Shopping Cart**
   - Session-based cart
   - Routes: `/cart`, `/cart/add`, `/cart/remove`
   - AJAX để update cart không reload page

5. **Checkout & Orders**
   - Routes: `/checkout`, `/orders`
   - Payment integration (Stripe, PayPal)
   - Order confirmation email

6. **Admin Panel**
   - Flask-Admin hoặc custom admin
   - Quản lý products, orders, users

7. **API Endpoints**
   - RESTful API cho mobile app
   - Flask-RESTful hoặc Flask-RESTX

### Cấu trúc mở rộng đề xuất:

```
app/
├── routes/
│   ├── main.py          # Public routes
│   ├── auth.py          # Authentication
│   ├── products.py      # Product routes
│   ├── cart.py          # Cart routes
│   ├── orders.py        # Order routes
│   └── admin.py         # Admin routes
├── services/
│   ├── auth_service.py
│   ├── product_service.py
│   ├── cart_service.py
│   └── order_service.py
├── models/
│   ├── user.py
│   ├── product.py
│   ├── order.py
│   └── cart.py
└── utils/
    ├── validators.py
    └── helpers.py
```

## 🛠️ Dependencies đề xuất cho E-commerce

Thêm vào `requirements.txt`:

```
Flask==3.0.0
Flask-Login==0.6.3
Flask-Bcrypt==1.0.1
Flask-SQLAlchemy==3.1.1
Flask-Migrate==4.0.5
Flask-Mail==0.9.1
Flask-Uploads==0.2.1
python-dotenv==1.0.0
```

## 📚 Tài liệu tham khảo

- [Flask Documentation](https://flask.palletsprojects.com/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)

## 📄 License

MIT License

## 👤 Author

Created for e-commerce project

