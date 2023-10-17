from hf_api_client.resources import base

class QueryPool(
    base.ResourcePool,
    base.ListableResource
):
    pass

class ActionPool(
    base.ResourcePool,
    base.CreatableResource
):
    pass

class EndpointNamespacePool(
    base.ResourcePool,
    base.ListableResource,
    base.GettableResource,
    base.UpdatableResource,
    base.DeletableResource
):
    def logs(self, name):
        return QueryPool(
            base.urljoin(
                self._endpoint, name, 'logs'
            ),
            self._session
        )
    
    def metrics(self, name):
        return ActionPool(
            base.urljoin(self._endpoint, name, 'metrics'), 
            self._session
        )

    def pause(self, name):
        return ActionPool(
            base.urljoin(self._endpoint, name, 'pause'), 
            self._session
        )

    def resume(self, name):
        return ActionPool(
            base.urljoin(self._endpoint, name, 'resume'), 
            self._session
        )

    def scale_to_zero(self, name):
        return ActionPool(
            base.urljoin(self._endpoint, name, 'scale-to-zero'), 
            self._session
        )


class EndpointPool(
    base.ResourcePool,
    base.CreatableResource,
):
    def namespace(self, namespace):
        return EndpointNamespacePool(
            base.urljoin(
                self._endpoint, namespace
            ),
            self._session
        )