let pageNumber = 1;
let postsRequestInProgress = false;

function getPostsPagePromise(page) {
  return new Promise((resolve, reject) => {
    $("#loader").toggleClass("hidden");
    $.ajax({
      type: "GET",
      url: `/ajax/posts/${page}`,
      contentType: "application/json",
      dataType: "json",
      success: function (posts) {
        $("#loader").toggleClass("hidden");
        resolve(posts);
      },
      error: function (err) {
        $("#loader").toggleClass("hidden");
        reject(err);
      },
    });
  });
}

function appendPosts(posts) {
  let postDisplayTemplate = ``;

  console.log(posts);

  posts.forEach((post) => {
    let d = new Date(post.created_at);
    postDisplayTemplate += `
            <article class="py-6 post" id="${"post_" + post.id}">
                <div class="flex items-center justify-between mb-3 text-gray-500">
                    <div>
                        <a class="bg-blue-100 text-blue-800 text-sm font-medium mr-2 px-2.5 py-1 rounded"
                            href="/blog/tag/laravel/">#Laravel</a>
                        <a class="bg-blue-100 text-blue-800 text-sm font-medium mr-2 px-2.5 py-1 rounded"
                            href="/blog/tag/laravel/">#PHP</a>
                    </div>
                    <span class="text-sm">Published on ${d.getUTCDate()}-${d.getUTCMonth()}-${d.getUTCFullYear()}</span>
                </div>
                
                <span class="text-gray-400 likesCount">
                    likes ${post.total_likes}
                </span>
                
                <h2 class="mb-2 text-2xl font-bold tracking-tight text-gray-900">
                    <a href="/blog/how-to-use-flowbite-ui-components-with-laravel-and-alpine-js/">${
                      post.title
                    }</a>
                </h2>
                
                ${
                  post.image_url
                    ? `<img class="w-full h-auto rounded-md" src="${post.image_url}" alt="${post.caption}"/>`
                    : ``
                }
                
                <p class="mb-5 text-gray-500">${post.content}
                </p>

                <div class="flex items-center justify-between">
                    <a class="flex items-center space-x-2" href="/blog/author/rich/">
                    ${post.owner_profile_pic ? `<img class="rounded-full w-7 h-7"
                    src="${post.owner_profile_pic}"
                    alt="Rich Klein profile picture">` : `<div class="rounded-full w-7 h-7"></div>`}
                        <span class="font-medium text-gray-500">${post.owner_full_name}</span>
                    </a>
                    <span class="flex justify-center align-middle items-center space-x-3">
                        <span>
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
                                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                stroke-linejoin="round" class="lucide lucide-heart stroke-blue-500 cursor-pointer hover:stroke-blue-600">
                                <path
                                    d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z" />
                            </svg>
                        </span>
                        <span class="likeButton">
                            <svg id="${
                              "likeBtn_" + post.id
                            }" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24"
                                fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                stroke-linejoin="round" class="lucide lucide-thumbs-up stroke-blue-500 cursor-pointer hover:stroke-blue-600 ${
                                  post.did_user_like_post ? "fill-blue-200" : ""
                                }">
                                <path d="M7 10v12" />
                                <path
                                    d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2h0a3.13 3.13 0 0 1 3 3.88Z" />
                            </svg>
                        </span>
                        <span>
                            <a class="inline-flex items-center font-medium text-blue-600 hover:underline dark:text-blue-500"
                                href="/blog/how-to-use-flowbite-ui-components-with-laravel-and-alpine-js/">
                                Read more
                                <svg class="w-4 h-4 ml-2" fill="currentColor" viewBox="0 0 20 20"
                                    xmlns="http://www.w3.org/2000/svg">
                                    <path fill-rule="evenodd"
                                        d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z"
                                        clip-rule="evenodd"></path>
                                </svg>
                            </a>
                        </span>
                    </span>
                </div>
            </article>
            `;
  });

  $("#post_container").append(postDisplayTemplate);
}

function bindLikeButtonEvent() {
  $(".likeButton").unbind();
  $(".likeButton").click(function () {
    let post = $(this).parents(".post");
    let id = $(post).attr("id");

    $.ajax({
      type: "GET",
      url: `/ajax/like/${id.split("_")[1]}`,
      dataType: "json",
      contentType: "application/json",
      success: function (res) {
        $(`#${id}`).children(".likesCount").text(`likes ${res.new_like_count}`);
        $(`#likeBtn_${id.split("_")[1]}`).toggleClass("fill-blue-200");
      },
      error: function (err) {
        console.log(err);
      },
    });
  });
}

$(document).ready(function () {
  let postPageNumber = 1;
  let hasPosts = true;

  // Initial posts load
  new Promise((resolve, reject) => {
    postsRequestInProgress = true;
    resolve(getPostsPagePromise(postPageNumber));
  })
    .then((posts) => {
      appendPosts(posts);

      if (posts.length) {
        postPageNumber++;
      } else {
        hasPosts = false;
        $("#post_container").html(
          "<h3 class='text-2xl text-gray-400 text-center'>No post found !!</h3>"
        );
      }

      postsRequestInProgress = false;
    })
    .then(() => bindLikeButtonEvent());

  // loads posts whenever the user scroll to the bottom
  $(document).scroll(function (e) {
    let bodyElement = document.querySelector("body");

    if (
      window.scrollY + window.innerHeight >= bodyElement.scrollHeight &&
      hasPosts &&
      !postsRequestInProgress
    ) {
      new Promise((resolve, reject) => {
        postsRequestInProgress = true;
        resolve(getPostsPagePromise(postPageNumber));
      })
        .then((posts) => {
          appendPosts(posts);

          if (posts.length) {
            postPageNumber++;
          } else {
            hasPosts = false;
          }

          postsRequestInProgress = false;
        })
        .then(() => bindLikeButtonEvent());
    }
  });
});
