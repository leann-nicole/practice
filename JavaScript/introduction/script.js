const message = "Hi!,My name is Leann,Nicole,Velasco,and,I study,computer science,About moi,I am a pro,...,crastinator,I know,how to surf,...,the internet,and,I love having,conversations,...,with myself,Scientifically,I'm a homo,sapien,hominid,primate,mammal,chordate,animal,and finally,eukaryote,Can you believe,I'm actually,20 years old,?,Anyway,I also want,to know your name,but,don't tell me,Maybe,I can,guess it"
const wordArray = message.split(","); 

let wordNo = 0
let text = document.querySelector("#message")
text.textContent = wordArray[wordNo]
let body = document.querySelector("body")

let girlNames = ["agnes", "claudine", "cokie", "diane", "jahazyl", "jessreal", "juvy", "kyll", "anne", "lyra", "pearl", "lezyl", "maureen", "shannen", "angelique", "zianne", "leann"]
let boyNames = ["allan", "christian", "dennish", "devon", "jan", "clark", "jay", "jhonell", "kim", "jovi", "kurt", "weyne", "ralp", "ronaldo", "padilla", "sam"]
let nameSet = [] 
let letterCount = 0
let currentLetter = "" 
let indicesToCheck = []
let triedLetters = ""
let lives = 6

function restart(){
    nameSet = [] 
    letterCount = 0
    currentLetter = "" 
    indicesToCheck = []
    triedLetters = ""
    lives = 6
    askGender()
}

function clearBody(){
    while (body.firstChild)
        body.removeChild(body.firstChild)
}

function removeGender(){
    if (this.id == "boy")
        nameSet = boyNames
    else nameSet = girlNames
    askLetterCount()    
}

function askGender(){
    clearBody()
    let container = document.createElement("div")
    container.id = "message"
    container.style.flexDirection = "column"
    let boy = document.createElement("div")
    let girl = document.createElement("div")
    boy.id = "boy"
    girl.id = "girl"
    boy.textContent = "BOY"
    girl.textContent = "GIRL"
    boy.addEventListener("click", removeGender)
    girl.addEventListener("click", removeGender)
    let question = document.createElement("h6")
    question.textContent = "Gender"
    question.id = "question"
    container.appendChild(question)
    container.appendChild(boy)
    container.appendChild(girl)
    body.appendChild(container)
}

function toggleIndex(){
    if (this.textContent == "?"){
        this.textContent = currentLetter
        indicesToCheck.push(this.dataset.index)
    }
    else {
        this.textContent = "?"
        const index = indicesToCheck.indexOf(this.dataset.index)
        indicesToCheck.splice(index, 1)
    } 
}

function displayName(){
    clearBody()
    let container = document.createElement("div")
    container.id = "message"
    container.style.flexDirection = "column"
    let question = document.createElement("h6")
    question.id = "question"
    let name = nameSet[0][0].toUpperCase() + nameSet[0].substring(1)
    question.textContent = `Hi, ${name}!`
    container.appendChild(question)
    body.appendChild(container)
}

function removeInvalids(){
    let filtered = nameSet.filter(function(value, index, arr){
        let match = true
        for (let i = 0; i < indicesToCheck.length; i++){
            if (value[indicesToCheck[i]] != currentLetter){
                match = false
                break
            }
        }
        return match
    })
    nameSet = filtered
    if (nameSet.length == 1) displayName()
    else if (!nameSet.length) giveUp()
    else guessLetter()
}

function pickSlots(){
    clearBody()
    indicesToCheck = []
    let container = document.createElement("div")
    container.id = "message"
    container.style.flexDirection = "column"
    let question = document.createElement("h6")
    question.id = "question"
    question.textContent = `Put letter ${currentLetter.toUpperCase()} in place.`
    let slots = document.createElement("div")
    slots.id = "slots"
    for (let i = 0; i < letterCount; i++){
        let slot = document.createElement("div")
        slot.id = "slot"
        slot.dataset.index = i
        slot.textContent = "?"
        slot.addEventListener("click", toggleIndex)
        slots.appendChild(slot)
    }
    let button = document.createElement("p")
    button.textContent = "DONE"
    button.id = "submitButton"
    button.addEventListener("click", removeInvalids)
    container.appendChild(question)
    container.appendChild(slots)
    container.appendChild(button)
    body.appendChild(container)
}

