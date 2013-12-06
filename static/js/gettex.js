!function gettex (str) {
	var totex = encodeURI(str);
	var purl = new URL("http://www.sciweavers.org/tex2img.php?eq=", totex);
	return purl;
}