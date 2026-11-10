#!/usr/bin/env python3
import json
import sys
from pathlib import Path

if len(sys.argv) != 3:
    sys.exit(f"usage: {sys.argv[0]} BUILD_DIR DATADIR")
build_dir, data_dir = Path(sys.argv[1]), sys.argv[2].rstrip("/")
profiles_dir = build_dir / "profiles"

rules = []
for model in json.loads((build_dir / "models.json").read_text()).values():
    rules.append({
        "matches": [{
            "alsa.id": f"t2-{model}",
            "api.alsa.pcm.stream": "playback",
            "device.profile.name": "HiFi: Speaker: sink",
        }],
        "actions": {"create-filter": {
            "filter-path": f"{data_dir}/t2-dsp/profiles/{model}/graph.json",
            "hide-parent": True,
        }},
    })
    if (profiles_dir / model / "mic.json").is_file():
        rules.append({
            "matches": [{
                "alsa.id": f"t2-{model}",
                "api.alsa.pcm.stream": "capture",
                "device.profile.name": "HiFi: Mic: source",
            }],
            "actions": {"create-filter": {
                "filter-path": f"{data_dir}/t2-dsp/profiles/{model}/mic.json",
                "hide-parent": True,
            }},
        })

conf = {
    "node.software-dsp.rules": rules,
    "monitor.alsa.rules": [{
        "matches": [{
            "alsa.id": "~t2-.*",
            "api.alsa.pcm.stream": "playback",
        }],
        "actions": {"update-props": {
            "audio.allowed-rates": [96000, 88200, 48000, 44100],
        }},
    }],
    "wireplumber.profiles": {"main": {"node.software-dsp": "required"}},
}
(build_dir / "50-t2-dsp.conf").write_text(json.dumps(conf, indent=4) + "\n")
