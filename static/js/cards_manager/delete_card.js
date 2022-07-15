const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

jQuery(document).ready(function () {
  jQuery(document).on('click', "#delete_card_button", function (e) {
    e.preventDefault()
    if (confirm("Are you sure you want to delete this card?")) {
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

