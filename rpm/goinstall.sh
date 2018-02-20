#!/bin/sh -x

prefix=''
gopath=/usr/share/gocode
goipps=''
ignore_dirs=''
ignore_trees=''
ignore_regex=''
file_list='devel.file-list'
exts_list=''
ipprefix=''

while [ $# -gt 0 ] ; do
  case $1 in
    -h|--help)        usage ;;
    -p|--prefix)      prefix=$(realpath -sm "$2") ; shift;;
    --ignore-dirs)    ignore_dirs="$2" ; shift;;
    -R|--ignore-trees)   ignore_trees="$2" ; shift;;
    -r|--ignore-regex)   ignore_regex="$2" ; shift;;
    -f|--file-list)   file_list="$2" ; shift;;
    -e|--extensions)  exts_list="$2" ; shift;;
    -i|--ipprefix)    ipprefix="$2" ; shift;;
    (--)              shift; break;;
    (-*)              echo "$0: error - unrecognized option $1" >&2; exit 3;;
    (*)               break;;
  esac
  shift
done

install -m 0755 -vd "${prefix}/${gopath}/src"
# create symlink
install -m 0755 -vd "$(dirname $PWD/_build/src/${ipprefix})"
ln -fs "$PWD" "$PWD/_build/src/${ipprefix}"

installfile() {
	file=${1}
	[[ ${file} == $PWD/_build/src/${ipprefix} ]] && continue
	file="${file##$PWD/_build/src/${ipprefix}/}"
	[[ -d "${file}" && ! -L "${file}" ]] && srcdir="${file}" || srcdir=$(dirname "${file}")
	destdir="${prefix}/${gopath}/src/${ipprefix}/${srcdir}"
	destdir="${destdir%/.}"
	dir="${destdir}"
	dirs=(${prefix}/${gopath}/src/${ipprefix})
	while [[ ! -e "${dir}" ]] && [[ "${dir##${prefix}${gopath}/src/}" != "${ipprefix}" ]] ; do
	  dirs=("$dir" "${dirs[@]}")
	  dir=$(dirname "${dir}")
	done
	for dir in "${dirs[@]}" ; do
	  install -m 0755 -vd "${dir}"
	  if $(echo "${dir}" | grep -q "^${prefix}/${gopath}/src/${ipprefix}") ; then
	    touch -r             ".${dir#${prefix}/${gopath}/src/${ipprefix}}" "${dir}"
	  fi
	  echo "%%dir \"${dir#${prefix}}\"" >> ${file_list}
	done
	if [[ -L "$file" ]] ; then
	  ln -s $(readlink "${file}") "${destdir}/$(basename ${file})"
	  touch -h      -r "${file}"  "${destdir}/$(basename ${file})"
	fi
	[[ -f "$file" && ! -L "$file" ]] && install -m 0644 -vp  "${file}" "${destdir}/"
	[[ -f "$file" ||   -L "$file" ]] && echo "${gopath}/src/${ipprefix}/${file}" >> ${file_list} || :
}

# Process automatically detected resources
for file in $(\
GOPATH=$PWD/_build golist \
	--to-install \
	--package-path ${ipprefix} \
	--with-extensions "${exts_list}" \
	--ignore-dirs  "${ignore_dirs}" \
	--ignore-trees "${ignore_trees}" \
	--ignore-regex "${ignore_regex}" \
); do
	installfile ${file}
done
# Process user specified resources
for file in $@; do
	if [[ -d "${file}" ]]; then
		echo "${gopath}/src/${ipprefix}/${file}" >> ${file_list}
		install -m 0755 -vd ${prefix}/${gopath}/src/${ipprefix}/$file
		cp -r $file/* ${prefix}/${gopath}/src/${ipprefix}/$file/.
		continue
	fi
	installfile ${file}
done

sort -u -o ${file_list} ${file_list}

