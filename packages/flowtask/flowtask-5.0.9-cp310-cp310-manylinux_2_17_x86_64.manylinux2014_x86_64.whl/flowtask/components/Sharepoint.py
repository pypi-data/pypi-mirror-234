import re
from typing import List
from collections.abc import Callable
# from office365.sharepoint.files.file import File
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.search.searchRequest import SearchRequest
from office365.sharepoint.search.searchService import SearchService
from flowtask.exceptions import FileError
from .O365Client import O365Client

class Sharepoint(O365Client):
    """
    Sharepoint Client.

    Managing connections to MS Sharepoint Resources.
    """
    def get_context(self, url: str, *args) -> Callable:
        return ClientContext(url, *args)

    def start(self):
        super(Sharepoint, self).start()
        # processing URL:
        site = f'sites/{self.site}/' if self.site is not None else ''
        self.url = f'https://{self.tenant}.sharepoint.com/{site}'
        for file in self._srcfiles:
            fd = file['directory']
            file['directory'] = f'/{site}{fd}'
        return True

    async def file_search(self) -> List:
        destinations = []
        try:
            search = SearchService(self.context)
            for file in self._srcfiles:
                directory = file['directory']
                fname = file['filename']
                request = SearchRequest(
                    f'Path:"{self.url}{directory}" IsDocument:1 FileExtension:{fname}'
                )
                result = search.post_query(request)
                self.context.execute_query()
                relevant_results = result.PrimaryQueryResult.RelevantResults
                paths = [
                    relevant_results['Table']['Rows'][x]['Cells'][6]['Value']
                    for x in relevant_results['Table']['Rows']
                ]
                r = re.compile("{}{}.*{}".format(self.url, directory, fname))
                paths_matched = list(filter(r.match, paths))
                if len(paths_matched) == 0:
                    self._logger.error(
                        f'Error downloading File: Pattern not match {fname}'
                    )
                    raise FileError(
                        f'Error downloading File: Pattern not match {fname}'
                    )
                else:
                    for path in paths_matched:
                        filename = path.replace(
                            'https://{}.sharepoint.com'.format(self.tenant), ''
                        )
                        file = path[path.rfind("/") + 1:len(path)]
                        destination = "{}/{}".format(self.directory, file)
                        try:
                            self.context.web.get_file_by_server_relative_url(filename).get().execute_query()
                            with open(destination, "wb") as local_file:
                                self.context.web.get_file_by_server_relative_url(filename).download(local_file).execute_query()
                                destinations.append(destination)
                        except Exception as err:
                            raise RuntimeError(
                                f'Sharepoint: Error downloading file {filename}: {err}'
                            ) from err
            return destinations
        except Exception as e:
            print(e)

    async def file_download(self) -> List:
        destinations = []
        for file in self._srcfiles:
            directory = file['directory']
            fname = file['filename']
            destination = self.filename
            source = '{}/{}'.format(directory, fname)
            try:
                self.context.web.get_file_by_server_relative_url(source).get().execute_query()
                with open(destination, "wb") as local_file:
                    self.context.web.get_file_by_server_relative_url(source).download(local_file).execute_query()
                destinations.append(destination)
            except Exception as err:
                self._logger.error(
                    f"Error downloading file {fname}: {err}"
                )
                raise FileError(
                    f"Error downloading file {fname}: {err}"
                ) from err
        return destinations
