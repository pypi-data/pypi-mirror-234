# Copyright (c) 2021 Julien Floret
# Copyright (c) 2021 Robin Jarry
# SPDX-License-Identifier: BSD-3-Clause

import asyncio
from typing import Callable

from aiohttp import web
import aiohttp_jinja2

from .util import BaseView, TarResponse


# --------------------------------------------------------------------------------------
class JobArchiveView(BaseView):
    @classmethod
    def urls(cls):
        yield "/branches/{branch}/{tag}/{job}.tar"
        yield "/~{user}/branches/{branch}/{tag}/{job}.tar"

    def _digests(self, job):
        digests = {}
        for fmt in job.get_formats():
            if self.access_granted(fmt.url()):
                for f, digest in fmt.get_digests().items():
                    digests[f"{fmt.name}/{f}"] = digest
        return digests

    async def get(self):
        job = _get_job(self.repo(), self.request, self.access_granted)
        url = job.url().rstrip("/") + ".tar"
        if url != self.request.path:
            raise web.HTTPFound(url)
        return TarResponse(
            self._digests(job), job.path(), job.archive_name(), job.timestamp
        )


# --------------------------------------------------------------------------------------
class JobView(BaseView):
    @classmethod
    def urls(cls):
        yield "/branches/{branch}/{tag}/{job}"
        yield "/branches/{branch}/{tag}/{job}/"
        yield "/~{user}/branches/{branch}/{tag}/{job}"
        yield "/~{user}/branches/{branch}/{tag}/{job}/"

    async def get(self):
        """
        Get info about a job including metadata and artifact formats.
        """
        job = _get_job(self.repo(), self.request, self.access_granted)
        if not job.exists():
            raise web.HTTPNotFound()
        if job.url() != self.request.path:
            raise web.HTTPFound(job.url())
        html = "html" in self.request.headers.get("Accept", "json")
        data = {"job": job.get_metadata()}
        data["job"]["internal"] = job.is_internal()
        data["job"]["timestamp"] = job.timestamp
        data["job"]["digest"] = job.get_digest()
        formats = []
        for f in job.get_formats():
            fmt_url = f.url()
            if self.access_granted(fmt_url):
                if html:
                    digests = f.get_digests()
                    deb = rpm = False
                    if "repodata/repomd.xml" in digests:
                        rpm = True
                    elif "Release" in digests:
                        deb = True
                    formats.append(
                        {
                            "name": f.name,
                            "internal": f.is_internal(),
                            "rpm": rpm,
                            "deb": deb,
                            "url": fmt_url,
                        }
                    )
                else:
                    formats.append(f.name)
        data["job"]["artifact_formats"] = formats
        if html:
            return aiohttp_jinja2.render_template("job.html", self.request, data)
        return web.json_response(data)

    async def put(self):
        job = _get_job(self.repo(), self.request)
        try:
            data = (await self.json_body())["job"]
            internal = data.get("internal")
            if internal is not None and not isinstance(internal, bool):
                raise TypeError()
            locked = data.get("locked")
            if locked is not None:
                if not isinstance(locked, bool):
                    raise TypeError()
                if not locked:
                    raise ValueError()
        except (TypeError, KeyError, ValueError) as e:
            raise web.HTTPBadRequest(reason="Invalid parameters") from e

        try:
            if internal is not None:
                job.set_internal(internal)
            if locked:
                await job.set_locked(True)
        except FileNotFoundError as e:
            raise web.HTTPNotFound() from e
        except OSError as e:
            raise web.HTTPBadRequest(reason=str(e)) from e

        return web.Response()

    async def post(self):
        job = _get_job(self.repo(), self.request)
        try:
            locked = (await self.json_body())["job"]["locked"]
            if not isinstance(locked, bool):
                raise TypeError()
            if locked:
                raise ValueError()
        except (TypeError, KeyError, ValueError) as e:
            raise web.HTTPBadRequest(reason="Invalid parameters") from e

        try:
            await job.set_locked(False)
        except FileNotFoundError as e:
            raise web.HTTPNotFound() from e
        except OSError as e:
            raise web.HTTPBadRequest(reason=str(e)) from e

        return web.Response()

    async def patch(self):
        """
        Update the metadata of a job.
        """
        try:
            data = (await self.json_body())["job"]
            if not isinstance(data, dict):
                raise TypeError()
        except (TypeError, KeyError) as e:
            raise web.HTTPBadRequest(reason="Invalid parameters") from e
        try:
            job = _get_job(self.repo(), self.request)
            job.add_metadata(data)
        except FileExistsError as e:
            raise web.HTTPBadRequest(reason=str(e)) from e
        return web.Response()

    async def delete(self):
        """
        Delete a job and all its contents.
        """
        loop = asyncio.get_running_loop()
        try:
            job = _get_job(self.repo(), self.request)
            await loop.run_in_executor(None, job.delete)
            self.repo().schedule_cleanup_orphans()
        except FileNotFoundError as e:
            raise web.HTTPNotFound() from e
        except OSError as e:
            raise web.HTTPBadRequest(reason=str(e)) from e
        return web.Response()


# --------------------------------------------------------------------------------------
def _get_job(repo, request, access_cb: Callable[[str], bool] = None):
    match_info = request.match_info
    if (
        match_info["tag"] in ("latest", "stable", "oldstable")
        and request.method != "GET"
    ):
        raise web.HTTPMethodNotAllowed(request.method, ["GET"])
    try:
        return (
            repo.get_branch(match_info["branch"])
            .get_tag(match_info["tag"], access_cb)
            .get_job(match_info["job"])
        )
    except FileNotFoundError as e:
        raise web.HTTPNotFound() from e
