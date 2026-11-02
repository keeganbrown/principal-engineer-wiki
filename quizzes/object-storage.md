# Quiz: Object Storage

## User photos stored in database columns made backups take nine hours. What's the fix?

- [x] Keep photos in a private bucket and only their keys in the database.
- [ ] Compress the photos heavily and keep them in the same database.
- [ ] Move the photos to a second database used only for storing files.
- [ ] Store the photos on the web servers' own local disks instead.

**Why:** Databases are poor file stores. In the example, the database shrank from 2 TB to 40 GB. See [[object-storage]].

## A mobile app uploads a photo by pre-signed URL, then crashes before telling the API. What cleans up the orphaned object?

- [x] A nightly job that deletes unrecorded objects older than a day.
- [ ] Nothing; orphaned objects cost too little to be worth cleaning up.
- [ ] The app re-uploads the photo the next time the user opens it.
- [ ] A database trigger that deletes the object when no row appears.

**Why:** Gaps between two systems need a recovery job with an age threshold and idempotent deletes. A client that records a key days later could point at a deleted object, so the record API checks the object exists. See [[object-storage]].

## Which workload does object storage not fit?

- [x] A database's own data files.
- [ ] Invoice PDFs written once and read many times.
- [ ] User-uploaded videos served through a CDN.
- [ ] Nightly backup archives kept for a year.

**Why:** Objects are written and read whole. A database needs fast random reads and writes inside a file, which takes block storage or a filesystem. See [[object-storage]].
