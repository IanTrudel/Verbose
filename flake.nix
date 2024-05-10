{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
      in
      {
        packages.default = pkgs.mkShell {
          buildInputs = [
            pkgs.python311Packages.pygobject3
            pkgs.python311Packages.termcolor
            pkgs.python311Packages.requests
            (pkgs.python311Packages.playsound.overrideAttrs(old: {
              version = "1.2.2";

              src = pkgs.fetchFromGitHub {
                owner = "TaylorSMarks";
                repo = "playsound";
                rev = "907f1fe73375a2156f7e0900c4b42c0a60fa1d00";
                sha256 = "1fh3m115h0c57lj2pfhhqhmsh5awzblb7csi1xc5a6f6slhl059k";
              };
            }))
            pkgs.gst_all_1.gstreamer
            pkgs.gst_all_1.gst-plugins-base
            pkgs.gst_all_1.gst-plugins-good
          ];
        };
      }
    );
}
# nixpkgs#python311Packages.pygobject3 nixpkgs#python311Packages.termcolor nixpkgs#python311Packages.requests nixpkgs/d7c9582ba8f7e953218e239fcca3145fb31cd79a#python311Packages.playsound
