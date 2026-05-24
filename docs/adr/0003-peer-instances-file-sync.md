# Peer instances with file-based sync

Each family member runs a local Instance (laptop, etc.) with its own SQLite database and photo store. Instances stay consistent by exchanging Sync packets — incremental ZIP exports of records created or changed since a timestamp — via an out-of-band channel (shared folder, AirDrop, USB). There is no centrally hosted server.

Event merge assumes disjoint entry: new Events are union-merged by stable UUID. All other records (profiles, regimens, tags, edited Events) merge last-write-wins by `updated_at`. All Instances are equal peers — no primary device.

**Considered options:** Single canonical server on home LAN, peer Instances with file sync (chosen), cloud-hosted multi-user.

**Consequences:** Every record needs a stable UUID and `updated_at` timestamp. Export/import is a core feature, not just backup. Sync merge rules for non-event data must be defined separately. v1 sync is manual export/import; watched-folder automation is deferred.
