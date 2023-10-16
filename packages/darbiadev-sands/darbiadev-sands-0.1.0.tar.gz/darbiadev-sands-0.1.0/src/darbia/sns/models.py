"""Models."""

from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class Warehouse:
    """Warehouse."""

    warehouseAbbr: str
    """Code identifying the Warehouse."""
    skuID: int
    """skuID identifying the Sku and Warehouse."""
    qty: int
    """Quantity available for sale."""
    closeout: bool
    """Skus that are discontinued and will not be replenished."""
    dropship: bool
    """This product does not ship from our warehouse."""
    excludeFreeFreight: bool
    """	This product does not qualify for free freight."""
    fullCaseOnly: bool
    """This product must be ordered in full case quantities."""
    returnable: bool
    """This product is eligible for return."""
    expectedInventory: str | None = None
    """Current enroute quantities with expected dates of receipt and current quantity on order with the mill. If no dates are available, None will be returned."""  # noqa: E501

    @classmethod
    def from_api_data(cls: type[Self], data: dict) -> Self:
        """Build an instance from an API response."""
        return cls(**data)


@dataclass(frozen=True)
class Product:
    """Product."""

    sku: str
    """Our sku number"""
    gtin: str
    """Our sku number"""
    skuID_Master: int
    """NO EXPLANATION"""
    yourSku: str
    """YourSku has been set up using the CrossRef API."""
    styleID: int
    """Unique ID for this style (Will never change)"""
    brandName: str
    """The brand that makes this style."""
    styleName: str
    """The style's name. Style names are unique within a brand."""
    colorName: str
    """The style's name. Style names are unique within a brand."""
    colorCode: str
    """Two digit color code part of the InventoryKey."""
    colorPriceCodeName: str
    """The pricing category of this color."""
    colorGroup: str
    """Colors with a similar color group are considered to be a similar color."""
    colorGroupName: str
    """Colors with a similar color group are considered to be a similar color."""
    colorFamilyID: str
    """Base color the color falls under."""
    colorFamily: str
    """Base color the color falls under."""
    colorSwatchImage: str
    """URL to the medium swatch image for this color"""
    colorSwatchTextColor: str
    """Html color code that is visible on top of the color swatch"""
    colorFrontImage: str
    """URL to the medium front image for this color"""
    colorSideImage: str
    """URL to the medium side image for this color"""
    colorBackImage: str
    """URL to the medium back image for this color"""
    colorDirectSideImage: str
    """URL to the medium direct side image for this color"""
    colorOnModelFrontImage: str
    """URL to the medium direct side image for this color"""
    colorOnModelSideImage: str
    """URL to the medium direct side image for this color"""
    colorOnModelBackImage: str
    """URL to the medium on model back image for this color"""
    color1: str
    """HTML Code for the primary color."""
    color2: str
    """HTML Code for the secondary color."""
    sizeName: str
    """Size Name that the spec belongs to."""
    sizeCode: str
    """One digit size code part of the InventoryKey."""
    sizeOrder: str
    """Sort order for the size compared to other sizes in the style."""
    sizePriceCodeName: str
    """The pricing category of this size."""
    caseQty: int
    """Number of units in a full case from the mill."""
    unitWeight: float
    """Weight of a single unit."""
    mapPrice: float
    """Minimum Advertised Price price"""
    piecePrice: float
    """Piece price level price"""
    dozenPrice: float
    """Dozen price level price"""
    casePrice: float
    """Case price level price"""
    salePrice: float
    """Sale price level price"""
    customerPrice: float
    """Your price"""
    noeRetailing: bool
    """When true, mill prohibits the selling of products on popular eRetailing platforms such as Amazon, Walmart, EBay."""  # noqa: E501
    caseWeight: int
    """Weight of full case in pounds"""
    caseWidth: int
    """Width of case in inches"""
    caseLength: float
    """Width of case in inches"""
    caseHeight: float
    """Height of case in inches"""
    polyPackQty: str
    """Number of pieces in a poly pack"""
    qty: int
    """Combined Inventory in all of our warehouses"""
    countryOfOrigin: str
    """Country of manufacture for product. Provided by mills."""
    warehouses: list[Warehouse]
    """List of Object"""
    saleExpiration: str | None = None
    """Your price"""

    @classmethod
    def from_api_data(cls: type[Self], data: dict) -> Self:
        """Build an instance from an API response."""
        data["warehouses"] = [Warehouse.from_api_data(row) for row in data["warehouses"]]
        return cls(**data)
