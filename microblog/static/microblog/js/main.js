let timeout;

let fade_out = ()=> {
    $(".messages").fadeOut().empty();
}

//Clear messages after 3 seconds
let resetMessages = setTimeout(fade_out, 3000);

//Search autocomplete

let searchBox = document.getElementById('id_q');
let autocompleteContainer = document.getElementById('autocomplete-suggestions')

searchBox.onchange = (e)=> {
    console.log("E", e.target.value)
    if (!e.target.value) {
        autocompleteContainer.classList.add('d-none')
    } else {
        autocompleteContainer.classList.remove('d-none')
    }
    clearTimeout(timeout);
    timeout = setTimeout(() => onSearch(e.target.value), 800);
}

let onSearch = ()=> {

}
