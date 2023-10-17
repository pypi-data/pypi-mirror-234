import asyncio
import platform

import bbpp
import httpx
from notifypy import Notify
from typing import List, Dict, Tuple
from .config import Config


class BitBucket:
    def __init__(self, config: Config):
        self.config: Config = config
        self.ENDPOINT: str = 'https://api.bitbucket.org/2.0'
        self.repositories: List[str] = []
        self.state: List[Tuple[str, str]] = []
        self.notifier_service: Notify = Notify()

    def get_repos(self) -> None:
        output = asyncio.run(self._get_first_repo())
        self.repositories = list(self.parse_repos(output))
        pages = int(output.get('size') / output.get('pagelen'))
        output = asyncio.run(self._get_all_pages(pages))
        for page in output:
            self.repositories += list(self.parse_repos(page))

    async def _get(self, client, url):
        r = await client.get(url, auth=self.config.auth)
        return r.json()

    async def _get_first_repo(self):
        url = f'{self.ENDPOINT}/repositories/{self.config.workspace}'
        async with httpx.AsyncClient() as client:
            r = await self._get(client, url)
            return r

    async def _get_all_pages(self, pages: int):
        async with httpx.AsyncClient() as client:
            tasks = []
            for page in range(1, pages + 1):
                url = f'{self.ENDPOINT}/repositories/{self.config.workspace}?page={page + 1}'
                tasks.append(asyncio.ensure_future(self._get(client, url)))

            repos = await asyncio.gather(*tasks)
            return repos

    def _get_pipelines(self, repo: str):
        r = httpx.get(
            f'{self.ENDPOINT}/repositories/{self.config.workspace}/{repo}/pipelines?sort=-created_on',
            auth=self.config.auth,
        )
        return r.json()

    def check(self, repo: str) -> None:
        pipelines = self._get_pipelines(repo)
        self.print_pipeline(pipelines)
        path = f'{bbpp.__path__[0]}/assets/audio/{self.config.sound}'
        if self.update_state(pipelines):
            self.notifier_service.title = f'BitBucket {repo} pipeline'
            self.notifier_service.message = 'Pipeline state changed'
            self.notifier_service.application_name = 'BBPP'
            if platform.system() == 'Darwin':
                self.notifier_service.audio = path
            self.notifier_service.send()

    def update_state(self, pipelines: Dict[str, List]) -> bool:
        state: List[Tuple[str, str]] = []

        from typing import Optional

        pipeline_values: Optional[List[Dict]] = pipelines.get('values')
        if pipeline_values:
            for pipeline in pipeline_values:
                state.append(self.parse_state(pipeline))

        if self.state != state:
            if self.state != []:
                return True

        self.state = state
        return False

    from typing import Iterator

    @staticmethod
    def parse_repos(output: Dict[str, List]) -> Iterator[str]:
        values = output.get('values')
        if values:
            for repo in values:
                yield repo.get('name')

    @staticmethod
    def print_pipeline(pipelines: Dict) -> None:
        values = pipelines.get('values')
        if values:
            for pipeline in values:
                print(
                    f"Pipeline: {pipeline.get('state').get('name')} {pipeline.get('created_on')} {pipeline.get('duration_in_seconds')}s"
                )

    @staticmethod
    def parse_state(pipeline: dict) -> Tuple[str, str]:
        uuid = pipeline.get('uuid')
        state = pipeline.get('state')

        if state:
            name = state.get('name')
        else:
            raise ValueError('Could not parse pipeline')

        if uuid and name:
            return uuid, name
        else:
            raise ValueError('Could not parse pipeline')
