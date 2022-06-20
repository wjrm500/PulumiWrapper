document.getElementById('content-type').addEventListener(
    'change',
    function() {
        var contentType = this.value;
        if (contentType == 'text') {
            document.getElementById('content-text').style.display = 'block';
            document.getElementById('content-url').style.display = 'none';
        }
        if (contentType == 'url') {
            document.getElementById('content-text').style.display = 'none';
            document.getElementById('content-url').style.display = 'block';
        }
    }
);