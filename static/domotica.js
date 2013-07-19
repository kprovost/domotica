function lightswitch()
{
    id = this.id.replace("light_", "");
    $.post("/lightswitch/toggle", { id: id })
        .fail(function(){
                console.log("Failed to post lightswitch/toggle" + id);
                location.reload();
            });
};

$(document).ready(function () {
    $(".toggle").each(function(index) {
        obj = $(".toggle")[index];
        document.querySelector('#' + obj.id).addEventListener('toggle', lightswitch, obj.id);
    });
});
