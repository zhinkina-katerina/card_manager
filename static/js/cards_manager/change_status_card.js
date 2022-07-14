jQuery(document).ready(function() {
        jQuery(document).on('click', "#change_status_button", function (e) {
        e.preventDefault()
             jQuery.ajax({
                 headers: {"X-CSRFToken": csrftoken},
                 url: this.href,
                 type: "POST",
                success:function(response) {
                    window.location.href=response.url

            }
             });
        });
 })