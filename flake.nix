{
  description = "A Typst package for chordsheets";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";
  };

  outputs =
    { flake-parts, ... }@inputs:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      perSystem =
        { pkgs, ... }:
        let
          manifest = (fromTOML (builtins.readFile ./typst.toml));
        in
        {
          devShells.default = pkgs.mkShell {
            packages = [
              pkgs.typst
              pkgs.tinymist
            ];

            env = {
              TYPST_PACKAGE_PATH = ".typst-local";
            };

            shellHook = ''
              mkdir -p .typst-local/local/chordish
              ln -sfn "$PWD" .typst-local/local/chordish/${manifest.package.version}
            '';
          };
        };
    };
}
