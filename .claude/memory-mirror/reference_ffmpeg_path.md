---
name: reference_ffmpeg_path
description: ffmpeg/ffprobe installed via winget (Gyan.FFmpeg) but NOT visible to tool shells — prepend its bin to PATH per command
metadata: 
  node_type: memory
  type: reference
  originSessionId: f3d84bc8-67b0-4258-b634-760aedee037d
---

ffmpeg + ffprobe are installed (winget Gyan.FFmpeg, v8.x) and the bin dir is
already in the **User** PATH, but the Bash/PowerShell tool shells are spawned
from a parent process that predates the PATH entry, so `ffmpeg`/`ffprobe`
resolve as "command not found" in every fresh tool call. `setx`/registry edits
do NOT help the current session.

Fix per command (this is the durable workaround until the shell host restarts):

```bash
export PATH="$PATH:/c/Users/sidor/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.2-full_build/bin"
```

Put that line at the top of any Bash command that runs ffmpeg/ffprobe OR a
helper that shells out to them (render.py, grade_sheet.py scan/sheet — their
subprocess inherits the shell PATH). The exact `ffmpeg-<ver>-full_build` folder
name changes on upgrade — glob or re-check with `Get-ChildItem` if it moves.
Do NOT waste the [[reference_video_use_settings]] freshness gate re-discovering
this each session.
