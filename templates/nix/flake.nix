{
  description = "Hermetic development environment for swe-skills projects";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    systems.url = "github:nix-systems/default";
  };

  outputs = { self, nixpkgs, systems }:
    let
      eachSystem = nixpkgs.lib.genAttrs (import systems);
    in
    {
      devShells = eachSystem (system:
        let
          pkgs = import nixpkgs { inherit system; };
        in
        {
          default = pkgs.mkShell {
            packages = with pkgs; [
              # Core Python & workspace tooling
              python312
              uv

              # System compilation & native seams
              pkg-config
              openssl
              git
            ];

            shellHook = ''
              # Keep virtualenvs local to project root
              export UV_PROJECT_ENVIRONMENT="''${PWD}/.venv"
              export PYTHONUNBUFFERED=1

              # Inform agent and user of active hermetic tier
              if [ -z "$DIRENV_IN_ENVRC" ]; then
                echo "❄️  Hermetic Nix devShell active (Tier 1). Native toolchain wrapped."
              fi
            '';
          };
        }
      );
    };
}
