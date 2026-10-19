# Changelog

## Unreleased
- Add a Blender MCP bridge for structured `result` responses and multi-angle/multi-frame review with live scene state restoration.
- Add Poly Haven texture/HDRI search, download planning, verified downloads and source manifests, plus guidance for licensed commercial materials, physical scale, grain direction and GLB delivery.
- Replace unavailable live `look` calls with review sheets and screenshots; clarify that Workbench colors do not evaluate PBR textures.
- Fix wireframe review spikes on beveled meshes. Add bridge regression tests and offline material sourcing tests in CI.

## [1.1.0] - 2026-10-16
- New `blender-time-of-day`: sky + sun measured from Blender's sky model, night with moon/stars, fog from visibility, moods (cyberpunk, horror, underwater, desert).
- New `blender-weather-fx`: looping rain/snow/dust/embers, wet surfaces, puddles with ripples, snow cover, lightning.
- With vs without skills comparison page, README banner and icon.

## [0.1.0] - 2026-10-14
- 20 Blender 5.2 skills for AI agents (Claude Code, Codex, OpenCode, Gemini CLI, Copilot, Cursor).
- 26 tested scripts (MCP + headless): QA, baking, UV/texel density, retopo, LODs, export presets, Rigify, skinning, animation bake, GN builder, render, lookdev, simulation, batch.
- Installers for every agent, Claude Code plugin/marketplace, validator, headless test suite, CI.
