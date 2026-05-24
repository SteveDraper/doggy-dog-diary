# Doggy Dog Diary

A personal record-keeping app for a single household to track a small number of pet dogs and their ongoing history.

## Language

**Household**:
The single implicit owner of all data in the app. There is no multi-tenant separation and no per-person accounts in v1.
_Avoid_: User, tenant, account

**Dog**:
A pet tracked by the household. Each Dog has one Profile, a life status (current or not), and appears in many Events.
_Avoid_: Pet (too generic), animal

**Dog status**:
Whether a Dog is actively tracked. Current dogs appear first on the home screen; non-current dogs (deceased, rehomed, etc.) remain visible with a visual indicator and sort after current dogs. History, search, and export are unchanged.
_Avoid_: Archived, inactive, deceased flag

**Profile**:
The stable identity and current facts for a Dog — name, photo, structured fields (DOB, sex, breed, kennel club registration, etc.), and a single mutable description. Not a chronological diary.
_Avoid_: Dog detail, dog page

**Kennel club registration**:
Structured Profile fields for official registry information — registered name, registration number, and registering body (e.g. The Kennel Club, AKC). Optional.
_Avoid_: Pedigree, KC info

**Event**:
A dated occurrence worth recording. Has optional free-form notes and tags. Most Events involve one Dog; shared activities (e.g. walks) may involve several. May contain Measurements. A child Event may link to a parent Event when something happens during something else (e.g. a pooh during a walk).
_Avoid_: History entry, log item, record

**Parent Event**:
An Event that groups context for nested child Events. A walk is a parent Event with multiple participating Dogs; a pooh recorded mid-walk is a child Event linked to that walk and attributed to one Dog.
_Avoid_: Container, session

**Measurement**:
A typed structured value on an Event (e.g. weight in lb, pooh size, walk length in miles). Measurements feed charts and aggregations. An Event may have zero or many.
_Avoid_: Field, metric, data point

**Walk**:
A multi-dog Exercise Event recording distance in miles. Child Events (e.g. a pooh) may link to the walk as their parent.
_Avoid_: Exercise session, activity

**Tag**:
A household-defined label applied to an Event's notes or profile description. Tags express cross-cutting concerns (health, concern, diet-change) shared across all Dogs.
_Avoid_: Label, category (when referring to history views like Weight or Health)

**View**:
A saved query over Events that powers a category icon on the dog detail screen — e.g. "all Events with a pooh Measurement" or "all Events tagged health". Views are entry shortcuts and filtered lists, not storage partitions.
_Avoid_: Category (as a storage bucket)

**Medication regimen**:
A period during which a Dog takes a specific medication — drug name, dose, frequency, start date, optional end date, and notes. Active regimens (no end date) represent current medications.
_Avoid_: Prescription, med record

**Dose Event**:
An optional dated Event recording a single medication administration, missed dose, or related observation. Linked to a Medication regimen. Not required for v1.
_Avoid_: Dose log, administration record

**Profile photo**:
The image shown on a Dog's home-screen tile. Always stored locally on the backend — never an external link alone.
_Avoid_: Avatar, thumbnail

**Photo reference**:
A pointer to one or more images outside the app — a single photo URL or an album/gallery URL (e.g. iCloud, Google Photos). The default way to attach photos to Events or the Photos view.
_Avoid_: Image link, URL

**Local copy**:
An optional backend-stored duplicate of a Photo reference's content. Created on demand via augmentation — improves load latency and guarantees the image survives if the external source disappears.
_Avoid_: Cache, mirror, download

**Album reference**:
A Photo reference pointing to an external album or gallery rather than a single image. v1 treats albums as bookmarks (display metadata, link out to view); album-wide import via augmentation is deferred to a later phase.
_Avoid_: Gallery link, photo album

**Search result**:
A match from a tag filter and/or text query over Event notes, profile descriptions, and related text. Each result links to its source — an Event, Medication regimen, or Dog profile — not an isolated snippet.
_Avoid_: Hit, match

**Instance**:
A copy of the app running on a device with its own local database. Multiple Instances within the Household exchange data via Sync packets — there is no central hosted server.
_Avoid_: Client, node, device

**Sync packet**:
A time-bounded ZIP export containing records created or changed since a prior sync timestamp. Imported by another Instance and merged into its local database.
_Avoid_: Delta export, sync file

**Sync merge**:
Rules for combining Sync packets. New Events union by UUID (disjoint entry assumed). All other records — profiles, regimens, tags, edited Events — merge by last-write-wins using `updated_at`. All Instances are equal peers; no primary device.
_Avoid_: Conflict resolution, replication

## UI conventions

Dog detail is a full screen (not a overlay on the home screen). Each View opens its own screen from there. Quick recording and editing use a lightweight overlay without navigating away. Search results open the source Event or profile directly.

## Example dialogue

**Dev:** "Nico had a medium pooh with blood in it — is that two records?"
**Expert:** "One Event. A pooh Measurement, notes about the blood, tags like health and concern. It shows up in the Pooh view and the Health view."
**Dev:** "Where do I write 'anxious around loud noises'?"
**Expert:** "Profile description — stable facts, updated in place. Dated observations are Events."
**Dev:** "We walked Nico and Bella for 40 minutes and Nico poohed mid-walk. One record or three?"
**Expert:** "One walk Event — both dogs, distance in miles. Plus a child pooh Event for Nico linked to that walk. Nico's pooh view shows the pooh; the walk detail shows both."
**Dev:** "What meds is Nico on right now?"
**Expert:** "Look at active Medication regimens — no end date. Past courses have an end date."
**Dev:** "Do I log every pill?"
**Expert:** "Not required. Regimens track what he's on; Dose Events are optional if you want that detail later."
**Dev:** "Can the profile photo be an iCloud link?"
**Expert:** "No — profile photo is always stored locally. Gallery photos default to external links, but you can augment with a local copy."
**Dev:** "I linked a Google Photos album from his birthday."
**Expert:** "v1 shows it as a bookmark — title, maybe a cover, tap to open the album. Augment works on single photos first; importing a whole album comes later."
**Dev:** "Can I search for everything tagged concern?"
**Expert:** "Yes — tags are the primary filter. Optional text narrows further. Every result jumps you to the source Event or profile."
**Dev:** "Nico passed away — do we delete his tile?"
**Expert:** "No. Mark him non-current — he stays on the home screen with a memorial indicator, sorted after Bella. All his history remains."
**Dev:** "Where does his KC registration number go?"
**Expert:** "Kennel club registration on the Profile — registered name, number, and registering body. Separate from Certificates history for show rosettes and titles."
**Dev:** "My partner edited Nico's profile on her laptop while I updated it here — what wins?"
**Expert:** "Whichever change has the later updated_at when you sync. All Instances are equal."
