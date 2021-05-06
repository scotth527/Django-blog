let fade_out = ()=> {
    $(".messages").fadeOut().empty();
}

//Clear messages after 3 seconds
let resetMessages = setTimeout(fade_out, 3000);

//Search autocomplete

let searchBox = document.getElementById('id_q');

searchBox.onchange = (e)=> {
    console.log("E", e.target.value)
    clearTimeout(timeout);
    timeout = setTimeout(() => onSearch(e.target.value), 800);
}

let onSearch = ()=> {

}
