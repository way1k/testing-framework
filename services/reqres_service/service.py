from models.reqres_service.registry_models import ReqresModels
from services.reqres_service.endpoints import ReqresEndpoints
from services.reqres_service.helper_methods import ReqresHelpers
from services.reqres_service.methods import ReqresMethods


class ReqresService:
    """reqres_service"""

    @property
    def endpoints(self) -> ReqresEndpoints:
        return ReqresEndpoints()

    @property
    def methods(self) -> ReqresMethods:
        return ReqresMethods()

    @property
    def models(self) -> ReqresModels:
        return ReqresModels()

    @property
    def helpers(self) -> ReqresHelpers:
        return ReqresHelpers()
