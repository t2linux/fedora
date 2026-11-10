#!/usr/bin/env python3
import json
import sys
from pathlib import Path

build_dir = Path(sys.argv[1])
data_dir = sys.argv[2].rstrip("/")
profiles_dir = build_dir / "profiles"
filter_rules = []
alsa_rules = []
for model in json.loads((build_dir / "models.json").read_text()).values():
    alsa_rules.append({
        "matches": [{
            "alsa.id": f"t2-{model}",
            "api.alsa.pcm.stream": "playback",
            "device.profile.name": "HiFi: Speaker: sink",
        }],
        "actions": {"update-props": {
            "node.name": f"alsa_output.t2-{model}.RawSpeakers",
            "audio.allowed-rates": [96000, 88200, 48000, 44100],
        }},
    })
    alsa_rules.append({
        "matches": [{
            "alsa.id": f"t2-{model}",
            "api.alsa.pcm.stream": "capture",
            "device.profile.name": "HiFi: Mic: source",
        }],
        "actions": {"update-props": {
            "node.name": f"alsa_input.t2-{model}.RawMic",
        }},
    })
    filter_rules.append({
        "matches": [{
            "node.name": f"alsa_output.t2-{model}.RawSpeakers",
        }],
        "actions": {"create-filter": {
            "filter-path": f"{data_dir}/t2-dsp/profiles/{model}/graph.json",
            "hide-parent": True,
        }},
    })
    if (profiles_dir / model / "mic.json").is_file():
        mic = json.loads((profiles_dir / model / "mic.json").read_text())
        mic["playback.props"]["priority.session"] = 2005
        (profiles_dir / model / "mic.json").write_text(
            json.dumps(mic, indent=4) + "\n")
        filter_rules.append({
            "matches": [{
                "node.name": f"alsa_input.t2-{model}.RawMic",
            }],
            "actions": {"create-filter": {
                "filter-path": f"{data_dir}/t2-dsp/profiles/{model}/mic.json",
                "hide-parent": True,
            }},
        })

conf = {
    "monitor.alsa.rules": alsa_rules,
    "node.software-dsp.rules": filter_rules,
    "wireplumber.profiles": {"main": {"node.software-dsp": "required"}},
}
(build_dir / "50-t2-dsp.conf").write_text(json.dumps(conf, indent=4) + "\n")
