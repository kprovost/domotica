function lightswitch()
{
    id = this.id.replace("light_", "");
    $.post("/lightswitch", { id: id });
};

$(document).ready(function () {
    $(".toggle").each(function(index) {
        obj = $(".toggle")[index];
        document.querySelector('#' + obj.id).addEventListener('toggle', lightswitch, obj.id);
    });
});
