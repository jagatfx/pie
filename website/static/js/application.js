function fetchTweets() {
    $.get("/ajax/feed/", function(data) {
        var tweets = "";
        $.each(data, function(key, value) {
             tweets += "<p><i class=\"icon-chevron-right\"></i>" + value.from
                      + ": " + value.content + " <span class=\"muted\"><i>- "
                      + value.date + "</i></span></p>";
        });
        $("#tweetWall").html(tweets);
    });
}
