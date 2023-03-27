let
  sourcesTarball = fetchTarball "https://github.com/mutwo-org/mutwo-nix/archive/refs/heads/main.tar.gz";
  mutwo-music = import (sourcesTarball + "/mutwo.music/default.nix") {};
  mutwo-music-local = mutwo-music.overrideAttrs (
    finalAttrs: previousAttrs: {
       src = ./.;
    }
  );
in
  mutwo-music-local
