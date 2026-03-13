class Smartman < Formula
  include Language::Python::Virtualenv

  desc "Modern Linux man page enhancer with AI explanations and TUI"
  homepage "https://github.com/ambaskaryash/smartman-cli"
  url "https://github.com/ambaskaryash/smartman-cli/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "b4c8bfa48f8a8c311b39ae1cbfb90c49cc3856a12d42bfb185e0675e0bfa0bc8"
  license "MIT"

  depends_on "python@3.12"

  def install
    virtualenv_install_with_resources
  end

  test do
    system "#{bin}/smartman", "--version"
  end
end
