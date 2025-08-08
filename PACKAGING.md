# Packaging guide for Clever

This document provides quick-start templates and notes for distributing Clever via popular package managers.

Note: Adjust metadata/URLs to match your repository and license.

## Homebrew (Formula template)

Create a tap repo (recommended): github.com/<you>/homebrew-tap

Example Formula (Formula/clever.rb):

class Clever < Formula
  desc "Popular command query tool (bilingual)"
  homepage "https://github.com/jasonwong1991/Clever"
  url "https://github.com/jasonwong1991/Clever/releases/download/v1.0.1/clever-v1.0.1.tar.gz"
  sha256 "<SHA256_OF_TARBALL>"
  license "MIT"

  depends_on "python@3.12" # adjust as needed

  def install
    # Install sources under libexec, create wrapper scripts in bin
    libexec.install "src"
    (bin/"clever").write <<~EOS
      #!/bin/bash
      cd "${HOMEBREW_PREFIX}/opt/clever/libexec"
      exec python3 src/__init__.py "$@"
    EOS
    chmod 0755, bin/"clever"

    (bin/"clr").write <<~EOS
      #!/bin/bash
      cd "${HOMEBREW_PREFIX}/opt/clever/libexec"
      exec python3 src/__init__.py "$@"
    EOS
    chmod 0755, bin/"clr"
  end

  test do
    system "#{bin}/clever", "--help"
  end
end

Usage:
- brew tap <you>/tap
- brew install clever

Update url/sha256 for each release.

## Debian/Ubuntu (apt) quick notes

Goal: produce a .deb that installs sources under /usr/lib/clever and creates /usr/bin/clever and /usr/bin/clr wrappers.

Directory layout example (debian/):
- debian/control
- debian/compat (if using debhelper < 13)
- debian/rules
- debian/install
- debian/copyright
- debian/changelog

Example snippets:

debian/control:
Package: clever
Version: 1.0.1
Section: utils
Priority: optional
Maintainer: Your Name <you@example.com>
Architecture: all
Depends: python3, ${misc:Depends}
Description: Popular command query tool (bilingual)
 A modern command query tool with bilingual support and data-code separation.

debian/install:
src usr/lib/clever
scripts/clever.sh usr/bin
scripts/clr.sh usr/bin

(Provide scripts/clever.sh and scripts/clr.sh as simple wrappers invoking python3 /usr/lib/clever/src/__init__.py "$@")

Build commands (modern dh):
- dpkg-buildpackage -us -uc -b

## Arch (PKGBUILD) sketch

- pkgname=clever
- pkgver=1.0.1
- source=("https://github.com/jasonwong1991/Clever/releases/download/v${pkgver}/clever-v${pkgver}.tar.gz")
- sha256sums=("<SHA256_OF_TARBALL>")
- depends=(python)

package() {
  install -d "$pkgdir/usr/lib/clever"
  cp -r src "$pkgdir/usr/lib/clever/"
  install -d "$pkgdir/usr/bin"
  printf '#!/bin/bash\ncd /usr/lib/clever\nexec python3 src/__init__.py "$@"\n' > "$pkgdir/usr/bin/clever"
  chmod 0755 "$pkgdir/usr/bin/clever"
  printf '#!/bin/bash\ncd /usr/lib/clever\nexec python3 src/__init__.py "$@"\n' > "$pkgdir/usr/bin/clr"
  chmod 0755 "$pkgdir/usr/bin/clr"
}

## openSUSE/Fedora (RPM) notes

- Use %files to place sources under /usr/lib/clever and create two wrapper scripts under /usr/bin.
- Add Requires: python3

## Windows (Chocolatey) notes

- Package installs files to tools\ and creates clever.cmd and clr.cmd that run: python src\__init__.py %*
- Specify dependencies (python) in nuspec.

## Checksums

For each uploaded asset, publish SHA256 sums and reference them in packaging.
- clever-v1.0.1.tar.gz: c18dc8aa6f1b3f58e5c963c7c6608e4ca943719cea1dc4b765293a486377d0d3
- clever-v1.0.1.zip: d9aedd8bef85c09b269910968e7d504c34213fdbbd46ea736a58f48d89fb6725

