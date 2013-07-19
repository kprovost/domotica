function lightswitch()
{
    $.post("/lightswitch", { id: this.id });
};

$(document).ready(function () {
    $(".toggle").each(function(index) {
        obj = $(".toggle")[index];
        document.querySelector('#' + obj.id).addEventListener('toggle', lightswitch, obj.id);
    });
});
