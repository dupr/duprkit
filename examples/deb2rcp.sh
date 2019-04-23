#!/bin/sh
set -e

# Convert existing debian package into .rcp (HFT inside)
# Usage: $0 <pkgname>

apt source ${1}
cd ${1}*/; hft -f debian/ -o ../${1}.hft; cd ..

# Generate the shell header
cat > ${1}.sh <<EOF
src="${1}"
description="${1}"
version="0"
section="utils"
license="Some Free Software License"
maintainer="Debian"
dk_get_source () {
	apt source ${1};
}
dk_prep_source () {
	ln -s \$(find . -maxdepth 1 -name "${1}*" -type d | head -n1) ${1}
	rm -rf \$src/debian
}
EOF

# create the rcp file
cat ${1}.sh ${1}.hft > ${1}.rcp
