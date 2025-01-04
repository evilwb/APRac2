#!/bin/bash

##
# This script takes care of bundling the apworld.
#
# Arguments:
# * $1: Can be "clean" to clean the build environment.
#
# Environment:
# * TAG:
#     A string used to tag the bundle name
#     eg: "v1.1.1" will name the bundle "rac2_apworld-v1.1.1"
#     (default: current date and time)
##

set -eo pipefail
shopt -s globstar

CWD="$(dirname $(realpath $0))"
REQS=("zip" "rsync" "pip")
SUPPORTED_PLATFORMS=("win_amd64" "manylinux_2_17_x86_64")
PYTHON_VERSIONS=("3.10" "3.11" "3.12")

##
# Make sure all the required utilities are installed.
##
function pre_flight() {
    local bad="0"
    for r in ${reqs[@]}; do
        if ! command -v $r > /dev/null; then
            echo "!=> Unable to locate the '${r}' utility in \$PATH. Make sure it is installed."
            bad="1"
        fi
    done

    [ "${bad}" = "1" ] && exit 1 ||:
}

##
# Generate the `lib` folder within the target directory.
# Uses the `requirements.txt` file of the project to get every dependencies and copy them over.
# Uses `requirements.ignore` to specify which files not to copy over from within each of the requirements.
##
function get_deps() {
    local platform="$1" version="$2" requirements_file="$3" to="$4"
    echo "=> Bundle requirements for ${platform}"

    # Fetch the libraries binary files for the specified platform.
    echo "  -> Fetch requirements"
    pip install \
        --target ${to}/${platform}-${version} \
        --platform ${platform} \
        --python-version ${version} \
        --only-binary=:all: \
        --requirement ${requirements_file}


    # This is for the `.dist-info` folder, which contains the metadata of the mod.
    # We just copy over the license file into the main library folder
    echo "  -> Processing metadata"
    for folder in ${to}/${platform}-${version}/*.dist-info; do
        local dir="$(basename ${folder} | cut -d '-' -f 1)"
        cp --verbose "${folder}/LICENSE" "${folder}/../${dir}/" ||:
        rm --force --recursive ${folder}
    done

    # Go though each of the downloaded libraries and copy the relevant parts.
    echo "  -> Transfer requirements to bundle"
    for folder in ${to}/${platform}-${version}/*; do
        echo "    - Processing: ${folder}"

        # The actual code of the library.
        local dir="$(basename ${folder})"
        mkdir -p ${to}/${dir}
        rsync \
            --progress \
            --recursive \
            --prune-empty-dirs \
            --exclude-from="${CWD}/requirements.ignore" \
            "${folder}/" "${to}/${dir}"
    done

    echo "  -> Cleaning"
    rm --force --recursive ${to}/${platform}-${version}
}

##
# Create the `apworld` file used by Archipelago.
#
# Arguments:
# * $1: project root
# * $2: destination directory
##
function mk_apworld() {
    local root="$1" destdir="$2"
    echo "=> Bundling apworld"
    echo "From: ${root}"
    echo "To: ${destdir}"
    mkdir --parents "${destdir}/rac2"
    rsync --progress \
        --recursive \
        --prune-empty-dirs \
        --exclude-from="${CWD}/apworld.ignore" \
        "${root}/" "${destdir}/rac2"

    echo "${tag}" > "${destdir}/rac2/version.txt"

    # If this already exists then ovewrite it
#    rm -rf "${destdir}/rac2/lib"
#    mv "${destdir}/lib/pcsx2_interface" "${destdir}"
    pushd "${destdir}"
    zip -9r "rac2.apworld" "rac2"
    popd

    rm --force --recursive "${destdir}/rac2"
}

##
# Copy static data into the destination directory.
##
function cp_data() {
    local root="$1" destdir="$2"
    echo "=> Copying over the extra data"
    cp --verbose ${root}/LICENSE.md ${destdir}
    cp --verbose ${root}/README.md ${destdir}
    cp --verbose "${root}/Ratchet & Clank 2.yaml" ${destdir}
}

##
# Create the final bundled archive.
#
# Arguments:
# * $1: The location from where the archive is created.
# * $2: The path of the output archive.
##
function bundle() {
    local from="$1" out="$2"
    echo "=> Finalize bundle"
    [ -f "${out}" ] && rm ${out} ||:
    pushd "${from}"
    zip -9r "${out}" "."
    popd
}

##
# Main entry point.
##
function main() {
    pre_flight

    local target_path="${CWD}/target"
    local bundle_base="rac2_apworld"
    mkdir --parents ${target_path}

    case "$1" in
    # Clean the build environment.
    clean)
        find "${target_path}" \
            -depth \
            -type d \
            -name "${bundle_base}-*" \
            -exec rm --force --recursive --verbose {} \;
        ;;

    # Create the release bundle.
    *)
        local tag="${TAG:-$(date '+%Y-%m-%d_%H%M')}"
        local project="$(realpath ${CWD}/..)"
        local bundle="${bundle_base}-${tag}"
        local destdir="${target_path}/${bundle}"

#        for platform in "${SUPPORTED_PLATFORMS[@]}"; do
#            for version in "${PYTHON_VERSIONS[@]}"; do
#              local requirements_file="${project}/requirements.txt"
#              get_deps "${platform}" "${version}" ${requirements_file} "${destdir}"
#              # copy deps to project folder as well for local dev
#              cp -r "${destdir}/pcsx2_interface" "${project}/lib"
#            done
#        done

        mk_apworld "${project}" "${destdir}"
        cp_data "${project}" "${destdir}"
        bundle "${destdir}" "${target_path}/${bundle}.zip"
        echo "! Bundle finalized as ${target_path}/${bundle}.zip"
        ;;
    esac
}
main "$@"
