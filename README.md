<!--
Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
SPDX-License-Identifier: BSD-3-Clause
-->
# Package branch — CentOS 10 Stream (`c10s`)

**This is the branch you work on.** It holds the `time-services` RPM's spec
file and `sources` pointer, plus the CI workflows that build and publish them.

Following the Fedora/CentOS **dist-git** convention, each distro stream gets its
own branch, and the packaging files live at the branch root:

| Branch | Stream | Contents |
|---|---|---|
| `main` | — | Template docs, onboarding guide, community files. Nothing is built here. |
| **`c10s`** | CentOS 10 Stream | **This branch.** `time-services.spec` + `sources` + workflows. |

Full onboarding guide, configuration reference, and troubleshooting live on
[`main`](../../tree/main) — see its `README.md` and `docs/workflows.md`.

---

## Layout

```
time-services.spec       # RPM spec for quic/time-services
sources                  # dist-git checksum pointer for the v0.1.2 release tarball
.github/workflows/       # build-on-pr.yml, pkg-release.yml
```

This RPM packages [`quic/time-services`](https://github.com/quic/time-services)
— the Qualcomm time daemon that synchronises time from the modem to the
applications processor and maintains time offsets across reboots. It mirrors
the Debian/Ubuntu packaging in
[`qualcomm-linux/pkg-time-services`](https://github.com/qualcomm-linux/pkg-time-services):
a dedicated `rtc` service user, a `CAP_SYS_TIME` systemd unit, and a udev rule
for `/dev/rtc0`, all generated inline in the spec's `%install` section.

> **Known gap:** `time-services` hard-depends on `qmi-framework`
> (`BuildRequires: pkgconfig(qmi-framework)`). A qmi-framework RPM is now built
> and released from
> [`qualcomm-linux/pkg-rpm-qmi-framework`](https://github.com/qualcomm-linux/pkg-rpm-qmi-framework)
> (`c10s` branch) — confirm its Artifactory dnf repo is reachable (registered
> via the `extra-repo` input on the workflows below) before relying on a clean
> `dnf builddep` here.

---

## Getting started

### Update the version

Two edits, every time:

1. Bump `Version:` in [`time-services.spec`](time-services.spec) (and the
   `Source0:` URL if the upstream release layout changed).
2. Recompute the checksum:
   ```bash
   sha512sum --tag time-services-<newversion>.tar.gz > sources
   ```

Commit both, open a PR against this branch, merge, then run **Release**. The
first release fetches the new upstream tarball, verifies it, and caches it back
automatically.

### Open a PR

`build-on-pr` fetches the tarball (from the lookaside cache, or from the spec's
`Source` URL on a cache miss), verifies the checksum, and builds the RPM.
Download it from the run's **Artifacts**.

### Release

**Actions → Release → Run workflow**, selecting this branch. A reviewer
approves the `pkg-release-approval` gate, then the RPM publishes to
Artifactory.
