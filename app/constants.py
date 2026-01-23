"""
Order status constants and helper functions.

This module provides constants for order statuses and helper functions
to get status labels and CSS classes for display in templates.
"""


class OrderStatus:
    """Order status constants."""
    
    PENDING = 0       # Chờ xử lý
    PROCESSING = 1    # Đang xử lý
    SHIPPING = 2      # Đang giao hàng
    COMPLETED = 3     # Hoàn thành
    CANCELLED = 4     # Đã hủy

    # All valid statuses
    ALL = [PENDING, PROCESSING, SHIPPING, COMPLETED, CANCELLED]
    
    # Statuses that can be cancelled by user
    USER_CANCELLABLE = [PENDING, PROCESSING]
    
    # Statuses that can be updated by admin
    ADMIN_UPDATABLE = [PENDING, PROCESSING, SHIPPING]
    
    # Labels for each status (Vietnamese)
    LABELS = {
        PENDING: "Chờ xử lý",
        PROCESSING: "Đang xử lý",
        SHIPPING: "Đang giao hàng",
        COMPLETED: "Hoàn thành",
        CANCELLED: "Đã hủy",
    }
    
    # CSS classes for status badges (Tailwind CSS)
    BADGE_CLASSES = {
        PENDING: "bg-amber-100 text-amber-700 ring-1 ring-amber-200",
        PROCESSING: "bg-blue-100 text-blue-700 ring-1 ring-blue-200",
        SHIPPING: "bg-purple-100 text-purple-700 ring-1 ring-purple-200",
        COMPLETED: "bg-emerald-100 text-emerald-700 ring-1 ring-emerald-200",
        CANCELLED: "bg-red-100 text-red-700 ring-1 ring-red-200",
    }

    @classmethod
    def get_label(cls, status):
        """Get the display label for a status.
        
        Args:
            status: The status code (int).
            
        Returns:
            str: The Vietnamese label for the status.
        """
        return cls.LABELS.get(status, "Không xác định")
    
    @classmethod
    def get_badge_class(cls, status):
        """Get the Tailwind CSS classes for a status badge.
        
        Args:
            status: The status code (int).
            
        Returns:
            str: The Tailwind CSS classes for the badge.
        """
        return cls.BADGE_CLASSES.get(status, "bg-slate-100 text-slate-700 ring-1 ring-slate-200")
    
    @classmethod
    def can_user_cancel(cls, status):
        """Check if a user can cancel an order with this status.
        
        Args:
            status: The status code (int).
            
        Returns:
            bool: True if the order can be cancelled by the user.
        """
        return status in cls.USER_CANCELLABLE
    
    @classmethod
    def can_admin_update(cls, status):
        """Check if an admin can update an order with this status.
        
        Args:
            status: The status code (int).
            
        Returns:
            bool: True if the order can be updated by an admin.
        """
        return status in cls.ADMIN_UPDATABLE
    
    @classmethod
    def get_all_statuses(cls):
        """Get a list of all statuses with their labels.
        
        Returns:
            list: List of tuples (status_code, label).
        """
        return [(status, cls.LABELS[status]) for status in cls.ALL]
