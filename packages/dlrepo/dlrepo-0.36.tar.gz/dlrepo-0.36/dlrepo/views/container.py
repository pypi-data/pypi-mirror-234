# Copyright (c) 2021 Julien Floret
# Copyright (c) 2021 Robin Jarry
# SPDX-License-Identifier: BSD-3-Clause

from http import HTTPStatus
import json

from aiohttp import web

from . import errors
from .util import BaseView


# --------------------------------------------------------------------------------------
class ContainerView(BaseView):
    def response(self, body=None, path=None, status=HTTPStatus.OK, headers=None):
        if isinstance(body, (dict, list)):
            resp = web.json_response(body, status=status, headers=headers)
        elif path is not None:
            resp = self.file_response(path, status=status, headers=headers)
        else:
            resp = web.Response(body=body, status=status, headers=headers)
        resp.headers["Docker-Distribution-Api-Version"] = "registry/2.0"
        return resp

    def repo(self):
        try:
            return super().repo()
        except web.HTTPForbidden as e:
            raise errors.Denied(str(e)) from e

    def registry(self):
        try:
            return super().repo().container_registry
        except web.HTTPForbidden as e:
            raise errors.Denied(str(e)) from e


# --------------------------------------------------------------------------------------
class RootView(ContainerView):
    @classmethod
    def urls(cls):
        yield "/v2/"

    async def get(self):
        return self.response({})


# --------------------------------------------------------------------------------------
class CatalogView(ContainerView):
    @classmethod
    def urls(cls):
        yield "/v2/_catalog"

    async def get(self):
        repositories = []
        for image in self.registry().repositories():
            if self.access_granted(f"/v2/{image}/"):
                repositories.append(image)
        return self.response({"repositories": repositories})


# --------------------------------------------------------------------------------------
class ManifestReadOnlyView(ContainerView):
    @classmethod
    def urls(cls):
        yield "/v2/{branch}/{job}/manifests/{reference}"
        yield "/v2/u/{user}/{branch}/{job}/manifests/{reference}"
        yield "/v2/{product}/{variant}/{product_branch}/manifests/{reference}"
        yield "/v2/u/{user}/{product}/{variant}/{product_branch}/manifests/{reference}"

    def get_manifest(self):
        match = self.request.match_info
        ref = match["reference"]
        registry = self.registry()
        try:
            if ":" in ref:
                path = registry.manifest_by_digest(ref)
                digest = ref
            else:
                if "product" in match:
                    parent = (
                        self.repo()
                        .get_product(match["product"])
                        .get_variant(match["variant"])
                        .get_branch(match["product_branch"])
                        .get_version(ref, self.access_granted)
                    )
                else:
                    parent = (
                        self.repo()
                        .get_branch(match["branch"])
                        .get_tag(ref, self.access_granted)
                        .get_job(match["job"])
                    )
                path, digest = registry.manifest_by_parent(parent.path())
        except ValueError as e:
            raise errors.ManifestInvalid(ref) from e
        except FileNotFoundError as e:
            raise errors.ManifestUnknown(ref) from e

        return path, digest

    async def head(self):
        return await self.get()

    async def get(self):
        path, digest = self.get_manifest()
        try:
            manifest = json.loads(path.read_text())
            media_type = manifest["mediaType"]
        except (ValueError, KeyError) as e:
            raise errors.ManifestInvalid() from e
        headers = {
            "Content-Type": media_type,
            "Docker-Content-Digest": digest,
        }
        if self.request.method == "HEAD":
            headers["Content-Length"] = str(path.stat().st_size)
            path = None
        return self.response(path=path, headers=headers)


# --------------------------------------------------------------------------------------
class ManifestView(ManifestReadOnlyView):
    CONTENT_TYPES = (
        "application/vnd.oci.image.manifest.v1+json",
        "application/vnd.docker.distribution.manifest.v2+json",
    )

    @classmethod
    def urls(cls):
        yield "/v2/{branch}/{job}/manifests/{reference}"
        yield "/v2/u/{user}/{branch}/{job}/manifests/{reference}"

    async def put(self):
        match = self.request.match_info
        if "product" in match:
            raise errors.Unsupported("uploading manifests by product is not supported")
        tag = match["reference"]
        if ":" in tag:
            raise errors.Unsupported("uploading manifests by digest is not supported")
        if tag in ("latest", "stable", "oldstable"):
            raise errors.Unsupported(
                "uploading explicit 'latest', 'stable' or 'oldstable' tags is not supported"
            )
        job = self.repo().get_branch(match["branch"]).get_tag(tag).get_job(match["job"])
        try:
            manifest = await self.request.json()
            if not isinstance(manifest, dict):
                raise ValueError()
            if manifest.get("mediaType") not in self.CONTENT_TYPES:
                raise errors.Unsupported()
            digest = self.registry().new_manifest(job, manifest)
        except PermissionError as e:
            raise errors.Denied(str(e)) from e
        except ValueError as e:
            raise errors.ManifestInvalid() from e
        except FileNotFoundError as e:
            raise errors.BlobUnknown() from e

        return self.response(
            status=HTTPStatus.CREATED,
            headers={
                "Location": self.request.path,
                "Content-Length": "0",
                "Docker-Content-Digest": digest,
            },
        )


