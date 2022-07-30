// post options button
let menu = false;
let last_id = "";
function menu_toggle(post_id){
    let el = document.getElementById("options-menu" + post_id);
    // let topPos = el.getBoundingClientRect().top + window.scrollY;
    // let leftPos = el.getBoundingClientRect().left + window.scrollX;
    // console.log(topPos);

    if(menu === false && last_id !== post_id){
        el.style.display = "block";
        menu = true;
        last_id = post_id;
    }else if(menu === true && last_id === post_id) {
        el.style.display = "none";
        last_id = "";
        menu = false;
    }else if(menu === true && last_id !== post_id){
        let last_el = document.getElementById("options-menu" + last_id);
        last_el.style.display = "none";
        el.style.display = "block";
        last_id = post_id;
    }
}

let day_mode = true;
function theme_toggle(){
    let el = document.getElementById("theme-toggle-knob");
    let root = document.documentElement;
    if(day_mode){
        // night mode
        root.classList.remove("light-theme");
        root.classList.add("dark-theme");
        el.classList.remove("theme-toggle-anim-light");
        el.classList.add("theme-toggle-anim-dark");
        day_mode = false;
    }else{
        // day mode
        root.classList.remove("dark-theme");
        root.classList.add("light-theme");
        el.classList.remove("theme-toggle-anim-dark");
        el.classList.add("theme-toggle-anim-light");
        day_mode = true;
    }
}

// change field selected file name
let selected_file = document.getElementById("upload");
selected_file.onchange = function(e){
    document.getElementById("file-name").innerText = selected_file.files[0].name;
}

// utility function to get current csrf value
let csrfcookie = function() {
    let cookieValue = null, name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};

// submit like to backend and update accordingly
function like(post_id){
    let request = new XMLHttpRequest();
    request.open("POST", "/post_like/" + post_id + "/", true);
    request.onload = function() {
        let post = document.getElementById("like-btn" + post_id);
        let like_count = document.getElementById("like-count" + post_id);
        if(request.status === 200){     // if 200 liked turn on hear-icon
            post.classList.add("on");
            post.classList.add("pulse-anim");
            like_count.innerText = parseInt(like_count.innerText) + 1;
        }else{                          // else turn off
            post.classList.remove("on");
            post.classList.remove("pulse-anim");
            like_count.innerText = (parseInt(like_count.innerHTML) > 0) ? parseInt(like_count.innerText) - 1 : 0;
        }
    };
    request.onerror = function() {
        console.log("error msg");
    };
    request.ontimeout = function() {
        console.log("connection error msg");
    };
    request.setRequestHeader("X-CSRFToken", csrfcookie());
    request.setRequestHeader("Accept","text/plain");
    request.send();
}