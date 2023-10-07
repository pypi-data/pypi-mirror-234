from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.canvas_initialize_webhook_v0 import CanvasInitializeWebhookV0
from ..models.canvas_interaction_webhook_v0 import CanvasInteractionWebhookV0
from ..models.lifecycle_activate_webhook_v0 import LifecycleActivateWebhookV0
from ..models.lifecycle_deactivate_webhook_v0 import LifecycleDeactivateWebhookV0
from ..models.webhook_envelope_v0_app import WebhookEnvelopeV0App
from ..models.webhook_envelope_v0_app_definition import WebhookEnvelopeV0AppDefinition
from ..models.webhook_envelope_v0_channel import WebhookEnvelopeV0Channel
from ..models.webhook_envelope_v0_version import WebhookEnvelopeV0Version
from ..types import UNSET, Unset

T = TypeVar("T", bound="WebhookEnvelopeV0")


@attr.s(auto_attribs=True, repr=False)
class WebhookEnvelopeV0:
    """  """

    _app: WebhookEnvelopeV0App
    _app_definition: WebhookEnvelopeV0AppDefinition
    _base_url: str
    _channel: WebhookEnvelopeV0Channel
    _message: Union[
        CanvasInteractionWebhookV0,
        CanvasInitializeWebhookV0,
        LifecycleActivateWebhookV0,
        LifecycleDeactivateWebhookV0,
        UnknownType,
    ]
    _tenant_id: str
    _version: WebhookEnvelopeV0Version
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("app={}".format(repr(self._app)))
        fields.append("app_definition={}".format(repr(self._app_definition)))
        fields.append("base_url={}".format(repr(self._base_url)))
        fields.append("channel={}".format(repr(self._channel)))
        fields.append("message={}".format(repr(self._message)))
        fields.append("tenant_id={}".format(repr(self._tenant_id)))
        fields.append("version={}".format(repr(self._version)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "WebhookEnvelopeV0({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        app = self._app.to_dict()

        app_definition = self._app_definition.to_dict()

        base_url = self._base_url
        channel = self._channel.value

        if isinstance(self._message, UnknownType):
            message = self._message.value
        elif isinstance(self._message, CanvasInteractionWebhookV0):
            message = self._message.to_dict()

        elif isinstance(self._message, CanvasInitializeWebhookV0):
            message = self._message.to_dict()

        elif isinstance(self._message, LifecycleActivateWebhookV0):
            message = self._message.to_dict()

        else:
            message = self._message.to_dict()

        tenant_id = self._tenant_id
        version = self._version.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if app is not UNSET:
            field_dict["app"] = app
        if app_definition is not UNSET:
            field_dict["appDefinition"] = app_definition
        if base_url is not UNSET:
            field_dict["baseURL"] = base_url
        if channel is not UNSET:
            field_dict["channel"] = channel
        if message is not UNSET:
            field_dict["message"] = message
        if tenant_id is not UNSET:
            field_dict["tenantId"] = tenant_id
        if version is not UNSET:
            field_dict["version"] = version

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_app() -> WebhookEnvelopeV0App:
            app = WebhookEnvelopeV0App.from_dict(d.pop("app"), strict=False)

            return app

        try:
            app = get_app()
        except KeyError:
            if strict:
                raise
            app = cast(WebhookEnvelopeV0App, UNSET)

        def get_app_definition() -> WebhookEnvelopeV0AppDefinition:
            app_definition = WebhookEnvelopeV0AppDefinition.from_dict(d.pop("appDefinition"), strict=False)

            return app_definition

        try:
            app_definition = get_app_definition()
        except KeyError:
            if strict:
                raise
            app_definition = cast(WebhookEnvelopeV0AppDefinition, UNSET)

        def get_base_url() -> str:
            base_url = d.pop("baseURL")
            return base_url

        try:
            base_url = get_base_url()
        except KeyError:
            if strict:
                raise
            base_url = cast(str, UNSET)

        def get_channel() -> WebhookEnvelopeV0Channel:
            _channel = d.pop("channel")
            try:
                channel = WebhookEnvelopeV0Channel(_channel)
            except ValueError:
                channel = WebhookEnvelopeV0Channel.of_unknown(_channel)

            return channel

        try:
            channel = get_channel()
        except KeyError:
            if strict:
                raise
            channel = cast(WebhookEnvelopeV0Channel, UNSET)

        def get_message() -> Union[
            CanvasInteractionWebhookV0,
            CanvasInitializeWebhookV0,
            LifecycleActivateWebhookV0,
            LifecycleDeactivateWebhookV0,
            UnknownType,
        ]:
            message: Union[
                CanvasInteractionWebhookV0,
                CanvasInitializeWebhookV0,
                LifecycleActivateWebhookV0,
                LifecycleDeactivateWebhookV0,
                UnknownType,
            ]
            _message = d.pop("message")

            if True:
                discriminator = _message["type"]
                if discriminator == "v0.app.activateRequested":
                    message = LifecycleActivateWebhookV0.from_dict(_message)
                elif discriminator == "v0.app.deactivated":
                    message = LifecycleDeactivateWebhookV0.from_dict(_message)
                elif discriminator == "v0.canvas.initialized":
                    message = CanvasInitializeWebhookV0.from_dict(_message)
                elif discriminator == "v0.canvas.userInteracted":
                    message = CanvasInteractionWebhookV0.from_dict(_message)
                else:
                    message = UnknownType(value=_message)

            return message

        try:
            message = get_message()
        except KeyError:
            if strict:
                raise
            message = cast(
                Union[
                    CanvasInteractionWebhookV0,
                    CanvasInitializeWebhookV0,
                    LifecycleActivateWebhookV0,
                    LifecycleDeactivateWebhookV0,
                    UnknownType,
                ],
                UNSET,
            )

        def get_tenant_id() -> str:
            tenant_id = d.pop("tenantId")
            return tenant_id

        try:
            tenant_id = get_tenant_id()
        except KeyError:
            if strict:
                raise
            tenant_id = cast(str, UNSET)

        def get_version() -> WebhookEnvelopeV0Version:
            _version = d.pop("version")
            try:
                version = WebhookEnvelopeV0Version(_version)
            except ValueError:
                version = WebhookEnvelopeV0Version.of_unknown(_version)

            return version

        try:
            version = get_version()
        except KeyError:
            if strict:
                raise
            version = cast(WebhookEnvelopeV0Version, UNSET)

        webhook_envelope_v0 = cls(
            app=app,
            app_definition=app_definition,
            base_url=base_url,
            channel=channel,
            message=message,
            tenant_id=tenant_id,
            version=version,
        )

        webhook_envelope_v0.additional_properties = d
        return webhook_envelope_v0

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def app(self) -> WebhookEnvelopeV0App:
        if isinstance(self._app, Unset):
            raise NotPresentError(self, "app")
        return self._app

    @app.setter
    def app(self, value: WebhookEnvelopeV0App) -> None:
        self._app = value

    @property
    def app_definition(self) -> WebhookEnvelopeV0AppDefinition:
        if isinstance(self._app_definition, Unset):
            raise NotPresentError(self, "app_definition")
        return self._app_definition

    @app_definition.setter
    def app_definition(self, value: WebhookEnvelopeV0AppDefinition) -> None:
        self._app_definition = value

    @property
    def base_url(self) -> str:
        """ Base tenant URL from which the webhook is coming """
        if isinstance(self._base_url, Unset):
            raise NotPresentError(self, "base_url")
        return self._base_url

    @base_url.setter
    def base_url(self, value: str) -> None:
        self._base_url = value

    @property
    def channel(self) -> WebhookEnvelopeV0Channel:
        if isinstance(self._channel, Unset):
            raise NotPresentError(self, "channel")
        return self._channel

    @channel.setter
    def channel(self, value: WebhookEnvelopeV0Channel) -> None:
        self._channel = value

    @property
    def message(
        self,
    ) -> Union[
        CanvasInteractionWebhookV0,
        CanvasInitializeWebhookV0,
        LifecycleActivateWebhookV0,
        LifecycleDeactivateWebhookV0,
        UnknownType,
    ]:
        if isinstance(self._message, Unset):
            raise NotPresentError(self, "message")
        return self._message

    @message.setter
    def message(
        self,
        value: Union[
            CanvasInteractionWebhookV0,
            CanvasInitializeWebhookV0,
            LifecycleActivateWebhookV0,
            LifecycleDeactivateWebhookV0,
            UnknownType,
        ],
    ) -> None:
        self._message = value

    @property
    def tenant_id(self) -> str:
        """ Global tenant id from which the webhook is coming """
        if isinstance(self._tenant_id, Unset):
            raise NotPresentError(self, "tenant_id")
        return self._tenant_id

    @tenant_id.setter
    def tenant_id(self, value: str) -> None:
        self._tenant_id = value

    @property
    def version(self) -> WebhookEnvelopeV0Version:
        """ Version of the webhook envelope shape. Always 0. """
        if isinstance(self._version, Unset):
            raise NotPresentError(self, "version")
        return self._version

    @version.setter
    def version(self, value: WebhookEnvelopeV0Version) -> None:
        self._version = value
