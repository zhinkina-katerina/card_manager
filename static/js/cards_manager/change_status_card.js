jQuery(document).ready(function () {
  jQuery(document).on('click', "#deactivate_card_button", function (e) {
    e.preventDefault()
    if (confirm("Are you sure you want to deactivate this card?")) {
      jQuery.ajax({
        headers: {"X-CSRFToken": csrftoken},
        url: this.href,
        type: "POST",
        success: function (response) {
          window.location.href = response.url
        }
      });
    }
  });
})

jQuery(document).ready(function () {
  jQuery(document).on('click', "#activate_card_button", function (e) {
    e.preventDefault()
      jQuery.ajax({
        headers: {"X-CSRFToken": csrftoken},
        url: this.href,
        type: "POST",
        success: function (response) {
          window.location.href = response.url
        }
      });
  });
})