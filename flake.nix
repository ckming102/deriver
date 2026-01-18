{
  description = "deriver dev shell (deps from pyproject.toml via pyproject-nix)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

    pyproject-nix.url = "github:pyproject-nix/pyproject.nix";
    pyproject-nix.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { nixpkgs, pyproject-nix, ... }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" ];

      project = pyproject-nix.lib.project.loadPyproject {
        projectRoot = ./.;
      };
    in
    {
      devShells = nixpkgs.lib.genAttrs systems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
          python = pkgs.python3;

          pythonEnv =
            python.withPackages (project.renderers.withPackages { inherit python; });
        in
        {
          default = pkgs.mkShell {
            packages = [ pythonEnv ];

            # deriver is in src/derive, so make src importable
            PYTHONPATH = "src";
          };
        });
    };
}
