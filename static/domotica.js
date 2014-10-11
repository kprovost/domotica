function toggle_power()
{
    id = this.id.replace("plug_", "");
    $.post("/powerplug/toggle/" + id)
        .fail(function(){
                console.log("Failed to post powerplug/toggle " + id);
                location.reload();
            });
}

function heating_change()
{
    id = this.id.replace("heating_", "");
    $.post("/heating/toggle/" + id)
        .fail(function(){
                console.log("Failed to post /heating/toggle " + id);
                location.reload();
            });
}

function toggle_light()
{
    id = this.id.replace("light_", "");
    $.post("/lightswitch/toggle", { id: id })
        .fail(function(){
                console.log("Failed to post lightswitch/toggle " + id);
                location.reload();
            });
};

function toggle_motion()
{
    id = this.id.replace("motion_", "");
    $.post("/lightswitch/toggle_motion", { id: id })
        .fail(function(){
                console.log("Failed to post lightswitch/toggle_motion " + id);
                location.reload();
            });
};

function toggle_blink()
{
    id = this.id.replace("blink_", "");
    $.post("/lightswitch/toggle_blink", { id: id })
        .fail(function(){
                console.log("Failed to post lightswitch/toggle_blink " + id);
                location.reload();
            });
};

function all_off()
{
    console.log("All lights off");
    $.post("/lightswitch/all_off")
        .fail(function(){
                console.log("Failed to turn all lights off");
                location.reload();
            });
};

function alarm_disarm()
{
    console.log("Disarm alarm");
    $.post("/alarm_action/disarm")
        .fail(function(){
            console.log("Failed to disarm alarm");
            location.reload();
        });
};

function alarm_arm()
{
    console.log("Arm alarm");
    $.post("/alarm_action/arm")
        .fail(function(){
            console.log("Failed to arm alarm");
            location.reload();
        });
};

function toggle_alarm_detector()
{
    console.log("Toggle alarm detector");
    id = this.id.replace("detector_", "");
    $.post("/alarm_action/toggle_detector", { id: id })
        .fail(function(){
            console.log("Failed to post toggle_detector");
            location.reload();
        });
};

function timeout_select()
{
    console.log("Update light timeout");

    $( "select option:selected" ).each(function() {
        timeout = $(this).val();
    });

    $(".timeout_select").each(function(index) {
        obj = $(".timeout_select")[index];
        id = obj.id.replace("timeout_", "");
    });

    $.post("/lightswitch/timeout", { id: id, timeout: timeout })
        .fail(function() {
            console.log("Failed to update timeout for " + id);
            location.reload();
        });
}

function refresh()
{
    document.location.reload(true);
};

function installPostHandlers() {
    $(".powerplug").each(function(index) {
        obj = $(".powerplug")[index];
        document.querySelector('#' + obj.id).addEventListener('toggle', toggle_power);
    });

    $(".heating").each(function(index) {
        obj = $(".heating")[index];
        document.querySelector('#' + obj.id).addEventListener('toggle', heating_change);
    });

    $(".light").each(function(index) {
        obj = $(".light")[index];
        document.querySelector('#' + obj.id).addEventListener('toggle', toggle_light);
    });

    $(".motion").each(function(index) {
        obj = $(".motion")[index];
        document.querySelector("#" + obj.id).addEventListener('toggle', toggle_motion);
    });

    $(".blink").each(function(index) {
        obj = $(".blink")[index];
        document.querySelector("#" + obj.id).addEventListener('toggle', toggle_blink);
    });

    $('.timeout_select').change(timeout_select);

    if (document.querySelector("#all_off"))
        document.querySelector("#all_off").addEventListener('touchend', all_off);
    if (document.querySelector("#refresh"))
        document.querySelector("#refresh").addEventListener('touchend', refresh);
    if (document.querySelector("#alarm_disarm"))
        document.querySelector("#alarm_disarm").addEventListener('touchend', alarm_disarm);
    if (document.querySelector("#alarm_arm"))
        document.querySelector("#alarm_arm").addEventListener('touchend', alarm_arm);

    $(".detector").each(function(index) {
        obj = $(".detector")[index];
        document.querySelector("#" + obj.id).addEventListener('toggle', toggle_alarm_detector);
    });
};

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function tryLocalStorageSession()
{
    sessionid = localStorage.getItem("sessionid");
    // Delete the existing localStorage entry, in case the session expired
    localStorage.setItem("sessionid", "");

    if (sessionid)
    {
        document.cookie = document.cookie + ";sessionid=" + sessionid;
        window.location.href="/";
    }
}

$(document).ready(function () {
    installPostHandlers();

    // Store the session ID in the localStorage as the iPhone doesn't keep
    // webapp cookies beyond the session
    sessionid = readCookie("sessionid");
    if (sessionid)
        localStorage.setItem("sessionid", sessionid);
});

window.addEventListener('push', function() {
    installPostHandlers();
});
