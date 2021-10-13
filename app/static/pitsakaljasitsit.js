$(document).ready(function () {
    $('input[type=radio][name=holi]').change(function () {
        if (document.getElementById('holi-0').checked) {
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
