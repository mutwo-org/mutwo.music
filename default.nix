with import <nixpkgs> {};
with pkgs.python310Packages;

let

  mutwo-core-archive = builtins.fetchTarball "https://github.com/mutwo-org/mutwo.core/archive/28a13e348876fa07929f5fd4f3953fee624c255c.tar.gz";
  mutwo-core = import (mutwo-core-archive + "/default.nix");

  mutwo-common-archive = builtins.fetchTarball "https://github.com/mutwo-org/mutwo.common/archive/346f8ccbd85ce58904cd62f6f9a16ca08436736f.tar.gz";
  mutwo-common = import (mutwo-common-archive + "/default.nix");

  panphon = pkgs.python310Packages.buildPythonPackage rec {
    name = "panphon";
    src = fetchFromGitHub {
      owner = "dmort27";
      repo = name;
      rev = "43389ed78b405412b3eee448875969de7a18b78a";
      sha256 = "sha256-HYdqoAYkbgMLbuWoSjUGKArkfvLEQmILVdJvvo3N9mg=";
    };
    propagatedBuildInputs = [ 
        flite
        python310Packages.unicodecsv
        python310Packages.pyyaml
        python310Packages.regex
        python310Packages.editdistance
        python310Packages.numpy
        python310Packages.munkres
        python310Packages.setuptools
    ];
  };

  epitran = pkgs.python310Packages.buildPythonPackage rec {
    name = "epitran";
    src = fetchFromGitHub {
      owner = "dmort27";
      repo = name;
      rev = "a30eef02327af0f5f1d161fa427f9e56545b3b64";
      sha256 = "sha256-AH4q8J5oMaUVJ559qe/ZlJXlCcGdxWnxMhnZKCH5Rlk=";
    };
    propagatedBuildInputs = [ 
        flite
        python310Packages.setuptools
        python310Packages.regex
        python310Packages.marisa-trie
        python310Packages.requests
        panphon
    ];
  };

  gradient-free-optimizers = pkgs.python310Packages.buildPythonPackage rec {
    name = "gradient-free-optimizers";
    src = fetchFromGitHub {
      owner = "SimonBlanke";
      repo = "Gradient-Free-Optimizers";
      rev = "5c025aeccf5c5ed1f51765c98e3b1b81012312cb";
      sha256 = "sha256-vClFUqPOOSrnXtce6+JLVRUqW1A7EHYbxn0EGRoW7r4=";
    };
    doCheck = false;
    propagatedBuildInputs = [ 
        python310Packages.tqdm
        python310Packages.scipy
        python310Packages.numpy
        python310Packages.pandas
        python310Packages.scikit-learn
    ];
  };

in

  buildPythonPackage rec {
    name = "mutwo.music";
    src = fetchFromGitHub {
      owner = "mutwo-org";
      repo = name;
      rev = "da20fa31796ed9698dbdcf0d4e1e4fa9d807973c";
      sha256 = "sha256-c8jgo0rX7AEK315/W3ElPkEv85xW22ypFDmzertI9/Y=";
    };
    checkInputs = [
      python310Packages.pytest
    ];
    propagatedBuildInputs = [ 
      python310Packages.numpy
      python310Packages.scipy
      python310Packages.sympy
      gradient-free-optimizers
      mutwo-core
      mutwo-common
      epitran
    ];
    checkPhase = ''
      runHook preCheck
      pytest
      runHook postCheck
    '';
    doCheck = true;
  }
