from dataclasses import dataclass
from datetime import date


@dataclass(unsafe_hash=True)
class OrderLine:
    """一個沒有方法，不可變的資料類別，代表現實場景的“訂單行”"""

    # 訂單ID
    orderid: str
    # 產品識別碼，庫存單位的簡稱（stock-keeping unit），像是: RED-CHAIR, TASTELESS-LAMP
    sku: str
    # 數量
    qty: int


class Batch:
    """Batch代表的是同一批採購進來商品的庫存, 每個batch都有一個專屬ID(reference)、SKU跟數量"""

    def __init__(self, ref: str, sku: str, qty: int, eta: date | None) -> None:
        # 貨批ID
        self.reference = ref
        self.sku = sku
        # 預計到達時間
        self.eta = eta
        self._purchased_quantity = qty
        self._allocation: set[OrderLine] = set()

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocation.add(line)

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_quantity >= line.qty

    def deallocate(self, line: OrderLine):
        if line in self._allocation:
            self._allocation.remove(line)

    @property
    def allocated_quantity(self) -> int:
        return sum(line.qty for line in self._allocation)

    @property
    def available_quantity(self) -> int:
        return self._purchased_quantity - self.allocated_quantity

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference

    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta


def allocate(line: OrderLine, batches: list[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)
        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")


class OutOfStock(Exception):
    pass
