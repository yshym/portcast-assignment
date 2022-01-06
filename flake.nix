{
  description = "Portcast Assignmement";

  inputs = {
    nixpkgs.url = "github:yevhenshymotiuk/nixpkgs/release-21.05";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let pkgs = nixpkgs.legacyPackages.${system};
      in {
        devShell = with pkgs;
          mkShell {
            nativeBuildInputs =
              [ chromedriver chromium poetry postgresql python36 ];
          };
      });
}
