document.addEventListener("DOMContentLoaded", function () {

  // Prevent default submission of bookmark and like forms
  let forms = document.querySelectorAll(".like-form");
  let len_forms = forms.length;
  for (i = 0; i < len_forms; i++) {
    forms[i].addEventListener("submit", function (event) {
      event.preventDefault();
    });
  }

  // Prevent default submission of bookmark forms
  let bookmarks_forms = document.querySelectorAll(".bookmark-form");
  let len_bforms = bookmarks_forms.length;
  for (i = 0; i < len_bforms; i++) {
    bookmarks_forms[i].addEventListener("submit", function (event) {
    event.preventDefault();
    });
  }

  create_word();
});

// Returns an array of maxLength (or less) page numbers
// where a 0 in the returned array denotes a gap in the series.
// Parameters:
//  totalPages:     total number of pages
//  page:           current page
//  maxLength:      maximum size of returned array
function getPageList(totalPages, page, maxLength) {
  if (maxLength < 5) throw "maxLength must be at least 5";

  function range(start, end) {
      return Array.from(Array(end - start + 1), (_, i) => i + start);
  } 

  var sideWidth = maxLength < 9 ? 1 : 2;
  var leftWidth = (maxLength - sideWidth*2 - 3) >> 1;
  var rightWidth = (maxLength - sideWidth*2 - 2) >> 1;
  if (totalPages <= maxLength) {
      // no breaks in list
      return range(1, totalPages);
  }
  if (page <= maxLength - sideWidth - 1 - rightWidth) {
      // no break on left of page
      return range(1, maxLength - sideWidth - 1)
          .concat(0, range(totalPages - sideWidth + 1, totalPages));
  }
  if (page >= totalPages - sideWidth - 1 - rightWidth) {
      // no break on right of page
      return range(1, sideWidth)
          .concat(0, range(totalPages - sideWidth - 1 - rightWidth - leftWidth, totalPages));
  }
  // Breaks on both sides
  return range(1, sideWidth)
      .concat(0, range(page - leftWidth, page + rightWidth),
              0, range(totalPages - sideWidth + 1, totalPages));
}

// Below is an example use of the above function.
$(function () {
  
  let totalPages = document.querySelector("#page-numbers").value; 
  // Number of buttons at the top, not counting prev/next,
  // but including the dotted buttons.
  // Must be at least 5:
  var paginationSize = 10; 
  var currentPage;

  function showPage(whichPage) {
      if (whichPage < 1 || whichPage > totalPages) return false;
      currentPage = whichPage;
      $("#page > .content").hide()
          .slice((currentPage*5-5), 
                  currentPage*5).show();
      // Replace the navigation items (not prev/next):            
      $("#pagination-demo li").slice(1, -1).remove();
      getPageList(totalPages, currentPage, paginationSize).forEach( item => {
          $("<li>").addClass("page-item")
                   .addClass(item ? "current-page" : "disabled")
                   .toggleClass("active", item === currentPage).append(
              $("<a>").addClass("page-link").attr({
                  href: "javascript:void(0)"}).text(item || "...")
          ).insertBefore("#next-page");
      });
      // Disable prev/next when at first/last page:
      $("#previous-page").toggleClass("disabled", currentPage === 1);
      $("#next-page").toggleClass("disabled", currentPage === totalPages);
      return true;
  }

  // Include the prev/next buttons:
  $(".pagination").append(
      $("<li>").addClass("page-item").attr({ id: "previous-page" }).append(
          $("<a>").addClass("page-link").attr({
              href: "javascript:void(0)"}).html("&#8249;")
      ),
      $("<li>").addClass("page-item").attr({ id: "next-page" }).append(
          $("<a>").addClass("page-link").attr({
              href: "javascript:void(0)"}).html("&#8250;")
      )
  );

  // Show the page links
  $("#page").show();
  showPage(1);

  // Use event delegation, as these items are recreated later    
  $(document).on("click", ".pagination li.current-page:not(.active)", function () {
      return showPage(+$(this).text());
  });
  $("#next-page").on("click", function () {
      return showPage(currentPage+1);
  });

  $("#previous-page").on("click", function () {
      return showPage(currentPage-1);
  });
  
});


function create_word() {

  // Clear out composition fields
  const title = document.querySelector("#new-title");
  const definition = document.querySelector("#new-definition");
  if (title) title.value = "";
  if (definition) definition.value = "";
  // If more clearing out is needed here below...

  submit_word();
}

