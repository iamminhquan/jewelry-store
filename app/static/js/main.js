// Main JavaScript file
document.addEventListener('DOMContentLoaded', function() {
    console.log('FlaskShop loaded');
    
    // Example: Add to cart functionality
    const addToCartButtons = document.querySelectorAll('.btn-primary');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            alert('Tính năng thêm vào giỏ hàng sẽ được triển khai sau!');
        });
    });
});

