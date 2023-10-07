# Copyright (C) 2022 Greenbone AG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from typing import AsyncIterator, Iterable, Union

from pontos.github.api.client import GitHubAsyncREST
from pontos.github.api.helper import JSON


class GitHubAsyncRESTLabels(GitHubAsyncREST):
    async def get_all(
        self,
        repo: str,
        issue: Union[int, str],
    ) -> AsyncIterator[str]:
        """
        Get all labels that are set in the issue/pr

        Args:
            repo:   GitHub repository (owner/name) to use
            issue:  Issue/Pull request number

        Returns:
            An async iterator yielding the labels

        Example:
            .. code-block:: python

                from pontos.github.api import GitHubAsyncRESTApi

                async with GitHubAsyncRESTApi(token) as api:
                    async for label in api.labels.get_all("foo/bar", 123):
                        print(label)
        """
        api = f"/repos/{repo}/issues/{issue}/labels"
        params = {"per_page": "100"}

        async for response in self._client.get_all(api, params=params):
            response.raise_for_status()
            data: JSON = response.json()

            for label in data:
                yield label["name"]  # type: ignore

    async def set_all(
        self, repo: str, issue: Union[int, str], labels: Iterable[str]
    ) -> None:
        """
        Set labels in the issue/pr. Existing labels will be overwritten

        Args:
            repo:   GitHub repository (owner/name) to use
            issue:  Issue/Pull request number
            labels: Iterable of labels, that should be set. Existing labels will
                be overwritten.

        Example:
            .. code-block:: python

                from pontos.github.api import GitHubAsyncRESTApi

                async with GitHubAsyncRESTApi(token) as api:
                    await api.labels.set_all("foo/bar", 123, ["bug", "doc"])
        """
        api = f"/repos/{repo}/issues/{issue}/labels"
        data: JSON = {"labels": labels}  # type: ignore
        response = await self._client.post(api, data=data)
        response.raise_for_status()
