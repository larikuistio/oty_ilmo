$(document).ready(function () {
    $("#alkoholi-1").prop("checked", true);
});


$(document).ready(function () {
    $('input[type=radio][name=alkoholi]').change(function () {
        if (document.getElementById('alkoholi-0').checked) {
            $('#mieto').show();
            $('#vakeva').show();
            $('#viini').show();
        }
        else {
            $('#mieto').hide();
            $('#vakeva').hide();
            $('#viini').hide();
        }
    });
});
