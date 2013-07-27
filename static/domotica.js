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
            });
};

function installPostHandlers() {
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

    document.querySelector("#all_off").addEventListener('touched', all_off);
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
