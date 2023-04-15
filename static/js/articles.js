let nextPage = null
let footer = document.querySelector('footer')

document.onload = setArticles()
function setArticles() {
  let url = localStorage.getItem('articles-search-url') ? JSON.parse(localStorage.getItem('articles-search-url')) : '/api/articles-list'
  loadArticles(url)
}

// Attach an event listener to the search form submission
document.getElementById('search-form').addEventListener('submit', function (event) {

  // Prevent the default form submission behavior
  event.preventDefault();

  // Get the search query from the input field
  var query = document.getElementById('search-query').value;

  // Send an AJAX request to retrieve articles matching the search query
  let url = '/api/articles-list?search=' + encodeURIComponent(query)
  var articleList = document.getElementById('article-list');
  articleList.innerHTML = '';
  loadArticles(url)
});


// Attach an event listener to the scroll event
window.addEventListener('scroll', function () {
  if (nextPage) {
    // Check if we've scrolled to the bottom of the page
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight - footer.offsetHeight) {
      // Increment the current page number and send an AJAX request for the next page of articles
      setTimeout(() => {
        loadArticles(nextPage)
      }, 3000);
    }
  }
});


function loadArticles(url) {
  var articleList = document.getElementById('article-list');

  // Show loading indicator
  var loadingDiv = document.createElement("div");
  loadingDiv.setAttribute("id", "loading");
  loadingDiv.innerHTML = "Loading...";
  articleList.appendChild(loadingDiv)

  var xhr = new XMLHttpRequest();
  xhr.open('GET', url);
  xhr.onload = function () {
    // Hide loading indicator
    var loadingElement = document.getElementById("loading");
    loadingElement.parentNode.removeChild(loadingElement);

    // Parse the response and append the new articles to the page
    var responseData = JSON.parse(xhr.responseText);
    nextPage = responseData.next
    let articles = responseData.results

    for (var i = 0; i < articles.length; i++) {
      var article = articles[i];
      var published_at = article.published_at.split('T')[0].split('-').join(', ');
      var element = `<div class="col-md-3 grid-item">
      <div class="card">
        <a href="${article.slug}">
        <img class="img-fluid" src="${article.image_url}" max-height="390px" alt="Tree of Codes">
        </a>
        <div class="card-block">
            <h2 class="card-title"><a href="${article.slug}">${article.title}</a>
            </h2>
            <div class="metafooter">
                <div class="wrapfooter">
                    <span class="author-meta">
                        <span class="post-date">${published_at}</span>
                    </span>
                    <span class="post-read-more">
                        <a href="${article.slug}" title="Read Story">
                            <i class="fa fa-link"></i>
                        </a>
                    </span>
                    <div class="clearfix">
                    </div>
                </div>
            </div>
        </div>
    </div>
  </div>`;
      articleList.innerHTML += element;
    }
    // Animate new items
    var items = document.getElementsByClassName("col-md-3");
    for (var i = 0; i < items.length; i++) {
      if (!isElementAnimating(items[i])) {
        setTimeout(function (item) {
          item.style.opacity = 0;
        }, i * 1000, items[i]);
      }
    }
  };
  xhr.send();

  // Check whether an element is currently being animated
  function isElementAnimating(element) {
    var opacity = element.style.opacity;
    return opacity === "" || opacity === "1";
  }
}


document.onscroll = function () {
  // console.log('window.innerHeight ',window.innerHeight)
  // console.log('window.scrollY ',window.scrollY )
  // console.log('document.body.offsetHeight  ',document.body.offsetHeight  )
  console.log(footer.offsetHeight)
}
