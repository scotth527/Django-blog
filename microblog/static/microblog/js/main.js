let fade_out = ()=> {
    $(".messages").fadeOut().empty();
}

let resetMessages = setTimeout(fade_out, 3000);

