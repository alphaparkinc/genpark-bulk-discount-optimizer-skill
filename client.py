"""
bulk-discount-optimizer-skill: Client SDK
Calculates optimal tiered bulk discounts to maximize wholesale profit margins.
"""
from __future__ import annotations
from typing import Optional


class BulkDiscountOptimizerClient:
    """
    SDK for tiered pricing and volume discount scheduling.
    """

    def optimize(
        self,
        unit_price: float,
        unit_cost: float,
        max_discount_pct: float = 25.0,
    ) -> dict:
        base_margin_pct = ((unit_price - unit_cost) / unit_price) * 100
        max_discount = min(max_discount_pct, base_margin_pct - 5.0)  # Preserve at least 5% margin

        # 4 Standard tiers
        tier_configs = [
            {"min_qty": 1, "discount_pct": 0.0},
            {"min_qty": 5, "discount_pct": round(max_discount * 0.3, 1)},
            {"min_qty": 20, "discount_pct": round(max_discount * 0.6, 1)},
            {"min_qty": 50, "discount_pct": round(max_discount, 1)},
        ]

        tiers = []
        for tier in tier_configs:
            disc = tier["discount_pct"]
            price_per_unit = round(unit_price * (1 - disc / 100), 2)
            margin_usd = round(price_per_unit - unit_cost, 2)
            margin_pct = round((margin_usd / price_per_unit) * 100, 1) if price_per_unit > 0 else 0
            tiers.append({
                "min_quantity": tier["min_qty"],
                "discount_percentage": disc,
                "price_per_unit": price_per_unit,
                "margin_per_unit_usd": margin_usd,
                "margin_percentage": margin_pct,
            })

        return {
            "base_unit_price": unit_price,
            "unit_cost": unit_cost,
            "tiers": tiers,
            "average_order_value_uplift_est": round(max_discount * 0.8, 1),
        }
