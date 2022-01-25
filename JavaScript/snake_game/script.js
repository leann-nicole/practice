let score = document.querySelector("#score > h2")

let gridRows = 10
let gridCols = 10
const keycodes = [37,38, 39, 40]

let grid = []
let food = []
let snake = [
    [5, 3],
    [5, 2],
]
let direction = 39 // snakes moves to the right initially
let foodEaten = score.textContent

let button = document.querySelector("#restart")
button.onclick = function(){
    location.reload()
}

function notInSnake(location){
    for (let i = 0; i < snake.length; i++)
        if (snake[i][0] == location[0] && snake[i][1] == location[1])
            return false
    return true
}

function makeFood(){
    // remove food from previous location
    let foodCell = document.querySelector(".food")
    if (foodCell)
        foodCell.classList.remove("food")
    // relocate to coordinate not part of snake
    while (true){
        let r = Math.floor(Math.random() * gridRows)
        let c = Math.floor(Math.random() * gridCols)
        if (notInSnake([r, c])){
            food = [r, c]
            grid[r][c].classList.add("food")
            break
        }
    }
}

function growSnake(){
    let tail1 = snake[snake.length-1]
    let tail2 = snake[snake.length-2]
    // if tail1 and tail2 are on the same row, grow new tail horizontally, else vertically
    if (tail1[0] == tail2[0])
        if (tail2[1] > tail1[1]) // snake is headed to the right, tail is at left
            snake.push([tail1[0], tail1[1]-1])
        else snake.push([tail1[0], tail1[1]+1])
    else
        if (tail2[0] > tail1[0]) // snake is headed to the bottom, tail is at up
            snake.push([tail1[0]-1, tail1[1]])
        else snake.push([tail1[0]+1, tail1[1]])
}

function moveSnake(){
    let tail = snake.pop()
    grid[tail[0]][tail[1]].classList.remove("snake") // problem here

    let head = []
    if (direction == 37)
        head.push(snake[0][0], snake[0][1]-1)
    else if (direction == 38)
        head.push(snake[0][0]-1, snake[0][1])
    else if (direction == 39)
        head.push(snake[0][0], snake[0][1]+1)
    else if (direction == 40)
        head.push(snake[0][0]+1, snake[0][1])

    // for wrapping
    if (head[0] < 0)
        head[0] = gridRows-1
    else if (head[0] > gridRows-1)
        head[0] = 0
    else if (head[1] < 0)
        head[1] = gridCols-1
    else if (head[1] > gridCols-1)
        head[1] = 0

    // for self-collision
    if (!notInSnake(head)){
        score.textContent = `You ate ${foodEaten} balls`
        clearInterval(movement)
    }
    
    snake.unshift(head)
    console.log(direction)
    console.log(head)

    if (JSON.stringify(head) == JSON.stringify(food)){
        score.textContent = ++foodEaten
        makeFood()
        growSnake()
    }
}

let drawn = false

function drawSnake(){
    moveSnake() 
    for (let i = 0; i < snake.length; i++){
        row = snake[i][0]
        col = snake[i][1]
        grid[row][col].classList.add("snake") 
    }
    drawn = true
}

function createBoard(){
    let board = document.querySelector("#gameBoard")
    for (let row = 0; row < gridRows; row++){
        grid.push(new Array(0))
        for (let col = 0; col < gridCols; col++){
            let cell = document.createElement("div")
            cell.className = "cell"
            grid[row].push(cell)
            board.appendChild(cell)
        }
    }
    makeFood()
}

function changeDirection(e){
    if (drawn){ // ignore direction changes while previous direction change not drawn
        // 37 left, 38 up, 39 right, 40 down
        if (keycodes.includes(e.keyCode)){ 
            if (Math.abs(direction - e.keyCode) != 2){
                drawn = false // set to false, turns true after completion of drawSnake() function
                console.log(Math.abs(direction - e.keyCode))
                direction = e.keyCode
            }
        }
    }
}

document.addEventListener("keyup", changeDirection) // need something that won't allow changing direction twice (while first change not registered/drawn yet)

createBoard()
let movement = setInterval(drawSnake, 200)