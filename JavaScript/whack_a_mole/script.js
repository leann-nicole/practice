let hits = document.querySelector("#score")
let time = document.querySelector("#time")
let holes = document.querySelectorAll(".hole")

holes.forEach(hole => {
    hole.addEventListener('mousedown', checkHit)
})

let moleHole = 0
let score = 0
let timeLeft = 60

function moveMole(){
    holes.forEach(hole => {
        hole.setAttribute("class", "hole")
    })
    moleHole = Math.floor(Math.random() * 9) + 1
    holes[moleHole-1].setAttribute("class", "mole")
}

function checkHit(){
    if (this.id == moleHole){
        score++
        hits.textContent = `WHACK - ${score} - MOLE`
    }
}

function restart(){
    location.reload()
}

let moleMove = setInterval(() => {
    moveMole()
}, 800)

let countdown = setInterval(() => {
    time.textContent = `Time: ${--timeLeft}s`
    if (!timeLeft){
        clearInterval(moleMove)
        clearInterval(countdown)
        time.textContent = `Score: ${score}`
    }
}, 1000)

