document.addEventListener('DOMContentLoaded', () => {

let restartBtn = document.getElementById("restartBtn");
restartBtn.onclick = function (){
    location.reload();
    buttonTxt.textContent = "RESTART";
}

const cards = [
    {
        name: 'black',
        img: 'images/black.png'
    },
    {
        name: 'black',
        img: 'images/black.png'
    },
    {
        name: 'blue',
        img: 'images/blue.png'
    },
    {
        name: 'blue',
        img: 'images/blue.png'
    },
    {
        name: 'brown',
        img: 'images/brown.png'
    },
    {
        name: 'brown',
        img: 'images/brown.png'
    },
    {
        name: 'cyan',
        img: 'images/cyan.png'
    },
    {
        name: 'cyan',
        img: 'images/cyan.png'
    },
    {
        name: 'green',
        img: 'images/green.png'
    },
    {
        name: 'green',
        img: 'images/green.png'
    },
    {
        name: 'lime',
        img: 'images/lime.png'
    },
    {
        name: 'lime',
        img: 'images/lime.png'
    },
    {
        name: 'orange',
        img: 'images/orange.png'
    },
    {
        name: 'orange',
        img: 'images/orange.png'
    },
    {
        name: 'pink',
        img: 'images/pink.png'
    },
    {
        name: 'pink',
        img: 'images/pink.png'
    },
    {
        name: 'purple',
        img: 'images/purple.png'
    },
    {
        name: 'purple',
        img: 'images/purple.png'
    },
    {
        name: 'red',
        img: 'images/red.png'
    },
    {
        name: 'red',
        img: 'images/red.png'
    },
    {
        name: 'white',
        img: 'images/white.png'
    },
    {
        name: 'white',
        img: 'images/white.png'
    },
    {
        name: 'yellow',
        img: 'images/yellow.png'
    },
    {
        name: 'yellow',
        img: 'images/yellow.png'
    }];

function showCardPreview(){
    cards.sort(() => 0.5 - Math.random());
    for( let i = 0; i < cards.length; i++){
        let card = document.createElement('img');
        card.style.width = "100px"
        card.style.height = "130px";
        card.style.padding = "10px 15px";
        card.setAttribute('src', cards[i].img);
        card.setAttribute('data-cardid', i);
        table.appendChild(card); 
    }
    setTimeout(layCards, 2500);
}

let table = document.querySelector("#table");
function layCards(){
    let allCards = document.querySelectorAll('img');
    allCards.forEach(card => {
        card.setAttribute('src', 'images/unflipped.png');
        card.addEventListener('click', flipCard);
    });
}

let selectedCardsID = [];
let matchedCardsID = [];

function checkMatch(){
    let allCards = document.querySelectorAll('img');
    if (cards[selectedCardsID[0]].name === cards[selectedCardsID[1]].name){
        matchedCardsID.push(selectedCardsID[0]);
        matchedCardsID.push(selectedCardsID[1]);
    } else {
        allCards[selectedCardsID[0]].setAttribute('src', 'images/unflipped.png');
        allCards[selectedCardsID[1]].setAttribute('src', 'images/unflipped.png');
    }

    // let player flip cards again
    allCards.forEach(card => {
        if (!matchedCardsID.includes(card.getAttribute('data-cardID'))){
            card.addEventListener('click', flipCard);
        }
    });

    selectedCardsID = [];

    if (matchedCardsID.length == cards.length){
        var buttonTxt = document.getElementById("buttonTxt")
        buttonTxt.textContent = "AGAIN?";
    }
}

function flipCard(){
    let cardNo = this.getAttribute('data-cardID');
    this.setAttribute('src', cards[cardNo].img); // flip it
    selectedCardsID.push(cardNo); // recognize that it was flipped
    this.removeEventListener('click', flipCard); // cannot click on same card

    setTimeout(() => {
        if (selectedCardsID.length == 1){
            this.setAttribute('src', 'images/unflipped.png');
            this.addEventListener('click', flipCard);
            selectedCardsID.pop();
        }
    }, 1500); // card without pair flips back after 900 ms

    if (selectedCardsID.length == 2) {
        let allCards = document.querySelectorAll('img'); // no more flips while checking match
        allCards.forEach(card => {
            card.removeEventListener('click', flipCard);
        })
        setTimeout(checkMatch, 1501); // IMPORTANT: checking time > time before self-unflip
    }
}

showCardPreview();

});

/* NOTE:
    checking time must be greater than time before self-unflip

    Reason:
        Say a flipped card unflips itself after 900 ms if there is only 1 card flipped (which is itself).
        Things go wrong if the checking happens too fast (shorter than 900 ms) because by that time the 
        checking function will have unflipped all the selected cards (0 cards flipped). Because of this
        the code inside the setTimeout function for self-unflipping will not be executed. You will still 
        see the crewmate, will not be able to click on it, and the card will not be popped from the 
        selectedCardsID array.
*/