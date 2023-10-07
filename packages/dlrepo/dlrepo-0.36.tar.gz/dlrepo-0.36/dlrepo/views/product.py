# Copyright (c) 2021 Julien Floret
# Copyright (c) 2021 Robin Jarry
# SPDX-License-Identifier: BSD-3-Clause

from typing import Callable

from aiohttp import web
import aiohttp_jinja2

from .util import BaseView, TarResponse


# --------------------------------------------------------------------------------------
class ProductsView(BaseView):
    @classmethod
    def urls(cls):
        yield "/products"
        yield "/products/"
        yield "/~{user}/products"
        yield "/~{user}/products/"

    async def get(self):
        """
        Get the list of products.
        """
        if not self.request.path.endswith("/"):
            raise web.HTTPFound(self.request.path + "/")
        products = []
        for p in self.repo().get_products():
            if self.access_granted(p.url()):
                products.append({"name": p.name})
        data = {"products": products}
        if "html" in self.request.headers.get("Accept", "json"):
            return aiohttp_jinja2.render_template("products.html", self.request, data)
        return web.json_response(data)


# --------------------------------------------------------------------------------------
class ProductView(BaseView):
    @classmethod
    def urls(cls):
        yield "/products/{product}"
        yield "/products/{product}/"
        yield "/~{user}/products/{product}"
        yield "/~{user}/products/{product}/"

    def _get_product(self):
        product = self.repo().get_product(self.request.match_info["product"])
        if not product.exists():
            raise web.HTTPNotFound()
        if not self.request.path.endswith("/"):
            raise web.HTTPFound(self.request.path + "/")
        return product

    async def get(self):
        """
        Get the list of variants for a product.
        """
        product = self._get_product()
        variants = []
        for v in product.get_variants():
            if self.access_granted(v.url()):
                variants.append({"name": v.name})
        data = {"product": {"name": product.name, "product_variants": variants}}
        if "html" in self.request.headers.get("Accept", "json"):
            return aiohttp_jinja2.render_template("product.html", self.request, data)
        return web.json_response(data)


# --------------------------------------------------------------------------------------
class ProductVariantView(BaseView):
    @classmethod
    def urls(cls):
        yield "/products/{product}/{variant}"
        yield "/products/{product}/{variant}/"
        yield "/~{user}/products/{product}/{variant}"
        yield "/~{user}/products/{product}/{variant}/"

    def _get_variant(self):
        variant = (
            self.repo()
            .get_product(self.request.match_info["product"])
            .get_variant(self.request.match_info["variant"])
        )
        if not variant.exists():
            raise web.HTTPNotFound()
        if not self.request.path.endswith("/"):
            raise web.HTTPFound(self.request.path + "/")
        return variant

    async def get(self):
        """
        Get the list of branches for a product variant.
        """
        variant = self._get_variant()
        branches = []
        for b in variant.get_branches():
            if self.access_granted(b.url()):
                branches.append({"name": b.name})
        data = {
            "product_variant": {
                "name": variant.name,
                "product_branches": branches,
            },
        }
        if "html" in self.request.headers.get("Accept", "json"):
            return aiohttp_jinja2.render_template(
                "product_variant.html", self.request, data
            )
        return web.json_response(data)


