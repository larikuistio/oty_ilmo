$(document).ready(function () {
    $('input[type=radio][name=aika]').change(function() {
        if (document.getElementById('aika-0').checked) {
            $('#huone1800').show();
            $('#huone1930').hide();
        } 
        else if (document.getElementById('aika-1').checked) {
            $('#huone1800').hide();
            $('#huone1930').show();
        }
        else {
            $('#huone1800').hide();
            $('#huone1930').hide();
        }
    });
    
    /*$('#huone1800-0').after('Pommi (Uusikatu)(varattu)');
    $('#huone1800-1').after('Kuolleen miehen saari (Uusikatu)(varattu)');
    $('#huone1800-2').after('Temppelin kirous (Uusikatu)(varattu)');
    $('#huone1800-3').after('Velhon perintö (Uusikatu)(varattu)');
    $('#huone1800-4').after('Murhamysteeri (Kajaaninkatu)(varattu)');
    $('#huone1800-5').after('Vankilapako (Kajaaninkatu)(varattu)');
    $('#huone1800-6').after('Professorin arvoitus (Kajaaninkatu)(varattu)');
    $('#huone1800-7').after('The SAW (Kirkkokatu)(varattu)');
    $('#huone1800-8').after('Alcatraz (Kirkkokatu)(varattu)');
    $('#huone1800-9').after('Matka maailman ympäri (Kirkkokatu)(varattu)');
    $('#huone1930-0').after('Pommi (Uusikatu)(varattu)');
    $('#huone1930-1').after('Kuolleen miehen saari (Uusikatu)(varattu)');
    $('#huone1930-2').after('Temppelin kirous (Uusikatu)(varattu)');
    $('#huone1930-3').after('Velhon perintö (Uusikatu)(varattu)');
    $('#huone1930-4').after('Murhamysteeri (Kajaaninkatu)(varattu)');
    $('#huone1930-5').after('Vankilapako (Kajaaninkatu)(varattu)');
    $('#huone1930-6').after('Professorin arvoitus (Kajaaninkatu)(varattu)');
    $('#huone1930-7').after('The SAW (Kirkkokatu)(varattu)');
    $('#huone1930-8').after('Alcatraz (Kirkkokatu)(varattu)');
    $('#huone1930-9').after('Matka maailman ympäri (Kirkkokatu)(varattu)');*/

    $.each(JSON.parse(varatut), function(i, item) {
        if(item[0] == "18:00") {
            if(item[1] == "Pommi (Uusikatu)") {
                $('#huone1800-0').after('Pommi (Uusikatu)(varattu)');
            } else {
                $('#huone1800-0').after('Pommi (Uusikatu)(vapaa)');
            }
            if(item[1] == "Kuolleen miehen saari (Uusikatu)") {
                $('#huone1800-1').after('Kuolleen miehen saari (Uusikatu)(varattu)');
            } else {
                $('#huone1800-1').after('Kuolleen miehen saari (Uusikatu)(vapaa)');
            }
            if(item[1] == "Temppelin kirous (Uusikatu)") {
                $('#huone1800-2').after('Temppelin kirous (Uusikatu)(varattu)');
            } else {
                $('#huone1800-2').after('Temppelin kirous (Uusikatu)(vapaa)');
            }
            if(item[1] == "Velhon perintö (Uusikatu)") {
                $('#huone1800-3').after('Velhon perintö (Uusikatu)(varattu)');
            } else {
                $('#huone1800-3').after('Velhon perintö (Uusikatu)(vapaa)');
            }
            if(item[1] == "Murhamysteeri (Kajaaninkatu)") {
                $('#huone1800-4').after('Murhamysteeri (Kajaaninkatu)(varattu)');
            } else {
                $('#huone1800-4').after('Murhamysteeri (Kajaaninkatu)(vapaa)');
            }
            if(item[1] == "Vankilapako (Kajaaninkatu)") {
                $('#huone1800-5').after('Vankilapako (Kajaaninkatu)(varattu)');
            } else {
                $('#huone1800-5').after('Vankilapako (Kajaaninkatu)(vapaa)');
            }
            if(item[1] == "Professorin arvoitus (Kajaaninkatu)") {
                $('#huone1800-6').after('Professorin arvoitus (Kajaaninkatu)(varattu)');
            } else {
                $('#huone1800-6').after('Professorin arvoitus (Kajaaninkatu)(vapaa)');
            }
            if(item[1] == "The SAW (Kirkkokatu)") {
                $('#huone1800-7').after('The SAW (Kirkkokatu)(varattu)');
            } else {
                $('#huone1800-7').after('The SAW (Kirkkokatu)(vapaa)');
            }
            if(item[1] == "Alcatraz (Kirkkokatu)") {
                $('#huone1800-8').after('Alcatraz (Kirkkokatu)(varattu)');
            } else {
                $('#huone1800-8').after('Alcatraz (Kirkkokatu)(vapaa)');
            }
            if(item[1] == "Matka maailman ympäri (Kirkkokatu)") {
                $('#huone1800-9').after('Matka maailman ympäri (Kirkkokatu)(varattu)');
            } else {
                $('#huone1800-9').after('Matka maailman ympäri (Kirkkokatu)(vapaa)');
            }
        } else if(item[0] == "19:30") {
            if(item[2] == "Pommi (Uusikatu)") {
                $('#huone1930-0').after('Pommi (Uusikatu)(varattu)');
            } else {
                $('#huone1930-0').after('Pommi (Uusikatu)(vapaa)');
            }
            if(item[2] == "Kuolleen miehen saari (Uusikatu)") {
                $('#huone1930-1').after('Kuolleen miehen saari (Uusikatu)(varattu)');
            } else {
                $('#huone1930-1').after('Kuolleen miehen saari (Uusikatu)(vapaa)');
            }
            if(item[2] == "Temppelin kirous (Uusikatu)") {
                $('#huone1930-2').after('Temppelin kirous (Uusikatu)(varattu)');
            } else {
                $('#huone1930-2').after('Temppelin kirous (Uusikatu)(vapaa)');
            }
            if(item[2] == "Velhon perintö (Uusikatu)") {
                $('#huone1930-3').after('Velhon perintö (Uusikatu)(varattu)');
            } else {
                $('#huone1930-3').after('Velhon perintö (Uusikatu)(vapaa)');
            }
            if(item[2] == "Murhamysteeri (Kajaaninkatu)") {
                $('#huone1930-4').after('Murhamysteeri (Kajaaninkatu)(varattu)');
            } else {
                $('#huone1930-4').after('Murhamysteeri (Kajaaninkatu)(vapaa)');
            }
            if(item[2] == "Vankilapako (Kajaaninkatu)") {
                $('#huone1930-5').after('Vankilapako (Kajaaninkatu)(varattu)');
            } else {
                $('#huone1930-5').after('Vankilapako (Kajaaninkatu)(vapaa)');
            }
            if(item[2] == "Professorin arvoitus (Kajaaninkatu)") {
                $('#huone1930-6').after('Professorin arvoitus (Kajaaninkatu)(varattu)');
            } else {
                $('#huone1930-6').after('Professorin arvoitus (Kajaaninkatu)(vapaa)');
            }
            if(item[2] == "The SAW (Kirkkokatu)") {
                $('#huone1930-7').after('The SAW (Kirkkokatu)(varattu)');
            } else {
                $('#huone1930-7').after('The SAW (Kirkkokatu)(vapaa)');
            }
            if(item[2] == "Alcatraz (Kirkkokatu)") {
                $('#huone1930-8').after('Alcatraz (Kirkkokatu)(varattu)');
            } else {
                $('#huone1930-8').after('Alcatraz (Kirkkokatu)(vapaa)');
            }
            if(item[2] == "Matka maailman ympäri (Kirkkokatu)") {
                $('#huone1930-9').after('Matka maailman ympäri (Kirkkokatu)(varattu)');
            } else {
                $('#huone1930-9').after('Matka maailman ympäri (Kirkkokatu)(vapaa)');
            }
        }
    });
});

function myFunc(vars) {
    return vars
}