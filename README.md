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
— Provides the Qualcomm time daemon that synchronises time from the modem to the
applications processor and maintains time offsets across reboots. It mirrors
the Debian/Ubuntu packaging in
[`qualcomm-linux/pkg-time-services`](https://github.com/qualcomm-linux/pkg-time-services):
a dedicated `rtc` service user, a `CAP_SYS_TIME` systemd unit, and a udev rule
for `/dev/rtc0`, all generated inline in the spec's `%install` section.


