/*!
* Start Bootstrap - Clean Blog v6.0.9 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/
window.addEventListener('DOMContentLoaded', () => {
    let scrollPos = 0;
    const mainNav = document.getElementById('mainNav');
    const headerHeight = mainNav.clientHeight;
    window.addEventListener('scroll', function() {
        const currentTop = document.body.getBoundingClientRect().top * -1;
        if ( currentTop < scrollPos) {
            // Scrolling Up
            if (currentTop > 0 && mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-visible');
            } else {
                console.log(123);
                mainNav.classList.remove('is-visible', 'is-fixed');
            }
        } else {
            // Scrolling Down
            mainNav.classList.remove(['is-visible']);
            if (currentTop > headerHeight && !mainNav.classList.contains('is-fixed')) {
                mainNav.classList.add('is-fixed');
            }
        }
        scrollPos = currentTop;
    });
})


// ALERT MESSAGES FOR SUBSCRIBER FORM //

$(document).ready(function () {
      $('.subscribe-form').submit(function (event) {
          event.preventDefault();  // Prevent the default form submission

          // Get form data
          var formData = $(this).serialize();

          // Reference to the message container
          var messageContainer = $('.ajax-message-container');

          // Perform AJAX request
          $.ajax({
              type: 'POST',
              url: $(this).attr('action'),
              data: formData,
              success: function (response) {
                  // Handle the response here
                  console.log(response);

                  // Display the appropriate message based on the status
                  if (response.status === 'success') {
                      messageContainer.html('<div class="alert alert-success alert-dismissible fade show" role="alert">' +
                          '<strong>Sucesso!</strong> ' + response.message +
                          '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
                          '</div>');

                      // Optionally, clear the form fields
                      $('.subscribe-form')[0].reset();
                  } else if (response.status === 'error') {
                      messageContainer.html('<div class="alert alert-danger alert-dismissible fade show" role="alert">' +
                          '<strong>Erro!</strong> ' + response.message +
                          '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
                          '</div>');
                  }
              },
              error: function (error) {
                  // Handle the error response here
                  console.error(error);

                  // Display a generic error message
                  messageContainer.html('<div class="alert alert-danger alert-dismissible fade show" role="alert">' +
                      '<strong>Erro!</strong> Ocorreu um erro ao cadastrar o email. Tente novamente.' +
                      '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
                      '</div>');
              }
          });
      });
  });



  // ALERT MESSAGES FOR CONTACT FORM //

$(document).ready(function () {
    $('#contactForm').submit(function (event) {
        event.preventDefault();  // Prevent the default form submission

        // CSRF Token
        var csrf_token = "{{ csrf_token() }}";

        // Get form data
        var formData = $(this).serialize();

        // Reference to the message container
        var messageContainer = $('.ajax-message-container');

        // Perform AJAX request
        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: formData,
            success: function (response) {
                // Handle the response here
                console.log(response);

                // Display the appropriate message based on the status
                if (response.status === 'success') {
                    messageContainer.html('<div class="alert alert-success alert-dismissible fade show" role="alert">' +
                        '<strong>Sucesso!</strong> ' + response.message +
                        '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
                        '</div>');

                    // Optionally, clear the form fields
                    $('#contactForm')[0].reset();
                } else if (response.status === 'error') {
                    messageContainer.html('<div class="alert alert-danger alert-dismissible fade show" role="alert">' +
                        '<strong>Erro!</strong> ' + response.message +
                        '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
                        '</div>');
                }
            },
            error: function (error) {
                // Handle the error response here
                console.error(error);

                // Display a generic error message
                messageContainer.html('<div class="alert alert-danger alert-dismissible fade show" role="alert">' +
                    '<strong>Erro!</strong> Ocorreu um erro ao enviar a mensagem. Tente novamente.' +
                    '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
                    '</div>');
            }
        });
    });
    // CSRF TOKEN
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf_token);
            }
        }
    });
});