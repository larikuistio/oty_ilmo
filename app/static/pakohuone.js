$(document).ready(function () {
    $('input[type=radio][name=aika]').change(function() {
        if (document.getElementById('aika-0').checked) {
            $('#huone1800').show()
            $('#huone1930').hide()
        } 
        else if (document.getElementById('aika-1').checked) {
            $('#huone1800').hide()
            $('#huone1930').show()
        }
        else {
            $('#huone1800').hide()
            $('#huone1930').hide()
        }
    });

    var varatut = varatut.toJSON();
});