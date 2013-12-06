// Let's an <a id="myAnchor" href="https://developer.mozilla.org/en-US/URLUtils.href"> element be in the document


function getLatex (str) {
	var anchor = document.getElementByID("myAnchor");
    var result = anchor.href; // Returns:'https://developer.mozilla.org/en-US/URLUtils.href'
    return encodeURI(str)
}