# --------------------------------------------------------------------------------------
class ProductBranchView(BaseView):
    @classmethod
    def urls(cls):
        yield "/products/{product}/{variant}/{product_branch}"
        yield "/products/{product}/{variant}/{product_branch}/"
        yield "/~{user}/products/{product}/{variant}/{product_branch}"
        yield "/~{user}/products/{product}/{variant}/{product_branch}/"

    def _get_branch(self):
        branch = (
            self.repo()
            .get_product(self.request.match_info["product"])
            .get_variant(self.request.match_info["variant"])
            .get_branch(self.request.match_info["product_branch"])
        )
        if not branch.exists():
            raise web.HTTPNotFound()
        if not self.request.path.endswith("/"):
            raise web.HTTPFound(self.request.path + "/")
        return branch

    async def get(self):
        """
        Get the list of versions for a product branch.
        """
        branch = self._get_branch()
        versions = []
        for v in branch.get_versions():
            if self.access_granted(v.url()):
                versions.append(
                    {
                        "name": v.name,
                        "timestamp": v.timestamp,
                        "locked": v.is_locked(),
                        "released": v.is_released(),
                        "stable": v.is_stable(),
                    }
                )
        data = {
            "product_branch": {
                "name": branch.name,
                "versions": versions,
            },
        }
        if "html" in self.request.headers.get("Accept", "json"):
            return aiohttp_jinja2.render_template(
                "product_branch.html", self.request, data
            )
        return web.json_response(data)


# --------------------------------------------------------------------------------------
class VersionView(BaseView):
    @classmethod
    def urls(cls):
        yield "/products/{product}/{variant}/{product_branch}/{version}"
        yield "/products/{product}/{variant}/{product_branch}/{version}/"
        yield "/~{user}/products/{product}/{variant}/{product_branch}/{version}"
        yield "/~{user}/products/{product}/{variant}/{product_branch}/{version}/"

    async def get(self):
        """
        Get the list of versions for a product version.
        """
        version = _get_version(
            self.repo(), self.request.match_info, self.access_granted
        )
        if version.url() != self.request.path:
            raise web.HTTPFound(version.url())
        html = "html" in self.request.headers.get("Accept", "json")

        formats = []
        branch_links = []
        for fmt in version.get_formats():
            fmt_url = fmt.url()
            if self.access_granted(fmt_url):
                if html:
                    digests = fmt.get_digests()
                    deb = rpm = False
                    if "repodata/repomd.xml" in digests:
                        rpm = True
                    elif "Release" in digests:
                        deb = True
                    formats.append(
                        {
                            "name": fmt.name,
                            "internal": fmt.is_internal(),
                            "rpm": rpm,
                            "deb": deb,
                            "url": fmt_url,
                        }
                    )
                    job = fmt.path().resolve().parent
                    link = f"{job.parent.parent.name}/{job.parent.name}/{job.name}"
                    if link not in branch_links and self.access_granted(
                        fmt.root().url() + link
                    ):
                        branch_links.append(link)
                else:
                    formats.append(fmt.name)

        data = {"version": {"name": version.name, "artifact_formats": formats}}

        if html:
            if branch_links:
                data["version"]["branch_links"] = branch_links

            return aiohttp_jinja2.render_template(
                "product_version.html", self.request, data
            )
        return web.json_response(data)


# --------------------------------------------------------------------------------------
class VersionArchiveView(BaseView):
    @classmethod
    def urls(cls):
        yield "/products/{product}/{variant}/{product_branch}/{version}.tar"
        yield "/~{user}/products/{product}/{variant}/{product_branch}/{version}.tar"

    def _digests(self, version):
        digests = {}
        for fmt in version.get_formats():
            if self.access_granted(fmt.url()):
                for f, digest in fmt.get_digests().items():
                    digests[f"{fmt.name}/{f}"] = digest
        return digests

    async def get(self):
        version = _get_version(
            self.repo(), self.request.match_info, self.access_granted
        )
        url = version.url().rstrip("/") + ".tar"
        if url != self.request.path:
            raise web.HTTPFound(version.url())
        return TarResponse(
            self._digests(version),
            version.path(),
            version.archive_name(),
            version.timestamp,
        )


# --------------------------------------------------------------------------------------
def _get_version(repo, match_info, access_cb: Callable[[str], bool] = None):
    try:
        version = (
            repo.get_product(match_info["product"])
            .get_variant(match_info["variant"])
            .get_branch(match_info["product_branch"])
            .get_version(match_info["version"], access_cb)
        )
    except FileNotFoundError as e:
        raise web.HTTPNotFound() from e
    if not version.exists():
        raise web.HTTPNotFound()
    return version
