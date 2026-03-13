class Smartman < Formula
  include Language::Python::Virtualenv

  desc "Modern Linux man page enhancer with AI explanations and TUI"
  homepage "https://github.com/ambaskaryash/smartman-cli"
  url "https://github.com/ambaskaryash/smartman-cli/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "8af6f43faf0c47f000f57343baebb9125bd011c962474433ce782edeee551da4"
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_install_with_resources
  end

  test do
    system "#{bin}/smartman", "--version"
  end
end
