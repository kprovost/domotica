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
};

$(document).ready(function () {
    installPostHandlers();
});

window.addEventListener('push', function() {
    installPostHandlers();
});
