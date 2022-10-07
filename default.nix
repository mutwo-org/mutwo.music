with import <nixpkgs> {};
with pkgs.python3Packages;

let

  mutwo-core-archive = builtins.fetchTarball "https://github.com/mutwo-org/mutwo.core/archive/97aea97f996973955889630c437ceaea405ea0a7.tar.gz";
  mutwo-core = import (mutwo-core-archive + "/default.nix");

  mutwo-common-archive = builtins.fetchTarball "https://github.com/mutwo-org/mutwo.common/archive/9a0f12a72b5b6224b8a55227273a4fe6870c6300.tar.gz";
  mutwo-common = import (mutwo-common-archive + "/default.nix");

  panphon = pkgs.python39Packages.buildPythonPackage rec {
    name = "panphon";
    src = fetchFromGitHub {
      owner = "dmort27";
      repo = name;
      rev = "43389ed78b405412b3eee448875969de7a18b78a";
      sha256 = "sha256-HYdqoAYkbgMLbuWoSjUGKArkfvLEQmILVdJvvo3N9mg=";
    };
    propagatedBuildInputs = [ 
        flite
        python39Packages.unicodecsv
        python39Packages.pyyaml
        python39Packages.regex
        python39Packages.editdistance
        python39Packages.numpy
        python39Packages.munkres
        python39Packages.setuptools
    ];
  };

  epitran = pkgs.python39Packages.buildPythonPackage rec {
    name = "epitran";
    src = fetchFromGitHub {
      owner = "dmort27";
      repo = name;
      rev = "a30eef02327af0f5f1d161fa427f9e56545b3b64";
      sha256 = "sha256-AH4q8J5oMaUVJ559qe/ZlJXlCcGdxWnxMhnZKCH5Rlk=";
    };
    propagatedBuildInputs = [ 
        flite
        python39Packages.setuptools
        python39Packages.regex
        python39Packages.marisa-trie
        python39Packages.requests
        panphon
    ];
  };

  gradient-free-optimizers = pkgs.python39Packages.buildPythonPackage rec {
    name = "gradient-free-optimizers";
    src = fetchFromGitHub {
      owner = "SimonBlanke";
      repo = "Gradient-Free-Optimizers";
      rev = "5c025aeccf5c5ed1f51765c98e3b1b81012312cb";
      sha256 = "sha256-vClFUqPOOSrnXtce6+JLVRUqW1A7EHYbxn0EGRoW7r4=";
    };
    doCheck = false;
    propagatedBuildInputs = [ 
        python39Packages.tqdm
        python39Packages.scipy
        python39Packages.numpy
        python39Packages.pandas
        python39Packages.scikit-learn
    ];
  };

in

  buildPythonPackage rec {
    name = "mutwo.music";
    src = fetchFromGitHub {
      owner = "mutwo-org";
      repo = name;
      rev = "b517933d17815f88f4c76deb7baa351d3470cee3";
      sha256 = "sha256-s6F/XbK1P4uWu4yrpfMECkhM3/7d0Rvbwzoy1M/Pa50=";
    };
    propagatedBuildInputs = [ 
      python39Packages.numpy
      python39Packages.scipy
      python39Packages.sympy
      gradient-free-optimizers
      mutwo-core
      mutwo-common
      epitran
    ];
    doCheck = true;
  }
