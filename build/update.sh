#!/bin/bash -e

if [[ ! $1 ]]; then
    echo "$(basename $0): Update dx-toolkit to a specified version."
    echo "Usage: $(basename $0) version [build_target_name]"
    exit 1
fi

new_version=$1
build_target_name=$2
build_dir=$(dirname $0)

function cleanup() {
    echo "$(basename $0): Unable to update to version ${new_version} $@"
}

trap cleanup ERR

if [[ $build_target_name == "" ]]; then
    if [[ -f "${build_dir}/info/target" ]]; then
        build_target_name=$(cat "${build_dir}/info/target")
    else
        echo "$(basename $0): Unable to determine which package to download" 1>&2
        false
    fi
fi

if [[ -f "${build_dir}/info/version" ]]; then
    current_version=$(cat "${build_dir}/info/version")
else
    echo "$(basename $0): Unable to determine current package version" 1>&2
    false
fi

pkg_name="dx-toolkit-v${new_version}-${build_target_name}.tar.gz"
echo "Downloading $pkg_name..."
(cd "$build_dir"; curl -O "http://wiki.dnanexus.com/images/files/${pkg_name}")

echo "Unpacking $pkg_name..."
tar -C "$build_dir" -xzf "${build_dir}/${pkg_name}"

echo "Backing up version ${current_version}..."
rm -rf "${build_dir}/${current_version}" 
mkdir "${build_dir}/${current_version}"
for i in "${build_dir}"/../*; do
    if [[ $(basename "$i") != "build" ]]; then
        mv "$i" "${build_dir}/${current_version}/"
    fi
done

echo "Moving version ${new_version} into place..."
for i in "${build_dir}"/dx-toolkit/*; do
    if [[ $(basename "$i") != "build" ]]; then
        mv "$i" "${build_dir}/../"
    fi
done

rm -rf "${build_dir}/dx-toolkit"
echo "${new_version}" > "${build_dir}/info/version"

echo "$(basename $0): Updated to version ${new_version}. Previous version saved in ${build_dir}/${current_version}."