let timeout;

let fade_out = ()=> {
    $(".messages").fadeOut().empty();
}

//Clear messages after 3 seconds
let resetMessages = setTimeout(fade_out, 3000);

