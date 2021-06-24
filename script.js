var currentPokename = "";
var pokeTeam = [];
var allPokes = [];
var evolutions = [];
var teamNumber = 1;
var statBox = document.getElementById("stats");
const searchBar = document.getElementById("main-search");


function getPokeName(element) {
    currentPokename = element.value;

    let selector = document.getElementById("selector");
    //this checks if the input is empty
    if(currentPokename.trim() !== "") {
        element.classList.add("dropdown");

        //this creates the selector div below the search bar
        if (selector == null) {
            selector = document.createElement("div");
            selector.id = "selector";
            element.parentNode.appendChild(selector);
            selector.style.left = element.getBoundingClientRect().left + "px";
            selector.style.top = element.getBoundingClientRect().bottom + "px";
            selector.style.width = element.getBoundingClientRect().width + "px";
        }

        selector.innerHTML = "";
        let empty = true;
        for (let item in allPokes) {
            let str = [item.toLocaleLowerCase(), allPokes[item][0].toLocaleLowerCase(), allPokes[item][1].toLocaleLowerCase()].join();
            if(str.indexOf(element.value) !== -1) {
                var catchButton = document.getElementById("catch");
                catchButton.setAttribute("onclick","insertValue(this);")
                catchButton.innerHTML = allPokes[item][0];
                selector.appendChild(opt);
                empty = false;
            }
        }
        //if result is empty display a disabled button with text
        if(empty == true) {
            var catchButton = document.getElementById("catch");
            //catchButton.disabled = true;
            //catchButton.innerHTML = "No Matches";
            //selector.appendChild(catchButton);
        }
    }
    else {
        if (selector !== null) {
            selector.parentNode.removeChild(selector);
            element.classList.remove("dropdown");
        }
    }
}

//uses api query to search for pokemon name specific info
async function search() {
    var response = await fetch("https://pokeapi.co/api/v2/pokemon/" + currentPokename);
    var pokeData = await response.json();
    addToTeam(pokeData);
    //console.log(pokeData);
}

//uses api query to search for pokemon evolution name
async function searchEvolves(pokeName) {
    var response = await fetch("https://pokeapi.co/api/v2/pokemon/" + pokeName);
    var evolveData = await response.json();
    addEvolves(evolveData);
}

function addToTeam(newPoke) {
    var pokeSnap = document.querySelector("#pokeSnap" + teamNumber);
    var pokeName = document.querySelector("#pokeName" + teamNumber);
    
    pokeSnap.src = newPoke.sprites.front_default;
    pokeName.innerText = newPoke.name;
    pokeTeam.push(newPoke);

    if(pokeTeam[teamNumber-1] != null) {
        teamNumber++;
    }
}

function evolve(poke) {
    var pokeSnap = document.querySelector("#pokeSnap" + teamNumber);
    var pokeName = document.querySelector("#pokeName" + teamNumber);
    
    pokeSnap.src = newPoke.sprites.front_default;
    pokeName.innerText = newPoke.name;
    pokeTeam.push(newPoke);
}

//adds evolutions of a pokemon to a list and displays the evolution and name in the stat box
function addEvolves(evolvePoke) {
    var evolveSnap = document.querySelector("#evolve-img1");
    var evolveName = document.querySelector("#evolve-name");
    
    evolveSnap.src = evolvePoke.sprites.front_default;
    evolveName.innerText = `Evolves into: ${ evolvePoke.name }`;
    evolutions.push(evolvePoke);
}

//displays stats for pokemon in party that you are viewing
function statDisplay(num) {

    var livePoke = pokeTeam[num-1];
    var statName = document.getElementById("stat-name");
    var statSnap1 = document.querySelector("#default-img");
    var statSnap2 = document.querySelector("#shiny-img");
    var statBox = document.getElementById("stats");
    statBox.style.display = "block";
    statName.innerText = livePoke.name;
    statSnap1.src = livePoke.sprites.front_default;
    statSnap2.src = livePoke.sprites.front_shiny;
    typeImages(livePoke);
    phys(livePoke);
    evos(livePoke);
    //console.log(livePoke);
}

function statDisplay2(num) {
    var livePoke = pokeTeam[num-1];
}

//closes out the pokemon info display box
function closeBox() {
    var statBox = document.getElementById("stats");
    statBox.style.display = "none";
}

//displays the types (1 or 2) that a pokemon is with one or two images representing 
function typeImages(livePoke) {

    var type1Img = document.querySelector("#type1");
    var type2Img = document.querySelector("#type2");
    var pokeType = livePoke.types[0].type.name;
    if(livePoke.types.length > 1) {
        var pokeType2 = livePoke.types[1].type.name;
    }

    type1Img.src = "/images/" + pokeType + ".png";
    if(livePoke.types.length > 1) {
        type2Img.src = "/images/" + pokeType2 + ".png";
    } else {
        type2Img.removeAttribute("src");
    }
}

//lists the games and regions a pokemon is a part of (through images???)
function regions(livePoke) {
    //var regions = document.querySelector("#regions");
    //var pokeRegion livePoke.region
}

//find and displays the physical features of the pokemon
function phys(livePoke) {
    var height = document.querySelector("#height");
    var weight = document.querySelector("#weight");
    var pokeHeight = livePoke.height;
    var pokeWeight = livePoke.weight;
    var evo = livePoke.species.url;
    height.innerText = "Height: " + pokeHeight;
    weight.innerText = "Weight: " + pokeWeight;
}

async function evos(livePoke) {  
    //fetching the pokemon species
    var evo = livePoke.species.url;
    var response = await fetch(evo);
    var pokeEvo = await response.json();

    //fetching the pokemon evolution chain
    var evolves = pokeEvo.evolution_chain.url;
    var response = await fetch(evolves);
    var pokeEvolves = await response.json();

    //finding the pokemon that this pokemon evolves into
    var finalEvo = pokeEvolves.chain.evolves_to[0].species.name;
    currentPokename = finalEvo;
    searchEvolves(currentPokename);
    console.log(currentPokename);

}


