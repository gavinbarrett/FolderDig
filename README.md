## Description
FolderDig (FolderDigest) is a forensic analysis tool used for taking file integrity measurements.

## Operations
FolderDig comes with a few key features:
1. Compute the cryptographic tag of a file system
2. Compute the cryptographic tag of every node in a file system
3. Generate an integrity proof of a file system
4. Verify these proofs and gain assurance of integrity of the filesystem's contents and pinpoint the files or subtrees that have been modified

## Filesystem Tagging
```bash
$ python fdig.py src/
2c446dd8a80ddb667efe5cd4f7b205fee02e9077208b0e2ff4451040c1c533b1	src
$
```

## Full Filesystem Tagging
Use either the `-f` or the `--full` flag
```bash
$ python fdig.py src/ -f
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855:	src/__init__.py
57521d74db6f179dbfeff1c220246898393833232beb06cfbdca0a02daa0507e:	src/prove.py
f2a041a5501cf6dc2bce6ce8ba1e1010915540fbd5ff8409af623b471ca5ea14:	src/parser.py
0590468a2119a010ea0a660627b4553ff1646900083b7114f405252bb99931ec:	src/verify.py
de24751f59cf181977e324a70a3567e2377716e9924e7fa7811bdc608a967579:	src/checksum.py
846dea2d7d387d60fab18b56abacce7bfb35b5b351bd34eb652650812de3510c:	src/__pycache__/prove.cpython-39.pyc
d1c600f61fac04a8b7a430a2cc651a2334aa30f483aa2419689ee3313bee8e9b:	src/__pycache__/verify.cpython-39.pyc
635a8aa26fd2bf05c11aa48ef41696b3058e3a020cdda2af4483eade1c204d6d:	src/__pycache__/checksum.cpython-39.pyc
396f6f668487cdced7344bce54da6fb156ca33384ab07d77da9557d5a770773e:	src/__pycache__/parser.cpython-39.pyc
b5143898ee04acecd5648864f16386b96beb8e63d1bb9aa51652dd3eebe7538d:	src/__pycache__/__init__.cpython-39.pyc
72a11df2507bda576753d9ba9f74ec5679c2dc353d13ee28af159b1ed8e58f6a:	src/__pycache__
2c446dd8a80ddb667efe5cd4f7b205fee02e9077208b0e2ff4451040c1c533b1:	src
$
```

## Generate Integrity Proof
Use the `-p` flag to generate a proof. You also need to provide the `-o` or `--output` flags along with an output file path, as well as the `-t` or `--tag` flag along with a tag that exists along the path you want to verify. Passing in this tag allows the user to generate a space-efficient proof specifically for the data that exists at and above the tag's corresponding node in the filesystem.

```bash
$ python fdig.py -p -o proof.json -t 846dea2d7d387d60fab18b56abacce7bfb35b5b351bd34eb652650812de3510c
$
```

You should now have a file in the output directory named `proof.json` containing a JSON encoded proof of your tag's place within your filesystem.

## Verify Integrity Proof
Use the `-v` flag to verify a proof. You also need to provide the `-i` or `--input` flag along with an input file path, as well as the `-t` or `--tag` flag along with a tag that exists along the path you want to verify. The program will raise an error if it finds a node (either a file or directory) in your filesystem that does not match the tag present in the proof. Otherwise, it will print a success message:

`Filesystem integrity maintained.`

```bash
$ python fdig.py -v -i proof.json -t 846dea2d7d387d60fab18b56abacce7bfb35b5b351bd34eb652650812de3510c
Filesystem integrity maintained.
$
```
