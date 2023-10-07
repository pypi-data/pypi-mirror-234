from typing import Union

from ..extensions import UnknownType
from ..models.canvas_initialize_webhook_v0 import CanvasInitializeWebhookV0
from ..models.canvas_interaction_webhook_v0 import CanvasInteractionWebhookV0
from ..models.lifecycle_activate_webhook_v0 import LifecycleActivateWebhookV0
from ..models.lifecycle_deactivate_webhook_v0 import LifecycleDeactivateWebhookV0

WebhookMessageV0 = Union[
    CanvasInteractionWebhookV0,
    CanvasInitializeWebhookV0,
    LifecycleActivateWebhookV0,
    LifecycleDeactivateWebhookV0,
    UnknownType,
]
