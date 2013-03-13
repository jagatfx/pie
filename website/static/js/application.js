function fetchTweets() {
    $.get("/ajax/feed/", function(data) {
        var tweets = "";
        $.each(data, function(key, value) {
             tweets += "<p><i class=\"icon-chevron-right\"></i>" + value.from
                      + ": " + value.content + " <span class=\"muted\"><i>- "
                      + value.date + "</i></span></p>";
        });
        $("#tweetWall").fadeTo("short", 0).html(tweets).fadeTo("short", 1);
        $("#tweetWall-lastRefresh").html("moments ago");
        tweetWall_lastRefresh = Math.floor($.now()/1000);
    });
}

function updateRefreshTime() {
    var diff = Math.floor($.now()/1000) - tweetWall_lastRefresh;
    $("#tweetWall-lastRefresh").html("about " + diff + " seconds ago");
}
