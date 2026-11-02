# Quiz: Object Storage

## User photos stored in database columns made backups take nine hours. What's the fix?

- [x] Store photos in a private bucket and keep only their keys in the database.
- [ ] Compress the photos and keep them in the database.
- [ ] Move photos to a second database used only for files.
- [ ] Store photos on the web servers' local disks.

**Why:** Databases are poor file stores. In the example, the database shrank from 2 TB to 40 GB. See [[object-storage]].

## The app uploads a photo but crashes before recording it. What handles the orphan?

- [x] A nightly cleanup that deletes objects older than 24 hours with no matching row.
- [ ] Nothing; orphaned objects are deleted by the store automatically.
- [ ] The app re-uploads the photo on its next launch.
- [ ] A database trigger that deletes the object.

**Why:** Gaps between two systems need a recovery job with a clear age threshold and idempotent deletes. See [[object-storage]].

## Which workload does object storage not fit?

- [x] A database's own data files, which need fast random reads and writes inside a file.
- [ ] Invoice PDFs written once and read many times.
- [ ] User-uploaded videos served through a CDN.
- [ ] Nightly backup archives kept for a year.

**Why:** Objects are written and read whole. In-place random access needs block storage or a filesystem. See [[object-storage]].
