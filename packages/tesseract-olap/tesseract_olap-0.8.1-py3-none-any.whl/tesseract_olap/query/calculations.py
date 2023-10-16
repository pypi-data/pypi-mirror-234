from dataclasses import dataclass, field
from typing import Any, Dict, Mapping, Optional, Union

import immutables as immu

from tesseract_olap.schema import Level, Measure


@dataclass(eq=False, order=False)
class CalculationRequest:
    """CalculationRequest dataclass.

    Instances of this class are used to define calculation parameters.
    Its values are directly inputted by the user, so should never be considered
    valid by itself. Once it passes validation, it should be replaced by a
    :class:`Calculation` instance.
    """
    kind: str
    name: Optional[str] = None
    params: Dict[str, str] = field(default_factory=dict)


@dataclass(eq=False, order=False)
class Calculation:
    """Calculation dataclass.

    Contains the parameters that define a request for a calculation.
    """
    kind: str
    name: Optional[str] = None
    params: Mapping[str, Any] = field(default_factory=immu.Map)


class GrowthCalculation(Calculation):
    """Defines a Growth calculation on the server."""

    def __init__(self, period: "Level", value: "Measure"):
        """Overrides the init definition for :class:`Calculation` class to fit Growth parameters."""
        super().__init__(kind="growth", params={
            "period": period,
            "value": value,
        })


class RcaCalculation(Calculation):
    """Defines a RCA calculation on the server."""

    def __init__(self, location: Level, category: Level, value: Measure):
        """Overrides the init definition for :class:`Calculation` class to fit Rca parameters."""
        super().__init__(kind="rca", params={
            "location": location,
            "category": category,
            "value": value,
        })


class TopkCalculation(Calculation):
    """Defines a TopK calculation on the server."""

    def __init__(
        self,
        amount: int,
        category: Level,
        value: Union[Calculation, Measure],
        descendent: bool = True
    ):
        """Overrides the init definition for :class:`Calculation` class to fit Topk parameters."""
        super().__init__(kind="topk", params={
            "amount": amount,
            "category": category,
            "value": value,
            "order": "asc" if not descendent else "desc",
        })
