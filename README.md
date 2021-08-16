## Description
FolderDig (FolderDigest) is a forensic analysis tool used for taking file integrity measurements.

## Operations
FolderDig comes with a few key features:
1. Compute the cryptographic tag of a file system
2. Compute the cryptographic tag of every node in a file system
3. Generate an integrity proof of a file system
4. Verify these proofs and gain assurance of integrity of the filesystem's contents
5. Pinpoint the files or subtrees that have been modified

## Usage
    $ python fdig.py src/
    $ 784e7c1afc469ccfa8f7c52c8080c5a9b484da4b0242dee915fb24e8f5808e18