# --------------------------------------------------------------------------------------
class TagsListView(ContainerView):
    @classmethod
    def urls(cls):
        yield "/v2/{branch}/{job}/tags/list"
        yield "/v2/u/{user}/{branch}/{job}/tags/list"
        yield "/v2/{product}/{variant}/{product_branch}/tags/list"
        yield "/v2/u/{user}/{product}/{variant}/{product_branch}/tags/list"

    async def get(self):
        match = self.request.match_info
        try:
            if "product" in match:
                args = (match["product"], match["variant"], match["product_branch"])
                tags = self.registry().product_tags(*args)
            else:
                args = (match["branch"], match["job"])
                tags = self.registry().job_tags(*args)
        except FileNotFoundError as e:
            raise errors.ManifestUnknown(self.request.path) from e

        image = "/".join(args)
        if "user" in match:
            root_url = f"/v2/{match['user']}/{image}"
        else:
            root_url = f"/v2/{image}"

        accessible_tags = []
        for t in tags:
            if self.access_granted(f"{root_url}/manifests/{t}"):
                accessible_tags.append(t)

        return self.response({"name": image, "tags": accessible_tags})


# --------------------------------------------------------------------------------------
class NewBlobUploadView(ContainerView):
    @classmethod
    def urls(cls):
        yield "/v2/{branch}/{job}/blobs/uploads/"
        yield "/v2/u/{user}/{branch}/{job}/blobs/uploads/"

    async def post(self):
        uuid = self.repo().next_upload()
        return self.response(
            status=HTTPStatus.ACCEPTED,
            headers={
                "Location": f"{self.request.path}{uuid}",
                "Range": "0-0",
                "Docker-Upload-Uuid": uuid,
            },
        )


# --------------------------------------------------------------------------------------
class BlobsUploadsView(ContainerView):
    @classmethod
    def urls(cls):
        yield "/v2/{branch}/{job}/blobs/uploads/{uuid}"
        yield "/v2/u/{user}/{branch}/{job}/blobs/uploads/{uuid}"

    async def get(self):
        uuid = self.request.match_info["uuid"]
        try:
            path = self.repo().upload_path(uuid)
            data_size = path.stat().st_size
        except PermissionError as e:
            raise errors.Denied(str(e)) from e
        except FileNotFoundError as e:
            raise errors.BlobUploadUnknown() from e
        return self.response(
            status=HTTPStatus.NO_CONTENT,
            headers={
                "Location": self.request.path,
                "Range": f"0-{data_size - 1}",
                "Docker-Upload-Uuid": uuid,
            },
        )

    async def patch(self):
        uuid = self.request.match_info["uuid"]
        try:
            data_size = await self.repo().update_upload(uuid, self.request.content.read)
        except PermissionError as e:
            raise errors.Denied(str(e)) from e
        except FileNotFoundError as e:
            raise errors.BlobUploadUnknown() from e
        return self.response(
            status=HTTPStatus.ACCEPTED,
            headers={
                "Location": self.request.path,
                "Range": f"0-{data_size - 1}",
                "Docker-Upload-Uuid": uuid,
            },
        )

    async def put(self):
        uuid = self.request.match_info["uuid"]
        try:
            digest = self.request.query["digest"]
            if int(self.request.headers.get("Content-Length", "0")) > 0:
                await self.repo().update_upload(uuid, self.request.content.read)
            await self.repo().finalize_upload(uuid, digest)
        except PermissionError as e:
            raise errors.Denied(str(e)) from e
        except ValueError as e:
            raise errors.BlobUploadInvalid() from e
        except KeyError as e:
            self.repo().cancel_upload(uuid)
            raise errors.BlobUploadInvalid() from e
        except FileNotFoundError as e:
            raise errors.BlobUploadUnknown() from e
        return self.response(
            status=HTTPStatus.CREATED,
            headers={
                "Location": self.request.path,
                "Docker-Content-Digest": digest,
            },
        )

    async def delete(self):
        try:
            self.repo().cancel_upload(self.request.match_info["uuid"])
        except FileNotFoundError as e:
            raise errors.BlobUploadUnknown() from e
        return self.response(status=HTTPStatus.NO_CONTENT)


# --------------------------------------------------------------------------------------
class BlobsView(ContainerView):
    @classmethod
    def urls(cls):
        yield "/v2/{branch}/{job}/blobs/{digest}"
        yield "/v2/u/{user}/{branch}/{job}/blobs/{digest}"
        yield "/v2/{product}/{variant}/{product_branch}/blobs/{digest}"
        yield "/v2/u/{user}/{product}/{variant}/{product_branch}/blobs/{digest}"

    def _blob_path(self):
        digest = self.request.match_info["digest"]
        try:
            path = self.repo().blob_path(digest)
        except ValueError as e:
            raise errors.BlobUnknown(str(e)) from e
        if not path.is_file():
            raise errors.BlobUnknown()
        return path, digest

    async def head(self):
        path, digest = self._blob_path()
        return self.response(
            headers={
                "Content-Length": str(path.stat().st_size),
                "Docker-Content-Digest": digest,
            },
        )

    async def get(self):
        path, digest = self._blob_path()
        return self.response(path=path, headers={"Docker-Content-Digest": digest})
