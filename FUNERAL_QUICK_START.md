# Funeral Avatar - Quick Start

**For Tuesday's funeral. Shorty speaks one last time.**

---

## Setup (Do Once)

```bash
cd /Users/EverettN/stillhere-work

# Install what we need
pip install TTS soundfile

# Create folders
mkdir -p funeral_materials/videos
mkdir -p funeral_materials/photos
```

---

## When Videos/Photos Arrive

**Step 1:** Save them to the right folders

```bash
# Videos go here:
/Users/EverettN/stillhere-work/funeral_materials/videos/

# Photos go here:
/Users/EverettN/stillhere-work/funeral_materials/photos/
```

**Step 2:** Process everything

```bash
python process_funeral_videos.py
```

This automatically:
- Extracts audio from all videos
- Picks the best voice sample
- Selects highest quality photos
- Gets everything ready

**Step 3:** Create the avatar

```bash
python create_funeral_avatar.py
```

This creates:
- `FUNERAL_AVATAR_FINAL.mp4` - Shorty speaking at her funeral

---

## The Message

Default message is in `create_funeral_avatar.py`.

You can edit it to say whatever you want her to say.

Just open the file and change the `message =` part.

---

## Playing At Funeral

1. Copy `FUNERAL_AVATAR_FINAL.mp4` to USB drive
2. Give to funeral home AV person
3. Or play from your laptop

**Duration:** ~60-90 seconds (depends on message length)

---

## If People Are Late Sending Files

No problem. The system is ready.

When files arrive:
1. Drop them in the folders
2. Run `process_funeral_videos.py`
3. Run `create_funeral_avatar.py`
4. Done in 10-15 minutes

---

## Need Help?

Call Everett. He's got you.

---

**She was one of the best. This honors that.**

