
function formatBytes(bytes) {
    if (bytes < 1024) return bytes + " Bytes";
    else if (bytes < 1048576) return (bytes / 1024).toFixed(2) + " KB";
    else if (bytes < 1073741824) return (bytes / 1048576).toFixed(2) + " MB";
    else return (bytes / 1073741824).toFixed(2) + " GB";
}

function GetFileSize() {
    document.getElementById('fp').innerHTML = "";
    var fi = document.getElementById('file');

    var list_colA = [];
    var list_colB = [];

    if (fi.files.length > 0) {

        for (var i = 0; i <= fi.files.length - 1; i++) {
            var chkEven = i %2;
            var fsize = fi.files.item(i).size;                  // file name size
            var fname = fi.files.item(i).name;                  // file name
            var name_len = fi.files.item(i).name.length;        // file name length

            if (name_len >= 38) {
                fname = fname.substr(0,38);
            }

            document.getElementById('fp').innerHTML = document.getElementById('fp').innerHTML +
                    '<br /> ' + '<b style=color:#000;>' +
                    formatBytes(fsize) +' ' +'</b>' + fname;

            if (chkEven) {
                list_colA.push(fname);
            }
            else {
                list_colB.push(fname);
            }
        }
    }
}
