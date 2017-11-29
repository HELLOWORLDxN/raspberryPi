dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
python3 -m compileall "$dir"
dst="/usr/bin/autofan"
echo 'dst' $dst
echo 'dir' $dir
if [ ! -d "$dst" ]; then
	mkdir "$dst"
fi
if [ ! -f "$dir/autofan.pid" ]; then
	touch "$dir/autofan.pid"
fi
cp -r $dir/* /usr/bin/autofan
cp -r $dir/service/autofan.service /lib/systemd/system/
