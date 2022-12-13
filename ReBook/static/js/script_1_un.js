$(document).ready(function () {  
  $("#Submit").click(function(){
    
    const Base = "https://www.googleapis.com/books/v1/volumes?q=";
    const search = $("#inputData").val();
    const option = $("#options").children("option:selected").val();
    const sort = $("#sort").children("option:selected").val();
    const name = $("#option_value").val();
    const range = $("#quantity").val();
    let dowload = "";
    let flag = 0;
    const objects = {};

    if (search == "") {
      alert("Empty data");
    }  

    if ($("#download").is(':checked')) {
        dowload = "&download=epub";
        flag = 1;
    }

    let URL = Base + search;

    if (name != "") {
      URL  += "+" + option + ":" + name; 
    }

    URL += "&maxResults=" + range + "&orderBy=" + sort;

    if ( flag == 1) {
      URL += dowload;
    } 

    $.ajax({
      type: "GET",
      url: URL,
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function(data) {
        
        const Clear = '<div class="clear"><input type="button" id="Clear" name="btnClick" value="Clear"></div>';
        const Container = '<div class="gallery"><div class="top_image"><div><img src="" alt="hello"></div><div><h1></h1><p class="author"></p><p class="publishedDate"></p></p><p class="rate"></p></div></div><div class="desc"><p class="description"></p><p class="read_more">READ MORE</p></div></div>';
        const DATA = data.items;
        
        if (DATA != undefined) {
          $("div.form").addClass("hide");
          $(".form").after(Clear);
        
            DATA.forEach((val, index) => {
              
              objects[index] = val;

              let title = val.volumeInfo.title;
              let publisher = val.volumeInfo.publisher;
              let authors = val.volumeInfo.authors;
              let categories = val.volumeInfo.categories;
              
              let author = "";
              for (i in authors) {
              author += authors[i];
              if (i < authors.length - 1) {
                author += " & ";
                }
              };

              let category = "";
              for (i in categories) {
              category += categories[i];
              if (i < categories.length - 1) {
                category += " & ";
                }
              };


              let date = val.volumeInfo.publishedDate;
              let rate = val.volumeInfo.averageRating;
              
              if (author == "") {
                author = "undefined";
              }
              objects[index].volumeInfo.authors = author;

              if (date == undefined) {
                date = "undefined";
              }

              if (rate == undefined) {
                rate = "undefined";
              }

              if (category == undefined) {
                category = "undefined";
              }
              objects[index].volumeInfo.categories = category;
              
              const description = val.volumeInfo.description;
              let description1 = description;
              
              if (description1 != undefined) {
                if (description1.length >= 535) {
                  description1 = description1.slice(0, 535) + " ...";
                }
              } else {
                description1 = "NO description available";
              }

              let image = "";
              if (val.volumeInfo.imageLinks == undefined) {
                  image = "book.jpg"
              } else {
                  image = val.volumeInfo.imageLinks.thumbnail;
              }

              $("div.article").append(Container);
              $("div.top_image div img").last().attr("src", image);
              $("div.top_image div h1").last().html(title);
              $(".author").last().html("<b>Author</b><br>" + author);
              $(".publishedDate").last().html("<b>Published Date</b><br>" + date);
              $(".rate").last().html("<b>Average Rating</b><br>" + rate)
              $(".description").last().html("<b>Description: </b>" + description1);
            });

          let j = 0;
          $(".read_more").each(function () {
            $(this).attr("id", j);
            j++;
          });

          $('.gallery').on('click', '.read_more', function () {
              let key = $(this).attr('id');
              let Json_data = objects[key];
              $.ajax({
                data: Json_data,
                url: '/process',
                type: 'POST'
              })
              .done(function (data) {
                if (data.error) {
                  alert("Error");
                } else {
                  let view = '<div class = "popup-container"><div class="popup-close"><p>Close</p></div><div class="popup-header"><div class="popup-image"><img src="" alt="hello"></div><div class="popup-short"><p class="title"></p><p class="subtitle"></p><p class="authors"></p><p class="publisher"></p><p class="publishedDate"></p><p class="pageCount"></p><p class="printType"></p><p class="categories"></p><p class="averageRating"></p><p class="ratingsCount"></p><p class="maturityRating"></p><p class="language"></p></div></div><div class="popup-long"><p class="description"></p><p class="saleInfo"></p><p class="scountry"></p><p class="saleability"></p><p class="isEbook"></p><p class="accessInfo"></p><p class="country"></p><p class="epub"></p><p class="pdf"></p><p class="viewability"></p><p class="publicDomain"></p><p class="embeddable"></p><p class="textToSpeechPermissio"></p><p class="accessViewStatus"></p><p class="quoteSharingAllowed"></p><p class="textSnippet"></p></div><div class="popup-access"><a href="" class="preview">Preview Link</a></div></div>'
                  $("header").after(view);
                  $("div.popup-image img").attr("src", data["thumbnail"]);
                  $("p.title").html(data['title']);
                  $("p.subtitle").html("<b>Subtitle: </b>" + data['subtitle']);
                  $("p.authors").html("<b>Author: </b>" + data['authors']);
                  $("p.publisher").html("<b>Publisher: </b>" + data['publisher']);
                  $("p.publishedDate").html("<b>Published Date: </b>: " + data['publishedDate']);
                  $("p.pageCount").html("<b>Page Count: </b>" + data['pageCount']);
                  $("p.printType").html("<b>Print Type: </b>" + data['printType']);
                  $("p.averageRating").html("<b>Average Rating: </b>" + data['averageRating']);
                  $("p.ratingsCount").html("<b>Rating Count: </b>" + data['ratingsCount']);
                  $("p.maturityRating").html("<b>Maturity Rating: </b>" + data['maturityRating']);
                  $("div.popup-container p.description").html("<b>Description: </b>" + data['description']);
                  $("p.categories").html("<b>Categories: </b>" + data['categories']);
                  $("p.language").html("<b>Language: </b>" + data['language']);
                  $("p.scountry").html("<b>Country: <b>" + data["scountry"]);
                  $("p.saleability").html("<b>Saleability: </b>" + data['saleability']);
                  $("p.isEbook").html("<b>isEbook: </b>" + data['isEbook']);
                  $("p.country").html("<b>Country: </b>" + data['country']);
                  $("p.epub").html("<b>EPUB: </b>" + data['epub']);
                  $("p.pdf").html("<b>PDF: </b>" + data['pdf']);
                  $("p.viewability").html("<b>Viewability: </b>" + data['viewability']);
                  $("p.publicDomain").html("<b>Public Domain: </b>" + data['publicDomain']);
                  $("p.embeddable").html("<b>Embeddable: </b>" + data['embeddable']);
                  $("p.textToSpeechPermission").html("<b>Text To Speech Permission: </b>" + data['textToSpeechPermission']);
                  $("p.accessViewStatus").html("<b>Access View Status: </b>" + data['accessViewStatus']);
                  $("p.quoteSharingAllowed").html("<b>Quote Sharing Allowed: </b>" + data['quoteSharingAllowed']);
                  $("p.textSnippet").html("<b>Text Snippet: </b>" + data['textSnippet']);
                  $("p.saleInfo").html("Sale Info");
                  $("p.accessInfo").html("Access Info");

                  if (data['embeddable'] == 'true') {
                    $("a.preview").click(function() {
                     $(this).attr('href', "/book" + "?id=" + data["id"]);
                    });
                  } else {
                    $("a.preview").html("<b>Inaccessible</b>");
                  }

                  $("#Clear").addClass("visible");
                  $(".popup-close p").click(function () {
                    $("div.popup-container").remove();
                    $("#Clear").removeClass("visible");
                  });

                }
              });
          });

          $("#Clear").click(function(){
            $("div.clear").remove();
            $("div.gallery").remove();
            $(".form").removeClass("hide");
          });
        } else {
          alert("No found");
        } 
      }
    
    });

  });
});
