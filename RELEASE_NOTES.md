# Clever v1.0.1 – Documentation updates

This release focuses on documentation clarity and usability.

Changes
- Clarified that “clr” is the short alias for “clever” and that the installer creates /usr/local/bin/clr
- Added a new section listing mainstream tools and installation commands (brew/apt/dnf/yum/pacman/zypper/choco/winget)
- Fixed the Chinese README title to a proper Chinese title and noted the clr alias

Why this matters
- Many users prefer the short alias “clr” in day-to-day usage; documenting it avoids confusion
- Quick-install snippets help users get common tools ready on their systems

Getting started
- Install via script:
  - chmod +x install.sh && ./install.sh
- Or run directly:
  - python3 src/__init__.py --help

Notes
- Some tools (e.g., Docker) may require post-install steps or a restart; see your distribution’s docs for details.
