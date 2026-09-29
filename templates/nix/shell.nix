# Legacy non-flakes fallback shell
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = with pkgs; [
    python312
    uv
    pkg-config
    openssl
    git
  ];

  shellHook = ''
    export UV_PROJECT_ENVIRONMENT="''${PWD}/.venv"
    export PYTHONUNBUFFERED=1
    echo "❄️  Nix shell active (Tier 1 legacy). Native toolchain wrapped."
  '';
}
