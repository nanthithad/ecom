"""
E-Commerce OOP Demo (Fully Commented)
-------------------------------------
Demonstrates major Object-Oriented Programming concepts in an e-commerce domain.

OOP Concepts Demonstrated:
1. Abstraction (Abstract Base Classes)
2. Inheritance (Subclasses extending a base class)
3. Polymorphism (Method overriding)
4. Encapsulation (Private/protected attributes & properties)
5. Composition (Order has OrderItems and Customer)
6. Mixins / Multiple Inheritance
7. Properties & Setters
8. Class & Static Methods
9. Dependency Inversion (using abstract interfaces for gateways/services)
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Iterable, Optional
from datetime import datetime
import uuid

# ===========================================================
# MIXIN CLASS – Demonstrates Multiple Inheritance
# ===========================================================

class AuditableMixin:
    """Adds logging or audit trail capability to any class that inherits this."""
    def _audit(self, message: str) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[AUDIT {timestamp}] {self.__class__.__name__}: {message}"


# ===========================================================
# BASIC VALUE OBJECTS
# ===========================================================

@dataclass(frozen=True)
class Address:
    """Immutable data holder for customer addresses."""
    line1: str
    city: str
    country: str
    postal_code: str


@dataclass
class Customer(AuditableMixin):
    """Represents a customer and inherits from AuditableMixin to gain audit logging."""
    customer_id: str
    name: str
    email: str
    address: Address

    def describe(self) -> str:
        """Human-readable summary of the customer details."""
        return (
            f"Customer[{self.customer_id}] {self.name} <{self.email}>\n"
            f"  Address: {self.address.line1}, {self.address.city}, "
            f"{self.address.country} - {self.address.postal_code}"
        )


# ===========================================================
# ABSTRACT BASE PRODUCT CLASS – Demonstrates Abstraction, Encapsulation, Properties
# ===========================================================

class Product(AuditableMixin, ABC):
    """Abstract base class for all products (physical, digital, etc.)"""

    def __init__(self, sku: str, name: str, price: float):
        # Encapsulation: Using private attribute _price to enforce validation
        if not self.validate_sku(sku):
            raise ValueError("Invalid SKU format. Must be uppercase alphanumeric (6–12 chars).")
        self._sku = sku
        self.name = name
        self.price = price  # invokes the property setter

    # ------------------- Encapsulation using property -------------------
    @property
    def price(self) -> float:
        """Public getter for price."""
        return self._price

    @price.setter
    def price(self, v: float) -> None:
        """Setter that validates price to prevent negative values."""
        if v < 0:
            raise ValueError("Price cannot be negative.")
        self._price = round(float(v), 2)

    # SKU as read-only property
    @property
    def sku(self) -> str:
        return self._sku

    # ------------------- Static & Class Methods -------------------
    @staticmethod
    def validate_sku(sku: str) -> bool:
        """Checks SKU format. Demonstrates a static utility method."""
        return sku.isalnum() and sku.isupper() and (6 <= len(sku) <= 12)

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        """Factory method that dynamically constructs correct subclass."""
        ptype = data.get("type")
        if ptype == "physical":
            return PhysicalProduct(
                sku=data["sku"], name=data["name"],
                price=data["price"], weight_kg=data.get("weight_kg", 0.0)
            )
        elif ptype == "digital":
            return DigitalProduct(
                sku=data["sku"], name=data["name"],
                price=data["price"], file_size_mb=data.get("file_size_mb", 0.0)
            )
        else:
            raise ValueError(f"Unknown product type: {ptype}")

    # Abstract method forces subclasses to implement it
    @abstractmethod
    def kind(self) -> str:
        """Describe product type (used for polymorphism)."""
        raise NotImplementedError

    def __str__(self) -> str:
        """String representation of product."""
        return f"{self.kind()} Product {self.sku} '{self.name}' @ {self.price:.2f}"


# ===========================================================
# CONCRETE PRODUCT SUBCLASSES – Demonstrate Inheritance & Polymorphism
# ===========================================================

class PhysicalProduct(Product):
    """Physical products have weight for shipping."""
    def __init__(self, sku, name, price, weight_kg):
        super().__init__(sku, name, price)
        self.weight_kg = max(0.0, float(weight_kg))

    def kind(self) -> str:
        """Implements abstract method from Product (Polymorphism)."""
        return "Physical"

    def shipping_weight(self) -> float:
        return self.weight_kg


class DigitalProduct(Product):
    """Digital products have no shipping weight."""
    def __init__(self, sku, name, price, file_size_mb):
        super().__init__(sku, name, price)
        self.file_size_mb = max(0.0, float(file_size_mb))

    def kind(self) -> str:
        return "Digital"

    def shipping_weight(self) -> float:
        """Digital goods have zero shipping weight."""
        return 0.0


# ===========================================================
# COMPOSITION: Orders contain multiple OrderItems
# ===========================================================

@dataclass
class OrderItem:
    """Represents a product and quantity inside an order."""
    product: Product
    quantity: int

    def line_total(self) -> float:
        """Compute total for this line."""
        return round(self.product.price * self.quantity, 2)

    def describe(self) -> str:
        return f"{self.quantity} x {self.product.name} ({self.product.sku}) = {self.line_total():.2f}"


@dataclass
class Order(AuditableMixin):
    """An order composed of many items (Composition) and a single customer."""
    order_id: str
    customer: Customer
    items: List[OrderItem] = field(default_factory=list)
    coupon_code: Optional[str] = None

    def subtotal(self) -> float:
        """Sum of all item totals."""
        return round(sum(i.line_total() for i in self.items), 2)

    def total_items(self) -> int:
        """Total number of products in order."""
        return sum(i.quantity for i in self.items)

    def describe(self) -> str:
        """Textual representation of the order contents."""
        lines = [f"Order[{self.order_id}] for {self.customer.name}",
                 f"Items ({self.total_items()} total):"]
        lines += [f"  - {i.describe()}" for i in self.items]
        lines.append(f"Subtotal: {self.subtotal():.2f}")
        if self.coupon_code:
            lines.append(f"Coupon: {self.coupon_code}")
        return "\n".join(lines)


# ===========================================================
# STRATEGY PATTERN – Different Discount Behaviors (Abstraction + Polymorphism)
# ===========================================================

class DiscountStrategy(ABC):
    """Abstract discount strategy."""
    @abstractmethod
    def apply(self, amount: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    """No discount applied."""
    def apply(self, amount: float) -> float:
        return round(amount, 2)


class PercentageDiscount(DiscountStrategy):
    """Applies a percentage-based discount."""
    def __init__(self, percent: float):
        self.percent = max(0.0, min(100.0, float(percent)))

    def apply(self, amount: float) -> float:
        return round(amount * (1 - self.percent / 100.0), 2)


class FixedAmountDiscount(DiscountStrategy):
    """Applies a fixed amount off the subtotal."""
    def __init__(self, amount_off: float):
        self.amount_off = max(0.0, float(amount_off))

    def apply(self, amount: float) -> float:
        return round(max(0.0, amount - self.amount_off), 2)


# ===========================================================
# ABSTRACT PAYMENT GATEWAY (Abstraction + Polymorphism)
# ===========================================================

class PaymentGateway(ABC):
    """Defines the common interface for all payment gateways."""
    @abstractmethod
    def process_payment(self, order: Order, amount: float) -> str:
        pass


class StripeGateway(PaymentGateway, AuditableMixin):
    """Concrete payment gateway simulating Stripe."""
    def process_payment(self, order: Order, amount: float) -> str:
        tx_id = f"stripe_{uuid.uuid4().hex[:12]}"
        self._audit(f"Processed payment {tx_id} for {order.order_id} amount {amount:.2f}")
        return tx_id


class CashOnDelivery(PaymentGateway, AuditableMixin):
    """Concrete gateway for Cash-on-Delivery payments."""
    def process_payment(self, order: Order, amount: float) -> str:
        tx_id = f"cod_{order.order_id}"
        self._audit(f"Marked COD for {order.order_id} amount {amount:.2f}")
        return tx_id


# ===========================================================
# SHIPPING SERVICES (Abstraction + Polymorphism)
# ===========================================================

class ShippingService(ABC):
    """Base interface for shipping calculation."""
    @abstractmethod
    def cost(self, order: Order) -> float:
        pass

    @abstractmethod
    def label(self) -> str:
        pass


class StandardShipping(ShippingService):
    """Regular delivery option with lower cost."""
    def cost(self, order: Order) -> float:
        # Weight-based cost calculation
        total_weight = 0.0
        for item in order.items:
            weight = getattr(item.product, "shipping_weight", lambda: 0.0)()
            total_weight += weight * item.quantity
        return round(50 + 30 * total_weight, 2)

    def label(self) -> str:
        return "Standard"


class ExpressShipping(ShippingService):
    """Faster shipping with premium charges."""
    def cost(self, order: Order) -> float:
        total_weight = 0.0
        for item in order.items:
            weight = getattr(item.product, "shipping_weight", lambda: 0.0)()
            total_weight += weight * item.quantity
        return round(120 + 50 * total_weight, 2)

    def label(self) -> str:
        return "Express"


# ===========================================================
# SERVICE CLASS – Demonstrates Dependency Inversion Principle
# ===========================================================

class OrderService(AuditableMixin):
    """Handles checkout and billing logic, depending only on abstractions."""

    def __init__(
        self,
        payment_gateway: PaymentGateway,
        shipping_service: ShippingService,
        discount_strategy: DiscountStrategy,
        currency_symbol: str = "₹",
    ):
        self.payment_gateway = payment_gateway
        self.shipping_service = shipping_service
        self.discount_strategy = discount_strategy
        self.currency_symbol = currency_symbol

    def compute_total(self, order: Order) -> dict:
        """Calculates subtotal, discount, shipping, and final amount."""
        subtotal = order.subtotal()
        discounted = self.discount_strategy.apply(subtotal)
        shipping = self.shipping_service.cost(order)
        grand_total = round(discounted + shipping, 2)
        return {
            "subtotal": subtotal,
            "discounted_subtotal": discounted,
            "shipping_cost": shipping,
            "grand_total": grand_total,
            "shipping_method": self.shipping_service.label(),
        }

    def checkout(self, order: Order) -> dict:
        """Performs full checkout: computes cost + processes payment."""
        pricing = self.compute_total(order)
        tx_id = self.payment_gateway.process_payment(order, pricing["grand_total"])
        return {"order_id": order.order_id, "transaction_id": tx_id, **pricing}


# ===========================================================
# DEMO: BUILDING PRODUCTS, CUSTOMER, AND ORDER
# ===========================================================

def seed_products() -> Iterable[Product]:
    """Creates example products using the factory method."""
    yield Product.from_dict({
        "type": "physical", "sku": "LAPTOP1", "name": "Ultrabook Pro 14",
        "price": 79999.00, "weight_kg": 1.4
    })
    yield Product.from_dict({
        "type": "physical", "sku": "MOUSE01", "name": "Ergo Mouse",
        "price": 1299.0, "weight_kg": 0.08
    })
    yield Product.from_dict({
        "type": "digital", "sku": "EBOOK01", "name": "Mastering Python eBook",
        "price": 999.00, "file_size_mb": 25.0
    })


def build_sample_order(customer: Customer, products: List[Product]) -> Order:
    """Composes an order from given products."""
    items = [
        OrderItem(products[0], 1),
        OrderItem(products[1], 2),
        OrderItem(products[2], 1),
    ]
    return Order(order_id=uuid.uuid4().hex[:10].upper(), customer=customer,
                 items=items, coupon_code="WELCOME10")


def render_invoice(order: Order, checkout_info: dict) -> str:
    """Formats the final invoice text."""
    lines = []
    lines.append("=" * 64)
    lines.append("               E  C  O  M  M  E  R  C  E    I N V O I C E")
    lines.append("=" * 64)
    lines.append(order.customer.describe())
    lines.append("")
    lines.append(order.describe())
    lines.append("")
    lines.append(f"Discounted Subtotal: {checkout_info['discounted_subtotal']:.2f}")
    lines.append(f"Shipping ({checkout_info['shipping_method']}): {checkout_info['shipping_cost']:.2f}")
    lines.append("-" * 64)
    lines.append(f"Grand Total: {checkout_info['grand_total']:.2f}")
    lines.append("-" * 64)
    lines.append(f"Payment Tx: {checkout_info['transaction_id']}")
    lines.append(f"Order ID  : {checkout_info['order_id']}")
    lines.append("=" * 64)
    return "\n".join(lines)


# ===========================================================
# MAIN FUNCTION
# ===========================================================

def main() -> None:
    """Runs the demo scenario and saves the output to a text file."""

    # Create a sample customer
    customer = Customer(
        customer_id=uuid.uuid4().hex[:8],
        name="Aarav Sharma",
        email="aarav@example.com",
        address=Address("221B, MG Road", "Bengaluru", "India", "560001")
    )

    # Initialize demo data
    products = list(seed_products())
    order = build_sample_order(customer, products)

    # Dependency Injection: inject abstract dependencies into OrderService
    discount = PercentageDiscount(10.0)
    shipping = StandardShipping()
    gateway = StripeGateway()
    service = OrderService(gateway, shipping, discount)

    # Checkout
    checkout_info = service.checkout(order)

    # Generate invoice text
    invoice_text = render_invoice(order, checkout_info)

    # Write invoice to file
    with open("ecommerce_demo_output.txt", "w", encoding="utf-8") as f:
        f.write(invoice_text)

    print("✅ Invoice generated and saved to ecommerce_demo_output.txt\n")
    print(invoice_text)


if __name__ == "__main__":
    main()