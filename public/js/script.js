$(document).ready(function(){
    // dropdown search
    $(".dropdown-toggle").click(function() {
        $(".dropdown-menu").toggle();
        $('.nav-input').focus();
    });

    // dropdown menu
    $("#icon-toggle").click(function (){
        $(".sidebar-links").toggle();
    })

    // Text area autosize
    $("textarea").on("keyup", function(e) {
        var scHeight = $(this)[0].scrollHeight;
    });
});

//  tinyMCE

tinymce.init({
selector: 'textarea.tiny-mce',
plugins: 'anchor autolink charmap codesample emoticons image link lists media searchreplace table visualblocks wordcount linkchecker',
toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table mergetags | addcomment showcomments | spellcheckdialog a11ycheck typography | align lineheight | checklist numlist bullist indent outdent | emoticons charmap | removeformat',
tinycomments_mode: 'embedded',
tinycomments_author: 'Author name',
mergetags_list: [
    { value: 'First.Name', title: 'First Name' },
    { value: 'Email', title: 'Email' },
],
ai_request: (request, respondWith) => respondWith.string(() => Promise.reject("See docs to implement AI Assistant")),
});

// limit amount of words in card
function truncateText(text, limit) {
    const words = text.split(' ');
  
    if (words.length > limit) {
      return words.slice(0, limit).join(' ') + '...';
    }
  
    return text;
  }
  
  const pElements = document.querySelectorAll('.card-header p');
  
  pElements.forEach(p => {
    p.textContent = truncateText(p.textContent, 40);
  });

