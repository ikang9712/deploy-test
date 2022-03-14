"use strict"

function getPost(){
    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }
    if (pageName == 'follower'){
        xhr.open("GET", "/socialnetwork/get-post-follower", true)
        xhr.send()
    } else{
        xhr.open("GET", "/socialnetwork/get-post", true)
        xhr.send()
    }
}

function updatePage(xhr){
    if (xhr.status == 200) {
        let response = JSON.parse(xhr.responseText)
        console.log('_________________________')
        console.log('response:')
        console.log(response)
        updatePost(response)
        updateComment(response)
        return
    }

    if (xhr.status == 0) {
        displayError("Cannot connect to server")
        return
    }


    if (!xhr.getResponseHeader('content-type') == 'application/json') {
        displayError("Received status=" + xhr.status)
        return
    }

    let response = JSON.parse(xhr.responseText)
    if (response.hasOwnProperty('error')) {
        displayError(response.error)
        return
    }

    displayError(response)
}

function displayError(message) {
    let errorElement = document.getElementById("error")
    errorElement.innerHTML = message
}



function updatePost(response){
    // find the post list container
    let list = document.getElementById("posts")
    // iterate each post from the list
    // console.log("response is this: " + response)
    let items = response['posts']
    for (let i = 0; i < items.length; i++) {
        let item = items[i]
        let itemID = String(item.id)
        // console.log('_________________________')
        // console.log('item info[' + i+ ']')
        // console.log('item ID:' + typeof(itemID))
        // console.log('item text:' + typeof(item.text))
        // console.log('item user:' + typeof(item.user))
        // console.log('item userID:' + typeof(item.userID))
        // console.log('my userID:' + typeof(myUserID))
        // console.log('item creation time:' + typeof(item.creation_time))
        // console.log('_______DONE_______')
        // console.log('_______DONE_______')
        let item_post_id = "id_post_profile_" + itemID
        // the item is not listed
        if (!(document.getElementById(item_post_id))){
            // user who made post
            let user_first = item.user_f
            let user_last = item.user_l
            // link to that user
            let user_url = otherProfileURL(item.userID)
            if (String(item.userID) === myUserID){
                user_url = myProfileURL
            }
            console.log("--------TESTING--------")
            console.log(item.userID)
            console.log(myUserID)
            console.log(typeof(item.userID))
            console.log(typeof(myUserID))
            console.log("--------------------")
            // post text
            let text = sanitize(item.text)
            // post creation time
            let creation_time = item.creation_time

            // build an element within HTML
            let element = document.createElement("li")
            element.style = "list-style: none;"
            let id_post_profile = '"id_post_profile_' + itemID + '"'
            let id_post_text = '"id_post_text_' + itemID + '"'
            let id_post_date_time = '"id_post_date_time_' + itemID + '"'
            let id_comment_text = '"id_comment_input_text_' + itemID + '"'
            let id_comment_button = '"id_comment_button_' + itemID + '"'
            element.innerHTML = '<div id="id_post_div_'+ itemID + '">' + 
                                '<label style="font-style: italic;"> Post by </label>' +
                                '<a href="' + user_url + '" id=' + id_post_profile + '>' + user_first + user_last + '</a>' + 
                                '<label> -- </label>' +
                                '<label id=' + id_post_text + '>' + text + '</label>' +
                                '<label> -- </label>' +
                                '<label style="font-style: italic;" id=' + id_post_date_time + '>' + creation_time + '</label>' +
                                '<div class="comment-container"><ol id="post-' + itemID + '-comments-go-here"></ol></div>' +
                                `<div>
                                    <label>New Comment:</label>
                                    <input type="text" id=` + id_comment_text + '>' + 
                                    `<button onclick="addComment(`+ itemID + `)" id=` + id_comment_button + `>Submit</button>
                                </div>
                                </div>`
                                
            // Adds the todo-list item to the HTML list
            list.prepend(element)
        }
    }
}

function updateComment(response){
    // iterate each post from the list
    let items = response['comments']
    for (let i = 0; i < items.length; i++) {
        let item = items[i]
        // the post id that the item(comment) is for
        let item_div_id = String(item.post_id)
        // the list id of comments in that post
        let item_ol_id = 'post-' + item_div_id +'-comments-go-here'
        let list = document.getElementById(item_ol_id)
        let itemID = String(item.id)
        let item_comment_id = "id_comment_profile_" + itemID
        // the item is not listed
        if (!(document.getElementById(item_comment_id))){
            // user who commented
            let user_first = item.user_f
            let user_last = item.user_l
            // link to that user
            let user_url = otherProfileURL(item.userID)
            if (String(item.userID) == myUserID){
                user_url = myProfileURL
            }
            // comment text
            let text = sanitize(item.text)
            // comment creation time
            let creation_time = item.creation_time

            // build an element within HTML 
            let element = document.createElement("li")
            element.style = "list-style: none;"
            let id_comment_profile = '"id_comment_profile_' + itemID + '"'
            let id_comment_text = '"id_comment_text_' + itemID + '"'
            let id_comment_date_time = '"id_comment_date_time_' + itemID + '"'
            element.innerHTML = '<div id="id_comment_div_'+ itemID + '">' + 
                                '<label style="font-style: italic;"> Comment by </label>' +
                                '<a href="' + user_url + '" id=' + id_comment_profile + '>' + user_first + user_last + '</a>' + 
                                '<label> -- </label>' +
                                '<label id=' + id_comment_text + '>' + text + '</label>' +
                                '<label> -- </label>' +
                                '<label style="font-style: italic;" id=' + id_comment_date_time + '>' + creation_time + '</label>' +
                                '</div>'

                                
            // Adds the todo-list item to the HTML list
            list.prepend(element)
        }
    }
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/%/g, '&percnt;')
            .replace(/{/g, '&lcub;')
            .replace(/}/g, '&rcub;')
}

function addPost() {
    let itemTextElement = document.getElementById("id_post_input_text")
    let itemTextValue   = itemTextElement.value

    // Clear input box and old error message (if any)
    itemTextElement.value = ''

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }

    xhr.open("POST", addPostURL, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("item="+itemTextValue+"&csrfmiddlewaretoken="+getCSRFToken());
}
function addComment(post_id) {
    let itemTextID = "id_comment_input_text_" + post_id
    let itemTextElement = document.getElementById(itemTextID)
    let itemTextValue   = itemTextElement.value
    console.log("-----COMMENT ADD FUNCTION-----")
    console.log("itemTEXT ID: " + itemTextID)
    console.log("itemTEXT ELEM: " + itemTextElement)
    console.log("itemTEXT value: " + itemTextValue)
    // Clear input box and old error message (if any)
    itemTextElement.value = ''

    let xhr = new XMLHttpRequest()
    xhr.onreadystatechange = function() {
        if (xhr.readyState != 4) return
        updatePage(xhr)
    }

    xhr.open("POST", addCommentURL, true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.send("comment_text="+itemTextValue+
             "&post_id="+post_id+
             "&csrfmiddlewaretoken="+getCSRFToken());
}

function getCSRFToken() {
    let cookies = document.cookie.split(";")
    for (let i = 0; i < cookies.length; i++) {
        let c = cookies[i].trim()

        if (c.startsWith("csrftoken=")) {
            return c.substring("csrftoken=".length, c.length)
        }
    }
    return "unknown"
}