function giveUp(){
    clearBody()
    let container = document.createElement("div")
    container.id = "message"
    container.style.flexDirection = "column"
    let question = document.createElement("h6")
    question.id = "question"
    question.textContent = "A special name, I could not have guessed it."
    let button = document.createElement("p")
    button.textContent = "RETRY"
    button.id = "submitButton"
    button.addEventListener("click", restart)
    container.appendChild(question)
    container.appendChild(button)
    body.appendChild(container)
}

function tryAgain(){
    lives--
    if (!lives)
        giveUp()
    else{ // remove names from the set containing the letter
        let filtered = nameSet.filter(function(value, index, arr){
            return !value.includes(currentLetter)
        })
        nameSet = filtered
        if (nameSet.length)
            guessLetter()
        else giveUp()
    }
}

function poolLetters(){
    let union = "" // union of all letters in nameSet
    nameSet.forEach(name => {
        union += name
    })
    let letters = {} // letters found in the union with their frequency
    union.split("").forEach(l => {
        letters[l] ? letters[l]++ : letters[l] = 1
    })
    // convert obj to array
    let lettersArray = []
    let keys = Object.keys(letters) 
    keys.forEach(key => {
        lettersArray.push([key, letters[key]])
    })
    lettersArray.sort(function(first, second){
        return second[1] - first[1]
    })

    while (triedLetters.includes(lettersArray[0][0])){
        lettersArray.shift()
    }
    
    currentLetter = lettersArray[0][0]
    triedLetters += currentLetter
}

function guessLetter(){
    clearBody()
    let container = document.createElement("div")
    container.id = "message"
    container.style.flexDirection = "column"
    let hearts = document.createElement("div")
    hearts.id = "hearts"
    for (let i = 0; i < lives; i++){
        let heart = document.createElement("div")
        heart.id = "heart"
        hearts.appendChild(heart)
    }
    let question = document.createElement("h6")
    question.id = "question"
    question.style.position = "relative"
    question.style.top = "-50px"
    poolLetters()
    question.textContent = `Do you have the letter ${currentLetter.toUpperCase()}?`
    let yes = document.createElement("div")
    let no = document.createElement("div")
    yes.id = "yes"
    no.id = "no"
    yes.textContent = "YES"
    no.textContent = "NO"
    yes.addEventListener("click", pickSlots)
    no.addEventListener("click", tryAgain)
    container.appendChild(hearts)
    container.appendChild(question)
    container.appendChild(yes)
    container.appendChild(no)
    body.appendChild(container)
}


function submitInput(){
    letterCount = document.getElementById("textInput").value
    if (!isNaN(letterCount)){
        let filteredNames = nameSet.filter(function(value, index, arr){
            if (value.length == letterCount)
                return true
        })
        nameSet = filteredNames
        if (nameSet.length) guessLetter()
        else giveUp()
    }
}

function askLetterCount(){
    clearBody()
    let container = document.createElement("div")
    container.id = "message"
    container.style.flexDirection = "column"
    let question = document.createElement("h6")
    question.textContent = "Number of letters"
    question.id = "question"
    let field = document.createElement("input")
    field.id = "textInput"
    let button = document.createElement("p")
    button.textContent = "ENTER"
    button.id = "submitButton"
    button.addEventListener("click", submitInput)
    container.appendChild(question)
    container.appendChild(field)
    container.appendChild(button)
    body.appendChild(container)
}

askGender()

function back(){
    if (wordNo)
        wordNo--
    text.textContent = wordArray[wordNo]
}

function next(){
    wordNo++
    if (wordNo <= wordArray.length-1)
        text.textContent = wordArray[wordNo]
    else{
        clearBody()
        askGender()
    }
}

// ETAOIN SHRDLU most commonly used letters in the English language
