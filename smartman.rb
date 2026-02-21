class Smartman < Formula
  desc "Modern Linux man page enhancer with AI explanations and TUI"
  homepage "https://github.com/ambaskaryash/smartman-cli"
  url "https://github.com/ambaskaryash/smartman-cli/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "REPLACE_WITH_ACTUAL_SHA256_AFTER_RELEASE"
  license "MIT"

  depends_on "python@3.12"
  depends_on "pipx"

  def install
    system "pipx", "install", "--force", "."
  end

  test do
    system "#{bin}/smartman", "--version"
  end
end
