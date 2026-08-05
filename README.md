# pkg-rpm-time-services

RPM packaging for [`quic/time-services`](https://github.com/quic/time-services)
— the Qualcomm time daemon that synchronises time from the modem to the
applications processor and maintains time offsets across reboots, once set
from any source.

This repo builds and publishes the `time-services` RPM via the shared
[`qualcomm-linux/qcom-rpm-utils`](https://github.com/qualcomm-linux/qcom-rpm-utils)
reusable workflows — it follows the same one-package-per-repo template used
across `qualcomm-linux/pkg-rpm-*`, and mirrors the Debian/Ubuntu packaging in
[`qualcomm-linux/pkg-time-services`](https://github.com/qualcomm-linux/pkg-time-services)
(dedicated `rtc` service user, `CAP_SYS_TIME` systemd unit, udev rule for
`/dev/rtc0`).

---

## Package contents

| File | Purpose |
|---|---|
| [`time-services.spec`](time-services.spec) | RPM spec for `time-services`. Builds via autotools (`autoreconf` + `%configure`), installs the `time_daemon` binary plus a `systemd` unit, `sysusers.d` entry, and `udev` rule generated inline in `%install`. |
| [`sources`](sources) | dist-git checksum pointer for the upstream `v0.1.2` release tarball (SHA512). The tarball itself is never committed — see [`docs/workflows.md`](docs/workflows.md) for the lookaside-cache model. |

> **Known gap:** `time-services` hard-depends on `qmi-framework`
> (`pkgconfig(qmi-framework)` in the spec). No RPM/dnf-repo for `qmi-framework`
> exists yet anywhere in `qualcomm-linux` (only Debian packaging in
> [`pkg-qmi-framework`](https://github.com/qualcomm-linux/pkg-qmi-framework)).
> Builds here will fail at `dnf builddep` until a `qmi-framework` RPM is
> published and registered via the `extra-repo` input on
> [`build-on-pr.yml`](.github/workflows/build-on-pr.yml) /
> [`pkg-release.yml`](.github/workflows/pkg-release.yml).

## Updating the package version

1. Bump `Version:` in [`time-services.spec`](time-services.spec) (and the
   `Source0:` URL if the upstream release layout changed).
2. Recompute the checksum for the new release tarball:
   ```bash
   sha512sum --tag time-services-<newversion>.tar.gz > sources
   ```
3. Commit the spec + `sources`, open a PR (`build-on-pr` verifies the tarball
   and builds it), merge, then run **Release**. The first release fetches the
   new upstream tarball, verifies it, and caches it back to Artifactory
   automatically.

---

## CI: build on PR, release on demand

| Workflow | Trigger | Purpose |
|---|---|---|
| [`build-on-pr.yml`](.github/workflows/build-on-pr.yml) | Pull request | Build the RPM so reviewers confirm the package still builds. Read-only — never publishes. |
| [`pkg-release.yml`](.github/workflows/pkg-release.yml) | Manual (`workflow_dispatch`) | Build **and** publish the RPM to Artifactory, behind an approval gate. |

Both delegate to reusable workflows in `qcom-rpm-utils`, which run `rpmbuild`
inside the prebuilt `rpm-builder` container image. Required repo configuration
(`CACHE_BASE_URL` variable, `ARTIFACTORY_ACCESS_TOKEN` secret,
`pkg-release-approval` environment, runner pool access) is documented in full
in [`docs/workflows.md`](docs/workflows.md), along with the dist-git
sources/lookaside-cache model and a troubleshooting table.

This repo was created from [`qualcomm-linux/pkg-rpm-template`](https://github.com/qualcomm-linux/pkg-rpm-template);
see that template's README if you're onboarding a *different* package and
want the generic step-by-step instructions.
