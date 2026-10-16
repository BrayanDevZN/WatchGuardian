from .replicate import Replicator, Settings, CacheManage
from src.logs.module import Logs

logger = Logs(loglevel="SUCCESS")

class Replicators:

    def __init__(self, settings:Settings)-> None:

        self.settings = settings
        self.name = settings.get_config("replicator_name")
        self.urls = list(settings.required_config("replicator_urls"))
        paths = settings.get_config("replicator_paths")
        self.paths = paths if paths is not None else "*"
        methods = settings.get_config("replicator_methods")
        self.methods = methods if methods is not None else "*"
        limit = settings.get_config("replicator_limit")
        self.limit = int(limit) if limit else 60
        self.cache = CacheManage(settings=settings)

    async def get_replicas(self) -> list[Replicator]:

        replicators = []

        for number, url in enumerate(self.urls):

            name = f"{self.name}_{number}"

            logger.info(f"Creating replica {name}...")

            instance = Replicator(
                url=url,
                name=name,
                paths=self.paths,
                methods=self.methods,
                limit_expires=self.limit,
                settings=self.settings,
                cache=self.cache
            )

            replicators.append(instance)

            logger.success(f"{name} created with sucess")

        return replicators

        