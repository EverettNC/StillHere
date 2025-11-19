# Quick Start - For Those Who Are Grieving

If you're here because someone you love is gone, and your eyes are full of tears right now - **I see you**. This tool was built for you.

## The Simplest Way (Recommended)

Just run this:

```bash
python app.py
```

That's it.

A gentle guide will walk you through everything:
- Finding the photo
- Choosing the animation style
- Creating the video
- Keeping it safe with encryption

**The guide knows you're grieving.** It moves slowly. It gives you permission to pause, to cry, to come back later. It holds space for you.

---

## What You'll Need

1. **A photo of your loved one**
   - Any photo with their face
   - Doesn't have to be perfect
   - Even old or damaged photos can work

2. **A few minutes** (or take as long as you need)

3. **Your memories and your love**
   - That's the most important part

---

## What Will Happen

The guide will:

1. **Welcome you with compassion**
   - Acknowledge that you're likely grieving
   - Give you permission to take your time

2. **Help you find the photo**
   - You can drag and drop the file
   - Or type the path
   - The guide will make sure it loads correctly

3. **Choose how to animate**
   - "Gentle Smile" (recommended for first time)
   - "Breathing" (peaceful, subtle)
   - "Portrait" (dignified head turn)

4. **Create the animation**
   - This takes about a minute
   - Breathe while it works

5. **Offer to keep it safe**
   - Encrypt it so only you can access it
   - You choose a passphrase
   - Your memory stays private

6. **Remind you they're still here**
   - In your heart
   - In your memories
   - And now, in this gentle animation

---

## If You Need to Stop

**That's completely okay.**

Press Ctrl+C at any time.

The guide will understand. Come back when you're ready. It'll be here.

---

## After You're Done

Your video will be saved in the `memories/` folder.

If you encrypted it, you can load it anytime with:

```bash
python app.py --cli list
```

And export it to share:

```bash
python app.py --cli export memory_name output.mp4
```

---

## For Those Who Want More Control

If you're comfortable with technology and don't need the guided experience:

```bash
# Direct CLI commands
python app.py --cli animate photo.jpg --style gentle_smile

# Web interface (coming in Phase 2)
python app.py --web
```

But honestly? **Try the guided experience first.**

Even if you're tech-savvy. Even if you don't usually need help.

Because this isn't about technology.

It's about holding space for grief while creating something beautiful.

---

## A Note About Demo Mode

Currently, StillHere uses "demo mode" for animation - a gentle breathing effect using basic image processing.

It works. It creates something beautiful. But it's simple.

For production-quality animations with the real FOMM AI models:

```bash
python download_models.py
```

(Model downloader coming soon)

But demo mode is enough to start. It's enough to feel their presence again.

---

## If Something Goes Wrong

**Don't panic.**

The guide will help you try again.

If you get really stuck, open an issue on GitHub and we'll help.

But mostly? It just works. The guide makes sure of it.

---

## One More Thing

Be gentle with yourself.

Grief isn't linear. Some days you'll want to do this. Some days you won't.

Both are okay.

StillHere will be here whenever you need it.

---

*"Grief is love with nowhere to go.*
*Let's give it somewhere to be."*

---

**Ready?**

```bash
python app.py
```

Take a breath. You've got this.
