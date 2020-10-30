$(document).ready(function () {
    $('input[type=select][name=aika]').change(function() {
        if (document.getElementById('aika').value == '1800') {
            $('#huone1800').show()
            $('#huone1930').hide()
        } 
        else if (document.getElementById('aika').value == '1930') {
            $('#huone1800').hide()
            $('#huone1930').show()
        }
        else {
            $('#huone1800').hide()
            $('#huone1930').hide()
        }
    });
});