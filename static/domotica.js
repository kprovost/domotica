function lightswitch()
{
    id = this.id.replace("light_", "");
    $.post("/lightswitch", { id: id })
        .fail(location.reload());
};

$(document).ready(function () {
    $(".toggle").each(function(index) {
        obj = $(".toggle")[index];
        document.querySelector('#' + obj.id).addEventListener('toggle', lightswitch, obj.id);
    });
});
