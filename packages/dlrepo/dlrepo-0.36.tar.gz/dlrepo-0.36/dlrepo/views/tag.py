# Copyright (c) 2021 Julien Floret
# Copyright (c) 2021 Robin Jarry
# SPDX-License-Identifier: BSD-3-Clause

import asyncio
from typing import Callable

from aiohttp import web
import aiohttp_jinja2

from .util import BaseView


# --------------------------------------------------------------------------------------
class TagView(BaseView):
    @classmethod
    def urls(cls):
        yield "/branches/{branch}/{tag}"
        yield "/branches/{branch}/{tag}/"
        yield "/~{user}/branches/{branch}/{tag}"
        yield "/~{user}/branches/{branch}/{tag}/"

    def _get_tag(self, access_cb: Callable[[str], bool] = None):
        match = self.request.match_info
        if match["tag"] in (
            "latest",
            "stable",
            "oldstable",
        ) and self.request.method not in (
            "GET",
            "HEAD",
        ):
            raise web.HTTPMethodNotAllowed(self.request.method, ["GET", "HEAD"])
        try:
            tag = (
                self.repo().get_branch(match["branch"]).get_tag(match["tag"], access_cb)
            )
            if not tag.exists():
                raise web.HTTPNotFound()
            if tag.url() != self.request.path:
                raise web.HTTPFound(tag.url())
            return tag
        except FileNotFoundError as e:
            raise web.HTTPNotFound() from e

    async def get(self):
        """
        List tag contents.
        """
        tag = self._get_tag(self.access_granted)
        data = {
            "tag": {
                "name": tag.name,
                "released": tag.is_released(),
                "locked": tag.is_locked(),
                "stable": tag.is_stable(),
                "publish_status": tag.publish_status(),
                "jobs": [],
            },
        }
        for job in tag.get_jobs():
            if not self.access_granted(job.url()):
                continue
            job_data = job.get_metadata()
            if self.request.query:
                for key, value in self.request.query.items():
                    if key not in job_data or str(job_data[key]) != value:
                        break
                else:
                    data["tag"]["jobs"].append(job_data)
            else:
                data["tag"]["jobs"].append(job_data)
        if "html" in self.request.headers.get("Accept", "json"):
            return aiohttp_jinja2.render_template("tag.html", self.request, data)
        return web.json_response(data)

    async def post(self):
        """
        Change the released, stable and/or locked statuses of a tag.
        """
        tag = self._get_tag()
        try:
            data = (await self.json_body())["tag"]
            released = data.get("released")
            if released is not None and not isinstance(released, bool):
                raise TypeError()
            locked = data.get("locked")
            if locked is not None and not isinstance(locked, bool):
                raise TypeError()
            stable = data.get("stable")
            if stable is not None and not isinstance(stable, bool):
                raise TypeError()
        except (TypeError, KeyError) as e:
            raise web.HTTPBadRequest(reason="invalid parameters") from e

        try:
            if released is not None:
                semaphore = self.request.app["dlrepo_publish_semaphore"]
                tag.set_released(released, semaphore)
            if locked is not None:
                tag.set_locked(locked)
            if stable is not None:
                tag.set_stable(stable)
        except FileNotFoundError as e:
            raise web.HTTPNotFound() from e
        except ValueError as e:
            raise web.HTTPMisdirectedRequest(reason=str(e)) from e

        return web.Response()

    async def delete(self):
        """
        Delete a tag and all its contents.
        """
        loop = asyncio.get_running_loop()
        try:
            tag = self._get_tag()
            await loop.run_in_executor(None, tag.delete)
            self.repo().schedule_cleanup_orphans()
            return web.Response()
        except OSError as e:
            raise web.HTTPBadRequest(reason=str(e)) from e
