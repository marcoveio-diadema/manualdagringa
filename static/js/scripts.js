/*!
* Start Bootstrap - Clean Blog v6.0.9 (https://startbootstrap.com/theme/clean-blog)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-clean-blog/blob/master/LICENSE)
*/

// hide nav bar as scroll down, show again when scrolling up

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
    $('#commentForm').submit(function (event) {
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

// AJAX FORM HANDLING AND MESSAGES FOR CONTACT FORM

$(document).ready(function() {
    $('#deleteComment').submit(function (e) {
        // send the form data here.
        var url = "{{ url_for('contato') }}"; 

        // Reference to the message container
        var messageContainer = $('.ajax-message-container');

        // AJAX function 
        $.ajax({
            type: "POST",
            url: url,
            data: $('#deleteComment').serialize(), // serializes the form's elements.
            success: function (response) {
                console.log(response);  // display the returned data in the console.

                // Display the appropriate message based on the status
                if (response.status === 'success') {
                    messageContainer.html('<div class="alert alert-success alert-dismissible fade show" role="alert">' +
                        '<strong>Sucesso!</strong> ' + response.message +
                        '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>' +
                        '</div>');

                    // Optionally, clear the form fields
                    $('#deleteComment')[0].reset();
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
        e.preventDefault(); // block the traditional submission of the form.
    });
});

// AJAX FORM HANDLING FOR NEW COMMENT FORM
$(document).ready(function () {
    $('#commentForm').unbind('submit').submit(function (e) {
        // send the form data here.
        var postId = $(this).data('post-id');
        var postSlug = $(this).data('post-slug');
        var url = "/post/" + postId + "/" + postSlug;

        // Prevent default form submission action
        e.preventDefault();
        
        // AJAX function 
        $.ajax({
            type: "POST",
            url: url,
            data: $('#commentForm').serialize(),
            success: function (response) {
                if (response.success) {
                    console.log(response);

                    // Your existing logic to prepend the new comment
                    var commentId = response.comment_data.comment_id;
                    var commentExists = $('#comment-' + commentId).length > 0;

                    if (!commentExists) {
                        var commentHTML = '<li class="border rounded">' +
                            '<div class="commenterImage"><img src="' + response.comment_data.comment_author_gravatar + '"></div>' +
                            '<div class="commentText">' +
                            '<p>' + response.comment_data.text + '</p>' +
                            '<span class="date sub-text">' +
                            response.comment_data.posted_date +
                            ' by <strong>' + response.comment_data.comment_author_name + '</strong></span>';

                        if (response.is_authenticated) {
                            commentHTML += '<span>';
                            commentHTML += '<a href="#" class="btn btn-link text-danger delete-comment" data-comment-id="' + response.comment_data.comment_id + '" data-post-id="' + response.comment_data.post_id + '" data-post-slug="' + response.comment_data.post_slug + '"> Delete </a>';
                            commentHTML += '</span>';
                        }

                        commentHTML += '</div>' + '</li>';

                        $('.commentList').prepend(commentHTML);
                    }

                    // Reload existing comments
                    $(".commentList").load(window.location.href + " .commentList");

                    // Clear the form fields
                    $('#commentForm')[0].reset();
                } else {
                    // Handle the error response here
                    console.error(response.error);
                }
            },
            error: function (error) {
                // Handle the error response here
                console.error(error);
            }
        });

    });
});


// AJAX HANDLING TO DELETE COMMENTS


$(document).ready(function() {
    // Attach a click event to the parent element of delete comment links
    $(".commentList").on("click", ".delete-comment", function(e) {
        e.preventDefault(); // Prevent the default link behavior

        var commentId = $(this).data("comment-id"); // Get the comment ID
        var postId = $(this).data("post-id"); // Get the post ID
        var postSlug = $(this).data("post-slug"); // Get the post slug
        var deleteUrl = "/delete-comment/" + commentId + "?post_id=" + postId + "&slug=" + postSlug;


        // Send an AJAX request to delete the comment
        $.ajax({
            url: deleteUrl,
            type: "POST",
            success: function(response) {
                // Check if the delete request came from the admin template
                if (response.fromAdmin) {
                    // Redirect back to the admin page
                    window.location.href = response.redirectUrl;
                } else {
                    // Reload only the commentList section
                    $(".commentList").load(window.location.href + " .commentList");
                }
            },
            error: function(error) {
                console.error("Error deleting comment:", error);
            }
        });
    });
});