function submit_word() {
    // Select the submit button and input to be used later
  const submit = document.querySelector("#create-submit");
  const title = document.querySelector("#id_title");
  const definition = document.querySelector("#id_definition");
  const category = document.querySelector("#id_category");
  const cat_submit = document.querySelector("#category-submit");
  const comment_submit = document.querySelector("#comment-submit");
  const comment = document.querySelector("#new-comment");
  const add_quote = document.querySelector('#add-submit');
  const quotation = document.querySelector('#id_quotation');
  

  // Disable new word submit button by default
  if (submit) submit.disabled = true;
  // Disable new category, comment, quote submit button by default
  if (cat_submit) cat_submit.disabled = true;
  if (comment_submit) comment_submit.disabled = true;
  if (add_quote) add_quote.disabled = true;
  

  // Listen for input to be typed into each of the input fields
  if (title) {
    title.onkeyup = () => {
      if (
        title.value.length > 0 &&
        definition.value.length > 0
      ) {
        submit.disabled = false;
      } else {
        submit.disabled = true;
      }
    };
  }

  if (definition) {
    definition.onkeyup = () => {
      if (
        title.value.length > 0 &&
        definition.value.length > 0
      ) {
        submit.disabled = false;
      } else {
        submit.disabled = true;
      }
    };
  }

  if (category) {
    category.onkeyup = () => {
      if (
        category.value.length > 0
      ) {
        cat_submit.disabled = false;
      } else {
        cat_submit.disabled = true;
      }
    };
  }

  if (comment) {
    comment.onkeyup = () => {
      if (
        comment.value.length > 0
      ) {
        comment_submit.disabled = false;
      } else {
        comment_submit.disabled = true;
      }
    };
  }

  if (quotation) {
    quotation.onkeyup = () => {
      if (
        quotation.value.length > 0
      ) {
        add_quote.disabled = false;
      } else {
        add_quote.disabled = true;
      }
    };
  }
}

// Csrf token by JS function
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

// Like post
function like(quotation_id, user_id) {
  // Change like heart background color after click and change back after click again
  let elem = document.getElementsByClassName(`far fa-heart like-heart${ quotation_id } fa-stack-2x`);
  let fas_elem = document.getElementsByClassName(`fas fa-heart like-heart${ quotation_id } fa-stack-2x`);
  
  // console.log(fas_elem[0]);
  if (fas_elem[0]) {fas_elem[0].setAttribute("class", `far fa-heart like-heart${ quotation_id } fa-stack-2x`);}
  else if (elem[0]) {elem[0].setAttribute("class", `fas fa-heart like-heart${ quotation_id } fa-stack-2x`);}
  
  const request = new Request(`/wordPlay/likes/${quotation_id}/${user_id}`, {
    headers: { "X-CSRFToken": csrftoken },
  });
  fetch(request, {
  // fetch(`http://127.0.0.1:8000/wordPlay/likes/${word_id}/${user_id}`, {
    method: "POST",
    mode: "same-origin",
    body: JSON.stringify({
      quotation: quotation_id,
      user: user_id,
    }),
  })
    .then((response) => response.json())
    .then((content) => {
      likes = content.likes
      like_count = 0;
      for (i = 0, len = likes.length; i < len; i++) {
        like_count++;
      }
      user_likes = content.user_likes
      user_count = 0;
      for (i = 0, len = user_likes.length; i < len; i++) {
        user_count++;
      }
      const count = document.querySelector(`.count${quotation_id}`);
      const index_likes = document.querySelector(`.count_likes`);
      count.innerHTML = like_count;
      if (index_likes) {index_likes.innerHTML = `${user_count} Likes`;}
      const likeCircle_bookmarks = document.querySelector('.likeCircle');
      if (likeCircle_bookmarks) {likeCircle_bookmarks.innerHTML = `${user_count}`;}
    });
}

// Bookmark post
function bookmark(word_id, user_id) {
  // Change bookmark font background color after click and change back after click again
  let elem = document.getElementsByClassName(`far fa-bookmark bookmark-mark${ word_id } fa-stack-2x`);
  let fas_elem = document.getElementsByClassName(`fas fa-bookmark bookmark-mark${ word_id } fa-stack-2x`);
  
  if (fas_elem[0]) {fas_elem[0].setAttribute("class", `far fa-bookmark bookmark-mark${ word_id } fa-stack-2x`);}
  else if (elem[0]) {elem[0].setAttribute("class", `fas fa-bookmark bookmark-mark${ word_id } fa-stack-2x`);}

  const request = new Request(`/wordPlay/add_bookmarks/${word_id}/${user_id}`, {
    headers: { "X-CSRFToken": csrftoken },
  });
  fetch(request, {
    method: "POST",
    mode: "same-origin",
    body: JSON.stringify({
      word: word_id,
      user: user_id,
    }),
  })
    .then((response) => response.json())
    .then((content) => {
      bookmarks = content.bookmarks
      bookmark_count = 0;
      for (i = 0, len = bookmarks.length; i < len; i++) {
        bookmark_count++;
      }
      user_bookmarks = content.user_bookmarks
      user_count = 0;
      for (i = 0, len = user_bookmarks.length; i < len; i++) {
        user_count++;
      }
      const index_bookmarks = document.querySelector('.count_bookmarks');
      if (index_bookmarks) {index_bookmarks.innerHTML = `${user_count} Bookmarks`;}
      const numberCircle_bookmarks = document.querySelector('.bookmarkCircle');
      if (numberCircle_bookmarks) {numberCircle_bookmarks.innerHTML = `${user_count}`;}
    });
}